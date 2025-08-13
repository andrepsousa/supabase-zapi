from src.services import supabase_client as sc


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeQuery:
    def __init__(self, data):
        self._data = data
        self._filters = []
        self._limit = None

    def select(self, *_):
        return self

    def eq(self, field, value):
        self._filters.append((field, value))
        return self

    def limit(self, n):
        self._limit = n
        return self

    def execute(self):
        rows = self._data
        for field, value in self._filters:
            rows = [r for r in rows if r.get(field) == value]
        if self._limit is not None:
            rows = rows[: self._limit]
        return FakeResponse(rows)


class FakeSB:
    def __init__(self, data):
        self._data = data

    def table(self, *_):
        return FakeQuery(self._data)


def test_fetch_contacts_filters_and_limits(monkeypatch):
    data = [
        {"id": "1", "name": "A", "phone": "5511", "active": True},
        {"id": "2", "name": "B", "phone": None, "active": True},
        {"id": "3", "name": "C", "phone": "5513", "active": False},
        {"id": "4", "name": "D", "phone": "5514", "active": True},
    ]
    fake = FakeSB(data)
    monkeypatch.setattr(sc, "get_supabase", lambda: fake, raising=True)

    res = sc.fetch_contacts(limit=3)
    ids = [c["id"] for c in res]
    assert ids == ["1", "4"]
    assert all(c.get("phone") for c in res)
