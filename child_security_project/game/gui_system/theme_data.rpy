init python:

    # -------------------------------------------------------------------------
    # 1. Color Palette (Raw Colors)
    # -------------------------------------------------------------------------
    ui_palette = {
        # Core Colors
        "primary": "#4A90E2",       # Blue
        "secondary": "#50E3C2",     # Teal
        "accent": "#F5A623",        # Orange
        "danger": "#E74C3C",        # Red
        "success": "#2ECC71",       # Green
        "warning": "#F1C40F",       # Yellow
        
        # Neutrals
        "white": "#FFFFFF",
        "black": "#000000",
        "dark_bg": "#1A2530",       # Dark Blue-Grey
        "panel_bg": "#2C3E50",      # Lighter Blue-Grey
        "text_main": "#ECF0F1",     # Off-white
        "text_mute": "#95A5A6",     # Grey
        "gradient_start": "#667eea",
        "gradient_start": "#667eea",
        "gradient_end": "#764ba2",
        
        # Minigame Specific
        "mg_bg": "#222244",         # Deep Purple/Blue
        "mg_panel": "#333333",      # Dark Grey
        "mg_success": "#00ff00",
        "mg_warn": "#ff6600",
    }

    # -------------------------------------------------------------------------
    # 2. Semantic Theme (Component Styles)
    # -------------------------------------------------------------------------
    ui_theme = {
        
        # --- Typography ---
        "text_h1": {
            "size": 60,
            "color": ui_palette["text_main"],
            "outlines": [(2, "#00000088", 2, 2)],
            "bold": True
        },
        "text_h2": {
            "size": 40,
            "color": ui_palette["secondary"],
            "bold": True
        },
        "text_body": {
            "size": 26,
            "color": ui_palette["text_main"],
            "line_spacing": 4
        },
        "text_warning": {
            "size": 24,
            "color": ui_palette["warning"],
            "italic": True
        },

        # --- Buttons ---
        "btn_primary": {
            "idle_background": Frame(Solid(ui_palette["primary"]), 10, 10),
            "hover_background": Frame(Solid(ui_palette["secondary"]), 10, 10),
            "selected_background": Frame(Solid(ui_palette["accent"]), 10, 10),
            "padding": (40, 20),
            "text_style": "text_body", # ref to typography style
            # "hover_sound": "audio/hover.ogg", # Placeholder
            "transform": "pulse_on_hover"
        },
        "btn_danger": {
            "idle_background": Frame(Solid(ui_palette["danger"]), 10, 10),
            "hover_background": Frame(Solid("#c0392b"), 10, 10),
            "padding": (40, 20),
            "text_style": "text_body",
            "transform": "click_shake"
        },
        "btn_ghost": {
            "idle_background": None,
            "hover_background": Frame(Solid("#FFFFFF22"), 10, 10),
            "padding": (20, 10),
            "text_style": "text_body"
        },
        "btn_rounded": {
            # Pure Shader Implementation!
            "idle_background": RoundedRect(300, 60, color=ui_palette["primary"], radius=20),
            "hover_background": RoundedRect(300, 60, color=ui_palette["secondary"], radius=20),
            "padding": (40, 15),
            "text_style": "text_body",
            "transform": "pulse_on_hover"
        },
        
        # --- Panels ---
        "panel_glass": {
            # Note: Blur is harder in Ren'Py < 8 without advanced setups, 
            # so we stick to semi-transparent rounded rect for now.
            "background": RoundedRect(800, 600, color=ui_palette["panel_bg"] + "CC", radius=30),
            "padding": (30, 30),
            "xalign": 0.5,
            "yalign": 0.5
        },
        "panel_gradient_mock": {
            # Mocking a gradient by using a solid color that represents the start color
            # Real gradients need images or shaders
            "background": Frame(Solid(ui_palette["gradient_start"]), 10, 10),
            "padding": (40, 40),
            "xalign": 0.5
        },
        "panel_card": {
            "background": Frame(Solid(ui_palette["dark_bg"]), 10, 10),
            "padding": (20, 20),
            "xfill": True
        },
        "panel_minigame": {
             # Rounded, dark blue/purple background for minigames
            "background": RoundedRect(700, 600, color=ui_palette["mg_bg"], radius=25),
            "padding": (60, 60),
            "xalign": 0.5,
            "yalign": 0.5
        },
        
        # --- Gauges ---
        "gauge_health": {
            "left_bar": Solid(ui_palette["danger"]),
            "right_bar": Solid(ui_palette["dark_bg"]),
            "thumb": None,
            "xsize": 300,
            "ysize": 30
        },
        "gauge_mic": {
             # A specific gauge for mic input
            "left_bar": Solid(ui_palette["mg_warn"]), # Default color, dynamic update logic is in screen
            "right_bar": Solid(ui_palette["mg_panel"]),
            "thumb": None,
            "xsize": 320,
            "ysize": 60
        }
    }

    # -------------------------------------------------------------------------
    # 3. Helper Functions
    # -------------------------------------------------------------------------
    def get_theme(key, property=None, default=None):
        """
        Safely retrieve theme data.
        If property is None, returns the whole dict for that key.
        """
        style_data = ui_theme.get(key, {})
        if property:
            return style_data.get(property, default)
        return style_data

    def resolve_style(key):
        """
        Returns the dictionary for a style key, or empty dict if not found.
        Used directly in screen properties.
        """
        return ui_theme.get(key, {})
