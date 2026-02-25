"""
RLS Bottom Panel — Timeline placeholder (Phase 2).

Provides a reserved area for future timeline / animation editing.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class BottomPanel(QWidget):
    """Bottom panel — timeline placeholder (height ≈ 200px)."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(80)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header bar
        header = QLabel("タイムライン")
        header.setStyleSheet(
            "font-weight: bold; font-size: 12px; color: #ccc;"
            "padding: 4px 8px; background: #2a2a2a;"
            "border-top: 1px solid #444;"
        )
        layout.addWidget(header)

        # Placeholder content
        placeholder = QLabel(
            "🕒  タイムライン機能は Phase 2 で実装予定です"
        )
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet(
            "color: #666; font-size: 13px; background: #1e1e1e;"
        )
        layout.addWidget(placeholder, 1)
