"""Controlled diagnosis exercise: three runs, two deliberately injected faults."""
from pathlib import Path
from dotenv import load_dotenv

# Load this project’s saved settings, even when run from another directory.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import argparse
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict, total=False):
    question: str
    case: str
    passage: str
    source: str
    answer: str


def retrieve(state: State) -> dict:
    # Case A deliberately selects an irrelevant document.
    if state["case"] == "a":
        return {
            "passage": "Unused items can be returned within 21 days of delivery.",
            "source": "Returns policy, section 2",
        }
    return {
        "passage": "Standard shipping takes 3 to 5 business days.",
        "source": "Shipping policy, section 1",
    }


def generate(state: State) -> dict:
    
    
    return {"answer": f'{state["passage"]} [{state["source"]}]'}


builder = StateGraph(State)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)
graph = builder.compile()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=["a", "b", "c"])
    args = parser.parse_args()
    result = graph.invoke(
        {"question": "How long does shipping take?", "case": args.case},
        config={"run_name": f"lesson-05-case-{args.case}"},
    )
    print("Case:", args.case.upper())
    print("Question:", result["question"])
    print("Retrieval output:", result["passage"])
    print("Source:", result["source"])
    print("Generation output:", result["answer"])
