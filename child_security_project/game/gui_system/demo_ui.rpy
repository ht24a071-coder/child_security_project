# Demo Screen for Semantic UI System

screen semantic_demo():
    modal True
    
    # 1. Background Overlay
    add Solid("#1a1a2d") # Dark rich background
    
    # 2. Main Content Container
    vpgrid:
        cols 1
        spacing 30
        draggable True
        mousewheel True
        scrollbars "vertical"
        xalign 0.5
        yalign 0.5
        xsize 1000
        ysize 720
        
        # --- Header Section ---
        use ui_panel(style="panel_gradient_mock", xfill=True):
            vbox:
                spacing 10
                use ui_text("Semantic UI Showcase", style="text_h1")
                use ui_text("Rich components controlled by a central theme.", style="text_body")

        # --- Buttons Showcase ---
        use ui_panel(style="panel_card"):
            vbox:
                spacing 20
                use ui_text("Button Styles", style="text_h2")
                hbox:
                    spacing 20
                    use ui_button("Default Primary", action=Notify("Primary"), style="btn_primary")
                    use ui_button("Danger", action=Notify("Danger"), style="btn_danger")
                    use ui_button("Ghost Button", action=Notify("Ghost"), style="btn_ghost")
                
                use ui_text("Rounded Buttons (CSS-like Shader Rendering!)", style="text_body", color="#aaa", size=20)
                hbox:
                    spacing 20
                    use ui_button("Shader Primary", action=Notify("Rounded Shader"), style="btn_rounded")
        
        # --- Cards & Glassmorphism ---
        use ui_panel(style="panel_glass"):
            vbox:
                spacing 10
                use ui_text("Glassmorphism Panel", style="text_h2")
                use ui_text("This panel has a semi-transparent background.", style="text_body")
                null height 10
                use ui_gauge(85, 100, style="gauge_health")

        # --- Close ---
        use ui_button("Close Demo", action=Hide("semantic_demo"), style="btn_danger", xalign=0.5)

screen heading(t):
    text t color "#888" size 20 bold True
