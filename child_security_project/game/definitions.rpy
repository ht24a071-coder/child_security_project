init -10 python:
    # これが「マスターリスト」になります
    # 他のファイルから safe_events.append(...) するのはこのリストです
    suspicious_events = [] 
    safe_events = []

# 定数定義
define PROB_SUSPICIOUS = 20 
define MAX_STEPS = 10 

# キャラクター定義
define officer = Character("常に右にいる人", color="#c8ffc8")
define t = Character("伊東マンショ", color="#c8ffc8")

# セリフテーブル
# 挨拶をした場合
define OfficerGreeting = ["元気のいい返事！気をつけて帰ってね！","うん、帰り道気をつけてね。","学校ごくろうさん。気をつけてね。"]

# 変数（セーブデータに含まれる）
default current_step = 0 
default has_encountered_suspicious = False 
default flag_know_110 = False 

# ★重複防止用の「山札（デッキ）」変数
default deck_suspicious = []
default deck_safe = []