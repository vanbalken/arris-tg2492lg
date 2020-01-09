import unittest

from arris_tg2492lg.single_value_cache import SingleValueCache


class TestSingleValueCache(unittest.TestCase):
    count = 0

    def counter(self):
        self.count += 1
        return self.count

    def setUp(self):
        self.count = 0

    def test_cached_value_is_used_before_expired(self):
        svc = SingleValueCache(100, self.counter)

        self.assertEqual(svc.get(), 1)
        self.assertEqual(svc.get(), 1)

    def test_supplier_method_is_used_after_value_expired(self):
        svc = SingleValueCache(0, self.counter)

        self.assertEqual(svc.get(), 1)
        self.assertEqual(svc.get(), 2)
