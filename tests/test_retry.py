
import pytest

import src.local_rag.retry as retry_module


def test_ollama_retry_succeeds_after_temporary_errors(monkeypatch):
    """Prüft, ob ein Aufruf nach temporären Fehlern erneut versucht wird."""

    # Wartezeit auf null setzen, damit der Test schnell ausgeführt wird.
    monkeypatch.setattr(
        retry_module,
        "wait_exponential",
        lambda **kwargs: lambda retry_state: 0,
    )

    calls = {"count": 0}

    @retry_module.ollama_retry(attempts=3)
    def unstable_call():
        calls["count"] += 1

        if calls["count"] < 3:
            raise ConnectionError("Temporärer Verbindungsfehler")

        return "OK"

    result = unstable_call()

    assert result == "OK"
    assert calls["count"] == 3


def test_ollama_retry_stops_after_maximum_attempts(monkeypatch):
    """Prüft, ob nach der maximalen Anzahl von Versuchen Schluss ist."""

    monkeypatch.setattr(
        retry_module,
        "wait_exponential",
        lambda **kwargs: lambda retry_state: 0,
    )

    calls = {"count": 0}

    @retry_module.ollama_retry(attempts=2)
    def failing_call():
        calls["count"] += 1
        raise ConnectionError("Ollama ist nicht erreichbar")

    with pytest.raises(ConnectionError):
        failing_call()

    assert calls["count"] == 2


def test_ollama_retry_rejects_invalid_attempt_count():
    """Prüft, ob null Versuche als ungültig erkannt werden."""

    with pytest.raises(ValueError):
        retry_module.ollama_retry(attempts=0)
