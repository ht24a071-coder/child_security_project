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
            return data["world_map"], data["event_pools"]
        except Exception as e:
            # 読み込み失敗時のエラーハンドリング
            # 開発中はここにエラー内容を表示させると便利です
            raise Exception("Failed to load mapdata.json: {}".format(e))

    # JSONからデータを取得
    world_map, event_pools = load_map_data()

    # 例：特定地点のミニマップ座標を取得するヘルパー関数
    def get_minimap_pos(node_id):
        return world_map.get(node_id, {}).get("minimap", [0, 0])