import pytest

from arris_tg2492lg.single_value_cache import SingleValueCache


class Counter:
    def __init__(self) -> None:
        self._count: int = 0

    def increment(self) -> str:
        self._count += 1
        return str(self._count)


@pytest.fixture()
def counter() -> Counter:
    return Counter()


class TestSingleValueCache:

    def test_cached_value_is_used_before_expired(self, counter: Counter) -> None:
        svc = SingleValueCache(100, counter.increment)

        assert svc.get() == "1"
        assert svc.get() == "1"

    def test_supplier_method_is_used_after_value_expired(self, counter: Counter) -> None:
        svc = SingleValueCache(-100, counter.increment)

        assert svc.get() == "1"
        assert svc.get() == "2"
