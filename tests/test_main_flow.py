import importlib
import src.main as main_mod


def reload_main():
    importlib.reload(main_mod)
    return main_mod


def test_main_no_contacts(monkeypatch, caplog):
    monkeypatch.setenv("MAX_CONTACTS", "3")
    monkeypatch.setattr(
        "src.services.supabase_client.fetch_contacts",
        lambda limit=3: [],
        raising=True,
    )

    m = reload_main()
    m.main()
    assert "Nenhum contato encontrado" in caplog.text


def test_main_contact_without_phone(monkeypatch, caplog):
    monkeypatch.setenv("MAX_CONTACTS", "3")
    contacts = [
        {"id": "1", "name": "SemFone", "phone": None, "active": True},
        {"id": "2", "name": "ComFone", "phone": "5511999999999", "active": True},
    ]
    monkeypatch.setattr(
        "src.services.supabase_client.fetch_contacts",
        lambda limit=3: contacts,
        raising=True,
    )

    sent_log = {"called": False}

    def fake_send(phone, msg):
        sent_log["called"] = True
        return {"ok": True, "status": 200, "data": {}}

    monkeypatch.setattr(
        "src.services.zapi_client.send_message",
        fake_send,
        raising=True,
    )

    m = reload_main()
    m.main()

    assert "Contato sem telefone" in caplog.text
    assert sent_log["called"] is True
    assert "✅ Enviadas: 1 | ❌ Falhas: 0" in caplog.text


def test_main_happy_path(monkeypatch, caplog):
    monkeypatch.setenv("MAX_CONTACTS", "2")
    contacts = [
        {"id": "1", "name": "Alice", "phone": "5511988887777", "active": True},
        {"id": "2", "name": "Bruno", "phone": "5511999998888", "active": True},
    ]
    monkeypatch.setattr(
        "src.services.supabase_client.fetch_contacts",
        lambda limit=2: contacts,
        raising=True,
    )

    calls = []

    def fake_send(phone, msg):
        calls.append((phone, msg))
        return {"ok": True, "status": 200, "data": {}}

    monkeypatch.setattr(
        "src.services.zapi_client.send_message", fake_send, raising=True)

    m = reload_main()
    m.main()

    assert len(calls) == 2
    assert calls[0][1] == "Olá Alice, tudo bem com você?"
    assert calls[1][1] == "Olá Bruno, tudo bem com você?"
    assert "✅ Enviadas: 2 | ❌ Falhas: 0" in caplog.text
