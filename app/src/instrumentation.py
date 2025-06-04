import logging
from logging_loki import LokiHandler
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from prometheus_flask_exporter import PrometheusMetrics
import os

# Configurações dos endpoints
TEMPO_ENDPOINT = os.getenv('TEMPO_ENDPOINT', 'http://191.252.111.133:3200')
PROMETHEUS_ENDPOINT = os.getenv('PROMETHEUS_ENDPOINT', 'http://191.252.111.133:9090')
LOKI_ENDPOINT = os.getenv('LOKI_ENDPOINT', 'http://191.252.111.133:3100')

def configure_logging():
    """Configura o logging com Loki"""
    # Configuração do handler do Loki
    loki_handler = LokiHandler(
        url=f"{LOKI_ENDPOINT}/loki/api/v1/push",
        tags={"application": "crypto-ticker"},
        version="1",
    )
    
    # Configurar formato do log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    loki_handler.setFormatter(formatter)
    
    # Configurar logger root
    root_logger = logging.getLogger()
    root_logger.addHandler(loki_handler)
    root_logger.setLevel(logging.INFO)
    
    # Logger específico da aplicação
    logger = logging.getLogger('crypto-ticker')
    logger.setLevel(logging.INFO)
    
    return logger

def configure_metrics(app):
    """Configura métricas do Prometheus"""
    metrics = PrometheusMetrics(app)
    
    # Métricas básicas da aplicação
    metrics.info('app_info', 'Application info', version='1.0.0')
    
    # Métricas personalizadas
    metrics.counter(
        'crypto_ticker_requests_total',
        'Number of requests to the crypto ticker',
        labels={'status': lambda r: r.status_code}
    )
    
    return metrics

def configure_traces():
    """Configura traces com OpenTelemetry"""
    resource = Resource.create({
        "service.name": "crypto-ticker",
        "service.version": "1.0.0",
        "deployment.environment": os.getenv('ENVIRONMENT', 'production')
    })
    
    provider = TracerProvider(resource=resource)
    
    # Configurar exportador OTLP para o Tempo
    otlp_exporter = OTLPSpanExporter(
        endpoint=f"{TEMPO_ENDPOINT}:4317",  # Porta gRPC do Tempo
        insecure=True
    )
    
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(provider)
    
    return provider

def configure_telemetry(app):
    """Configura toda a instrumentação de observabilidade"""
    try:
        # Configurar logging com Loki
        logger = configure_logging()
        logger.info("Iniciando configuração de telemetria")
        
        # Configurar traces com OpenTelemetry
        provider = configure_traces()
        
        # Instrumentar Flask com OpenTelemetry
        FlaskInstrumentor().instrument_app(app, tracer_provider=provider)
        
        # Instrumentar requests HTTP
        RequestsInstrumentor().instrument(tracer_provider=provider)
        
        # Configurar métricas do Prometheus
        metrics = configure_metrics(app)
        
        logger.info("Configuração de telemetria concluída com sucesso")
        
        return logger, metrics
        
    except Exception as e:
        logging.error(f"Erro ao configurar telemetria: {str(e)}", exc_info=True)
        raise 