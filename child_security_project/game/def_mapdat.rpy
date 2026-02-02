# =============================================================================
# マップ関連データ管理
# =============================================================================

init -10 python:
    # =========================================================================
    # 1. 地点（ノード）の設定
    # =========================================================================
    # 注意：選択肢テキストにもルビタグを使用可能
    
    world_map = {
        "start_point": {
            "bg": "back_school",
            "links": {"{rb}外{/rb}{rt}そと{/rt}に{rb}出{/rb}{rt}で{/rt}る": "school_park"},
            "group": "safe",
            "chance": 0
        },
        "school_park": {
            "bg": "back_school_park",
            "links": {
                "{rb}左{/rb}{rt}ひだり{/rt}に{rb}曲{/rb}{rt}ま{/rt}がる": "street_1",
                "{rb}学校{/rb}{rt}がっこう{/rt}に{rb}行{/rb}{rt}い{/rt}く": "start_point"
            },
            "group": "safe",
            "chance": 0
        },
        "street_1": {
            "bg": "back_street_0",
            "links": {
                "{rb}左{/rb}{rt}ひだり{/rt}の{rb}道{/rb}{rt}みち{/rt}へ": "school_park",
                "{rb}真{/rb}{rt}ま{/rt}っ{rb}直{/rb}{rt}す{/rt}ぐ{rb}進{/rb}{rt}すす{/rt}む": "street_2",
            },
            "group": "safe",
            "chance": 30
        },
        "street_2": {
            "bg": "back_street_1",
            "links": {
                "{rb}左{/rb}{rt}ひだり{/rt}の{rb}路地{/rb}{rt}ろじ{/rt}へ": "dark_alley",
                "{rb}大通{/rb}{rt}おおどお{/rt}りへ": "main_road",
                "{rb}踏切{/rb}{rt}ふみきり{/rt}を{rb}渡{/rb}{rt}わた{/rt}る": "railway_point"
            },
            "group": "safe",
            "chance": 30
        },
        "dark_alley": {
            "bg": "back_tunnel",
            "links": {"{rb}奥{/rb}{rt}おく{/rt}へ{rb}進{/rb}{rt}すす{/rt}む": "home_front"},
            "group": "suspicious",
            "chance": 60
        },
        "main_road": {
            "bg": "back_town",
            "links": {"{rb}近道{/rb}{rt}ちかみち{/rt}に{rb}入{/rb}{rt}はい{/rt}る": "home_front"},
            "group": "safe",
            "chance": 20
        },
        "railway_point": {
            "bg": "back_railway",
            "links": {"{rb}家{/rb}{rt}いえ{/rt}へ{rb}向{/rb}{rt}む{/rt}かう": "home_front"},
            "group": "crossing",
            "chance": 100
        },
        "home_front": {
            "bg": "back_town",
            "links": {},
            "group": "none",
            "chance": 0
        }
    }

    # =========================================================================
    # 2. イベントグループの設定
    # =========================================================================
    event_pools = {
        "safe": [
            "safe_e_test_1",
            "safe_e_test_2",
            "encounter_e_safe_person",
            "daily_e_find_110house"
        ],
        "suspicious": [
            "suspi_e_test_1",
            "suspi_e_test_2",
            "encounter_e_stranger",
            "suspi_e_car"
        ],
        "special": [
            "special_e_find_110",
            "special_e_encounter_flow"
        ],
        "crossing": [
            "safe_e_railway"
        ],
        "none": []
    }
