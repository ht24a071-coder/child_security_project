"""
Ren'Py Layout Studio (RLS) — Application entry point.

Usage:
    python -m rls.main [game_dir]
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from rls.gui.main_window import RLSMainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Ren'Py Layout Studio")
    app.setApplicationVersion("0.1.0")

    window = RLSMainWindow()

    # If a game dir was passed on the command line, auto-open it
    if len(sys.argv) > 1:
        game_dir = sys.argv[1]
        window._open_project_at(game_dir)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
