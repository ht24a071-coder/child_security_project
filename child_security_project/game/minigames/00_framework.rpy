init -1 python:
    # =========================================================================
    # 共通基盤クラス
    # =========================================================================
    class BaseMinigame(object):
        def __init__(self, key="dismiss", title="ミニゲーム", text="スペースキーを押して開始！", **kwargs):
            self.key = key
            self.title = title
            self.text = text
            self.started = False  # まだ始まっていない状態
            self.result = None
            self.show_result = False
            self.finished = False
            self.last_st = -1
            self.start_timestamp = None # 開始時刻

# =============================================================================
# 共通：説明オーバーレイ（これを各ゲーム画面の中で使う）
# =============================================================================

# --- アニメーション定義 (ATL) ---

# 左からスライドイン
transform intro_slide_left:
    xoffset -500 alpha 0.0
    easein_back 0.6 xoffset 0 alpha 1.0

# 右からスライドイン（少し遅れて開始）
transform intro_slide_right:
    xoffset 500 alpha 0.0
    pause 0.2
    easein_back 0.6 xoffset 0 alpha 1.0

# 下からふわっと浮き上がる（さらに遅れて開始）
transform intro_fade_up:
    yoffset 50 alpha 0.0
    pause 0.5
    easeout 0.5 yoffset 0 alpha 1.0

# 背景の装飾図形が走るアニメーション
transform intro_bg_shape(delay, start_x, start_y):
    xoffset start_x yoffset start_y alpha 0.0 rotate -30
    pause delay
    parallel:
        easeout_quart 1.0 xoffset 0 yoffset 0
    parallel:
        linear 0.5 alpha 0.3

# ----------------------------------------

screen minigame_intro_overlay(game):
    modal True
    
    # 1. 背景（黒い幕）
    add Solid("#000000E6") 

    # 2. 背景の装飾（幾何学的な図形がインしてくる）
    # 画面の後ろに少し動きをつけることでリッチに見せます
    fixed:
        # 左の帯
        add Solid("#ffcc00", xsize=1500, ysize=1500):
            align (5.7, 0.2)
            at intro_bg_shape(0.2, -1000, 0)
        
        # 右の帯（色を変えて逆方向から）
        add Solid("#00ccff", xsize=1500, ysize=1500):
            align (-5.3, 0.8)
            at intro_bg_shape(0.6, 1000, 0)

        # 上の帯
        add Solid("#ff0000", xsize=1800, ysize=800):
            align (10.5, 1.2)
            at intro_bg_shape(0.0, 0, -1000)

        # 下の帯（色を変えて逆方向から）
        add Solid("#04ff00", xsize=1800, ysize=800):
            align (-12.3, 0.0)
            at intro_bg_shape(0.4, 0, 1000)

    # 3. メインコンテンツ
    vbox:
        align (0.5, 0.5)
        spacing 40
        
        # タイトル（左からイン）
        text game.title:
            size 70 xalign 0.5 color "#fff" outlines [(4, "#000", 0, 0)] bold True
            at intro_slide_left
        
        # 説明文（右からイン）
        text game.text:
            size 32 xalign 0.5 color "#ddd" text_align 0.5
            at intro_slide_right
        
        null height 40
        
        # スタートボタン（下からイン）
        textbutton "START":
            style "confirm_button"
            xalign 0.5
            action SetField(game, "started", True)
            at intro_fade_up

# ボタンのスタイル
style confirm_button:
    background Solid("#444")
    padding (40, 20)
    hover_background Solid("#666")

style confirm_button_text:
    color "#fff"
    size 40
