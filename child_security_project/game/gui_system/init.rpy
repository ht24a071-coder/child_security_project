# Initialization order for the Semantic UI System
# ensuring it loads before screens and other scripts that might use it.

init -10 python:
    # Initialize global registries
    if not hasattr(store, "ui_theme"):
        store.ui_theme = {}
    
    if not hasattr(store, "ui_palette"):
        store.ui_palette = {}
