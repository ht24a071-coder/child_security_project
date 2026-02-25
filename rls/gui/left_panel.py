"""
RLS Left Panel — Component list and Layer tree (tabbed).

The component list provides draggable Ren'Py UI elements.
The layer tree shows the current screen hierarchy.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


# ---------------------------------------------------------------------------
# Component catalogue — items available for placement
# ---------------------------------------------------------------------------

COMPONENT_CATALOGUE = [
    ("text", "テキスト", "📝"),
    ("image", "イメージ", "🖼️"),
    ("button", "ボタン", "🔘"),
    ("textbutton", "テキストボタン", "🅰️"),
    ("imagebutton", "イメージボタン", "🖱️"),
    ("hbox", "HBox (横並び)", "⬜"),
    ("vbox", "VBox (縦並び)", "⬛"),
    ("frame", "フレーム", "🗔"),
    ("fixed", "Fixed (自由配置)", "📌"),
    ("viewport", "ビューポート", "🔲"),
    ("bar", "バー", "📊"),
    ("input", "テキスト入力", "⌨️"),
]


class LeftPanel(QWidget):
    """Left panel with Component list and Layer tree tabs (240px default)."""

    # Emitted when user selects a component type for placement
    component_selected = Signal(str)  # component type key

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(180)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._tabs = QTabWidget()
        self._tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Tab 1: Component list
        self._component_list = self._create_component_tab()
        self._tabs.addTab(self._component_list, "コンポーネント")

        # Tab 2: Layer tree
        self._layer_tree = self._create_layer_tree_tab()
        self._tabs.addTab(self._layer_tree, "レイヤー")

        layout.addWidget(self._tabs)

    # ── Component list ────────────────────────────────────────────────────

    def _create_component_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)

        hint = QLabel("ドラッグまたはダブルクリックで配置")
        hint.setStyleSheet("color: #999; font-size: 11px;")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        comp_list = QListWidget()
        comp_list.setStyleSheet(
            "QListWidget { background: #2d2d2d; border: none; }"
            "QListWidget::item { padding: 6px 8px; color: #ddd; }"
            "QListWidget::item:hover { background: #3d3d3d; }"
            "QListWidget::item:selected { background: #0078d4; }"
        )
        for key, label, icon_char in COMPONENT_CATALOGUE:
            item = QListWidgetItem(f"{icon_char}  {label}")
            item.setData(Qt.ItemDataRole.UserRole, key)
            comp_list.addItem(item)

        comp_list.itemDoubleClicked.connect(self._on_component_double_click)
        self._comp_list_widget = comp_list
        layout.addWidget(comp_list)

        return widget

    def _on_component_double_click(self, item: QListWidgetItem) -> None:
        key = item.data(Qt.ItemDataRole.UserRole)
        if key:
            self.component_selected.emit(key)

    # ── Layer tree ────────────────────────────────────────────────────────

    def _create_layer_tree_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        lbl = QLabel("レイヤー構造")
        lbl.setStyleSheet("font-weight: bold; color: #ccc;")
        toolbar.addWidget(lbl)
        toolbar.addStretch()

        btn_expand = QPushButton("⊞")
        btn_expand.setToolTip("すべて展開")
        btn_expand.setFixedSize(24, 24)
        btn_collapse = QPushButton("⊟")
        btn_collapse.setToolTip("すべて折りたたみ")
        btn_collapse.setFixedSize(24, 24)
        toolbar.addWidget(btn_expand)
        toolbar.addWidget(btn_collapse)
        layout.addLayout(toolbar)

        tree = QTreeWidget()
        tree.setHeaderLabels(["名前", "種類"])
        tree.setColumnWidth(0, 140)
        tree.setStyleSheet(
            "QTreeWidget { background: #2d2d2d; border: none; color: #ddd; }"
            "QTreeWidget::item:hover { background: #3d3d3d; }"
            "QTreeWidget::item:selected { background: #0078d4; }"
        )

        # Placeholder items to show the concept
        root = QTreeWidgetItem(tree, ["screen main_menu", "screen"])
        vbox = QTreeWidgetItem(root, ["navigation_vbox", "vbox"])
        QTreeWidgetItem(vbox, ["btn_start", "textbutton"])
        QTreeWidgetItem(vbox, ["btn_load", "textbutton"])
        QTreeWidgetItem(vbox, ["btn_settings", "textbutton"])
        QTreeWidgetItem(root, ["title_image", "image"])
        tree.expandAll()

        btn_expand.clicked.connect(tree.expandAll)
        btn_collapse.clicked.connect(tree.collapseAll)

        self._tree_widget = tree
        layout.addWidget(tree)

        return widget

    # ── Public API ────────────────────────────────────────────────────────

    @property
    def tree_widget(self) -> QTreeWidget:
        return self._tree_widget

    @property
    def component_list(self) -> QListWidget:
        return self._comp_list_widget
