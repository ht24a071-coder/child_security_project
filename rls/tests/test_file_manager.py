"""Tests for rls.core.file_manager — directory and file I/O management."""

from pathlib import Path

import pytest

from rls.core.file_manager import RLSFileManager, WriteProtectionError


class TestSetupProjectDir:
    def test_creates_rls_dir(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        result = fm.setup_project_dir()
        assert result.is_dir()
        assert result.name == "rls"

    def test_idempotent(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        fm.setup_project_dir()
        fm.setup_project_dir()  # should not raise
        assert fm.rls_dir.is_dir()


class TestIsRlsManaged:
    def test_file_inside_rls(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        fm.setup_project_dir()
        target = fm.rls_dir / "screen_main.rpy"
        assert fm.is_rls_managed(target)

    def test_file_outside_rls(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        fm.setup_project_dir()
        target = tmp_path / "screens.rpy"
        assert not fm.is_rls_managed(target)

    def test_nested_file_inside_rls(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        fm.setup_project_dir()
        target = fm.rls_dir / "sub" / "nested.rpy"
        assert fm.is_rls_managed(target)


class TestAssertWritable:
    def test_allows_rls_file(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        fm.setup_project_dir()
        fm.assert_writable(fm.rls_dir / "test.rpy")  # should not raise

    def test_blocks_user_file(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        fm.setup_project_dir()
        with pytest.raises(WriteProtectionError):
            fm.assert_writable(tmp_path / "screens.rpy")


class TestSafeWrite:
    def test_writes_inside_rls(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        fm.setup_project_dir()
        target = fm.rls_dir / "output.rpy"
        fm.safe_write(target, "screen test:\n    pass")
        assert target.read_text(encoding="utf-8") == "screen test:\n    pass"

    def test_rejects_outside_rls(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        fm.setup_project_dir()
        with pytest.raises(WriteProtectionError):
            fm.safe_write(tmp_path / "script.rpy", "label start:\n    pass")


class TestListFiles:
    def test_list_user_rpy_files(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        fm.setup_project_dir()
        # Create user files
        (tmp_path / "screens.rpy").write_text("screen s:", encoding="utf-8")
        (tmp_path / "script.rpy").write_text("label l:", encoding="utf-8")
        # Create RLS-managed file
        (fm.rls_dir / "managed.rpy").write_text("screen m:", encoding="utf-8")

        user_files = fm.list_user_rpy_files()
        basenames = [f.name for f in user_files]
        assert "screens.rpy" in basenames
        assert "script.rpy" in basenames
        assert "managed.rpy" not in basenames

    def test_list_rls_rpy_files(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        fm.setup_project_dir()
        (fm.rls_dir / "managed.rpy").write_text("screen m:", encoding="utf-8")
        rls_files = fm.list_rls_rpy_files()
        assert len(rls_files) == 1
        assert rls_files[0].name == "managed.rpy"

    def test_list_rls_rpy_files_empty_dir(self, tmp_path: Path) -> None:
        fm = RLSFileManager(tmp_path)
        # rls dir not created yet
        assert fm.list_rls_rpy_files() == []
