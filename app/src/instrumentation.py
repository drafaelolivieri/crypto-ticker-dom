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

# Configurações dos endpoints (usando IP externo e portas corretas)
TEMPO_ENDPOINT = os.getenv('TEMPO_ENDPOINT', 'http://191.252.111.133:4317')  # Usando gRPC
PROMETHEUS_ENDPOINT = os.getenv('PROMETHEUS_ENDPOINT', 'http://191.252.111.133:9090')
LOKI_ENDPOINT = os.getenv('LOKI_ENDPOINT', 'http://191.252.111.133:3100')

# Configuração de fallback para logging quando Loki não está disponível
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def configure_logging():
    """Configura o logging com Loki"""
    try:
        # Configuração do handler do Loki
        loki_handler = LokiHandler(
            url=f"{LOKI_ENDPOINT}/loki/api/v1/push",
            tags={"application": "crypto-ticker"},
            version="1",
        )
        
        # Configurar formato do log
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        loki_handler.setFormatter(formatter)
        
        # Logger específico da aplicação
        logger = logging.getLogger('crypto-ticker')
        logger.setLevel(logging.INFO)
        logger.addHandler(loki_handler)
        
        return logger
    except Exception as e:
        # Em caso de erro, retorna um logger padrão
        logger = logging.getLogger('crypto-ticker')
        logger.warning(f"Falha ao configurar Loki, usando logging padrão: {str(e)}")
        return logger

def configure_metrics(app):
    """Configura métricas do Prometheus"""
    try:
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
    except Exception as e:
        logging.warning(f"Falha ao configurar Prometheus metrics: {str(e)}")
        return None

def configure_traces():
    """Configura traces com OpenTelemetry"""
    try:
        resource = Resource.create({
            "service.name": "crypto-ticker",
            "service.version": "1.0.0",
            "deployment.environment": os.getenv('ENVIRONMENT', 'production')
        })
        
        provider = TracerProvider(resource=resource)
        
        # Configurar exportador OTLP para o Tempo
        otlp_exporter = OTLPSpanExporter(
            endpoint=TEMPO_ENDPOINT,  # Já usando a porta gRPC correta
            insecure=True
        )
        
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        trace.set_tracer_provider(provider)
        
        return provider
    except Exception as e:
        logging.warning(f"Falha ao configurar OpenTelemetry traces: {str(e)}")
        return None

def configure_telemetry(app):
    """Configura toda a instrumentação de observabilidade"""
    # Configurar logging primeiro para ter logs disponíveis
    logger = configure_logging()
    logger.info("Iniciando configuração de telemetria")
    
    # Configurar traces com OpenTelemetry
    provider = configure_traces()
    if provider:
        # Instrumentar Flask com OpenTelemetry
        try:
            FlaskInstrumentor().instrument_app(app, tracer_provider=provider)
            RequestsInstrumentor().instrument(tracer_provider=provider)
        except Exception as e:
            logger.warning(f"Falha ao instrumentar Flask/Requests: {str(e)}")
    
    # Configurar métricas do Prometheus
    metrics = configure_metrics(app)
    
    logger.info("Configuração de telemetria concluída")
    
    return logger, metrics 