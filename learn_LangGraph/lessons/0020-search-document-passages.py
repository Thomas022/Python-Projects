"""Rank real document passages by shared words."""
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')

from document_search import load_passages, search

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('question')
    args = parser.parse_args()
    passages = load_passages(Path(__file__).with_name('documents'))
    hits = search(args.question, passages)
    print('Question:', args.question)
    for hit in hits:
        print(f"Score: {hit['score']} | Source: {hit['source']}")
        print('Passage:', hit['text'])
    if not hits:
        print('No matching passage.')
