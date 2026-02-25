"""
RLS Right Panel — Property editor with Basic / Style / Action tabs.

Provides input fields for editing the selected component's properties.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class RightPanel(QWidget):
    """Right panel with Basic / Style / Action property tabs (320px default)."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(250)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QLabel("プロパティ")
        header.setStyleSheet(
            "font-weight: bold; font-size: 13px; color: #ccc;"
            "padding: 6px 8px; background: #2a2a2a;"
        )
        layout.addWidget(header)

        self._tabs = QTabWidget()
        self._tabs.setTabPosition(QTabWidget.TabPosition.North)

        self._tabs.addTab(self._create_basic_tab(), "基本")
        self._tabs.addTab(self._create_style_tab(), "スタイル")
        self._tabs.addTab(self._create_action_tab(), "アクション")

        layout.addWidget(self._tabs)

    # ── Basic tab ─────────────────────────────────────────────────────────

    def _create_basic_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        form = QFormLayout(content)
        form.setContentsMargins(8, 8, 8, 8)
        form.setSpacing(6)

        # Component name / ID
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("component_id")
        form.addRow("名前:", self._name_edit)

        # Position
        pos_group = QGroupBox("位置")
        pos_layout = QFormLayout(pos_group)

        self._x_spin = QSpinBox()
        self._x_spin.setRange(-9999, 9999)
        self._x_spin.setSuffix(" px")
        pos_layout.addRow("X:", self._x_spin)

        self._y_spin = QSpinBox()
        self._y_spin.setRange(-9999, 9999)
        self._y_spin.setSuffix(" px")
        pos_layout.addRow("Y:", self._y_spin)

        form.addRow(pos_group)

        # Size
        size_group = QGroupBox("サイズ")
        size_layout = QFormLayout(size_group)

        self._w_spin = QSpinBox()
        self._w_spin.setRange(0, 9999)
        self._w_spin.setSuffix(" px")
        size_layout.addRow("幅:", self._w_spin)

        self._h_spin = QSpinBox()
        self._h_spin.setRange(0, 9999)
        self._h_spin.setSuffix(" px")
        size_layout.addRow("高さ:", self._h_spin)

        form.addRow(size_group)

        # Anchor / Align
        anchor_group = QGroupBox("アンカー / アライン")
        anchor_layout = QFormLayout(anchor_group)

        self._xalign_combo = QComboBox()
        self._xalign_combo.addItems([
            "なし", "0.0 (左)", "0.5 (中央)", "1.0 (右)", "カスタム"
        ])
        anchor_layout.addRow("xalign:", self._xalign_combo)

        self._yalign_combo = QComboBox()
        self._yalign_combo.addItems([
            "なし", "0.0 (上)", "0.5 (中央)", "1.0 (下)", "カスタム"
        ])
        anchor_layout.addRow("yalign:", self._yalign_combo)

        self._xanchor_spin = QDoubleSpinBox()
        self._xanchor_spin.setRange(0.0, 1.0)
        self._xanchor_spin.setSingleStep(0.1)
        anchor_layout.addRow("xanchor:", self._xanchor_spin)

        self._yanchor_spin = QDoubleSpinBox()
        self._yanchor_spin.setRange(0.0, 1.0)
        self._yanchor_spin.setSingleStep(0.1)
        anchor_layout.addRow("yanchor:", self._yanchor_spin)

        form.addRow(anchor_group)

        # Text content (for text / textbutton)
        self._text_edit = QLineEdit()
        self._text_edit.setPlaceholderText("テキスト内容")
        form.addRow("テキスト:", self._text_edit)

        scroll.setWidget(content)
        return scroll

    # ── Style tab ─────────────────────────────────────────────────────────

    def _create_style_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        form = QFormLayout(content)
        form.setContentsMargins(8, 8, 8, 8)
        form.setSpacing(6)

        # Text colour
        color_row = QHBoxLayout()
        self._color_edit = QLineEdit("#ffffff")
        self._color_edit.setMaximumWidth(100)
        self._color_btn = QPushButton("選択…")
        self._color_btn.setFixedWidth(60)
        color_row.addWidget(self._color_edit)
        color_row.addWidget(self._color_btn)
        form.addRow("文字色:", color_row)

        # Background colour
        bg_row = QHBoxLayout()
        self._bg_color_edit = QLineEdit("transparent")
        self._bg_color_edit.setMaximumWidth(100)
        self._bg_color_btn = QPushButton("選択…")
        self._bg_color_btn.setFixedWidth(60)
        bg_row.addWidget(self._bg_color_edit)
        bg_row.addWidget(self._bg_color_btn)
        form.addRow("背景色:", bg_row)

        # Font size
        self._font_size_spin = QSpinBox()
        self._font_size_spin.setRange(8, 200)
        self._font_size_spin.setValue(24)
        self._font_size_spin.setSuffix(" px")
        form.addRow("フォントサイズ:", self._font_size_spin)

        # Opacity
        self._opacity_spin = QDoubleSpinBox()
        self._opacity_spin.setRange(0.0, 1.0)
        self._opacity_spin.setSingleStep(0.05)
        self._opacity_spin.setValue(1.0)
        form.addRow("不透明度:", self._opacity_spin)

        # Bold / Italic
        self._bold_check = QCheckBox("太字 (Bold)")
        self._italic_check = QCheckBox("斜体 (Italic)")
        form.addRow(self._bold_check)
        form.addRow(self._italic_check)

        scroll.setWidget(content)
        return scroll

    # ── Action tab ────────────────────────────────────────────────────────

    def _create_action_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Preset actions
        preset_group = QGroupBox("プリセットアクション")
        preset_layout = QFormLayout(preset_group)

        self._action_combo = QComboBox()
        self._action_combo.addItems([
            "なし",
            "Start() — ゲーム開始",
            "ShowMenu('save') — セーブ画面",
            "ShowMenu('load') — ロード画面",
            "ShowMenu('preferences') — 設定画面",
            "Return() — 戻る",
            "Quit(confirm=True) — 終了",
            "NullAction() — 無効",
            "カスタム (rls_hooks.rpy)",
        ])
        preset_layout.addRow("クリック時:", self._action_combo)
        layout.addWidget(preset_group)

        # Custom action hint
        hooks_group = QGroupBox("カスタムアクション")
        hooks_layout = QVBoxLayout(hooks_group)

        hooks_hint = QLabel(
            "プリセット外のアクションが必要な場合は、\n"
            "rls_hooks.rpy にコードを記述し、\n"
            "ここでフック名を指定してください。"
        )
        hooks_hint.setStyleSheet("color: #aaa; font-size: 11px;")
        hooks_hint.setWordWrap(True)
        hooks_layout.addWidget(hooks_hint)

        self._hook_name_edit = QLineEdit()
        self._hook_name_edit.setPlaceholderText("例: my_custom_action")
        hooks_layout.addWidget(QLabel("フック名:"))
        hooks_layout.addWidget(self._hook_name_edit)

        hooks_layout.addWidget(QLabel("引数 (JSON):"))
        self._hook_args_edit = QLineEdit()
        self._hook_args_edit.setPlaceholderText('例: {"screen": "inventory"}')
        hooks_layout.addWidget(self._hook_args_edit)

        layout.addWidget(hooks_group)
        layout.addStretch()

        scroll.setWidget(content)
        return scroll
