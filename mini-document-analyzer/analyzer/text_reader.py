from pathlib import Path


def read_text_file(file_path: str) -> str:
    """
    Reads text from a .txt file
    Args:
        file_path (str): Path to the text file
    Returns:
        str: File content as a string
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not a .txt file
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix != ".txt":
        raise ValueError("Only .txt files are supported")

    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    return text