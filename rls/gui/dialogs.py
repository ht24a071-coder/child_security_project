"""
RLS Dialogs — PySide6 dialog components.

Provides the desync warning dialog and other utility dialogs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget

    from rls.core.desync_detector import DesyncResult


class DesyncWarningDialog(QDialog):
    """Dialog shown when externally modified files are detected on startup.

    Displays a list of changed files and lets the user choose to overwrite
    them from the JSON data or cancel.
    """

    def __init__(
        self, desync_result: DesyncResult, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("RLS — 外部変更を検知しました")
        self.setMinimumWidth(480)
        self.setMinimumHeight(320)
        self._desync = desync_result
        self._setup_ui()

    # -- UI setup -----------------------------------------------------------

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Warning message
        warn_label = QLabel(
            "<b>rls/ フォルダ内のファイルが外部で変更されています。</b><br>"
            "「JSONで上書き」を押すと、RLS のプロジェクトデータで上書きします。<br>"
            "「キャンセル」を押すと、変更をそのまま残します（非推奨）。"
        )
        warn_label.setWordWrap(True)
        layout.addWidget(warn_label)

        # File list
        self._file_list = QListWidget()
        self._populate_file_list()
        layout.addWidget(self._file_list)

        # Buttons
        button_box = QDialogButtonBox()
        self._overwrite_btn = button_box.addButton(
            "JSONで上書き", QDialogButtonBox.ButtonRole.AcceptRole
        )
        self._cancel_btn = button_box.addButton(
            "キャンセル", QDialogButtonBox.ButtonRole.RejectRole
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _populate_file_list(self) -> None:
        for f in self._desync.modified_files:
            item = QListWidgetItem(f"🔄 変更: {f}")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self._file_list.addItem(item)
        for f in self._desync.missing_files:
            item = QListWidgetItem(f"❌ 削除: {f}")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self._file_list.addItem(item)
        for f in self._desync.new_files:
            item = QListWidgetItem(f"➕ 新規(未追跡): {f}")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self._file_list.addItem(item)
