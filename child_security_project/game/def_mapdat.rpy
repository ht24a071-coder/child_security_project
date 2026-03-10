# =============================================================================
# マップ関連データ管理（JSON読み込み版）
# =============================================================================

init -10 python:
    import json

    def load_map_data():
        # gameフォルダ直下の mapdata.json を開く
        try:
            with renpy.file("mapdata.json") as f:
                data = json.load(f)
            return (
                data["world_map"],
                data["event_pools"],
                data.get("home_nodes", []),
                data.get("near_school_nodes", []),
                data.get("map_image", "images/gui/minimap_bg.png")
            )
        except Exception as e:
            # 読み込み失敗時のエラーハンドリング
            raise Exception("Failed to load mapdata.json: {}".format(e))

    # JSONからデータを取得
    world_map, event_pools, home_nodes, NEAR_SCHOOL_NODES, map_bg_image = load_map_data()

    # 例：特定地点のミニマップ座標を取得するヘルパー関数
    def get_minimap_pos(node_id):
        return world_map.get(node_id, {}).get("minimap", [0, 0])