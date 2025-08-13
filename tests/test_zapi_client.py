import respx
import httpx
import pytest
from src.services.zapi_client import send_message


def test_send_message_missing_env_url(monkeypatch):
    monkeypatch.delenv("ZAPI_SEND_URL", raising=False)
    monkeypatch.setenv("ZAPI_CLIENT_TOKEN", "X")
    with pytest.raises(RuntimeError):
        send_message("5511", "hi")


def test_send_message_missing_env_token(monkeypatch):
    monkeypatch.setenv("ZAPI_SEND_URL", "https://api")
    monkeypatch.delenv("ZAPI_CLIENT_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        send_message("5511", "hi")


@respx.mock
def test_send_message_network_exception(monkeypatch):
    monkeypatch.setenv("ZAPI_SEND_URL", "https://api")
    monkeypatch.setenv("ZAPI_CLIENT_TOKEN", "X")

    respx.post("https://api").mock(side_effect=httpx.ConnectTimeout("x"))
    result = send_message("5511", "hi")
    assert result["ok"] is False
    assert result["status"] is None
    assert "x" in result["error"]
