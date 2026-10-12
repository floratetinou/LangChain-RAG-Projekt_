from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

def ollama_retry(attempts: int):
    """Decorator für vorübergehende Ollama-Verbindungsfehler."""
    return retry(
        retry=retry_if_exception_type((ConnectionError, TimeoutError, OSError)),
        stop=stop_after_attempt(attempts),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True,
    )
