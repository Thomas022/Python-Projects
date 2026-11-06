"""Retry keyword retrieval while skipping previously tried sources."""
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
    skip_tried: bool
    case: str
    attempts: int
    passage: str
    source: str
    evidence_ok: bool
    reason: str
    answer: str


DOCUMENTS = [
    {"keywords": {"shipping", "delivery"},
     "passage": "Unused items can be returned within 21 days of delivery.",
     "source": "Returns policy, section 2"},
    {"keywords": {"shipping", "standard"},
     "passage": "Standard shipping arrives in 3 to 5 business days.",
     "source": "Shipping policy, section 1"},
]


def retrieve(state: State) -> dict:
    words = set(state["question"].lower().strip("?!. ").split())
    tried = state["tried_sources"]
    for document in DOCUMENTS:
        if state["skip_tried"] and document["source"] in tried:
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
    # Lesson 7's expanded teaching rule, still only for this fixed question.
    if "standard shipping takes" in passage or "standard shipping arrives" in passage:
        return {"evidence_ok": True, "reason": "The passage states standard shipping duration."}
    return {"evidence_ok": False, "reason": "The passage does not state standard shipping duration."}


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
    parser.add_argument("--repeat", action="store_true", help="Do not skip tried sources.")
    args = parser.parse_args()
    question = {"a": "How long does standard shipping take?",
                "b": "How long does standard postage take?",
                "c": "How much does express postage cost?"}[args.case]
    print("Case:", args.case.upper())
    print("Question:", question)
    for update in graph.stream(
        {"question": question, "case": args.case, "attempts": 0,
         "tried_sources": [], "skip_tried": not args.repeat},
        config={"run_name": f"lesson-09-case-{args.case}"},
        stream_mode="updates",
    ):
        for node, values in update.items():
            print("Node:", node)
            for key, value in values.items():
                print(f"  {key}: {value if value != '' else '(empty)'}")
