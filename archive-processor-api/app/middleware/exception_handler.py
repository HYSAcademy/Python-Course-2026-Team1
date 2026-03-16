import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class InvalidFileException(Exception):
    """Exception raised when an uploaded file fails validation."""

    def __init__(self, message: str):
        self.message = message


async def invalid_file_handler(
        request: Request, exc: InvalidFileException
) -> JSONResponse:
    """Handles 400 Bad Request errors for file validation failures."""
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid File", "message": exc.message},
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles unexpected 500 Server Errors securely without leaking internals."""
    # Log the actual error for debugging, do not expose to the client
    logger.error(f"Unexpected server error at {request.url}: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Server Error",
            "message": "An unexpected internal error occurred. Please try again later.",
        },
    )