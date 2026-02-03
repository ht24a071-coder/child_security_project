init python:

    def grid(col, row, cols=12, rows=12, w=1, h=1):
        """
        Calculates position properties for a grid-based layout.
        
        Args:
            col (int): Column index (0-based)
            row (int): Row index (0-based)
            cols (int): Total columns in the grid
            rows (int): Total rows in the grid
            w (int): Width span (in columns) - mostly for future use or custom sizing logic
            h (int): Height span (in rows)
            
        Returns:
            dict: Properties for xpos, ypos, xanchor, yanchor.
        """
        # Standard Grid, centered anchors by default for easy placement
        # This implies placing the center of the object at the specific grid intersection?
        # Or top-left? Let's assume standard intuitive grid where (0,0) is top-left cell.
        
        # Let's align to the center of the cell for now to make "grid(6,6)" meaningful as center.
        
        x = float(col) / cols
        y = float(row) / rows
        
        # Adjust to center of the cell? 
        # If we use strict points:
        # grid(0,0) = 0.0, 0.0. grid(12,12) = 1.0, 1.0.
        
        return {
            "xpos": x,
            "ypos": y,
            #"xanchor": 0.5, # Let the user decide anchor or default to center in component
            #"yanchor": 0.5
        }

    def grid_center():
        """Helper for absolute center"""
        return {"xalign": 0.5, "yalign": 0.5}
