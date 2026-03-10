import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from exporter import export_to_json


@pytest.mark.asyncio
@patch("aiofiles.open")
async def test_export_to_json_success(mock_aio_open) -> None:
    """
    Tests the successful generation and export of the analysis JSON payload.

    Mocks the asynchronous context manager for file I/O to prevent actual disk
    writes. Asserts that the file is opened with the correct path and encoding,
    and verifies that the resulting JSON string strictly adheres to the
    required dictionary schema.

    Args:
        mock_aio_open (MagicMock): The patched aiofiles.open method.
    """
    mock_file = AsyncMock()

    ctx_manager = MagicMock()
    ctx_manager.__aenter__.return_value = mock_file
    ctx_manager.__aexit__.return_value = None

    mock_aio_open.return_value = ctx_manager

    await export_to_json(
        output_path="fake_output.json",
        filename="input.txt",
        total_characters=100,
        total_words=20,
        total_sentences=2,
        cleaned_text="clean text",
        tokens=["clean", "text"],
        word_frequencies={"clean": 1, "text": 1},
        top_10_words=[("clean", 1), ("text", 1)]
    )

    mock_aio_open.assert_called_once_with("fake_output.json", mode="w", encoding="utf-8")

    written_string = mock_file.write.call_args[0][0]
    written_data = json.loads(written_string)

    assert written_data["document"]["filename"] == "input.txt"
    assert written_data["document"]["total_sentences"] == 2
    assert written_data["content"]["cleaned_text"] == "clean text"
    assert written_data["statistics"]["top_10_words"] == [["clean", 1], ["text", 1]]


@pytest.mark.asyncio
@patch("aiofiles.open", new_callable=AsyncMock)
async def test_export_to_json_io_error(mock_aio_open) -> None:
    """
    Tests error handling during the JSON export process.

    Simulates an underlying system exception during the file open operation
    and asserts that the application correctly catches it and raises a
    custom IOError with the specific failure message.

    Args:
        mock_aio_open (AsyncMock): The patched aiofiles.open method.
    """
    mock_aio_open.side_effect = Exception("Disk full")

    with pytest.raises(IOError, match="Failed to write JSON output"):
        await export_to_json(
            "fake.json", "file.txt", 0, 0, 0, "", [], {}, []
        )