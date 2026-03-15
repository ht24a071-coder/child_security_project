init -1 python:
    # =========================================================================
    # 共通基盤クラス
    # =========================================================================
    class BaseMinigame(object):
        def __init__(self, key="dismiss", title="ミニゲーム", text="スペースキーを押してかいし！", **kwargs):
            self.key = key
            self.title = title
            self.text = text
            self.started = False  # まだ始まっていない状態
            self.result = None
            self.show_result = False
            self.finished = False
            self.last_st = -1
            self.start_timestamp = None # かいしじ刻

# =============================================================================
# 共通：説明オーバーレイ（これを各ゲーム画面のなかで使う）
# =============================================================================

# --- アニメーション定義 (ATL) ---

# ひだりからスライドイン
transform intro_slide_left:
    xoffset -500 alpha 0.0
    easein_back 0.6 xoffset 0 alpha 1.0

# みぎからスライドイン（すこし遅れてかいし）
transform intro_slide_right:
    xoffset 500 alpha 0.0
    pause 0.2
    easein_back 0.6 xoffset 0 alpha 1.0

# したからふわっと浮きうえがる（さらに遅れてかいし）
transform intro_fade_up:
    yoffset 50 alpha 0.0
    pause 0.5
    easeout 0.5 yoffset 0 alpha 1.0

# 背景の装飾図かたちがはしるアニメーション
transform intro_bg_shape(delay, start_x, start_y):
    xoffset start_x yoffset start_y alpha 0.0 rotate -30
    pause delay
    parallel:
        easeout_quart 1.0 xoffset 0 yoffset 0
    parallel:
        linear 0.5 alpha 0.3

# ----------------------------------------

# =============================================================================
# ゲームなか 共通アニメーション (ATL)
# =============================================================================

# ゆっくりうえしたに浮遊する（背景図かたち用）
transform mg_bg_float(delay=0.0, amp=15):
    yoffset 0
    pause delay
    block:
        easeout 1.8 yoffset amp
        easeout 1.8 yoffset 0
        easeout 1.8 yoffset -amp
        easeout 1.8 yoffset 0
        repeat

# 拡大縮小を繰り返すパルス（同こころ円・ひかり彩用）
transform mg_bg_pulse(delay=0.0, lo=0.9, hi=1.1, period=1.6):
    zoom lo
    pause delay
    block:
        ease period/2 zoom hi
        ease period/2 zoom lo
        repeat

# 画面をゆっくりよこに流れる（帯・粒こ用）
transform mg_bg_drift(delay=0.0, dist=120, period=4.0):
    xoffset 0
    pause delay
    block:
        linear period/2 xoffset dist
        linear period/2 xoffset 0
        repeat

# したからうえへ消えながらうえ昇するパーティクル
transform mg_particle_rise(delay=0.0, rise=300, period=3.0):
    yoffset 0 alpha 0.0
    pause delay
    block:
        alpha 0.6
        linear period yoffset -rise alpha 0.0
        yoffset 0
        repeat

# 画面全からだを一瞬ひかりらせるフラッシュ（叫び・れんだヒットじ用）
transform mg_flash_in:
    alpha 0.0
    linear 0.05 alpha 0.7
    linear 0.25 alpha 0.0

# ----------------------------------------

screen minigame_intro_overlay(game):
    modal True
    
    # 1. 背景（くろい幕）
    add Solid("#000000E6") 

    # 2. 背景の装飾（幾なに学的な図かたちがインしてくる）
    # 画面のうしろろにすこし動きをつけることでリッチに見せます
    fixed:
        # ひだりの帯
        add Solid("#ffcc00", xsize=1500, ysize=1500):
            align (5.7, 0.2)
            at intro_bg_shape(0.2, -1000, 0)
        
        # みぎの帯（いろを変えて逆かた向から）
        add Solid("#00ccff", xsize=1500, ysize=1500):
            align (-5.3, 0.8)
            at intro_bg_shape(0.6, 1000, 0)

        # うえの帯
        add Solid("#ff0000", xsize=1800, ysize=800):
            align (10.5, 1.2)
            at intro_bg_shape(0.0, 0, -1000)

        # したの帯（いろを変えて逆かた向から）
        add Solid("#04ff00", xsize=1800, ysize=800):
            align (-12.3, 0.0)
            at intro_bg_shape(0.4, 0, 1000)

    # 3. メインコンテンツ
    vbox:
        align (0.5, 0.5)
        spacing 40
        
        # タイトル（ひだりからイン）
        text game.title:
            size 70 xalign 0.5 color "#fff" outlines [(4, "#000", 0, 0)] bold True
            at intro_slide_left
        
        # 説明文（みぎからイン）
        text game.text:
            size 32 xalign 0.5 color "#ddd" text_align 0.5
            at intro_slide_right
        
        null height 40
        
        # スタートボタン（したからイン）
        textbutton "START":
            style "confirm_button"
            xalign 0.5
            action [SoundAction("minigame_start"), SetField(game, "started", True)]
            hovered SoundAction("hover")
            at intro_fade_up

# ボタンのスタイル
style confirm_button:
    background Solid("#444")
    padding (40, 20)
    hover_background Solid("#666")

style confirm_button_text:
    color "#fff"
    size 40
