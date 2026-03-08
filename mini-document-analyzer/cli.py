from pathlib import Path
from typing import List

import analyzer
from exporter import export_to_json
from analyzer import read_text_file_async


class CLIError(Exception):
    """Base class for CLI errors"""
    pass


class NotEnoughArgumentsError(CLIError):
    """Raised when the user provides fewer arguments than required"""
    pass


class TooManyArgumentsError(CLIError):
    """Raised when the user provides more arguments than allowed"""
    pass


async def process_arguments(input_file: str, output_file: str) -> None:
    """
        Asynchronously orchestrates the text analysis workflow.

        This function reads the target file, processes the text to extract tokens
        and statistics, and triggers the JSON export[cite: 6, 7].

        Args:
            input_file (str): The file path of the input text document.
            output_file (str): The file path where the resulting JSON should be saved.

        Raises:
            FileNotFoundError: If the input file does not exist.
            IsADirectoryError: If the input path points to a directory.
            ValueError: If the input file lacks a .txt extension.
            IOError: If writing to the destination file fails.
        """
    text: str = await read_text_file_async(input_file)

    cleaned_text = analyzer.clean_text(text)
    tokens = analyzer.tokenize(cleaned_text)

    number_of_characters = analyzer.count_characters(text)
    number_of_words = analyzer.count_words(tokens)
    number_of_sentences = analyzer.count_sentences(text)
    word_frequencies_dict = analyzer.word_frequencies(tokens)
    top_10 = analyzer.top_10_words(tokens)

    filename = Path(input_file).name

    await export_to_json(
        output_path=output_file,
        filename=filename,
        total_characters=number_of_characters,
        total_words=number_of_words,
        total_sentences=number_of_sentences,
        cleaned_text=cleaned_text,
        tokens=tokens,
        word_frequencies=word_frequencies_dict,
        top_10_words=top_10
    )


async def cli(args: List[str]) -> None:
    arg_count = len(args)

    if arg_count < 2:
        raise NotEnoughArgumentsError("Insufficient arguments. Expected at least an input file.")
    if arg_count > 3:
        raise TooManyArgumentsError("Too many arguments. Expected input and optional output file.")

    input_file = args[1]

    if arg_count == 3:
        output_file = f"{args[2]}.analysis.json"
    else:
        input_path = Path(input_file)
        output_file = str(input_path.with_name(f"{input_path.stem}.analysis.json"))

    await process_arguments(input_file, output_file)