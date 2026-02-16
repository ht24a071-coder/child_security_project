
import json
import os

MAP_FILE = "c:/Users/hk624/github/child_security_project/child_security_project/game/mapdata.json"

def fix_map_data():
    try:
        with open(MAP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        world_map = data.get("world_map", {})
        if not world_map:
            print("Error: world_map not found or empty")
            return

        missing_nodes = set()
        
        # Identify missing nodes
        for node_id, node_data in world_map.items():
            links = node_data.get("links", {})
            for link_text, dest_id in links.items():
                if dest_id not in world_map:
                    print(f"Found missing node ref: '{dest_id}' (from '{node_id}')")
                    missing_nodes.add(dest_id)
        
        if not missing_nodes:
            print("No missing nodes found.")
            return

        # Add placeholders
        print(f"Adding {len(missing_nodes)} placeholder nodes...")
        for node_id in missing_nodes:
            print(f"  + Adding '{node_id}'")
            world_map[node_id] = {
                "bg": "back_town", # Default safe background
                "links": {},       # No outside links initially
                "group": "safe",
                "chance": 0,
                "minimap": [0, 0]  # Default coordinates (hidden or top-left)
            }
        
        # Save back
        data["world_map"] = world_map
        with open(MAP_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("Successfully updated mapdata.json")

    except Exception as e:
        print(f"Error fixing mapdata.json: {e}")

if __name__ == "__main__":
    fix_map_data()
