from src.main import build_message


def test_build_message():
    assert build_message("João") == "Olá João, tudo bem com você?"
