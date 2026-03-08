import aiofiles
from pathlib import Path

async def read_text_file_async(file_path: str) -> str:
    """
    Asynchronously reads text from a .txt file, with error handling.

    This function performs the following steps:
    1. Checks if the given path exists; raises FileNotFoundError if not.
    2. Checks if the path is a directory; raises IsADirectoryError if so.
    3. Checks if the file has a .txt extension; raises ValueError otherwise.
    4. Reads the content of the file asynchronously using aiofiles.
    5. Returns the content as a string.

    Args:
        file_path (str): Path to the .txt file to read.

    Returns:
        str: The content of the text file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If the path is a directory instead of a file.
        ValueError: If the file is not a .txt file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.is_dir():
        raise IsADirectoryError(f"Expected a file but got directory: {file_path}")

    if path.suffix != ".txt":
        raise ValueError("Only .txt files are supported")

    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        text = await f.read()

    return text