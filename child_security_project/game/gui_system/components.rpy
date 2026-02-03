# -------------------------------------------------------------------------
# Semantic UI Components
# These screens wrap the raw Ren'Py displayables and apply themes automatically.
# -------------------------------------------------------------------------

# --- Semantic Text ---
screen ui_text(content, style="text_body", **kwargs):
    text content:
        # Merge theme properties and overrides
        properties dict(resolve_style(style), **kwargs)


# --- Semantic Button ---
screen ui_button(label, action=NullAction(), style="btn_primary", **kwargs):
    button:
        action action
        
        # Merge theme properties and overrides
        properties dict(resolve_style(style), **kwargs)
        
        # Apply Transform if defined in theme
        if get_theme(style, "transform"):
            at getattr(store, get_theme(style, "transform"))

        # Inner Text
        text label:
            # Look for "text_style" in the button theme, otherwise default to body
            properties resolve_style(get_theme(style, "text_style", "text_body"))
            align (0.5, 0.5)


# --- Semantic Panel (Container) ---
screen ui_panel(style="panel_glass", **kwargs):
    frame:
        properties dict(resolve_style(style), **kwargs)
        
        # Allow content to be inserted here
        transclude


# --- Semantic Gauge (Bar) ---
screen ui_gauge(value, max_value, style="gauge_health", **kwargs):
    # Wrapper frame (optional, for background/padding if needed, or just bar)
    
    bar value value range max_value:
        left_bar get_theme(style, "left_bar")
        right_bar get_theme(style, "right_bar")
        thumb get_theme(style, "thumb")
        
        xsize get_theme(style, "xsize", 300)
        ysize get_theme(style, "ysize", 30)
        
        properties kwargs
