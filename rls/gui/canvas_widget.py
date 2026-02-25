"""
RLS Canvas Widget — zoomable, scrollable editing canvas.

Uses QGraphicsView / QGraphicsScene to provide a resolution-aware
workspace where components are placed visually.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QPainter,
    QPen,
    QPixmap,
    QWheelEvent,
)
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView


class CanvasWidget(QGraphicsView):
    """Zoomable, scrollable canvas with resolution boundary display."""

    # Emitted whenever the zoom level changes (as percentage, e.g. 100.0)
    zoom_changed = Signal(float)

    MIN_ZOOM = 0.25
    MAX_ZOOM = 4.0
    ZOOM_STEP = 1.15  # multiplicative step per wheel notch

    def __init__(
        self,
        width: int = 1280,
        height: int = 720,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._base_w = width
        self._base_h = height
        self._zoom = 1.0
        self._bg_pixmap_item = None

        # Scene setup — generous margin around the base resolution
        margin = 400
        scene = QGraphicsScene(
            -margin, -margin,
            width + margin * 2, height + margin * 2,
            self,
        )
        self.setScene(scene)

        # Rendering
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )

        # Background styling
        self.setBackgroundBrush(QBrush(QColor("#2b2b2b")))

        # Draw the resolution boundary rectangle
        self._draw_resolution_boundary()

        # Centre the view on the canvas
        self.centerOn(width / 2, height / 2)

    # ── Public API ────────────────────────────────────────────────────────

    def set_resolution(self, width: int, height: int) -> None:
        """Update the base resolution and redraw the boundary."""
        self._base_w = width
        self._base_h = height
        self.scene().clear()
        self._bg_pixmap_item = None
        self._draw_resolution_boundary()
        self.centerOn(width / 2, height / 2)

    def set_background(self, image_path: str | Path) -> None:
        """Set a background image for the canvas area."""
        pixmap = QPixmap(str(image_path))
        if pixmap.isNull():
            return
        pixmap = pixmap.scaled(
            self._base_w,
            self._base_h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        if self._bg_pixmap_item is not None:
            self.scene().removeItem(self._bg_pixmap_item)
        self._bg_pixmap_item = self.scene().addPixmap(pixmap)
        self._bg_pixmap_item.setZValue(-100)
        self._bg_pixmap_item.setPos(0, 0)

    def current_zoom_percent(self) -> float:
        return self._zoom * 100.0

    def set_zoom(self, factor: float) -> None:
        """Set absolute zoom level (1.0 = 100%)."""
        factor = max(self.MIN_ZOOM, min(self.MAX_ZOOM, factor))
        scale = factor / self._zoom
        self._zoom = factor
        self.scale(scale, scale)
        self.zoom_changed.emit(self.current_zoom_percent())

    # ── Events ────────────────────────────────────────────────────────────

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Ctrl+wheel to zoom, plain wheel to scroll."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                new_zoom = self._zoom * self.ZOOM_STEP
            else:
                new_zoom = self._zoom / self.ZOOM_STEP
            self.set_zoom(new_zoom)
            event.accept()
        else:
            super().wheelEvent(event)

    # ── Internal ──────────────────────────────────────────────────────────

    def _draw_resolution_boundary(self) -> None:
        """Draw a dashed rectangle showing the base resolution boundary."""
        pen = QPen(QColor("#5599ff"), 2, Qt.PenStyle.DashLine)
        self.scene().addRect(
            QRectF(0, 0, self._base_w, self._base_h), pen
        )
        # Fill canvas area with a slightly lighter colour
        fill_pen = QPen(Qt.PenStyle.NoPen)
        fill_brush = QBrush(QColor("#333333"))
        rect_item = self.scene().addRect(
            QRectF(0, 0, self._base_w, self._base_h),
            fill_pen, fill_brush,
        )
        rect_item.setZValue(-200)

        # Resolution label
        label = self.scene().addSimpleText(
            f"{self._base_w} × {self._base_h}"
        )
        label.setBrush(QBrush(QColor("#5599ff")))
        label.setPos(4, self._base_h + 4)
