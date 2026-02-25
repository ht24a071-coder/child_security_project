"""Tests for rls.core.rpy_writer — .rpy file generation with RLS header."""

from pathlib import Path

import pytest

from rls.core.file_manager import RLSFileManager, WriteProtectionError
from rls.core.rpy_writer import RLS_HEADER, RpyWriter


@pytest.fixture
def writer(tmp_path: Path) -> RpyWriter:
    fm = RLSFileManager(tmp_path)
    fm.setup_project_dir()
    return RpyWriter(fm)


@pytest.fixture
def rls_dir(tmp_path: Path) -> Path:
    d = tmp_path / "rls"
    d.mkdir()
    return d


class TestWriteRpy:
    def test_creates_file_with_header(
        self, writer: RpyWriter, rls_dir: Path
    ) -> None:
        target = rls_dir / "test_screen.rpy"
        writer.write_rpy(target, 'screen test_screen():\n    text "Hello"')
        content = target.read_text(encoding="utf-8")
        assert content.startswith(RLS_HEADER)

    def test_body_present_after_header(
        self, writer: RpyWriter, rls_dir: Path
    ) -> None:
        target = rls_dir / "test_screen.rpy"
        body = 'screen test_screen():\n    text "Hello"'
        writer.write_rpy(target, body)
        content = target.read_text(encoding="utf-8")
        assert body in content

    def test_hooks_comment_present(
        self, writer: RpyWriter, rls_dir: Path
    ) -> None:
        target = rls_dir / "test_screen.rpy"
        writer.write_rpy(target, "screen x():\n    pass")
        content = target.read_text(encoding="utf-8")
        assert "rls_hooks.rpy" in content

    def test_rejects_user_file(
        self, writer: RpyWriter, tmp_path: Path
    ) -> None:
        with pytest.raises(WriteProtectionError):
            writer.write_rpy(
                tmp_path / "screens.rpy", "screen s():\n    pass"
            )

    def test_empty_body(self, writer: RpyWriter, rls_dir: Path) -> None:
        target = rls_dir / "empty.rpy"
        writer.write_rpy(target, "")
        content = target.read_text(encoding="utf-8")
        assert content.startswith(RLS_HEADER)


class TestHasRlsHeader:
    def test_file_with_header(
        self, writer: RpyWriter, rls_dir: Path
    ) -> None:
        target = rls_dir / "managed.rpy"
        writer.write_rpy(target, "screen x():\n    pass")
        assert writer.has_rls_header(target)

    def test_file_without_header(self, writer: RpyWriter, tmp_path: Path) -> None:
        target = tmp_path / "user.rpy"
        target.write_text("screen custom():\n    pass", encoding="utf-8")
        assert not writer.has_rls_header(target)

    def test_nonexistent_file(self, writer: RpyWriter, tmp_path: Path) -> None:
        assert not writer.has_rls_header(tmp_path / "nope.rpy")
