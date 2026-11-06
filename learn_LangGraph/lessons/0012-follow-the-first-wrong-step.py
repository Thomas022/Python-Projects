"""Inspect Lesson 11's graph one node update at a time."""
from pathlib import Path
from dotenv import load_dotenv

# Load this project’s saved settings, even when run from another directory.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import argparse
from pathlib import Path
import runpy

# Reuse the exact graph from Lesson 11; only the display changes.
lesson = runpy.run_path(str(Path(__file__).with_name("0011-check-the-answer.py")))
graph = lesson["graph"]
FIELDS = ("attempts", "passage", "source", "evidence_ok", "draft", "answer_ok", "answer")


def initial_state(scenario: str) -> dict:
    return {
        "question": lesson["COST_QUESTION"],
        "case": "b", "attempts": 0, "tried_sources": [],
        "passage_only": False,
        "include_cost": scenario != "missing",
        "bad_draft": scenario in ("caught", "missed"),
        "citation_only": scenario == "missed",
    }


def show(label: str, values: dict) -> None:
    print(label)
    for field in FIELDS:
        value = repr(values[field]) if field in values else "(not set)"
        print(f"  {field}: {value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=["good", "caught", "missed", "missing"])
    args = parser.parse_args()
    state = initial_state(args.scenario)
    print("Question:", state["question"])
    print("Scenario:", args.scenario)
    visited = []
    for update in graph.stream(
        state.copy(),
        config={"run_name": f"lesson-12-{args.scenario}"},
        stream_mode="updates",
    ):
        for node, values in update.items():
            visited.append(node)
            print(f"\nStep {len(visited)}: {node}")
            show("BEFORE (selected state fields)", state)
            print("UPDATE:", values)
            # This graph is sequential and uses replacement for every field.
            state.update(values)
            show("AFTER (selected state fields)", state)
    print("\nVisited:", " → ".join(visited))
    print("Final answer:", state["answer"])
