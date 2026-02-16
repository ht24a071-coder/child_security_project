
import json

def verify_map_data():
    try:
        with open("c:/Users/hk624/github/child_security_project/child_security_project/game/mapdata.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        world_map = data.get("world_map", {})
        if not world_map:
            print("Error: world_map not found or empty")
            return

        missing_nodes = []
        for node_id, node_data in world_map.items():
            links = node_data.get("links", {})
            for link_text, dest_id in links.items():
                if dest_id not in world_map:
                    print(f"Broken link in '{node_id}': '{link_text}' -> '{dest_id}' (Node not found)")
                    missing_nodes.append(dest_id)
        
        if not missing_nodes:
            print("Map integrity check passed: All links point to existing nodes.")
        else:
            print(f"Found {len(missing_nodes)} broken links.")

    except Exception as e:
        print(f"Error reading mapdata.json: {e}")

if __name__ == "__main__":
    verify_map_data()
