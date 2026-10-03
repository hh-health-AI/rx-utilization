import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from _pagination import fetch_all
with patch.dict(os.environ, {"HH_CONTACT": "Offline regression tests"}):
    import open_payments
    import partd_prescribers


class PaginationTests(unittest.TestCase):
    def test_exact_cap_is_complete(self):
        rows = [{"id": n} for n in range(4)]
        self.assertEqual(fetch_all(lambda off, size: rows[off:off + size], 2, 4), rows)

    def test_over_cap_is_rejected(self):
        rows = [{"id": n} for n in range(5)]
        with self.assertRaisesRegex(ValueError, "TRUNCATED"):
            fetch_all(lambda off, size: rows[off:off + size], 2, 4)

    def test_nonmultiple_cap(self):
        rows = [{"id": n} for n in range(3)]
        self.assertEqual(fetch_all(lambda off, size: rows[off:off + size], 2, 3), rows)

    def test_server_side_page_cap_does_not_end_early(self):
        rows = [{"id": n} for n in range(5)]
        self.assertEqual(fetch_all(lambda off, size: rows[off:off + min(size, 2)], 10, 5), rows)

    def test_invalid_schema_and_repeated_page(self):
        for page in [lambda off, size: {"error": "bad dataset"},
                     lambda off, size: [{"id": 1}, {"id": 2}]]:
            with self.assertRaises(ValueError):
                fetch_all(page, 2, 10)

    def test_nonpositive_limits_rejected(self):
        for size, cap in [(0, 10), (10, 0), (-1, 10)]:
            with self.assertRaises(ValueError):
                fetch_all(lambda *_: [], size, cap)

    def test_clients_do_not_swallow_error_payloads(self):
        with patch.object(open_payments, "get", return_value={"error": "schema changed"}):
            with self.assertRaises(KeyError):
                open_payments.query("id", [], 2, 10)
        with patch.object(partd_prescribers, "get", return_value={"error": "schema changed"}):
            with self.assertRaises(ValueError):
                partd_prescribers.fetch("id", {}, 2, 10)


if __name__ == "__main__":
    unittest.main()
