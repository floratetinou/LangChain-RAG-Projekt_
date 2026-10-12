
import logging

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

# Vorübergehende Verbindungs- und Netzwerkfehler.
TRANSIENT_ERRORS = (
    ConnectionError,
    TimeoutError,
    OSError,
    httpx.TimeoutException,
    httpx.NetworkError,
)


def ollama_retry(attempts: int):
    """Wiederholt Ollama-Aufrufe bei vorübergehenden Netzwerkfehlern."""
    if attempts < 1:
        raise ValueError("Die Anzahl der Versuche muss mindestens 1 sein.")

    return retry(
        retry=retry_if_exception_type(TRANSIENT_ERRORS),
        stop=stop_after_attempt(attempts),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
