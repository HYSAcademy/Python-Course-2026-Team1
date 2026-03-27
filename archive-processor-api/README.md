# **Archive Processor API**

A high-performance asynchronous system for ZIP archive extraction, TF-IDF indexing, and similarity-based document search. Built with a focus on scalability and sub-second response times under heavy concurrent load.

## **Core Features**

- **Asynchronous Processing**: Non-blocking ZIP extraction and indexing using Celery and Redis.
- **TF-IDF Search Engine**: Vector-based document retrieval using Scikit-learn with cosine similarity scoring.
- **High Concurrency Support**: Optimized FastAPI/SQLAlchemy integration capable of handling 500+ RPS.
- **Automated Validation**: Pydantic-driven request validation and robust error handling.
- **Scalable Infrastructure**: Containerized environment with separate web and worker services.

## **Technical Architecture**

### **Stack**

- **Framework**: FastAPI (Asynchronous ASGI)
- **Task Queue**: Celery \+ Redis
- **Database**: PostgreSQL with SQLAlchemy (Asyncio \+ NullPool)
- **Text Analysis**: Scikit-learn (TfidfVectorizer)
- **Linting/Formatting**: Ruff

### **Key Architectural Decisions**

- **NullPool Strategy**: Connection pooling is disabled to prevent event loop conflicts during high-frequency asynchronous task execution, ensuring every worker task maintains a fresh, loop-local database connection.
- **Shared Volume Logic**: Web and worker services share a persistent volume for processed indices, allowing instant search availability once indexing tasks conclude.
- **Scoped Search**: Search is scoped by archive\_id to ensure mathematical accuracy in term weighting (IDF) and to minimize RAM overhead for large datasets.

## **Performance Benchmarks (SCRUM-30)**

The system was subjected to extensive stress testing using Locust to verify stability and throughput.

| Metric | Target | Actual Result |
| --- | --- | --- |
| **Concurrent Users** | N/A | 1,320 |
| **Throughput (RPS)** | 20+ | **504.7** |
| **Stability** | No Crashes | 0% Failure Rate |
| **Search Latency (Median)** | Sub-second | 240 ms |
| **Saturation Point** | N/A | \~1,900 Users |

*Note: Saturation testing revealed that the system hits OS-level file descriptor limits before the application code fails, demonstrating high architectural efficiency.*

## **Getting Started**

### **Prerequisites**

- Docker & Docker Compose
- Python 3.12+

### **Installation**

1. Clone the repository:  
  git clone \<repository-url\>  
  cd archive-processor-api
  
2. Start the services:  
  docker-compose up \--build
  
3. Access the API documentation at http://localhost:8000/docs.
  

### **Running Load Tests**

Locust is used for performance verification. Ensure the test data exists in data/uploads/test.zip.  
locust \-f app/locustfile.py \--host http://localhost:8000

## **API Specification**

### **Archives**

- POST /api/v1/upload-archives/: Upload ZIP files for extraction.
- GET /api/v1/status/{archive\_id}/status: Check extraction and metadata status.

### **Indexing & Search**

- POST /api/v1/archives/trigger: Manually trigger TF-IDF indexing for a processed archive.
- GET /api/v1/search/{archive\_id}?query=...: Search within an archive using natural language queries.

**Author**: Team 1 
**Date**: March 2026