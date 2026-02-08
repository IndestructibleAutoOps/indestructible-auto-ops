"""Tests for Patcher action handling."""

from pathlib import Path

from indestructibleautoops.patcher import Patcher


def test_patcher_write_file_if_missing(tmp_path: Path):
    """Test write_file_if_missing action creates files."""
    patcher = Patcher(tmp_path, allow_writes=True)
    plan = {
        "actions": [
            {"kind": "write_file_if_missing", "path": "test.txt"}
        ]
    }
    result = patcher.apply(plan)
    assert result["ok"] is True
    assert len(result["applied"]) == 1
    assert len(result["skipped"]) == 0
    assert (tmp_path / "test.txt").exists()


def test_patcher_write_file_if_missing_exists(tmp_path: Path):
    """Test write_file_if_missing skips existing files."""
    (tmp_path / "existing.txt").write_text("content", encoding="utf-8")
    patcher = Patcher(tmp_path, allow_writes=True)
    plan = {
        "actions": [
            {"kind": "write_file_if_missing", "path": "existing.txt"}
        ]
    }
    result = patcher.apply(plan)
    assert result["ok"] is True
    assert len(result["applied"]) == 0
    assert len(result["skipped"]) == 1
    assert result["skipped"][0]["reason"] == "exists"


def test_patcher_mkdir(tmp_path: Path):
    """Test mkdir action creates directories."""
    patcher = Patcher(tmp_path, allow_writes=True)
    plan = {
        "actions": [
            {"kind": "mkdir", "path": "src"}
        ]
    }
    result = patcher.apply(plan)
    assert result["ok"] is True
    assert len(result["applied"]) == 1
    assert len(result["skipped"]) == 0
    assert (tmp_path / "src").is_dir()


def test_patcher_mkdir_exists(tmp_path: Path):
    """Test mkdir skips existing directories."""
    (tmp_path / "existing_dir").mkdir()
    patcher = Patcher(tmp_path, allow_writes=True)
    plan = {
        "actions": [
            {"kind": "mkdir", "path": "existing_dir"}
        ]
    }
    result = patcher.apply(plan)
    assert result["ok"] is True
    assert len(result["applied"]) == 0
    assert len(result["skipped"]) == 1
    assert result["skipped"][0]["reason"] == "exists"


def test_patcher_unsupported_action(tmp_path: Path):
    """Test unsupported actions are skipped."""
    patcher = Patcher(tmp_path, allow_writes=True)
    plan = {
        "actions": [
            {"kind": "unknown_action", "path": "test"}
        ]
    }
    result = patcher.apply(plan)
    assert result["ok"] is True
    assert len(result["applied"]) == 0
    assert len(result["skipped"]) == 1
    assert result["skipped"][0]["reason"] == "unsupported"


def test_patcher_writes_disabled(tmp_path: Path):
    """Test actions are skipped when writes are disabled."""
    patcher = Patcher(tmp_path, allow_writes=False)
    plan = {
        "actions": [
            {"kind": "write_file_if_missing", "path": "test.txt"},
            {"kind": "mkdir", "path": "src"}
        ]
    }
    result = patcher.apply(plan)
    assert result["ok"] is True
    assert result["allowWrites"] is False
    assert len(result["applied"]) == 0
    assert len(result["skipped"]) == 2
    assert all(s["reason"] == "writes_disabled" for s in result["skipped"])


def test_patcher_mixed_actions(tmp_path: Path):
    """Test patcher handles multiple action kinds correctly."""
    patcher = Patcher(tmp_path, allow_writes=True)
    plan = {
        "actions": [
            {"kind": "mkdir", "path": "src"},
            {"kind": "write_file_if_missing", "path": "src/main.py"},
            {"kind": "mkdir", "path": "tests"},
            {"kind": "unknown_action", "path": "ignored"}
        ]
    }
    result = patcher.apply(plan)
    assert result["ok"] is True
    assert len(result["applied"]) == 3
    assert len(result["skipped"]) == 1
    assert (tmp_path / "src").is_dir()
    assert (tmp_path / "src" / "main.py").exists()
    assert (tmp_path / "tests").is_dir()
    assert result["skipped"][0]["reason"] == "unsupported"
