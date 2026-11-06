"""A simple terminal interface for the fictional shop assistant."""
import argparse
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')

import httpx
from google.genai import errors
from app import graph


HELP = 'Ask: cost or receipt. Other questions may be refused. Commands: /help, /quit.'


def answer_question(question: str, mode: str) -> dict:
    # A new input dictionary for every question; no previous draft or evidence
    # is carried into this invocation. The interface displays only final answer.
    return graph.invoke({'question': question, 'mode': mode},
                        config={'run_name': f'shop-chat-{mode}', 'tags': ['terminal-chat']})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true', help='Use Gemini instead of fixture drafts.')
    args = parser.parse_args()
    mode = 'live' if args.live else 'good'
    print('Fictional shop assistant')
    print('Generation:', 'live Gemini; uses your saved key and free-tier quota' if args.live
          else 'fixtures; no Gemini calls')
    print(HELP)
    while True:
        try:
            question = input('\nYou: ').strip()
            if not question:
                continue
            if question.casefold() == '/quit':
                break
            if question.casefold() == '/help':
                print(HELP)
                continue
            result = answer_question(question, mode)
            print('Assistant:', result['answer'])
            print('Status:', result['status'])
        except (EOFError, KeyboardInterrupt):
            break
        except ValueError:
            print('No answer released. Check your saved Gemini setup or try again; the draft may be incomplete.')
        except errors.APIError as error:
            print('No answer released. Gemini request failed; HTTP code:', error.code)
            print('Check model access and free-tier quota.')
        except (httpx.HTTPError, TimeoutError, ConnectionError):
            print('No answer released. Connection issue; try again.')
        except OSError:
            print('No answer released. Check that the project documents are readable.')
    print('\nGoodbye.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
