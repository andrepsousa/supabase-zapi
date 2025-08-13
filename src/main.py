import os
from dotenv import load_dotenv
from src.services.supabase_client import fetch_contacts
from src.services.zapi_client import send_message
from src.utils.logger import get_logger

logger = get_logger("main")


def build_message(name: str) -> str:
    return f"Olá {name}, tudo bem com você?"


def main():
    load_dotenv()
    max_contacts = int(os.getenv("MAX_CONTACTS", "3"))

    contacts = fetch_contacts(limit=max_contacts)
    if not contacts:
        logger.warning(
            "Nenhum contato encontrado. "
            "Verifique a tabela 'contacts'."
        )
        return

    results = []
    for c in contacts:
        name = c.get("name") or "contato"
        phone = c.get("phone")
        if not phone:
            logger.warning("Contato sem telefone: %s", c)
            continue

        msg = build_message(name)
        res = send_message(phone, msg)
        results.append(
            {
                "id": c.get("id"),
                "name": name,
                "phone": phone,
                **res,
            }
        )

    sent = [r for r in results if r.get("ok")]
    failed = [r for r in results if not r.get("ok")]
    logger.info("✅ Enviadas: %d | ❌ Falhas: %d", len(sent), len(failed))

    if failed:
        logger.info("Falhas:")
        for r in failed:
            logger.info(
                "- %s (%s): %s %s",
                r["name"],
                r["phone"],
                r.get("status"),
                r.get("error"),
            )


if __name__ == "__main__":
    main()
