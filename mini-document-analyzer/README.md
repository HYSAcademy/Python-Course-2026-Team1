
# Mini Document Analyzer

## Project Description

Mini Document Analyzer is a Python application designed to process plain text documents and extract useful textual information.

The application reads `.txt` files, performs preprocessing and tokenization, and calculates basic statistics about the document content.

The system is built with a modular architecture that separates:

-   document reading
    
-   text tokenization
    
-   statistical analysis
    
-   CLI interface
    
-   containerized execution
    

The project can run either **locally using Python** or **inside a Docker container**.

----------

# Architecture Overview

The project is organized into independent modules responsible for different parts of the processing pipeline.

```text
mini-document-analyzer/
│
├── analyzer/
│   ├── text_reader.py      # Asynchronous file reading
│   ├── tokenizer.py        # Text preprocessing and tokenization
│   └── statistics.py       # Text statistics calculations
│
├── data/                   # Example input files
│
├── cli.py                  # CLI argument parsing
├── exporter.py             # Export processed data
├── main.py                 # Application entry point
│
├── Dockerfile              # Container definition
├── compose.yaml            # Docker Compose configuration
│
├── pyproject.toml          # Poetry dependency configuration
├── poetry.lock
│
└── README.md

```

### Processing Flow

1.  User provides a `.txt` file.
    
2.  `text_reader` loads the file.
    
3.  `tokenizer` cleans and splits the text into tokens.
    
4.  `statistics` calculates word frequencies and other metrics.
    
5.  Results are returned to output.txt
    

----------

# Setup Instructions

## Local Environment Setup

### Requirements

-   Python **3.12+**
    
-   **Poetry** dependency manager
    

Install Poetry:

[https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

### Install Dependencies

```bash
poetry install

----------

# Running the Application Locally

Run the analyzer with a text file:

python main.py data/example.txt
```


The program will read the file and output analysis results to the output.txt.

----------

# Docker Setup

The project can also run inside a Docker container.

### Build Container

```bash
docker compose build

```

### Run the Application

```bash
docker compose run --rm server python main.py data/example.txt

```

The `data` folder is mounted into the container:

```
./data → /app/data

```

This allows the container to access local input files.

----------

# API Endpoint Documentation

The container exposes port **8000**, which allows interaction with the application through HTTP requests.

Base URL:

```
http://localhost:8000

```

### Example Endpoint

#### Analyze Document

**Request**

```
POST /analyze

```

Example request:

```bash
curl -X POST http://localhost:8000/analyze \
-F "file=@data/example.txt"

```

Example response:

```json
{
  "filename": "example.txt",
  "total_words": 120,
  "unique_words": 85
}

```

_(Note: actual response structure may depend on implementation.)_

----------

# Environment Variables

Docker loads environment variables from a `.env` file defined in `compose.yaml`.

Example configuration:

```
LOG_LEVEL=INFO
APP_PORT=8000

```

Variable

Description

Default

LOG_LEVEL

Logging verbosity level

INFO

APP_PORT

Application port

8000

----------

# Usage Examples

### Local Execution

```
python main.py data/sample.txt

```

### Docker Execution

```
docker compose run --rm server python main.py data/sample.txt

```

### API Request Example

```
curl http://localhost:8000/analyze

```

----------

# Troubleshooting

### File Not Found

Ensure the file path is correct relative to the execution directory.

Example:

```
data/example.txt

```

----------

### Docker Cannot Access File

Files must be placed inside the mounted `data` directory.

```
./data → /app/data

```

----------

### Poetry Installation Issues

Reinstall dependencies:

```bash
poetry lock
poetry install

```

----------

# Future Improvements

Planned improvements include:

-   exporting results to JSON
