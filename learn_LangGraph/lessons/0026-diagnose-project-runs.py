"""Diagnose controlled shop-assistant runs without using Gemini quota."""
import json
from pathlib import Path
import sys

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')
sys.path.insert(0, str(ROOT / 'final-project'))

from app import graph
from evaluate import evaluate_result


def diagnosis_cases() -> list[dict]:
    baseline = json.loads((ROOT / 'final-project' / 'cases.json').read_text())
    cases = []
    for question, mode in [('cost', 'wrong_price'), ('cost', 'wrong_source'),
                           ('warranty', 'good'), ('shipping insurance', 'good')]:
        case = next(dict(c) for c in baseline if c['question'] == question and c['mode'] == mode)
        case['name'] = f'{question}-{mode}'.replace(' ', '-')
        cases.append(case)
    # Deliberately stale expectation for this exercise only. No policy, graph,
    # or baseline case file is changed. References never enter graph state.
    stale = next(dict(c) for c in baseline if c['question'] == 'cost' and c['mode'] == 'good')
    stale.update(name='stale-reference',
                 expected_answer='Standard shipping costs $7 per order. [shipping.txt#paragraph-2]')
    cases.append(stale)
    return cases


def main() -> int:
    passed = 0
    print('Fixtures only: no Gemini calls. Restore the project shipping price to $5 first.')
    for case in diagnosis_cases():
        name = f"lesson-26-{case['name']}"
        print(f'\nRun: {name}')
        print('Expected status:', case['expected_status'])
        print('Expected answer:', case['expected_answer'] or '(a refusal, not the draft)')
        state = {'question': case['question'], 'mode': case['mode']}
        config = {'run_name': name, 'tags': ['lesson-26', 'fixture'],
                  'metadata': {'expected_status': case['expected_status'],
                               'expected_answer': case['expected_answer']}}
        for update in graph.stream(state.copy(), stream_mode='updates', config=config):
            for node, values in update.items():
                state.update(values)
                print('Node:', node)
                for key in ('hits', 'evidence_ok', 'reason', 'draft', 'answer_ok', 'answer_reason'):
                    if key in values:
                        print(f'  {key}: {values[key]}')
        ok = evaluate_result(state, case)
        passed += int(ok)
        print('Actual status:', state['status'])
        print('Actual answer:', state['answer'])
        print('Evaluation:', 'PASS' if ok else 'FAIL')
    print(f'\n{passed}/5 diagnostic cases passed. The stale-reference FAIL is intentional.')
    print('The unchanged baseline suite should still pass 7/7.')
    return 0 if passed == 5 else 1


if __name__ == '__main__':
    raise SystemExit(main())
