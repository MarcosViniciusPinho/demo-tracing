from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import atexit

def init_observability(service_name, host: str):
    # Configuração do Tracer Provider
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({
                "service.name": service_name
            })
        )
    )

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=host,
                insecure=True
            )
        )
    )

    # Instrumenta a biblioteca requests
    RequestsInstrumentor().instrument()

    # Registra o shutdown para finalizar o tracer provider no encerramento da aplicação
    atexit.register(lambda: (trace.get_tracer_provider().shutdown(), print("Trace encerrado na aplicação")))

def start_span(trace_name: str, span_name: str):
    tracer = trace.get_tracer(trace_name)
    return tracer.start_as_current_span(span_name)

def log_request_info(message: str):
    print(message)

def set_span_attributes(span, attributes: dict):
    for key, value in attributes.items():
        if value is not None:
            span.set_attribute(key, value)
        else:
            span.set_attribute(key, "undefined")

def set_span_record_exception(span, attributes: dict):
    for key, value in attributes.items():
        if value is not None:
            span.record_exception(key, value)
        else:
            span.record_exception(key, "undefined")