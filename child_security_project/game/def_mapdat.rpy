# ここでマップ関連のデータを管理します
# JSON形式の記述になります

init -10 python:
    # 1. 地点（ノード）の設定
    # "地点ID": {"name": "表示名", "bg": "画像名", "links": {"方向名": "移動先ID"}, "group": "イベント群", "chance": 発生率}
    world_map = {
        "start_point": {
            "bg": "back_danger",
            "links": {"外に出る": "street_1"},
            "group": "safe",
            "chance": 0
        },
        "street_1": {
            "bg": "back_dark",
            "links": {"左の路地へ": "dark_alley", "大通りへ": "main_road", "踏切を渡る": "railway_point"},
            "group": "safe",
            "chance": 30
        },
        "dark_alley": {
            "bg": "back_tunnel",
            "links": {"奥へ進む": "home_front"},
            "group": "suspicious",
            "chance": 60
        },
        "main_road": {
            "bg": "back_town",
            "links": {"近道に入る": "home_front"},
            "group": "safe",
            "chance": 20
        },
        "railway_point": {
            "bg": "back_railway",          # ここに来た時点で背景が back_railway になります
            "links": {"家へ向かう": "home_front"}, # 渡った後の行き先
            "group": "crossing",           # 踏切専用のグループを指定
            "chance": 100                  # 100%の確率でイベント発生
        },
        "home_front": {
            "bg": "back_town",
            "links": {}, # 空にするとゴール判定用
            "group": "none",
            "chance": 0
        }
    }

    # 2. イベントグループの設定
    # 地点ごとに設定されたグループ名から、未実行のラベルが抽選されます
    event_pools = {
        "safe": ["safe_e_test_1", "safe_e_test_2"],
        "suspicious": ["suspi_e_test_1", "suspi_e_test_2"],
        "special": ["special_e_find_110", "special_e_encounter_flow"],
        "crossing": ["safe_e_railway"],
        "none": []
    }
