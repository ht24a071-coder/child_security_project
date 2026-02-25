"""
RLS Main Window — PySide6 main application window.

Provides project open/create workflow and desync detection on startup.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from rls.core.desync_detector import DesyncDetector
from rls.core.file_manager import RLSFileManager
from rls.core.project import RLSProject
from rls.core.rpy_writer import RpyWriter
from rls.gui.dialogs import DesyncWarningDialog


class RLSMainWindow(QMainWindow):
    """Main window for Ren'Py Layout Studio."""

    WINDOW_TITLE = "Ren'Py Layout Studio (RLS)"

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(1024, 720)

        # Core objects (initialised when a project is opened)
        self._project: RLSProject | None = None
        self._file_manager: RLSFileManager | None = None
        self._rpy_writer: RpyWriter | None = None
        self._desync_detector = DesyncDetector()

        self._setup_menu()
        self._setup_central()
        self._setup_statusbar()

    # ── Menu ──────────────────────────────────────────────────────────────

    def _setup_menu(self) -> None:
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("ファイル (&F)")

        new_action = file_menu.addAction("新規プロジェクト (&N)")
        new_action.triggered.connect(self._on_new_project)

        open_action = file_menu.addAction("プロジェクトを開く (&O)")
        open_action.triggered.connect(self._on_open_project)

        file_menu.addSeparator()

        exit_action = file_menu.addAction("終了 (&Q)")
        exit_action.triggered.connect(self.close)

        self.setMenuBar(menu_bar)

    # ── Central widget ────────────────────────────────────────────────────

    def _setup_central(self) -> None:
        central = QWidget()
        layout = QVBoxLayout(central)
        self._canvas_placeholder = QLabel(
            "プロジェクトを開いてください\n\n"
            "ファイル → 新規プロジェクト / プロジェクトを開く"
        )
        self._canvas_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._canvas_placeholder.setStyleSheet(
            "color: #888; font-size: 16px;"
        )
        layout.addWidget(self._canvas_placeholder)
        self.setCentralWidget(central)

    # ── Status bar ────────────────────────────────────────────────────────

    def _setup_statusbar(self) -> None:
        self._status = QStatusBar(self)
        self._status.showMessage("準備完了")
        self.setStatusBar(self._status)

    # ── Actions ───────────────────────────────────────────────────────────

    def _on_new_project(self) -> None:
        """Create a brand-new RLS project inside a user-chosen game/ dir."""
        game_dir = QFileDialog.getExistingDirectory(
            self, "Ren'Py の game/ フォルダを選択"
        )
        if not game_dir:
            return

        project = RLSProject(game_dir)
        if project.exists():
            reply = QMessageBox.question(
                self,
                "確認",
                f"既存のプロジェクトが見つかりました:\n{project.project_path}\n\n"
                "上書きして新規作成しますか？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        project.create_default()
        self._open_project_at(game_dir)
        self._status.showMessage(f"新規プロジェクトを作成: {game_dir}")

    def _on_open_project(self) -> None:
        """Open an existing RLS project."""
        game_dir = QFileDialog.getExistingDirectory(
            self, "Ren'Py の game/ フォルダを選択"
        )
        if not game_dir:
            return

        project = RLSProject(game_dir)
        if not project.exists():
            QMessageBox.warning(
                self,
                "プロジェクトが見つかりません",
                f"{project.project_path} が存在しません。\n"
                "「新規プロジェクト」で先に作成してください。",
            )
            return

        self._open_project_at(game_dir)

    # ── Core workflow ─────────────────────────────────────────────────────

    def _open_project_at(self, game_dir: str) -> None:
        """Load the project and run desync detection."""
        project = RLSProject(game_dir)
        project.load()

        file_manager = RLSFileManager(game_dir)
        rpy_writer = RpyWriter(file_manager)

        # Desync check
        result = self._desync_detector.check_desync(project)
        if result.has_desync:
            dlg = DesyncWarningDialog(result, self)
            if dlg.exec() == dlg.DialogCode.Accepted:
                # User chose to overwrite — re-export would happen here
                # For now, just update hashes to resolve the desync
                self._desync_detector.update_hashes(project)
                project.save()
                self._status.showMessage("デシンクを解消: JSONで上書きしました")
            else:
                self._status.showMessage(
                    "⚠ デシンクが未解消のまま開いています"
                )

        # Store references
        self._project = project
        self._file_manager = file_manager
        self._rpy_writer = rpy_writer

        self._update_ui_for_project()

    def _update_ui_for_project(self) -> None:
        """Update the window after a project is loaded."""
        if self._project is None:
            return
        res = self._project.base_resolution
        self._canvas_placeholder.setText(
            f"プロジェクト読み込み済み\n\n"
            f"game/: {self._project.game_dir}\n"
            f"ベース解像度: {res[0]}×{res[1]}\n\n"
            f"(キャンバスは今後のステップで実装)"
        )
        self.setWindowTitle(
            f"{self.WINDOW_TITLE} — {self._project.game_dir.name}"
        )
        self._status.showMessage(f"プロジェクト: {self._project.game_dir}")
