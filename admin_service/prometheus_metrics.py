from flask import request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Metrics definitions
REQUEST_COUNT = Counter(
    'flask_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'flask_http_request_latency_seconds',
    'HTTP request latency',
    ['endpoint']
)

def setup_metrics(app):
    # Before request: start timer
    @app.before_request
    def start_timer():
        try:
            endpoint = request.path or "unknown"
            request.start_time = REQUEST_LATENCY.labels(endpoint=endpoint).time()
        except Exception as e:
            print(f"Error in start_timer: {e}")

    # After request: record metrics
    @app.after_request
    def record_request_data(response):
        try:
            endpoint = request.path or "unknown"
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                http_status=str(response.status_code)
            ).inc()

            if hasattr(request, 'start_time'):
                request.start_time.observe_duration()
        except Exception as e:
            print(f"Error in record_request_data: {e}")

        return response

    # Expose /metrics endpoint
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)