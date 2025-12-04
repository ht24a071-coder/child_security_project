# ==========================================
# ★重要：このファイルを他のファイルより先に読み込ませる設定
# ==========================================
init offset = -1

# ==========================================
# 1. 定数（define）
# ==========================================
define PROB_SUSPICIOUS = 50
define MAX_STEPS = 10 

# ==========================================
# 2. 変数・フラグ（default）
# ==========================================
default current_step = 0
default has_encountered_suspicious = False
default flag_know_110 = False

# ==========================================
# 3. イベントリスト（init python）
# ==========================================
init python:
    suspicious_events = [
        "event_bad_cookie",
        "event_bad_car",
    ]
    
    safe_events = [
        "event_safe_grandma",
        "event_safe_dog",
        "event_safe_shop",
    ]