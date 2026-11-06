"""Check retrieved evidence against two supported shipping questions."""
from pathlib import Path
from dotenv import load_dotenv

# Load this project’s saved settings, even when run from another directory.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import argparse
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

MAX_ATTEMPTS = 2  # First retrieval plus one retry.


class State(TypedDict, total=False):
    question: str
    tried_sources: list[str]
    passage_only: bool
    include_cost: bool
    case: str
    attempts: int
    passage: str
    source: str
    evidence_ok: bool
    reason: str
    answer: str


DURATION_QUESTION = "How long does standard shipping take?"
COST_QUESTION = "How much does standard shipping cost?"
DOCUMENTS = [
    {"keywords": {"shipping", "standard"},
     "passage": "Standard shipping arrives in 3 to 5 business days.",
     "source": "Shipping policy, section 1"},
]
COST_DOCUMENT = {
    "keywords": {"shipping", "standard", "cost"},
    "passage": "Standard shipping costs $5 per order.",
    "source": "Shipping policy, section 2",
}


def retrieve(state: State) -> dict:
    words = set(state["question"].lower().strip("?!. ").split())
    tried = state["tried_sources"]
    documents = DOCUMENTS + ([COST_DOCUMENT] if state["include_cost"] else [])
    for document in documents:
        if document["source"] in tried:
            continue
        if words & document["keywords"]:
            return {
                "attempts": state["attempts"] + 1,
                "passage": document["passage"],
                "source": document["source"],
                "tried_sources": tried + [document["source"]],
            }
    return {"attempts": state["attempts"] + 1, "passage": "", "source": ""}


def check_evidence(state: State) -> dict:
    passage = state["passage"].lower()
    if not passage:
        return {"evidence_ok": False, "reason": "No passage was retrieved."}
    duration_ok = "standard shipping arrives in" in passage and "business days" in passage
    if state["passage_only"]:
        return {"evidence_ok": duration_ok, "reason": "Legacy check looks only for shipping duration."}
    question = state["question"]
    if question == DURATION_QUESTION:
        accepted = duration_ok
        reason = "The question needs shipping duration."
    elif question == COST_QUESTION:
        accepted = "standard shipping costs $" in passage and "per order" in passage
        reason = "The question needs shipping cost per order."
    else:
        accepted = False
        reason = "This question is outside the two supported questions."
    return {"evidence_ok": accepted, "reason": reason}


def choose_next(state: State) -> Literal["generate", "retrieve", "fallback"]:
    if state["evidence_ok"]:
        return "generate"
    if state["attempts"] < MAX_ATTEMPTS:
        return "retrieve"
    return "fallback"


def generate(state: State) -> dict:
    return {"answer": f'{state["passage"]} [{state["source"]}]'}


def fallback(state: State) -> dict:
    return {"answer": f'I cannot answer from the retrieved evidence after {state["attempts"]} attempt(s). {state["reason"]}'}


builder = StateGraph(State)
builder.add_node("retrieve", retrieve)
builder.add_node("check_evidence", check_evidence)
builder.add_node("generate", generate)
builder.add_node("fallback", fallback)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "check_evidence")
builder.add_conditional_edges("check_evidence", choose_next)
builder.add_edge("generate", END)
builder.add_edge("fallback", END)
graph = builder.compile()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=["a", "b", "c"])
    parser.add_argument("--passage-only", action="store_true", help="Use the old duration-only check.")
    parser.add_argument("--with-cost", action="store_true", help="Add a shipping cost document.")
    args = parser.parse_args()
    question = {"a": DURATION_QUESTION, "b": COST_QUESTION,
                "c": "Can I return standard shipping packaging?"}[args.case]
    print("Case:", args.case.upper())
    print("Question:", question)
    for update in graph.stream(
        {"question": question, "case": args.case, "attempts": 0,
         "tried_sources": [], "passage_only": args.passage_only, "include_cost": args.with_cost},
        config={"run_name": f"lesson-10-case-{args.case}"},
        stream_mode="updates",
    ):
        for node, values in update.items():
            print("Node:", node)
            for key, value in values.items():
                print(f"  {key}: {value if value != '' else '(empty)'}")
