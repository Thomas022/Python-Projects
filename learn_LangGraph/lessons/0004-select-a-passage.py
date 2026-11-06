"""Tiny keyword retrieval with real LangGraph; generation still quotes evidence."""
from pathlib import Path
from dotenv import load_dotenv

# Load this project’s saved settings, even when run from another directory.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import sys
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict, total=False):
    question: str
    passage: str
    source: str
    answer: str


DOCUMENTS = [
    {
        "keywords": {"return", "returns"},
        "passage": "Unused items can be returned within 21 days of delivery.",
        "source": "Returns policy, section 2",
    },
    {
        "keywords": {"shipping", "delivery"},
        "passage": "Standard shipping takes 3 to 5 business days.",
        "source": "Shipping policy, section 1",
    },
]


def retrieve(state: State) -> dict:
    words = set(state["question"].lower().strip("?!.").split())
    for document in DOCUMENTS:
        if words & document["keywords"]:
            return {"passage": document["passage"], "source": document["source"]}
    return {"passage": "", "source": ""}


def generate(state: State) -> dict:
    if not state["passage"]:
        return {"answer": "I could not find a matching passage in these documents."}
    return {"answer": f'{state["passage"]} [{state["source"]}]'}


builder = StateGraph(State)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)
graph = builder.compile()

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How long do I have to return an unused item?"
    result = graph.invoke({"question": question})
    print("Question:", result["question"])
    print("Retrieved passage:", result["passage"] or "(none)")
    print("Answer:", result["answer"])
