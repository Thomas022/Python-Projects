"""Load text files and preserve paragraph source labels."""
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')

from document_search import load_passages

if __name__ == '__main__':
    passages = load_passages(Path(__file__).with_name('documents'))
    for passage in passages:
        print(f"[{passage['source']}] {passage['text']}")
    print(f'Total passages: {len(passages)}')
