# 定数・設定（define）
# ※ゲーム中に中身が変わらないもの

# 不審者出現率
define PROB_SUSPICIOUS = 50

# ゴールまでの歩数
define MAX_STEPS = 10

# イベントリスト定義
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


# 変数・フラグ（default）
# ※ゲーム中に中身が変わるもの

# 現在の歩数
default current_step = 0

# フラグ：不審者に会ったか？
default has_encountered_suspicious = False

# フラグ：110番の家を知っているか？
default flag_know_110 = False