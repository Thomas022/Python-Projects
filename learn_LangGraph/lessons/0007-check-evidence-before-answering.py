"""Check evidence for one fixed shipping question before choosing a path."""
from pathlib import Path
from dotenv import load_dotenv

# Load this project’s saved settings, even when run from another directory.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import argparse
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict, total=False):
    question: str
    case: str
    passage: str
    source: str
    evidence_ok: bool
    reason: str
    answer: str


def retrieve(state: State) -> dict:
    if state["case"] == "a":
        return {
 r            "passage": "Unused items can be returned within 21 days of delivery.",
            "source": "Returns policy, section 2",
        }
    if state["case"] == "b":
        return {
            "passage": "standard shipping takes in 3 to 5 business days.",
            "source": "Shipping policy, section 1",
        }
    return {"passage": "", "source": ""}


def check_evidence(state: State) -> dict:
    # Teaching rule for the fixed question, not a general relevance checker.
    if not state["passage"]:
        return {"evidence_ok": False, "reason": "No passage was retrieved."}
    if "standard shipping takes" in state["passage"].lower():
        return {"evidence_ok": True, "reason": "The passage states standard shipping duration."}
    return {"evidence_ok": False, "reason": "The passage does not state standard shipping duration."}


def choose_next(state: State) -> Literal["generate", "fallback"]:
    return "generate" if state["evidence_ok"] else "fallback"


def generate(state: State) -> dict:
    return {"answer": f'{state["passage"]} [{state["source"]}]'}


def fallback(state: State) -> dict:
    return {"answer": f'I cannot answer from the retrieved evidence. {state["reason"]}'}


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
        {"question": question, "case": args.case},
        config={"run_name": f"lesson-07-case-{args.case}"},
        stream_mode="updates",
    ):
        for node, values in update.items():
            print("Node:", node)
            for key, value in values.items():
                print(f"  {key}: {value if value != '' else '(empty)'}")
