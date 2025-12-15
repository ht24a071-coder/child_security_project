init -1 python:
    # -----------------------------------------------------------
    # 1. 既存のイベントリスト（名前はそのまま維持）
    # -----------------------------------------------------------
    # 共同作成者の方はこれまで通り、ここに追加していけばOKです
    suspicious_events = []  # 危険イベントリスト
    safe_events = []        # 安全イベントリスト

    # -----------------------------------------------------------
    # 2. マップデータの定義（新規追加）
    # -----------------------------------------------------------
    map_data = {
        # --- スタート地点 ---
        'school': {
            'name': '学校',
            'bg': 'bg_school',             # 画像ファイル名は適宜変更してください
            'next': ['main_road_1', 'shortcut_1'], 
            'danger_add': 0,               
            'is_school_route': True,       
        },

        # --- 正規ルート（安全・遠回り） ---
        'main_road_1': {
            'name': '大通り',
            'bg': 'bg_main_street',
            'next': ['koban', 'park'],
            'danger_add': 5,
            'is_school_route': True,
        },

        # --- 近道（危険） ---
        'shortcut_1': {
            'name': '裏道の入口',
            'bg': 'bg_alley_entrance',
            'next': ['alley_deep'],
            'danger_add': 20,
            'is_school_route': False, # 寄り道
        },
        'alley_deep': {
            'name': '暗い路地裏',
            'bg': 'bg_alley_deep',
            'next': ['park'], 
            'danger_add': 40, 
            'is_school_route': False,
        },

        # --- 合流地点 ---
        'park': {
            'name': '公園',
            'bg': 'bg_park',
            'next': ['house_110', 'home'],
            'danger_add': 10,
            'is_school_route': True,
        },

        # --- ギミック ---
        'house_110': {
            'name': 'こども110番の家',
            'bg': 'bg_house110',
            'next': ['home'],
            'danger_add': -30, 
            'is_school_route': True,
        },
        'koban': {
            'name': '交番',
            'bg': 'bg_koban',
            'next': ['home'],
            'danger_add': -50,
            'is_school_route': True,
        },

        # --- ゴール ---
        'home': {
            'name': '自宅',
            'bg': 'bg_home',
            'next': [], 
            'danger_add': 0,
            'is_school_route': True,
        }
    }

    # -----------------------------------------------------------
    # 3. システム用変数（新規追加）
    # -----------------------------------------------------------
    # 山札（デッキ）用リスト
    # ゲーム開始時に suspicious_events の中身をここにコピーして使います
    deck_suspicious = []
    deck_safe = []


# ===========================================================
# 定義・変数（元のコードを維持）
# ===========================================================

# 定数
define PROB_SUSPICIOUS = 20  # ※新システムではdanger_meterを使いますが、念のため残します
define MAX_STEPS = 10        # ※新システムでは使いませんが、エラー防止で残します

# キャラクター
define i = Character("常に右にいる人", color="#c8ffc8")
define t = Character("伊東マンショ", color="#c8ffc8")

# 変数（デフォルト値）
default current_step = 0                  # エラー防止のため維持
default has_encountered_suspicious = False # 危険イベント遭遇フラグ（維持）
default flag_know_110 = False             # 110番通報を知っているか（維持）

# --- 新システムで使う変数 ---
default current_location_id = 'school'    # 現在地ID
default current_bg_image = "bg_school"    # 背景管理用
default danger_meter = 0                  # 危険度メーター
default is_stalked = False                # 尾行フラグ