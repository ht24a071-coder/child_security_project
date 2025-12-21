init -10 python:
    # これが「マスターリスト」になります
    # 他のファイルから safe_events.append(...) するのはこのリストです
    suspicious_events = [] 
    safe_events = []

# 定数定義
define PROB_SUSPICIOUS = 20 
define MAX_STEPS = 10 

# キャラクター定義
define i = Character("常に右にいる人", color="#c8ffc8")
define t = Character("伊東マンショ", color="#c8ffc8")

# 変数（セーブデータに含まれる）
default current_step = 0 
default has_encountered_suspicious = False 
default flag_know_110 = False 

# ★重複防止用の「山札（デッキ）」変数
default deck_suspicious = []
default deck_safe = []