import os
import httpx
import time
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger("zapi")


def _normalize_phone(phone: str) -> str:
    digits = "".join(c for c in (phone or "").strip() if c.isdigit())
    return digits


def send_message(phone: str, message: str) -> Dict[str, Any]:
    url = os.getenv("ZAPI_SEND_URL")
    client_token = os.getenv("ZAPI_CLIENT_TOKEN")

    if not url:
        raise RuntimeError("ZAPI_SEND_URL é obrigatório (.env).")
    if not client_token:
        raise RuntimeError("ZAPI_CLIENT_TOKEN é obrigatório (.env).")

    payload = {"phone": _normalize_phone(phone), "message": message}

    headers = {
        "Client-Token": client_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    attempts = 0
    backoff = 1.0
    while attempts < 3:
        attempts += 1
        try:
            with httpx.Client(timeout=15, headers=headers) as client:
                resp = client.post(url, json=payload)
                if 200 <= resp.status_code < 300:
                    logger.info(
                        "Mensagem enviada para %s.",
                        _normalize_phone(phone),
                    )
                    try:
                        data = resp.json()
                    except Exception:
                        data = {"raw": resp.text}
                    return {
                        "ok": True,
                        "status": resp.status_code,
                        "data": data,
                    }
                else:
                    logger.warning(
                        "Falha (%s) ao enviar para %s: %s",
                        resp.status_code,
                        _normalize_phone(phone),
                        resp.text,
                    )
                    if 500 <= resp.status_code < 600 and attempts < 3:
                        time.sleep(backoff)
                        backoff *= 2
                        continue
                    return {
                        "ok": False,
                        "status": resp.status_code,
                        "error": resp.text,
                    }
        except httpx.HTTPError as e:
            logger.warning(
                "Erro de rede ao enviar para %s: %s",
                _normalize_phone(phone),
                e,
            )
            if attempts < 3:
                time.sleep(backoff)
                backoff *= 2
                continue
            return {"ok": False, "status": None, "error": str(e)}
    return {
        "ok": False,
        "status": None,
        "error": "Tentativas esgotadas",
    }
