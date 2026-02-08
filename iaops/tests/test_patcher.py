"""Tests for the Patcher class to ensure mkdir and write_file_if_missing actions work correctly."""

from pathlib import Path

from indestructibleautoops.patcher import Patcher


def test_patcher_mkdir_action_creates_directory(tmp_path: Path):
    """Test that Patcher correctly applies mkdir actions when allow_writes is True."""
    patcher = Patcher(tmp_path, allow_writes=True)

    plan = {
        "actions": [
            {"id": "create_src", "kind": "mkdir", "path": "src"},
        ]
    }

    result = patcher.apply(plan)

    assert result["ok"] is True
    assert result["allowWrites"] is True
    assert len(result["applied"]) == 1
    assert len(result["skipped"]) == 0
    assert result["applied"][0]["action"]["kind"] == "mkdir"
    assert result["applied"][0]["action"]["path"] == "src"

    # Verify the directory was actually created
    assert (tmp_path / "src").exists()
    assert (tmp_path / "src").is_dir()


def test_patcher_mkdir_action_skips_existing_directory(tmp_path: Path):
    """Test that Patcher skips mkdir actions when directory already exists."""
    # Create the directory first
    (tmp_path / "src").mkdir()

    patcher = Patcher(tmp_path, allow_writes=True)

    plan = {
        "actions": [
            {"id": "create_src", "kind": "mkdir", "path": "src"},
        ]
    }

    result = patcher.apply(plan)

    assert result["ok"] is True
    assert len(result["applied"]) == 0
    assert len(result["skipped"]) == 1
    assert result["skipped"][0]["action"]["kind"] == "mkdir"
    assert result["skipped"][0]["reason"] == "exists"


def test_patcher_mkdir_action_respects_allow_writes_false(tmp_path: Path):
    """Test that Patcher doesn't create directories when allow_writes is False."""
    patcher = Patcher(tmp_path, allow_writes=False)

    plan = {
        "actions": [
            {"id": "create_src", "kind": "mkdir", "path": "src"},
        ]
    }

    result = patcher.apply(plan)

    assert result["ok"] is True
    assert result["allowWrites"] is False
    assert len(result["applied"]) == 0
    assert len(result["skipped"]) == 1
    assert result["skipped"][0]["action"]["kind"] == "mkdir"
    assert result["skipped"][0]["reason"] == "writes_disabled"

    # Verify the directory was NOT created
    assert not (tmp_path / "src").exists()


def test_patcher_write_file_if_missing_action_creates_file(tmp_path: Path):
    """Test that Patcher correctly applies write_file_if_missing actions."""
    patcher = Patcher(tmp_path, allow_writes=True)

    plan = {
        "actions": [
            {"id": "add_readme", "kind": "write_file_if_missing", "path": "README.md"},
        ]
    }

    result = patcher.apply(plan)

    assert result["ok"] is True
    assert len(result["applied"]) == 1
    assert len(result["skipped"]) == 0

    # Verify the file was created
    readme_path = tmp_path / "README.md"
    assert readme_path.exists()
    assert readme_path.is_file()
    assert "generated placeholder: README.md" in readme_path.read_text()


def test_patcher_unsupported_action_is_skipped(tmp_path: Path):
    """Test that Patcher skips unsupported action kinds."""
    patcher = Patcher(tmp_path, allow_writes=True)

    plan = {
        "actions": [
            {"id": "unknown", "kind": "unknown_action_type", "path": "something"},
        ]
    }

    result = patcher.apply(plan)

    assert result["ok"] is True
    assert len(result["applied"]) == 0
    assert len(result["skipped"]) == 1
    assert result["skipped"][0]["action"]["kind"] == "unknown_action_type"
    assert result["skipped"][0]["reason"] == "unsupported"


def test_patcher_mixed_actions_applied_correctly(tmp_path: Path):
    """Test that Patcher correctly handles a plan with mixed action types."""
    patcher = Patcher(tmp_path, allow_writes=True)

    plan = {
        "actions": [
            {"id": "add_src", "kind": "mkdir", "path": "src"},
            {"id": "add_readme", "kind": "write_file_if_missing", "path": "README.md"},
            {"id": "add_docs", "kind": "mkdir", "path": "docs"},
        ]
    }

    result = patcher.apply(plan)

    assert result["ok"] is True
    assert len(result["applied"]) == 3
    assert len(result["skipped"]) == 0

    # Verify all actions were applied
    assert (tmp_path / "src").is_dir()
    assert (tmp_path / "docs").is_dir()
    assert (tmp_path / "README.md").is_file()


def test_python_adapter_mkdir_action_integration(tmp_path: Path):
    """Integration test: Verify PythonAdapter's mkdir action works with Patcher.

    This test verifies that the issue from PR #37 is fixed:
    PythonAdapter.repair_plan() emits a mkdir action, and Patcher.apply()
    now correctly supports it (added in commit 49949af).
    """
    from indestructibleautoops.adapters.generic import AdapterContext
    from indestructibleautoops.adapters.python import PythonAdapter

    # Create a minimal Python project without src directory
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'\n", encoding="utf-8")

    # Create adapter context and adapter
    state_dir = tmp_path / ".state"
    state_dir.mkdir()
    ctx = AdapterContext(project_root=tmp_path, state_dir=state_dir)
    adapter = PythonAdapter(ctx)

    # Get the repair plan from the adapter
    index = adapter.index()
    repair_plan = adapter.repair_plan(index)

    # Verify the adapter emits a mkdir action for missing src directory
    assert len(repair_plan) == 1
    assert repair_plan[0]["kind"] == "mkdir"
    assert repair_plan[0]["path"] == "src"

    # Apply the plan with Patcher
    patcher = Patcher(tmp_path, allow_writes=True)
    plan = {"actions": repair_plan}
    result = patcher.apply(plan)

    # Verify the mkdir action was successfully applied
    assert result["ok"] is True
    assert len(result["applied"]) == 1
    assert len(result["skipped"]) == 0
    assert result["applied"][0]["action"]["kind"] == "mkdir"

    # Verify the src directory was created
    assert (tmp_path / "src").exists()
    assert (tmp_path / "src").is_dir()
