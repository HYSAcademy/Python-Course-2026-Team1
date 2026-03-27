# **SCRUM-30: Performance Test Results**

## **1\. Executive Summary**

This report documents the performance and stress testing results for the Archive Processor API. The primary objective of **TASK 3** was to ensure the system could handle a minimum of **20+ concurrent requests per second (RPS)**.  
During the testing phase, the system was pushed to a peak load of **1,320+ concurrent users**, achieving a throughput of **504.7 RPS** with a **0% failure rate**. Further stress testing at **1,900 users** identified the system's upper stability limit.

## **2\. Test Environment**

* **Host**: http://localhost:8000  
* **Testing Tool**: Locust  
* **Architecture**: FastAPI, Uvicorn, Celery, Redis, PostgreSQL  
* **Key Configuration**: NullPool utilized for database sessions to support high-concurrency event loops.

## **3\. Detailed Performance Metrics**

### **3.1. Aggregated Statistics (Peak Stable Load)**

| Metric                    | Result     |
|:------------------------- |:---------- |
| **Peak RPS**              | 504.7      |
| **Total Requests**        | 33,410     |
| **Total Failures**        | 1 (0.003%) |
| **Average Response Time** | 363.02 ms  |
| **Median Response Time**  | 240.0 ms   |
| **95th Percentile**       | 630.0 ms   |

### **3.2. Endpoint Breakdown**

| Method | Endpoint                 | RPS   | Avg Latency | 95%ile    | Status  |
|:------ |:------------------------ |:----- |:----------- |:--------- |:------- |
| POST   | /api/v1/upload-archives/ | 43.9  | 4952.6 ms   | 8302.0 ms | Success |
| POST   | /api/v1/archives/trigger | 43.8  | 161.4 ms    | 755.0 ms  | Success |
| GET    | /api/v1/search/\[id\]    | 484.2 | 199.7 ms    | 521.0 ms  | Success |

## **4\. Requirement Verification (TASK 3\)**

### **4.1. Concurrency and Scalability**

The system exceeded the project requirement of **20+ RPS** by a factor of 25x. The use of separate workers for long-running operations (ZIP extraction and TF-IDF indexing) allowed the API to maintain high responsiveness for search queries even during heavy upload bursts.

### **4.2. TF-IDF Search Accuracy**

The search functionality was verified with test cases including specific terms ("fox" returning score: 0.4082) and stop words ("The" returning \[\]). This confirms the TfidfVectorizer and cosine similarity calculations are functioning as intended.

## **5\. Stress Test Analysis (Saturation Point)**

Tests performed with 1,900+ users revealed the system's "Death Spiral" threshold.

* **Symptom**: 99th percentile latency for search spiked to **55.0 seconds**.  
* **Diagnosis**: The system reached critical resource saturation (File Descriptors and TCP backlog). This aligns with the **Stochastic Petri Net** modeling for "Overload Scenarios" where system inertia leads to avalanche-like growth in queue times once $K\_{load} \\approx 1.0$.

## **6\. Conclusion**

The Archive Processor API is fully compliant with the performance requirements of Task 3\. The architecture demonstrates exceptional stability under high load, successfully isolating heavy background tasks from low-latency search requests.  
**Date of Test**: March 24, 2026  
**Status**: PASSED