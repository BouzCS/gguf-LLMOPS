import time
from fastapi import Request, Response
from prometheus_client import Counter, Gauge, Histogram

# Prometheus metrics
REQUEST_COUNT = Counter(
    "api_request_count", "Total number of requests", ["method", "endpoint"]
)
REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds", "Latency of API requests in seconds", ["method", "endpoint"]
)
ERROR_COUNT = Counter(
    "api_error_count", "Total number of errors", ["method", "endpoint"]
)

async def monitoring_middleware(request: Request, call_next):
    # Record the start time of the request
    start_time = time.time()

    # Extract request details
    method = request.method
    endpoint = request.url.path

    # Increment the request count
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

    try:
        # Process the request
        response = await call_next(request)

        # Calculate the latency
        latency = time.time() - start_time

        # Record the latency
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)

        # Check for errors (non-2xx status codes)
        if response.status_code >= 400:
            ERROR_COUNT.labels(method=method, endpoint=endpoint).inc()

        return response

    except Exception as e:
        # Increment the error count if an exception occurs
        ERROR_COUNT.labels(method=method, endpoint=endpoint).inc()
        raise e