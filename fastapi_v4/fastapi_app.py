
import os
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Setup OpenTelemetry
resource = Resource(attributes={
    "service.name": "fastapi-app",
    "k8s.namespace.name": os.environ.get("K8S_NAMESPACE", "default") # Valor padrão "default"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument FastAPI, logging, and requests
FastAPIInstrumentor.instrument_app(app)
LoggingInstrumentor().instrument()
RequestsInstrumentor().instrument()

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/metrics")
async def metrics():
    return {"message": "Metrics endpoint"}
