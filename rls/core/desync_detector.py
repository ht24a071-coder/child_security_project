"""
RLS Desync Detector — detects external modifications to RLS-managed files.

Compares SHA-256 hashes stored in rls_project.json against the current
state of files on disk.  If a mismatch is found the GUI can prompt the
user to confirm an overwrite.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rls.core.project import RLSProject


@dataclass
class DesyncResult:
    """Container for desync-check results."""

    modified_files: list[str] = field(default_factory=list)
    missing_files: list[str] = field(default_factory=list)
    new_files: list[str] = field(default_factory=list)

    @property
    def has_desync(self) -> bool:
        return bool(self.modified_files or self.missing_files or self.new_files)

    def summary(self) -> str:
        """Return a human-readable summary."""
        lines: list[str] = []
        if self.modified_files:
            lines.append("外部で変更されたファイル:")
            for f in self.modified_files:
                lines.append(f"  • {f}")
        if self.missing_files:
            lines.append("ディスクから削除されたファイル:")
            for f in self.missing_files:
                lines.append(f"  • {f}")
        if self.new_files:
            lines.append("JSONに記録されていない新規ファイル:")
            for f in self.new_files:
                lines.append(f"  • {f}")
        return "\n".join(lines) if lines else "デシンクなし — すべて同期済みです。"


class DesyncDetector:
    """Compares on-disk file hashes with those stored in the project JSON."""

    # -- hashing -----------------------------------------------------------

    @staticmethod
    def compute_hash(path: str | Path) -> str:
        """Return the SHA-256 hex-digest of the file at *path*."""
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    # -- desync check ------------------------------------------------------

    def check_desync(self, project: RLSProject) -> DesyncResult:
        """Compare stored hashes in *project* against actual files on disk.

        Returns a ``DesyncResult`` describing any mismatches.
        """
        result = DesyncResult()
        rls_dir = project.rls_dir
        stored_hashes = project.file_hashes

        # 1. Check every file that has a stored hash
        for rel_path, expected_hash in stored_hashes.items():
            abs_path = rls_dir / rel_path
            if not abs_path.exists():
                result.missing_files.append(rel_path)
                continue
            actual_hash = self.compute_hash(abs_path)
            if actual_hash != expected_hash:
                result.modified_files.append(rel_path)

        # 2. Check for new .rpy files on disk that are not tracked
        if rls_dir.exists():
            for rpy_file in rls_dir.glob("**/*.rpy"):
                rel = str(rpy_file.relative_to(rls_dir)).replace("\\", "/")
                if rel not in stored_hashes:
                    result.new_files.append(rel)

        return result

    # -- utility: update hashes after a write ------------------------------

    @staticmethod
    def update_hashes(project: RLSProject) -> None:
        """Recompute and store hashes for all .rpy files in rls/.

        Call this after generating / exporting files to bring the
        project JSON back in sync.
        """
        rls_dir = project.rls_dir
        if not rls_dir.exists():
            return
        new_hashes: dict[str, str] = {}
        for rpy_file in rls_dir.glob("**/*.rpy"):
            rel = str(rpy_file.relative_to(rls_dir)).replace("\\", "/")
            new_hashes[rel] = DesyncDetector.compute_hash(rpy_file)
        project._data["file_hashes"] = new_hashes

    def __repr__(self) -> str:
        return "DesyncDetector()"
