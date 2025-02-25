import logging
import os

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

service_name = os.environ.get("service_name")
instance_id = os.environ.get("instance_id")
endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")

logger_provider = LoggerProvider(
    resource=Resource.create(
        {
            "service.name": service_name,
            "service.instance.id": instance_id,
        }
    ),
)
set_logger_provider(logger_provider)

exporter = OTLPLogExporter(
    endpoint=endpoint,
)

logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

logging.getLogger().addHandler(handler)
logger = logging.getLogger(service_name)
logger.setLevel(logging.INFO)

def send_logs(logs_data):
    logger.info(logs_data)

def send_error(*error_message):
    logger.error(msg=error_message)
