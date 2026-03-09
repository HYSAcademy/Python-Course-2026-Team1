import pytest
from pathlib import Path

from analyzer import (
    read_text_file_async,
    clean_text,
    tokenize,
    count_characters,
    count_words,
    count_sentences,
    word_frequencies,
    top_10_words
)


@pytest.mark.asyncio
async def test_read_text_file_async_success(tmp_path: Path) -> None:
    """
    Tests successful asynchronous reading of a valid .txt file.

    Creates a temporary text file with known content, passes its path to the
    reader function, and asserts that the returned string matches the input.

    Args:
        tmp_path (Path): Built-in pytest fixture providing a temporary directory.
    """
    test_file = tmp_path / "valid_input.txt"
    expected_content = "This is a test document."
    test_file.write_text(expected_content, encoding="utf-8")

    content = await read_text_file_async(str(test_file))
    assert content == expected_content


@pytest.mark.asyncio
async def test_read_text_file_async_file_not_found() -> None:
    """
    Tests error handling when the target text file does not exist.

    Asserts that a FileNotFoundError is raised when attempting to read
    from an invalid path.
    """
    with pytest.raises(FileNotFoundError):
        await read_text_file_async("non_existent_file.txt")


@pytest.mark.asyncio
async def test_read_text_file_async_is_directory(tmp_path: Path) -> None:
    """
    Tests error handling when the target path is a directory.

    Asserts that an IsADirectoryError is raised when the provided path
    points to a folder instead of a target file.

    Args:
        tmp_path (Path): Built-in pytest fixture providing a temporary directory.
    """
    with pytest.raises(IsADirectoryError):
        await read_text_file_async(str(tmp_path))


@pytest.mark.asyncio
async def test_read_text_file_async_invalid_extension(tmp_path: Path) -> None:
    """
    Tests error handling when the target file lacks a .txt extension.

    Creates a temporary .csv file and asserts that a ValueError is explicitly
    raised regarding unsupported file types.

    Args:
        tmp_path (Path): Built-in pytest fixture providing a temporary directory.
    """
    invalid_file = tmp_path / "data.csv"
    invalid_file.write_text("data", encoding="utf-8")

    with pytest.raises(ValueError, match="Only .txt files are supported"):
        await read_text_file_async(str(invalid_file))


@pytest.mark.parametrize("input_text, expected", [
    ("Hello World!", "hello world"),
    ("Punctuation, removed.", "punctuation removed"),
    ("123 Numbers remain!", "123 numbers remain"),
    ("", "")
])
def test_clean_text(input_text: str, expected: str) -> None:
    """
    Tests the text cleaning utility across multiple input scenarios.

    Asserts that the function correctly converts all characters to lowercase
    and strips all standard punctuation marks.

    Args:
        input_text (str): The raw string to be cleaned.
        expected (str): The anticipated output string.
    """
    assert clean_text(input_text) == expected


def test_tokenize() -> None:
    """
    Tests the tokenization of a cleaned text string.

    Asserts that a continuous string of words separated by spaces is
    correctly split into a list of individual word tokens.
    """
    text = "this is a cleaned text string"
    expected = ["this", "is", "a", "cleaned", "text", "string"]
    assert tokenize(text) == expected


def test_count_characters() -> None:
    """
    Tests the character counting logic.

    Asserts that the function calculates the exact integer length of the raw
    string, including spaces and newline characters.
    """
    text = "Hello\nWorld!"
    assert count_characters(text) == 12


def test_count_words() -> None:
    """
    Tests the word counting logic.

    Asserts that the function returns the correct integer length of the
    provided list of tokens.
    """
    tokens = ["this", "is", "a", "test"]
    assert count_words(tokens) == 4


@pytest.mark.parametrize("input_text, expected_count", [
    ("One sentence.", 1),
    ("Two sentences! Right?", 2),
    ("No punctuation here", 0),
    ("Wait... what?!", 2)
])
def test_count_sentences(input_text: str, expected_count: int) -> None:
    """
    Tests the sentence counting logic across multiple punctuation scenarios.

    Asserts that the function accurately counts occurrences of terminal
    punctuation marks (., !, ?).

    Args:
        input_text (str): The raw string to be evaluated.
        expected_count (int): The expected integer count of sentences.
    """
    assert count_sentences(input_text) == expected_count


def test_word_frequencies() -> None:
    """
    Tests the generation of the word frequency dictionary.

    Asserts that a list of tokens is correctly mapped to a dictionary where
    keys are unique words and values are their occurrence counts.
    """
    tokens = ["test", "data", "test", "word"]
    expected = {"test": 2, "data": 1, "word": 1}
    assert word_frequencies(tokens) == expected


def test_top_10_words() -> None:
    """
    Tests the extraction and sorting of the top 10 most frequent words.

    Asserts that the function returns a list of tuples sorted by frequency
    in descending order.
    """
    tokens = ["a"] * 15 + ["b"] * 10 + ["c"] * 5 + ["d"] * 2
    expected = [("a", 15), ("b", 10), ("c", 5), ("d", 2)]
    assert top_10_words(tokens) == expected