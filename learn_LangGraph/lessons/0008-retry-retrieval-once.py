"""Retry rejected retrieval once, then generate or stop with fallback."""
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
    case: str
    attempts: int
    passage: str
    source: str
    evidence_ok: bool
    reason: str
    answer: str


def retrieve(state: State) -> dict:
    attempt = state["attempts"] + 1
    # Controlled results: A switches documents on its second attempt.
    if state["case"] == "b" or (state["case"] == "a" and attempt >= 2):
        passage = "Standard shipping arrives in 3 to 5 business days."
        source = "Shipping policy, section 1"
    elif state["case"] == "a":
        passage = "Unused items can be returned within 21 days of delivery."
        source = "Returns policy, section 2"
    else:
        passage, source = "", ""
    return {"attempts": attempt, "passage": passage, "source": source}


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
    args = parser.parse_args()
    question = "How long does standard shipping take?"
    print("Case:", args.case.upper())
    print("Question:", question)
    for update in graph.stream(
        {"question": question, "case": args.case, "attempts": 0},
        config={"run_name": f"lesson-08-case-{args.case}"},
        stream_mode="updates",
    ):
        for node, values in update.items():
            print("Node:", node)
            for key, value in values.items():
                print(f"  {key}: {value if value != '' else '(empty)'}")
