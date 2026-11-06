import re

def parse_evaluation_response(text: str) -> tuple[int, str]:
    text = text.strip()

    # Match "7" or "7/10"
    match = re.search(r"\b(10|[1-9])(?:\s*/\s*10)?\b", text)
    
    score = int(match.group(1)) if match else 5

    # Remove only the first occurrence of the score
    if match:
        start, end = match.span()
        feedback = (text[:start] + text[end:]).strip()
    else:
        feedback = text

    return score, feedback