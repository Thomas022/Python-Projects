"""Small file loader and word-overlap search shared by Lessons 19–21."""
from pathlib import Path
import re
from typing import TypedDict


class Passage(TypedDict):
    text: str
    source: str


class Hit(Passage):
    score: int


def load_passages(folder: Path) -> list[Passage]:
    passages: list[Passage] = []
    for path in sorted(folder.glob('*.txt')):
        paragraphs = re.split(r'\n\s*\n', path.read_text(encoding='utf-8').strip())
        for number, paragraph in enumerate(paragraphs, start=1):
            if paragraph.strip():
                passages.append({'text': paragraph.strip(),
                                 'source': f'{path.name}#paragraph-{number}'})
    return passages


STOP_WORDS = {'a', 'an', 'the', 'is', 'are', 'do', 'does', 'how', 'much',
              'what', 'when', 'can', 'i', 'of', 'in', 'to', 'for', 'it', 'my'}


def words(text: str) -> set[str]:
    # Tiny normalization: costs -> cost, returns -> return. Not a full stemmer.
    return {word[:-1] if word.endswith('s') and len(word) > 3 else word
            for word in re.findall(r'[a-z0-9]+', text.lower())
            if word not in STOP_WORDS}


def search(question: str, passages: list[Passage], limit: int = 1) -> list[Hit]:
    scored: list[Hit] = []
    for passage in passages:
        score = len(words(question) & words(passage['text']))
        if score > 0:
            scored.append({**passage, 'score': score})
    # Equal scores keep the loader's filename/paragraph order.
    return sorted(scored, key=lambda hit: hit['score'], reverse=True)[:limit]
