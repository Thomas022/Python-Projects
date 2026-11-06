"""Evaluate the shop assistant against saved reference cases, without Gemini calls."""
import json
from pathlib import Path

from app import State, graph


def evaluate_result(result: State, case: dict) -> bool:
    if result['status'] != case['expected_status']:
        return False
    if case['expected_status'] == 'released':
        return result['answer'] == case['expected_answer']
    return bool(result['answer']) and result['answer'] != result.get('draft')


def main() -> int:
    cases = json.loads(Path(__file__).with_name('cases.json').read_text())
    passed = 0
    print('Case | Actual status | Evaluation')
    for case in cases:
        question, mode = case['question'], case['mode']
        if mode not in {'good', 'wrong_price', 'wrong_source', 'extra_claim'}:
            raise ValueError('Evaluation cases must use fixture modes.')
        result = graph.invoke({'question': question, 'mode': mode},
                              config={'run_name': f'shop-evaluation-{mode}-{question}'})
        ok = evaluate_result(result, case)
        passed += int(ok)
        print(f"{question} / {mode} | {result['status']} | {'PASS' if ok else 'FAIL'}")
    print(f'{passed}/{len(cases)} cases passed (fixtures; no Gemini calls)')
    return 0 if passed == len(cases) else 1


if __name__ == '__main__':
    raise SystemExit(main())
