def read_text_file(file_path: str) -> str:
    """
    Reads text from a .txt file.

    Args:
        file_path (str): Path to the text file

    Returns:
        str: File content as a string
    """
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text
# fix