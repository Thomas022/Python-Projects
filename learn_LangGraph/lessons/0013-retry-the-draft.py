"""Retry a rejected draft once using the same accepted evidence."""
from pathlib import Path
from dotenv import load_dotenv

# Load this project’s saved settings, even when run from another directory.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import argparse
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

MAX_ATTEMPTS = 2  # First retrieval plus one retry.
MAX_GENERATIONS = 2  # First draft plus one retry.


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
    draft: str
    answer_ok: bool
    answer_reason: str
    mode: str
    generation_attempts: int
    citation_only: bool


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
    passage = state["passage"]
    count = state["generation_attempts"] + 1
    if state["mode"] == "stuck" or (state["mode"] == "repair" and count == 1):
        passage = passage.replace("$5", "$50")
    return {"draft": f'{passage} [{state["source"]}]',
            "generation_attempts": count, "answer_ok": False}


def check_answer(state: State) -> dict:
    citation = f'[{state["source"]}]'
    if state["citation_only"]:
        accepted = citation in state["draft"]
        reason = "Legacy check looks only for the source citation."
    else:
        expected = f'{state["passage"]} {citation}'
        accepted = state["draft"] == expected
        reason = "This exercise requires the exact accepted passage and its citation."
    return {"answer_ok": accepted, "answer_reason": reason}


def choose_answer(state: State) -> Literal["release", "generate", "reject_answer"]:
    if state["answer_ok"]:
        return "release"
    if state["generation_attempts"] < MAX_GENERATIONS:
        return "generate"
    return "reject_answer"


def release(state: State) -> dict:
    return {"answer": state["draft"]}


def reject_answer(state: State) -> dict:
    return {"answer": "I cannot release the draft after two failed generation attempts."}


def fallback(state: State) -> dict:
    return {"answer": f'I cannot answer from the retrieved evidence after {state["attempts"]} attempt(s). {state["reason"]}'}


builder = StateGraph(State)
builder.add_node("retrieve", retrieve)
builder.add_node("check_evidence", check_evidence)
builder.add_node("generate", generate)
builder.add_node("fallback", fallback)
builder.add_node("check_answer", check_answer)
builder.add_node("release", release)
builder.add_node("reject_answer", reject_answer)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "check_evidence")
builder.add_conditional_edges("check_evidence", choose_next)
builder.add_edge("generate", "check_answer")
builder.add_conditional_edges("check_answer", choose_answer)
builder.add_edge("release", END)
builder.add_edge("reject_answer", END)
builder.add_edge("fallback", END)
graph = builder.compile()

def initial_state(mode: str) -> State:
    return {
        "question": COST_QUESTION, "case": "b", "attempts": 0,
        "tried_sources": [], "passage_only": False, "include_cost": True,
        "mode": mode, "generation_attempts": 0, "citation_only": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["good", "repair", "stuck"])
    args = parser.parse_args()
    state = initial_state(args.mode)
    visited = []
    for update in graph.stream(
        state.copy(), config={"run_name": f"lesson-13-{args.mode}"},
        stream_mode="updates",
    ):
        for node, values in update.items():
            visited.append(node)
            state.update(values)
            print("Node:", node)
            print("  update:", values)
            if node in ("generate", "check_answer"):
                print("  passage:", state["passage"])
                print("  draft:", state["draft"])
                print("  answer_ok:", state["answer_ok"])
    print("\nSummary")
    print("Retrieval attempts:", state["attempts"])
    print("Generation attempts:", state["generation_attempts"])
    print("Final node:", visited[-1])
    print("Final passage:", state["passage"])
    print("Final draft:", state["draft"])
    print("Final answer:", state["answer"])
