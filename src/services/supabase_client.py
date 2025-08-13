import os
from supabase import create_client
from src.utils.logger import get_logger

logger = get_logger("supabase")


def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL e SUPABASE_ANON_KEY são obrigatórios (.env).")
    return create_client(url, key)


def fetch_contacts(limit: int = 3):
    sb = get_supabase()
    res = (
        sb.table("contacts")
        .select("id,name,phone,active")
        .eq("active", True)
        .limit(limit)
        .execute()
    )
    data = [c for c in (res.data or []) if c.get("phone")]
    logger.info(f"{len(data)} contato(s) carregado(s) do Supabase.")
    return data
