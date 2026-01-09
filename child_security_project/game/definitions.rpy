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

# スコア変数
default current_score = 0

# --- プレイヤー設定 ---
default player_name = "ナナシ"       # デフォルトの名前
default player_icon = "icon_dog"     # デフォルトのアイコン識別子

# 主人公のキャラ定義
# image="player" を指定することで、サイドイメージ（顔アイコン）が連動します
define pc = Character("[player_name]", image="player")

# アイコン画像を動的に切り替える定義
# ユーザーが選んだ player_icon の値（"icon_dog"など）に合わせて画像が変わります
image side player = "images/icons/[player_icon].png"