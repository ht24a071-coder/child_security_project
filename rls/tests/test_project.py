"""Tests for rls.core.project — RLSProject JSON management."""

import json
from pathlib import Path

import pytest

from rls.core.project import DEFAULT_PROJECT, PROJECT_FILENAME, RLS_DIR_NAME, RLSProject


class TestRLSProjectCreateDefault:
    """Tests for creating a new default project."""

    def test_create_default_creates_directory(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        project.create_default()
        assert (tmp_path / RLS_DIR_NAME).is_dir()

    def test_create_default_creates_json_file(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        project.create_default()
        assert project.project_path.exists()

    def test_create_default_contains_valid_json(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        project.create_default()
        data = json.loads(project.project_path.read_text(encoding="utf-8"))
        assert data["version"] == "1.0.0"
        assert data["base_resolution"] == [1280, 720]
        assert isinstance(data["screens"], dict)
        assert isinstance(data["components"], dict)
        assert isinstance(data["placeholders"], dict)
        assert isinstance(data["file_hashes"], dict)

    def test_create_default_schema_matches(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        project.create_default()
        data = json.loads(project.project_path.read_text(encoding="utf-8"))
        assert set(data.keys()) == set(DEFAULT_PROJECT.keys())


class TestRLSProjectLoadSave:
    """Tests for load / save round-trip."""

    def test_load_nonexistent_raises(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        with pytest.raises(FileNotFoundError):
            project.load()

    def test_save_then_load_roundtrip(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        project.create_default()
        # modify and save
        project._data["placeholders"]["player_name"] = "太郎"
        project.save()
        # load into a new instance
        project2 = RLSProject(tmp_path)
        project2.load()
        assert project2.placeholders["player_name"] == "太郎"

    def test_save_utf8(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        project.create_default()
        project._data["screens"]["メイン"] = {"type": "screen"}
        project.save()
        raw = project.project_path.read_text(encoding="utf-8")
        assert "メイン" in raw


class TestRLSProjectProperties:
    """Property accessors."""

    def test_base_resolution(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        project.create_default()
        assert project.base_resolution == (1280, 720)

    def test_file_hashes_initially_empty(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        project.create_default()
        assert project.file_hashes == {}

    def test_set_and_get_file_hash(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        project.create_default()
        project.set_file_hash("screen_main.rpy", "abc123")
        assert project.get_file_hash("screen_main.rpy") == "abc123"
        assert project.get_file_hash("nonexistent.rpy") is None

    def test_exists(self, tmp_path: Path) -> None:
        project = RLSProject(tmp_path)
        assert not project.exists()
        project.create_default()
        assert project.exists()
