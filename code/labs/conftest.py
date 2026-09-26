"""Under CHAOS_STARTERS=fail every lab test is a strict expected failure.

A starter that passes its own test is then reported as an unexpected pass,
which pytest counts as a failure -- so `CHAOS_STARTERS=fail uv run pytest
labs` exits 0 exactly when every starter still has work in it. Every test of
a lab must therefore depend on the reader's answer: a reassuring extra check
that the untouched starter already passes breaks the gate, correctly.
"""

from __future__ import annotations

import os

import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    if os.environ.get("CHAOS_STARTERS") != "fail":
        return
    marker = pytest.mark.xfail(
        reason="a starter must fail until the reader finishes it",
        strict=True,
    )
    for item in items:
        if "labs" in item.path.parts:
            item.add_marker(marker)
