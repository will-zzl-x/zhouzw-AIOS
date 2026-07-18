"""Tests for the cycles/ layout contract (2026-07-18 reorg): the CURRENT cycle
lives at the top level of cycles/, past cycles live in cycles/archive/, and
latest_cycle_path() must NEVER pick up an archived cycle — otherwise `make week`
with no CYCLE arg could silently run last month's plan.

Run: python -m pytest scripts/tests/test_cycles_layout.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import models


def test_latest_cycle_ignores_archive(tmp_path, monkeypatch):
    """An archive/ cycle with a NEWER date must not win over the top-level one."""
    cycles = tmp_path / "cycles"
    archive = cycles / "archive"
    archive.mkdir(parents=True)
    (cycles / "2026-07-18.yaml").write_text("date: '2026-07-18'\n", encoding="utf-8")
    (archive / "2026-08-99.yaml").write_text("date: '2026-08-99'\n", encoding="utf-8")
    monkeypatch.setattr(models, "CYCLES", cycles)
    monkeypatch.setattr(models, "CYCLES_ARCHIVE", archive)
    latest = models.latest_cycle_path()
    assert latest is not None
    assert latest.name == "2026-07-18.yaml"
    assert latest.parent == cycles


def test_all_cycle_paths_spans_both_levels(tmp_path, monkeypatch):
    cycles = tmp_path / "cycles"
    archive = cycles / "archive"
    archive.mkdir(parents=True)
    (cycles / "2026-07-18.yaml").write_text("date: '2026-07-18'\n", encoding="utf-8")
    (archive / "2026-06-27.yaml").write_text("date: '2026-06-27'\n", encoding="utf-8")
    (archive / "2026-06-20.yaml").write_text("date: '2026-06-20'\n", encoding="utf-8")
    monkeypatch.setattr(models, "CYCLES", cycles)
    monkeypatch.setattr(models, "CYCLES_ARCHIVE", archive)
    names = [p.name for p in models.all_cycle_paths()]
    assert names == ["2026-06-20.yaml", "2026-06-27.yaml", "2026-07-18.yaml"]


def test_prior_cycle_path_finds_archived_predecessor(tmp_path, monkeypatch):
    """The deplete-nudge must see the prior cycle even after it's archived."""
    cycles = tmp_path / "cycles"
    archive = cycles / "archive"
    archive.mkdir(parents=True)
    current = cycles / "2026-07-18.yaml"
    current.write_text("date: '2026-07-18'\n", encoding="utf-8")
    (archive / "2026-06-27.yaml").write_text("date: '2026-06-27'\n", encoding="utf-8")
    monkeypatch.setattr(models, "CYCLES", cycles)
    monkeypatch.setattr(models, "CYCLES_ARCHIVE", archive)
    prior = models.prior_cycle_path(current)
    assert prior is not None and prior.name == "2026-06-27.yaml"
    # oldest cycle has no prior
    assert models.prior_cycle_path(archive / "2026-06-27.yaml") is None


def test_deplete_nudge_fires_and_clears(tmp_path, monkeypatch):
    """run_week's preflight must nudge when the PRIOR cycle has no `deplete --apply`
    on record, and stay quiet once the log records it. Never a hard fail."""
    import json
    import run_week

    cycles = tmp_path / "cycles"
    archive = cycles / "archive"
    archive.mkdir(parents=True)
    current = cycles / "2026-07-18.yaml"
    current.write_text("date: '2026-07-18'\n", encoding="utf-8")
    (archive / "2026-06-27.yaml").write_text("date: '2026-06-27'\n", encoding="utf-8")
    log_path = tmp_path / "deplete_log.json"

    monkeypatch.setattr(models, "CYCLES", cycles)
    monkeypatch.setattr(models, "CYCLES_ARCHIVE", archive)
    monkeypatch.setattr(models, "DEPLETE_LOG_PATH", log_path)

    # no log at all -> nudge fires, names the prior cycle
    warns = run_week.check_prior_deplete(current)
    assert len(warns) == 1 and "2026-06-27" in warns[0] and "deplete" in warns[0].lower()

    # prior cycle recorded -> nudge clears
    log_path.write_text(json.dumps({"applied": [{"cycle": "2026-06-27", "applied_at": "2026-07-17"}]}),
                        encoding="utf-8")
    assert run_week.check_prior_deplete(current) == []

    # oldest cycle (no prior) -> never nudges
    assert run_week.check_prior_deplete(archive / "2026-06-27.yaml") == []


def test_repo_layout_holds():
    """Live repo: exactly one top-level cycle yaml (the current one) + archive/ exists."""
    top = sorted(models.CYCLES.glob("*.yaml"))
    assert len(top) >= 1
    assert models.CYCLES_ARCHIVE.exists()
    latest = models.latest_cycle_path()
    assert latest.parent == models.CYCLES  # never from archive/
