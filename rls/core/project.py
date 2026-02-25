"""
RLS Project — JSON-based project data management.

The rls_project.json file is the single source of truth for all
editor state. .rpy files are generated output only.
"""

from __future__ import annotations

import json
import copy
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Default Schema
# ---------------------------------------------------------------------------

DEFAULT_PROJECT: dict[str, Any] = {
    "version": "1.0.0",
    "base_resolution": [1280, 720],
    "screens": {},
    "components": {},
    "placeholders": {},
    "file_hashes": {},
}

PROJECT_FILENAME = "rls_project.json"
RLS_DIR_NAME = "rls"


class RLSProject:
    """Manages loading, saving, and accessing rls_project.json data."""

    def __init__(self, game_dir: str | Path) -> None:
        self.game_dir = Path(game_dir)
        self.rls_dir = self.game_dir / RLS_DIR_NAME
        self.project_path = self.rls_dir / PROJECT_FILENAME
        self._data: dict[str, Any] = {}

    # -- properties ---------------------------------------------------------

    @property
    def data(self) -> dict[str, Any]:
        """Return the current project data (read-only view)."""
        return self._data

    @property
    def base_resolution(self) -> tuple[int, int]:
        res = self._data.get("base_resolution", [1280, 720])
        return (int(res[0]), int(res[1]))

    @property
    def file_hashes(self) -> dict[str, str]:
        return self._data.setdefault("file_hashes", {})

    @property
    def screens(self) -> dict[str, Any]:
        return self._data.setdefault("screens", {})

    @property
    def components(self) -> dict[str, Any]:
        return self._data.setdefault("components", {})

    @property
    def placeholders(self) -> dict[str, Any]:
        return self._data.setdefault("placeholders", {})

    # -- I/O ----------------------------------------------------------------

    def create_default(self) -> None:
        """Initialise with the default schema and persist to disk."""
        self._data = copy.deepcopy(DEFAULT_PROJECT)
        self.save()

    def load(self) -> None:
        """Load project data from rls_project.json.

        Raises FileNotFoundError if the file does not exist.
        """
        if not self.project_path.exists():
            raise FileNotFoundError(
                f"Project file not found: {self.project_path}"
            )
        text = self.project_path.read_text(encoding="utf-8")
        self._data = json.loads(text)

    def save(self) -> None:
        """Persist current data to rls_project.json (creating dirs if needed)."""
        self.rls_dir.mkdir(parents=True, exist_ok=True)
        text = json.dumps(self._data, ensure_ascii=False, indent=2)
        self.project_path.write_text(text, encoding="utf-8")

    # -- hash bookkeeping ---------------------------------------------------

    def set_file_hash(self, relative_path: str, hash_value: str) -> None:
        """Record the SHA-256 hash for *relative_path* (relative to rls_dir)."""
        self.file_hashes[relative_path] = hash_value

    def get_file_hash(self, relative_path: str) -> str | None:
        """Return the stored hash for *relative_path*, or None."""
        return self.file_hashes.get(relative_path)

    # -- helpers ------------------------------------------------------------

    def exists(self) -> bool:
        """Return True if the project file exists on disk."""
        return self.project_path.exists()

    def __repr__(self) -> str:
        return f"RLSProject(game_dir={self.game_dir!r})"
