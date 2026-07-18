"""Regression: a zero-quantity on-hand entry must NOT fake coverage of a fuzzy
name-match (2026-06-27). 'Crushed tomatoes' was reading as covered/CHECK because
the cycle snapshot carried 'Roma tomatoes: 0' (an out-of-stock placeholder) and the
shared 'tomatoes' token name-matched it. A qty==0 means "have none" → must BUY.

Run: python -m pytest scripts/tests/test_grocery_zero_qty.py
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # meal-planning/
PY = sys.executable


def _grocery(cycle):
    r = subprocess.run([PY, str(ROOT / "scripts" / "grocery.py"), str(cycle)],
                       capture_output=True, text=True, encoding="utf-8")
    return r.stdout


def test_zero_qty_snapshot_does_not_fake_coverage():
    """On the live Banff cycle, crushed tomatoes (not on hand; only a Roma:0
    placeholder shares the 'tomatoes' token) must be a BUY, not covered/CHECK."""
    out = _grocery(ROOT / "cycles" / "2026-06-27.yaml")
    # find the crushed tomatoes line
    line = next((l for l in out.splitlines() if "Crushed tomatoes" in l), "")
    assert line, "crushed tomatoes line missing from grocery output"
    assert "buy" in line.lower(), f"crushed tomatoes should be BUY, got: {line.strip()}"
    assert "covered" not in line.lower()


def test_real_quantity_still_covers():
    """Sanity: items with a REAL on-hand quantity still net as covered (chicken/beef),
    so the zero-guard didn't over-correct into false BUYs."""
    out = _grocery(ROOT / "cycles" / "2026-06-27.yaml")
    chick = next((l for l in out.splitlines() if "Raw chicken breast" in l), "")
    assert "covered" in chick.lower(), f"chicken should stay covered, got: {chick.strip()}"
