import pytest
from unittest.mock import patch, AsyncMock
from cli import cli, NotEnoughArgumentsError, TooManyArgumentsError


@pytest.mark.asyncio
async def test_cli_not_enough_args() -> None:
    """
    Tests argument validation when an insufficient number of arguments is provided.

    Asserts that a NotEnoughArgumentsError is raised when the system arguments
    list contains only the script name and omits the required input file.
    """
    with pytest.raises(NotEnoughArgumentsError):
        await cli(["main.py"])


@pytest.mark.asyncio
async def test_cli_too_many_args() -> None:
    """
    Tests argument validation when an excessive number of arguments is provided.

    Asserts that a TooManyArgumentsError is raised when the system arguments
    list contains more than the allowed maximum of three elements.
    """
    with pytest.raises(TooManyArgumentsError):
        await cli(["main.py", "input.txt", "output.json", "extra_arg"])


@pytest.mark.asyncio
@patch("cli.process_arguments", new_callable=AsyncMock)
async def test_cli_default_output_path(mock_process) -> None:
    """
    Tests the dynamic generation of the default output file path.

    Mocks the core processing function and asserts that when only the input
    file argument is provided, the CLI correctly generates a fallback filename
    by appending '.analysis.json' to the input file's stem.

    Args:
        mock_process (AsyncMock): The patched process_arguments function.
    """
    await cli(["main.py", "document.txt"])
    mock_process.assert_called_once_with("document.txt", "document.analysis.json")


@pytest.mark.asyncio
@patch("cli.process_arguments", new_callable=AsyncMock)
async def test_cli_explicit_output_path(mock_process) -> None:
    """
    Tests the enforcement of the JSON file extension for user-defined output paths.

    Mocks the core processing function and asserts that if a user provides an
    output filename missing the '.json' extension, the CLI correctly appends
    it before executing the core logic.

    Args:
        mock_process (AsyncMock): The patched process_arguments function.
    """
    await cli(["main.py", "input.txt", "QWERTY"])
    mock_process.assert_called_once_with("input.txt", "QWERTY.json")