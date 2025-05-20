
FROM python:3.9-slim

WORKDIR /app

COPY fastapi_app.py .

RUN pip install fastapi uvicorn opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-logging opentelemetry-instrumentation-requests prometheus-fastapi-instrumentator

CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
