"""Compare four graph outcomes with fixed expectations."""
import argparse
import contextlib
import io
from pathlib import Path
import runpy

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

load_dotenv(Path(__file__).resolve().parents[1] / '.env')

# Reuse Lesson 17 without executing its terminal entry point.
lesson = runpy.run_path(str(Path(__file__).with_name('0017-trace-retries.py')))
graph = lesson['graph']
initial_state = lesson['initial_state']

# Expectations stay fixed when the graph implementation changes.
CASES = [
    ('good', 'released'),
    ('repair', 'released'),
    ('stuck', 'draft_rejected'),
    ('missing', 'no_evidence'),
]


def evaluate_outcome(actual: str, expected: str) -> bool:
    return actual == expected


def run_suite(variant: str) -> int:
    # Intentional regression: publish the rejected draft after retry exhaustion.
    # This changes the release boundary, leaving the checker intact.
    if variant == 'unsafe':
        def unsafe_reject(state):
            return {'answer': state['draft'], 'outcome': 'released'}
        builder = StateGraph(lesson['State'])
        for name in ('retrieve', 'check_evidence', 'generate', 'check_answer',
                     'release', 'fallback', 'summarize'):
            builder.add_node(name, lesson[name])
        builder.add_node('reject_answer', unsafe_reject)
        builder.add_edge(START, 'retrieve')
        builder.add_edge('retrieve', 'check_evidence')
        builder.add_conditional_edges('check_evidence', lesson['choose_next'])
        builder.add_edge('generate', 'check_answer')
        builder.add_conditional_edges('check_answer', lesson['choose_answer'])
        for name in ('release', 'reject_answer', 'fallback'):
            builder.add_edge(name, 'summarize')
        builder.add_edge('summarize', END)
        candidate = builder.compile()
    else:
        candidate = graph
    passed = 0
    print('Mode | Expected outcome | Actual outcome | Evaluation')
    for mode, expected in CASES:
        with contextlib.redirect_stdout(io.StringIO()):
            result = candidate.invoke(initial_state(mode), config={
                'run_name': f'lesson-18-{variant}-{mode}',
            })
        ok = evaluate_outcome(result['outcome'], expected)
        passed += ok
        print(f"{mode} | {expected} | {result['outcome']} | {'PASS' if ok else 'FAIL'}")
    print(f'{passed}/{len(CASES)} cases passed')
    return 0 if passed == len(CASES) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('variant', choices=['baseline', 'unsafe'], default='baseline', nargs='?')
    raise SystemExit(run_suite(parser.parse_args().variant))
