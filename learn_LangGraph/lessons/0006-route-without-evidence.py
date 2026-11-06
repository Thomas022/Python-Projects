"""Route to an evidence-based answer or a fallback using conditional edges."""
from pathlib import Path
from dotenv import load_dotenv

# Load this project’s saved settings, even when run from another directory.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import sys
from typing import Literal, TypedDict

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
    {
    "keywords": {"warranty"},
    "passage": "The warranty lasts 12 months from purchase.",
    "source": "Warranty policy, section 3",
},
]


def retrieve(state: State) -> dict:
    words = set(state["question"].lower().strip("?!.").split())
    for document in DOCUMENTS:
        if words & document["keywords"]:
            return {"passage": document["passage"], "source": document["source"]}
    return {"passage": "", "source": ""}


def choose_next(state: State) -> Literal["generate", "fallback"]:
    return "generate" if state["passage"] else "fallback"


def generate(state: State) -> dict:
    return {"answer": f'{state["passage"]} [{state["source"]}]'}


def fallback(state: State) -> dict:
    return {"answer": "I could not find a matching passage in these documents."}


builder = StateGraph(State)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_node("fallback", fallback)
builder.add_edge(START, "retrieve")
builder.add_conditional_edges("retrieve", choose_next)
builder.add_edge("generate", END)
builder.add_edge("fallback", END)
graph = builder.compile()

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How long does shipping take?"
    print("Question:", question)
    for update in graph.stream(
        {"question": question},
        config={"run_name": "lesson-06-route-without-evidence"},
        stream_mode="updates",
    ):
        for node, values in update.items():
            print("Node:", node)
            if node == "retrieve":
                print("Retrieved passage:", values["passage"] or "(none)")
                print("Source:", values["source"] or "(none)")
            else:
                print("Answer:", values["answer"])
