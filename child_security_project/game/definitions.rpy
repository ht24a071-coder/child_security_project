init -1 python:
    # イベントリスト
    suspicious_events = [] 
    safe_events = []        

    # 山札用リスト
    deck_suspicious = []
    deck_safe = []

    # マップデータ定義
    map_data = {
        # --- スタート地点 ---
        'school': {
            'name': '学校の前',
            'bg': 'bg_school',
            'next': {
                'straight': 'main_road',
                'right': 'shortcut_entrance'
            },
            'danger_add': 0,
            'is_school_route': True,
            'is_event_spot': False,       
            'distance_to_goal': 3,        
            'pos': (20, 20),
        },

        # --- 正規ルート（安全） ---
        'main_road': {
            'name': '大通り',
            'bg': 'bg_main_street',
            'next': {
                'straight': 'residential_area'
            },
            'danger_add': 5,
            'is_school_route': True,
            'is_event_spot': True,
            'distance_to_goal': 2,
            'pos': (100, 20),
        },
        'residential_area': {
            'name': '住宅街',
            'bg': 'bg_residential', 
            'next': {
                'straight': 'home'
            },
            'danger_add': 5,
            'is_school_route': True,
            'is_event_spot': True,
            'distance_to_goal': 1,
            'pos': (180, 20),
        },

        # --- 寄り道ルート（危険） ---
        'shortcut_entrance': {
            'name': '裏道の入口',
            'bg': 'bg_alley_entrance',
            'next': {
                'straight': 'alley_deep'
            },
            'danger_add': 20,
            'is_school_route': False,
            'is_event_spot': False,
            'distance_to_goal': 3,
            'pos': (20, 100),
        },
        'alley_deep': {
            'name': '暗い路地裏',
            'bg': 'bg_alley_deep',
            'next': {
                'straight': 'park'
            },
            'danger_add': 40, 
            'is_school_route': False,
            'is_event_spot': True,
            'distance_to_goal': 2,
            'pos': (100, 100),
        },
        'park': {
            'name': '公園',
            'bg': 'bg_park',
            'next': {
                'straight': 'home'
            },
            'danger_add': 10,
            'is_school_route': False,
            'is_event_spot': True,
            'distance_to_goal': 1,
            'pos': (180, 100),
        },

        # --- ゴール ---
        'home': {
            'name': '自宅',
            'bg': 'bg_home',
            'next': {}, 
            'danger_add': 0,
            'is_school_route': True,
            'is_event_spot': False,
            'distance_to_goal': 0,
            'pos': (260, 60),
        }
    }

# Pythonブロック外での定義
define PROB_SUSPICIOUS = 20
define MAX_STEPS = 10
define i = Character("常に右にいる人", color="#c8ffc8")
define t = Character("伊東マンショ", color="#c8ffc8")

default current_location_id = 'school'
default current_bg_image = "bg_school"
default current_minimap_image = "minimap_guide.png" 
default danger_meter = 0
default is_stalked = False
default knows_safe_house = False 
default heard_rumor_110 = False
default visited_locations = set()