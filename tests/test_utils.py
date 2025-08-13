from src.services.zapi_client import _normalize_phone


def test_normalize_phone():
    assert _normalize_phone("+55 (11) 99999-8888") == "5511999998888"
    assert _normalize_phone(" 11999998888 ") == "11999998888"
    assert _normalize_phone(None) == ""
