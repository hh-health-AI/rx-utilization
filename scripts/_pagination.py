"""Strict offset pagination: never return a capped partial population as complete."""
import hashlib
import json


def fetch_all(page, size, max_rows):
    if size < 1 or max_rows < 1:
        raise ValueError("Page size and row limit must be positive")
    rows, fingerprints = [], set()
    while True:
        # Probe one extra row at the cap to distinguish exact completion from truncation.
        requested = min(size, max_rows - len(rows) + 1)
        batch = page(len(rows), requested)
        if not isinstance(batch, list) or any(not isinstance(r, dict) for r in batch):
            raise ValueError("Unexpected page schema; partial results discarded")
        if len(batch) > requested:
            raise ValueError("API ignored page-size limit; partial results discarded")
        if batch:
            fingerprint = hashlib.sha256(json.dumps(batch, sort_keys=True).encode()).digest()
            if fingerprint in fingerprints:
                raise ValueError("Repeated page; offset may have been ignored")
            fingerprints.add(fingerprint)
        rows.extend(batch)
        if len(rows) > max_rows:
            raise ValueError("TRUNCATED: query exceeds --max-rows; narrow filters or raise the cap. "
                             "No partial population is returned.")
        # Some endpoints enforce a smaller page size than requested. A short
        # page is not proof of exhaustion; advance by actual rows until empty.
        if not batch:
            return rows
