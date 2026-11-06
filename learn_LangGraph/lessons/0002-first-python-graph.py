"""Real LangGraph execution; simulated retrieval and generation."""
from pathlib import Path
from dotenv import load_dotenv

# Load this project’s saved settings, even when run from another directory.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from typing import TypedDict
from langgraph.graph import END, START, StateGraph


class State(TypedDict, total=False):
    question: str
    passage: str
    source: str
    answer: str


def retrieve(state: State) -> dict:
    # Teaching stub: always selects this passage; no search yet.
    return {
        "passage": "Unused items can be returned within 21 days of delivery.",
        "source": "Returns policy, section 2",
    }


def generate(state: State) -> dict:
    # Teaching stub: quotes the passage; no language model yet.
    return {"answer": f'{state["passage"]} [{state["source"]}]'}


builder = StateGraph(State)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)
graph = builder.compile()

if __name__ == "__main__":
    initial_state = {"question": "How long do I have to return an unused item?"}
    result = graph.invoke(initial_state)
    print("Question:", result["question"])
    print("Answer:", result["answer"])
