"""
RLS File Manager — directory and file I/O management.

Enforces the strict ownership rule:
  - rls/ folder files → RLS may create/overwrite
  - User files (screens.rpy, script.rpy, etc.) → read-only access
"""

from __future__ import annotations

from pathlib import Path

RLS_DIR_NAME = "rls"


class WriteProtectionError(Exception):
    """Raised when attempting to write to a user-managed file."""


class RLSFileManager:
    """Manages the rls/ directory inside a Ren'Py game/ folder."""

    def __init__(self, game_dir: str | Path) -> None:
        self.game_dir = Path(game_dir)
        self.rls_dir = self.game_dir / RLS_DIR_NAME

    # -- directory operations -----------------------------------------------

    def setup_project_dir(self) -> Path:
        """Create the ``game/rls/`` directory. Returns the rls_dir path."""
        self.rls_dir.mkdir(parents=True, exist_ok=True)
        return self.rls_dir

    def get_rls_dir(self) -> Path:
        """Return the path to the rls/ folder."""
        return self.rls_dir

    # -- ownership check ----------------------------------------------------

    def is_rls_managed(self, path: str | Path) -> bool:
        """Return True if *path* lives inside the ``rls/`` directory."""
        try:
            Path(path).resolve().relative_to(self.rls_dir.resolve())
            return True
        except ValueError:
            return False

    def assert_writable(self, path: str | Path) -> None:
        """Raise WriteProtectionError if *path* is outside rls/."""
        if not self.is_rls_managed(path):
            raise WriteProtectionError(
                f"RLS is not allowed to write to user-managed file: {path}\n"
                f"Only files inside {self.rls_dir} may be modified by RLS."
            )

    # -- user file listing ---------------------------------------------------

    def list_user_rpy_files(self) -> list[Path]:
        """List .rpy files in game/ that are *not* inside rls/.

        These are user-managed files; RLS must never write to them.
        """
        user_files: list[Path] = []
        for rpy in self.game_dir.glob("**/*.rpy"):
            if not self.is_rls_managed(rpy):
                user_files.append(rpy)
        return sorted(user_files)

    def list_rls_rpy_files(self) -> list[Path]:
        """List .rpy files inside the rls/ directory."""
        if not self.rls_dir.exists():
            return []
        return sorted(self.rls_dir.glob("**/*.rpy"))

    # -- safe write ----------------------------------------------------------

    def safe_write(self, path: str | Path, content: str) -> None:
        """Write *content* to *path* only if it is inside rls/.

        Raises WriteProtectionError otherwise.
        """
        path = Path(path)
        self.assert_writable(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    # -- safe read (for user files) -----------------------------------------

    @staticmethod
    def safe_read(path: str | Path) -> str:
        """Read and return text contents of any file (no write side-effects)."""
        return Path(path).read_text(encoding="utf-8")

    def __repr__(self) -> str:
        return f"RLSFileManager(game_dir={self.game_dir!r})"
