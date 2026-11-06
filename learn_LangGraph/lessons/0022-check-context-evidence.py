"""Gate model-input preparation on a narrow, question-aware evidence check."""
import argparse
from pathlib import Path
import re
from typing import Literal, TypedDict
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')

from langgraph.graph import END, START, StateGraph
from document_search import Hit, Passage, load_passages, search, words


class State(TypedDict, total=False):
    question: str
    passages: list[Passage]
    hits: list[Hit]
    evidence_ok: bool
    reason: str
    context: str
    status: str


def load_documents(state: State) -> dict:
    return {'passages': load_passages(Path(__file__).with_name('documents'))}


def retrieve(state: State) -> dict:
    return {'hits': search(state['question'], state['passages'])}


def check_evidence(state: State) -> dict:
    if not state['hits']:
        return {'evidence_ok': False, 'reason': 'No passage was retrieved.'}
    # This exercise supports two exact normalized question forms only.
    question = words(state['question'])
    passage = state['hits'][0]['text']
    if question == {'cost'}:
        accepted = re.fullmatch(r'Standard shipping costs \$\d+(?:\.\d{2})? per order\.', passage) is not None
        reason = 'The cost question requires a shipping price per order.'
    elif question == {'receipt'}:
        accepted = passage == 'Returns require the original receipt.'
        reason = 'The receipt question requires the returns receipt requirement.'
    else:
        accepted = False
        reason = 'This question is outside the two supported question forms: cost and receipt.'
    return {'evidence_ok': accepted, 'reason': reason}


def route(state: State) -> Literal['prepare_generation', 'fallback']:
    return 'prepare_generation' if state['evidence_ok'] else 'fallback'


def prepare_generation(state: State) -> dict:
    context = '\n\n'.join(f"[{hit['source']}]\n{hit['text']}" for hit in state['hits'])
    return {'context': context, 'status': 'generation_allowed'}


def fallback(state: State) -> dict:
    # Keep unaccepted passages out of the prepared model context.
    return {'context': '', 'status': 'evidence_rejected'}


builder = StateGraph(State)
for node in (load_documents, retrieve, check_evidence, prepare_generation, fallback):
    builder.add_node(node.__name__, node)
builder.add_edge(START, 'load_documents')
builder.add_edge('load_documents', 'retrieve')
builder.add_edge('retrieve', 'check_evidence')
builder.add_conditional_edges('check_evidence', route)
builder.add_edge('prepare_generation', END)
builder.add_edge('fallback', END)
graph = builder.compile()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('question')
    args = parser.parse_args()
    state: State = {'question': args.question}
    for update in graph.stream(state.copy(), stream_mode='updates',
                               config={'run_name': 'lesson-22-evidence'}):
        for node, values in update.items():
            state.update(values)
            print('Node:', node)
            if node == 'retrieve':
                print('Retrieved sources:', [hit['source'] for hit in state['hits']])
            elif node == 'check_evidence':
                print('Evidence accepted:', state['evidence_ok'])
                print('Reason:', state['reason'])
    print('Status:', state['status'])
    print('Context:', state['context'] or '(empty)')
