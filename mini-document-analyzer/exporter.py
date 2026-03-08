import json
import aiofiles
from typing import Dict, List, Tuple

async def export_to_json(
    output_path: str,
    filename: str,
    total_characters: int,
    total_words: int,
    total_sentences: int,
    cleaned_text: str,
    tokens: List[str],
    word_frequencies: Dict[str, int],
    top_10_words: List[Tuple[str, int]]
) -> None:
    """
    Asynchronously formats and writes the analysis results to a JSON file.

    Args:
        output_path: The file path where the JSON will be saved.
        filename: The original name of the analyzed text file.
        total_characters: Total character count including spaces.
        total_words: Total word count.
        total_sentences: Total sentence count based on punctuation.
        cleaned_text: The text converted to lowercase with punctuation removed.
        tokens: A list of individual words from the cleaned text.
        word_frequencies: A dictionary mapping words to their frequency counts.
        top_10_words: A list of tuples containing the top 10 words and their counts.

    Raises:
        IOError: If writing to the destination file fails.
    """
    payload = {
        "document": {
            "filename": filename,
            "total_characters": total_characters,
            "total_words": total_words,
            "total_sentences": total_sentences
        },
        "content": {
            "cleaned_text": cleaned_text,
            "tokens": tokens
        },
        "statistics": {
            "word_frequencies": word_frequencies,
            "top_10_words": top_10_words
        }
    }

    try:
        async with aiofiles.open(output_path, mode="w", encoding="utf-8") as f:
            await f.write(json.dumps(payload, indent=2))
    except Exception as e:
        raise IOError(f"Failed to write JSON output to {output_path}: {str(e)}")