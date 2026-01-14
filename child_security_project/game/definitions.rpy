init -10 python:
    # これが「マスターリスト」になります
    # 他のファイルから safe_events.append(...) するのはこのリストです
    suspicious_events = [] 
    safe_events = []
    # ---------------------------------------------------------
    # 二つ名用単語リスト（モジュール化）
    # ---------------------------------------------------------
    # パート1：形容詞・枕詞
    list_part1 = [
        "虚無の", "発光する", "時給800円の", "来世から来た", "訳ありの",
        "ギリギリの", "自称", "驚きの白さの", "誰にも言えない", "徒歩5分の",
        "意識低い", "昨日見た", "量産型の", "哀しみの", "限りなく透明に近い"
    ]
    # パート2：属性・状態
    list_part2 = [
        "ぬるぬるの", "半透明の", "激しく揺れる", "生暖かい", "常温の",
        "嘘みたいに軽い", "哲学的な", "毛深い", "食べられない", "爆発寸前の",
        "カビた", "無味無臭の", "ベタベタする", "中古の", "想像上の"
    ]
    # パート3：名詞（本体）
    list_part3 = [
        "室外機", "有給休暇", "排水溝", "換気扇", "三角コーナー",
        "承認欲求", "確定申告", "生ゴミ", "門松", "角質",
        "親知らず", "段ボール", "レシート", "電柱", "二酸化炭素"
    ]

    # ---------------------------------------------------------
    # アバターアイコンリスト
    # ---------------------------------------------------------
    avatar_list = [
        ("bear",      "images/icons/bear.png"),
        ("buffalo",   "images/icons/buffalo.png"),
        ("chick",     "images/icons/chick.png"),
        ("chicken",   "images/icons/chicken.png"),
        ("cow",       "images/icons/cow.png"),
        ("crocodile", "images/icons/crocodile.png"),
        ("dog",       "images/icons/dog.png"),
        ("duck",      "images/icons/duck.png"),
        ("elephant",  "images/icons/elephant.png"),
        ("frog",      "images/icons/frog.png"),
        ("giraffe",   "images/icons/giraffe.png"),
        ("goat",      "images/icons/goat.png"),
        ("gorilla",   "images/icons/gorilla.png"),
        ("hippo",     "images/icons/hippo.png"),
        ("horse",     "images/icons/horse.png"),
        ("monkey",    "images/icons/monkey.png"),
        ("moose",     "images/icons/moose.png"),
        ("narwhal",   "images/icons/narwhal.png"),
        ("owl",       "images/icons/owl.png"),
        ("panda",     "images/icons/panda.png"),
        ("parrot",    "images/icons/parrot.png"),
        ("penguin",   "images/icons/penguin.png"),
        ("pig",       "images/icons/pig.png"),
        ("rabbit",    "images/icons/rabbit.png"),
        ("rhino",     "images/icons/rhino.png"),
        ("sloth",     "images/icons/sloth.png"),
        ("snake",     "images/icons/snake.png"),
        ("walrus",    "images/icons/walrus.png"),
        ("whale",     "images/icons/whale.png"),
        ("zebra",     "images/icons/zebra.png"),
    ]

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
default player_icon = "bear"     # デフォルトのアイコン識別子

# 主人公のキャラ定義
# image="player" を指定することで、サイドイメージ（顔アイコン）が連動します
define pc = Character("[player_name]", image="player")

# アイコン画像を動的に切り替える定義
# ユーザーが選んだ player_icon の値（"icon_dog"など）に合わせて画像が変わります
image side player = "images/icons/[player_icon].png"