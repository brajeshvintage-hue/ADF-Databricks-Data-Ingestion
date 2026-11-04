"""Contract: null/blank names become None; whitespace collapses; uppercase.

The shared Python/Spark comparison dataset uses ASCII names. Unicode case and
whitespace rules need a separate explicit contract before international use.
"""
import re


def normalize_name(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("name must be a string or None")
    result = re.sub(r"\s+", " ", value).strip().upper()
    return result or None
