import re
from typing import List


NEGATION_PATTERNS = [
    r"\bnever\b",
    r"\bno\b",
    r"\bnot\b",
    r"\brefuse\b",
    r"\bdeny\b",
]

AFFIRMATION_PATTERNS = [
    r"\balways\b",
    r"\byes\b",
    r"\ballow\b",
    r"\bconfirm\b",
    r"\bapprove\b",
]


def find_contradictions(text: str) -> List[str]:
    """
    A heuristic contradiction detector that looks for statements that contain
    both affirmation and negation cues within close proximity.
    """
    normalized = text.lower()
    sentences = re.split(r"[\.;\n]+", normalized)
    contradictions: List[str] = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        has_negation = any(re.search(pattern, sentence) for pattern in NEGATION_PATTERNS)
        has_affirmation = any(re.search(pattern, sentence) for pattern in AFFIRMATION_PATTERNS)
        if has_negation and has_affirmation:
            contradictions.append(sentence)

    return contradictions
