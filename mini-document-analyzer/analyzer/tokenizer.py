import string


def clean_text(text: str) -> str:
    """
    Cleans text:
    - converts to lowercase
    - removes punctuation

    Args:
        text (str): raw text

    Returns:
        str: cleaned text
    """
    text = text.lower()
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    return text


def tokenize(text: str) -> list[str]:
    """
    Splits text into tokens (words)

    Args:
        text (str): cleaned text

    Returns:
        list[str]: list of words
    """
    tokens = text.split()
    return tokens
# fix