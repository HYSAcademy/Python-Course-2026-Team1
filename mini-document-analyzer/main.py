import sys
import asyncio
from cli import cli, CLIError


def main() -> None:
    """
    Application entry point.

    Executes the asynchronous CLI workflow and acts as the top-level exception handler.
    It routes distinct error types to standard error (stderr) to provide clear error
    messages and exits the process with a non-zero status code upon failure[cite: 9].

    Returns:
        None
    """
    try:
        asyncio.run(cli(sys.argv))

    except CLIError as e:
        # Handles NotEnoughArgumentsError and TooManyArgumentsError
        print(f"CLI Error: {e}", file=sys.stderr)
        sys.exit(1)

    except (FileNotFoundError, IsADirectoryError, ValueError) as e:
        # Handles the explicit errors raised by read_text_file_async
        print(f"File Error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        # Failsafe for unhandled runtime exceptions
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
