"""
RLS Screen Tabs — tab bar for switching between screens.

Provides tabs like メインメニュー, HUD, セーブ・ロード and a "+" button
to add new screens.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QTabBar,
    QToolButton,
    QWidget,
)


class ScreenTabBar(QWidget):
    """Tab bar for switching between Ren'Py screens being edited."""

    # Emitted with the screen name when a tab is selected
    screen_changed = Signal(str)
    # Emitted with the new screen name when a tab is added
    screen_added = Signal(str)

    DEFAULT_SCREENS = ["メインメニュー", "HUD", "セーブ・ロード"]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._tab_bar = QTabBar()
        self._tab_bar.setExpanding(False)
        self._tab_bar.setMovable(True)
        self._tab_bar.setTabsClosable(False)
        self._tab_bar.setStyleSheet(
            "QTabBar { background: #252525; }"
            "QTabBar::tab {"
            "  background: #333; color: #bbb;"
            "  padding: 6px 16px;"
            "  margin-right: 1px;"
            "  border-top-left-radius: 4px;"
            "  border-top-right-radius: 4px;"
            "}"
            "QTabBar::tab:selected {"
            "  background: #444; color: #fff;"
            "  border-bottom: 2px solid #0078d4;"
            "}"
            "QTabBar::tab:hover { background: #3a3a3a; }"
        )

        for name in self.DEFAULT_SCREENS:
            self._tab_bar.addTab(name)

        self._tab_bar.currentChanged.connect(self._on_tab_changed)
        layout.addWidget(self._tab_bar)

        # "+" button to add new screens
        add_btn = QToolButton()
        add_btn.setText("+")
        add_btn.setToolTip("新しい画面を追加")
        add_btn.setStyleSheet(
            "QToolButton {"
            "  background: #333; color: #0078d4;"
            "  font-size: 16px; font-weight: bold;"
            "  padding: 4px 10px; border: none;"
            "  border-top-left-radius: 4px;"
            "  border-top-right-radius: 4px;"
            "}"
            "QToolButton:hover { background: #3a3a3a; }"
        )
        add_btn.clicked.connect(self._on_add_screen)
        layout.addWidget(add_btn)

        layout.addStretch()

        self.setStyleSheet("background: #252525;")

    # ── Handlers ──────────────────────────────────────────────────────────

    def _on_tab_changed(self, index: int) -> None:
        if index >= 0:
            name = self._tab_bar.tabText(index)
            self.screen_changed.emit(name)

    def _on_add_screen(self) -> None:
        name, ok = QInputDialog.getText(
            self, "新しい画面", "画面名を入力してください:"
        )
        if ok and name.strip():
            name = name.strip()
            self._tab_bar.addTab(name)
            self._tab_bar.setCurrentIndex(self._tab_bar.count() - 1)
            self.screen_added.emit(name)

    # ── Public API ────────────────────────────────────────────────────────

    def current_screen(self) -> str:
        idx = self._tab_bar.currentIndex()
        return self._tab_bar.tabText(idx) if idx >= 0 else ""

    def screen_names(self) -> list[str]:
        return [
            self._tab_bar.tabText(i) for i in range(self._tab_bar.count())
        ]
