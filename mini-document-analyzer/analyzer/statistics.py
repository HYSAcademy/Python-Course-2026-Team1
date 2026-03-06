from collections import Counter
import re
from typing import List, Dict, Tuple


def count_characters(text: str) -> int:
    """
    Count total characters in text (including spaces).
    """
    return len(text)


def count_words(tokens: List[str]) -> int:
    """
    Count total words based on tokens.
    """
    return len(tokens)


def count_sentences(text: str) -> int:
    """
    Count sentences 
    """
    sentences = re.findall(r"[.!?]", text)
    return len(sentences)


def word_frequencies(tokens: List[str]) -> Dict[str, int]:
    """
    Create a dictionary with word frequencies.
    """
    return dict(Counter(tokens))


def top_10_words(tokens: List[str]) -> List[Tuple[str, int]]:
    """
    Return the 10 most common words.
    """
    counter = Counter(tokens)
    return counter.most_common(10)
