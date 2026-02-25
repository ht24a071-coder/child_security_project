"""Tests for rls.core.desync_detector — external-edit detection."""

import hashlib
from pathlib import Path

import pytest

from rls.core.desync_detector import DesyncDetector, DesyncResult
from rls.core.project import RLSProject


@pytest.fixture
def project_with_file(tmp_path: Path) -> tuple[RLSProject, Path]:
    """Create a project and a single .rpy file inside rls/, hashes synced."""
    project = RLSProject(tmp_path)
    project.create_default()

    rpy = project.rls_dir / "screen_main.rpy"
    rpy.write_text("screen main():\n    pass", encoding="utf-8")

    # Store correct hash
    detector = DesyncDetector()
    h = detector.compute_hash(rpy)
    project.set_file_hash("screen_main.rpy", h)
    project.save()

    return project, rpy


class TestComputeHash:
    def test_deterministic(self, tmp_path: Path) -> None:
        f = tmp_path / "test.txt"
        f.write_text("hello", encoding="utf-8")
        detector = DesyncDetector()
        assert detector.compute_hash(f) == detector.compute_hash(f)

    def test_different_content_different_hash(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("aaa", encoding="utf-8")
        f2.write_text("bbb", encoding="utf-8")
        detector = DesyncDetector()
        assert detector.compute_hash(f1) != detector.compute_hash(f2)

    def test_matches_stdlib_sha256(self, tmp_path: Path) -> None:
        f = tmp_path / "test.txt"
        content = b"hello world"
        f.write_bytes(content)
        expected = hashlib.sha256(content).hexdigest()
        assert DesyncDetector.compute_hash(f) == expected


class TestCheckDesync:
    def test_no_desync(
        self, project_with_file: tuple[RLSProject, Path]
    ) -> None:
        project, _ = project_with_file
        detector = DesyncDetector()
        result = detector.check_desync(project)
        assert not result.has_desync

    def test_detects_modified_file(
        self, project_with_file: tuple[RLSProject, Path]
    ) -> None:
        project, rpy = project_with_file
        # externally modify the file
        rpy.write_text("screen main():\n    text 'hacked'", encoding="utf-8")
        detector = DesyncDetector()
        result = detector.check_desync(project)
        assert result.has_desync
        assert "screen_main.rpy" in result.modified_files

    def test_detects_missing_file(
        self, project_with_file: tuple[RLSProject, Path]
    ) -> None:
        project, rpy = project_with_file
        rpy.unlink()
        detector = DesyncDetector()
        result = detector.check_desync(project)
        assert result.has_desync
        assert "screen_main.rpy" in result.missing_files

    def test_detects_new_untracked_file(
        self, project_with_file: tuple[RLSProject, Path]
    ) -> None:
        project, _ = project_with_file
        new_file = project.rls_dir / "extra.rpy"
        new_file.write_text("screen extra():\n    pass", encoding="utf-8")
        detector = DesyncDetector()
        result = detector.check_desync(project)
        assert result.has_desync
        assert "extra.rpy" in result.new_files


class TestUpdateHashes:
    def test_update_brings_in_sync(
        self, project_with_file: tuple[RLSProject, Path]
    ) -> None:
        project, rpy = project_with_file
        rpy.write_text("screen main():\n    text 'updated'", encoding="utf-8")
        detector = DesyncDetector()
        # Should be desynced
        assert detector.check_desync(project).has_desync
        # Update hashes
        detector.update_hashes(project)
        # Should now be in sync
        assert not detector.check_desync(project).has_desync


class TestDesyncResult:
    def test_summary_no_desync(self) -> None:
        result = DesyncResult()
        assert "同期済み" in result.summary()

    def test_summary_with_modified(self) -> None:
        result = DesyncResult(modified_files=["screen_a.rpy"])
        summary = result.summary()
        assert "変更" in summary
        assert "screen_a.rpy" in summary
