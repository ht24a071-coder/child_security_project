default persistent.ranking_list = []

init -10 python:
    # これが「マスターリスト」になります
    # 他のファイルから safe_events.append(...) するのはこのリストです
    suspicious_events = [] 
    safe_events = []
    special_events = []

    # ---------------------------------------------------------
    # 二つ名用単語リスト（小学生向け・ルビ修正版）
    # ---------------------------------------------------------
    
    # パート1：形容詞・枕詞
    list_part1 = [
        "{rb}伝説{/rb}{rt}でんせつ{/rt}の",
        "{rb}謎{/rb}{rt}なぞ{/rt}の",
        "ピカピカの",
        "{rb}無敵{/rb}{rt}むてき{/rt}の",
        "はらぺこの",

        # ★修正: 「点」と「満点」を合体させました
        "100{rb}点満点{/rb}{rt}てんまんてん{/rt}の",
        "みんなの",
        "ものすごい",
        "{rb}秘密{/rb}{rt}ひみつ{/rt}の",
        "{rb}元気{/rb}{rt}げんき{/rt}な",

        "やる{rb}気{/rb}{rt}き{/rt}マンマンの",
        # ★修正: 「昨日」と「見」を合体させました（きのうみた）
        "{rb}昨日見{/rb}{rt}きのうみ{/rt}た",
        "{rb}正義{/rb}{rt}せいぎ{/rt}の",
        "{rb}勇気{/rb}{rt}ゆうき{/rt}ある",
        "{rb}未来{/rb}{rt}みらい{/rt}から{rb}来{/rb}{rt}き{/rt}た",

        "{rb}世界一{/rb}{rt}せかいいち{/rt}の",
        "フワフワの",
        "{rb}眠{/rb}{rt}ねむ{/rt}そうな",
        "とってもあまい",
        "お{rb}母{/rb}{rt}かあ{/rt}さんの"
    ]

    # パート2：属性・状態
    list_part2 = [
        "キラキラの",
        "{rb}透明{/rb}{rt}とうめい{/rt}な",
        "ニコニコの",
        "あったかい",
        "プニプニの",

        "{rb}空{/rb}{rt}そら{/rt}を{rb}飛{/rb}{rt}と{/rt}ぶ",
        "キンキラキンの",
        "かっこいい",
        "モチモチの",
        "{rb}元気{/rb}{rt}げんき{/rt}いっぱいの",

        "おしゃれな",
        "{rb}巨大{/rb}{rt}きょだい{/rt}な",
        "サラサラの",
        "しゃべる",
        # ★修正: 「想像」と「上」を合体
        "{rb}想像上{/rb}{rt}そうぞうじょう{/rt}の",

        "いい{rb}匂{/rb}{rt}にお{/rt}いの",
        "カチコチに{rb}凍{/rb}{rt}こお{/rt}った",
        "{rb}最強{/rb}{rt}さいきょう{/rt}の",
        "{rb}踊{/rb}{rt}おど{/rt}っている",
        "{rb}虹色{/rb}{rt}にじいろ{/rt}の"
    ]

    # パート3：名詞
    list_part3 = [
        "{rb}冒険{/rb}{rt}ぼうけん{/rt}",
        "{rb}給食{/rb}{rt}きゅうしょく{/rt}",
        "ロボット",
        # ★修正: 「校長」と「先生」を合体（こうちょうせんせい）
        "{rb}校長先生{/rb}{rt}こうちょうせんせい{/rt}",
        "バナナ",

        "{rb}勇者{/rb}{rt}ゆうしゃ{/rt}",
        "ロケット",
        "{rb}宝石{/rb}{rt}ほうせき{/rt}",
        "ライオン",
        "{rb}宇宙人{/rb}{rt}うちゅうじん{/rt}",

        # ★修正: 「魔法」と「使」を合体
        "{rb}魔法使{/rb}{rt}まほうつか{/rt}い",
        "ダンボール",
        "{rb}消{/rb}{rt}け{/rt}しゴム",
        "パフェ",
        "{rb}靴下{/rb}{rt}くつした{/rt}",

        "アイドル",
        "ランドセル",
        "プリン",
        "ハンバーグ",
        "ハムスター"
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


# セリフテーブル
# 挨拶をした場合
define OfficerGreeting = ["元気のいい返事！気をつけて帰ってね！","うん、帰り道気をつけてね。","学校ごくろうさん。気をつけてね。"]
define OfficerMissGreeting = ["ちゃんとあいさつはするようにね。注意して帰ってね。","あいさつはしないと良くないよ。気をつけて帰ってね。","あいさつすることは大事だよ。気をつけて帰りなさい。"]

define WomanGreeting = ["元気のいい返事ね～！気をつけて帰りなさいね～！","帰り道気をつけてね～","今日も学校おつかれさまね。気をつけてね。"]
define WomanMissGreeting = ["ちゃんとあいさつはしなさいよ。気をつけて帰りなさい。","あいさつもしないなんて、最近の子は...","あいさつをすることが、あなたを守るのに..次はあいさつするようにね。"]