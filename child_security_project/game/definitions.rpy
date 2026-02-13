# 変数（セーブデータに含まれる）
default current_step = 0 
default has_encountered_suspicious = False 
default flag_know_110 = False 
default total_score = 0
default trust_point = 0
default current_score = 0

# プレイヤー設定
default player_name = "ナナシ"
default player_icon = "bear"

# 山札変数
default deck_suspicious = []
default deck_safe = []
 
# キャラクター定義
define officer = Character("おまわりさん", color="#c8ffc8")
define woman = Character("おねえさん", color="#c8ffc8")
define stranger = Character("???", color="#ff8888")  # 不審者用
define pc = Character("[player_name]", image="player")
define t = Character("伊東マンショ", color="#c8ffc8")

# 不審者のランダム画像用
default stranger_type = "stranger"

# 不審者の見た目ごとのボイスマッピング
define stranger_voice_map = {
    "stranger": {
        "001": "audio/stranger1_kaeri.wav",
        "002": "audio/stranger1_okuru.wav",
        "003": "audio/stranger1_hello.wav",
    },
    "stranger2": {
        "001": "audio/stranger2_kaeri.wav",
        "002": "audio/stranger2_okuru.wav",
        "003": "audio/stranger2_hello.wav",
    },
}

# 定数
define PROB_SUSPICIOUS = 20 
define MAX_STEPS = 10 

# 画像定義
image side player = "images/icons/[player_icon].png"
image side officer = "images/actor/officer.png"
image side woman = "images/actor/woman.png"
image side stranger = ConditionSwitch(
    "stranger_type == 'stranger2'", "images/actor/stranger2.png",
    "True", "images/actor/stranger.png"
)
image stranger = ConditionSwitch(
    "stranger_type == 'stranger2'", "images/actor/stranger2.png",
    "True", "images/actor/stranger.png"
)

# -----------------------------------------------------------
# スコア表示システム
# -----------------------------------------------------------

# -----------------------------------------------------------
# スコア表示システム
# -----------------------------------------------------------

# 1. 常時表示するスコアボード
screen score_hud():
    zorder 100
    style_prefix "score_hud"

    frame:
        xalign 0.02 yalign 0.02 # 画面の配置（左上）
        padding (20, 10)        # 枠の内側の余白
        background "#00000080"  # 半透明の黒背景

        # ★修正ポイント：
        # 文字と数字を「一行のテキスト」にまとめることで、
        # ズレずにきれいに真ん中に配置されます。
        text "スコア: [total_score]":
            color "#ffff00"  # 黄色
            size 32          # 文字サイズ
            bold True        # 太字
            xalign 0.5       # 左右の真ん中寄せ
            yalign 0.5       # 上下の真ん中寄せ

# 2. 点数変動時のポップアップ演出
screen score_popup(amount):
    zorder 101 # スコアボードよりさらに手前

    # プラスかマイナスかで色と記号を変える
    if amount >= 0:
        $ display_text = "+" + str(amount)
        $ text_color = "#00ff00" # 緑色
    else:
        $ display_text = str(amount) # マイナスは最初からついてる
        $ text_color = "#ff0000" # 赤色

    # ふわっと消えるアニメーションを適用
    text "[display_text]" at score_float_up:
        color text_color
        size 40
        outlines [(2, "#000000", 0, 0)] # 黒いフチドリで見やすく
        # ★修正済み：bold True
        bold True
        xalign 0.05 yalign 0.08 # スコアボードのちょっと下に表示

    # 1.5秒後に自動で消す
    timer 1.5 action Hide("score_popup")

# 3. アニメーションの動き定義（トランスフォーム）
transform score_float_up:
    alpha 0.0 yoffset 20 # 最初は透明でちょっと下
    easein 0.3 alpha 1.0 yoffset 0 # 0.3秒で現れる
    time 1.0 # 1秒間そのまま
    easeout 0.5 alpha 0.0 yoffset -30 # 0.5秒かけて上に浮きながら消える

# 4. 便利な関数（update_score）
init python:
    def update_score(amount):
        # グローバル変数のスコアを更新
        global total_score
        total_score += amount
        
        # ポップアップ演出を表示（引数で増減値を渡す）
        renpy.show_screen("score_popup", amount=amount)
        
        # 音を鳴らす（ファイルがない場合はコメントアウトしてください）
        # if amount > 0:
        #    renpy.play("audio/se_good.ogg", channel="sound")
        # elif amount < 0:
        #    renpy.play("audio/se_bad.ogg", channel="sound")

    def setup_stranger():
        """ランダムで不審者の見た目を選ぶ"""
        global stranger_type
        stranger_type = renpy.random.choice(["stranger", "stranger2"])

    def get_stranger_voice(line_id):
        """現在のstranger_typeに対応するボイスファイルパスを返す"""
        return stranger_voice_map.get(stranger_type, {}).get(line_id, None)