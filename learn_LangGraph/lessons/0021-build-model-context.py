"""Build cited context in LangGraph; no model call yet."""
import argparse
from pathlib import Path
from typing import Literal, TypedDict
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')

from langgraph.graph import END, START, StateGraph
from document_search import Hit, Passage, load_passages, search


class State(TypedDict, total=False):
    question: str
    passages: list[Passage]
    hits: list[Hit]
    context: str
    status: str


def load_documents(state: State) -> dict:
    return {'passages': load_passages(Path(__file__).with_name('documents'))}


def retrieve(state: State) -> dict:
    return {'hits': search(state['question'], state['passages'])}


def route(state: State) -> Literal['build_context', 'no_context']:
    return 'build_context' if state['hits'] else 'no_context'


def build_context(state: State) -> dict:
    context = '\n\n'.join(f"[{hit['source']}]\n{hit['text']}" for hit in state['hits'])
    return {'context': context, 'status': 'context_ready'}


def no_context(state: State) -> dict:
    return {'context': '', 'status': 'no_context'}


builder = StateGraph(State)
for node in (load_documents, retrieve, build_context, no_context):
    builder.add_node(node.__name__, node)
builder.add_edge(START, 'load_documents')
builder.add_edge('load_documents', 'retrieve')
builder.add_conditional_edges('retrieve', route)
builder.add_edge('build_context', END)
builder.add_edge('no_context', END)
graph = builder.compile()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('question')
    args = parser.parse_args()
    state: State = {'question': args.question}
    for update in graph.stream(state.copy(), stream_mode='updates',
                               config={'run_name': 'lesson-21-context'}):
        for node, values in update.items():
            state.update(values)
            print('Node:', node)
            if node == 'retrieve':
                print('Retrieved sources:', [hit['source'] for hit in state['hits']])
    print('Status:', state['status'])
    print('Context:', state['context'] or '(empty)')
