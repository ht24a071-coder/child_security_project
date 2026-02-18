init -1 python:
    import math

    # =========================================================================
    # 共通基盤クラス
    # =========================================================================
    class BaseMinigame(object):
        def __init__(self, key="dismiss", title="ミニゲーム", text="ボタンを押して開始！"):
            self.key = key
            self.title = title
            self.text = text
            self.started = False  # まだ始まっていない状態
            self.result = None
            self.show_result = False
            self.finished = False
            self.last_st = -1
            self.start_timestamp = None # 開始時刻

    # バーが左右に動くタイプ（タイミング・脱出）の共通ロジック
    class MovingBarMinigame(BaseMinigame):
        def __init__(self, speed=2.0, target_range=30, width=600, height=100, bar_width=20, **kwargs):
            super(MovingBarMinigame, self).__init__(**kwargs)
            self.speed = speed
            self.target_range = target_range
            self.width, self.height = width, height
            self.bar_width = bar_width
            self.position = 0.0
            self.direction = 1
            
        def update_position(self, st, multiplier=200):
            # まだ始まってなければ動かさない
            if not self.started: return 0.0

            if self.last_st == -1: self.last_st = st
            dt = st - self.last_st
            self.last_st = st
            
            if not self.show_result:
                max_pos = (self.width / 2) - (self.bar_width / 2)
                self.position += self.direction * self.speed * dt * multiplier
                if abs(self.position) >= max_pos:
                    self.position = max_pos if self.position > 0 else -max_pos
                    self.direction *= -1
            return self.position

    # 1. タイミングミニゲーム
    class TimingMinigame(MovingBarMinigame):
        def __init__(self, perfect_range=30, good_range=60, **kwargs):
            super(TimingMinigame, self).__init__(target_range=perfect_range, **kwargs)
            self.perfect_range = perfect_range
            self.good_range = good_range
            self.bg_displayable = Solid("#2d2d5f", xsize=self.width, ysize=self.height)

        def update(self, st, at):
            pos = self.update_position(st)
            bar = Solid("#ff00ff", xsize=self.bar_width, ysize=self.height)
            return Transform(child=bar, xalign=0.5, yalign=0.5, xoffset=int(pos)), 0.0

        def check_timing(self):
            if not self.started or self.show_result: return
            dist = abs(self.position)
            if dist <= self.perfect_range: self.result = "perfect"
            elif dist <= self.good_range: self.result = "good"
            else: self.result = "miss"
            self.show_result = True

    # 2. 連打ミニゲーム
    class MashingMinigame(BaseMinigame):
        def __init__(self, target_count=10, time_limit=3.0, **kwargs):
            super(MashingMinigame, self).__init__(**kwargs)
            self.target_count = target_count
            self.time_limit = time_limit
            self.current_count = 0
            self._real_start_time = None
            self.title = "れんだミニゲーム"
            self.text = "けっていボタンを　れんだしろ！"

        def get_remaining(self):
            # まだ始まってない、あるいは開始時刻が決まってないなら制限時間をそのまま返す
            if not self.started or self._real_start_time is None: 
                return self.time_limit
            
            elapsed = renpy.get_game_runtime() - self._real_start_time
            return max(0, self.time_limit - elapsed)

        def update(self, st, at):
            if not self.started:
                # 始まってない時は空の更新を返す
                return Solid("#ff6600", xsize=1, ysize=40), 0.1

            # 開始直後に現在時刻を記録
            if self._real_start_time is None: 
                self._real_start_time = renpy.get_game_runtime()

            if not self.show_result and self.get_remaining() <= 0:
                self.result, self.show_result, self.finished = "miss", True, True
            
            progress = min(1.0, float(self.current_count) / self.target_count)
            return Solid("#ff6600", xsize=max(1, int(400 * progress)), ysize=40), 0.01

        def on_mash(self):
            if not self.started or self.show_result or self.finished: return
            self.current_count += 1
            if self.current_count >= self.target_count:
                rem = self.get_remaining()
                self.result = "perfect" if rem > self.time_limit * 0.5 else "good"
                self.show_result = self.finished = True

    # 3. 脱出ミニゲーム（連打ベースに変更）
    class EscapeMinigame(MashingMinigame):
        def __init__(self, difficulty="hard", **kwargs):
            # 難易度を連打回数と制限時間にマッピング
            # easy: 10回/4秒, normal: 20回/5秒, hard: 30回/5秒
            settings = {
                "easy": (10, 4.0), 
                "normal": (20, 5.0), 
                "hard": (30, 5.0)
            }
            count, limit = settings.get(difficulty, settings["hard"])
            
            # 親クラス(MashingMinigame)を初期化
            super(EscapeMinigame, self).__init__(target_count=count, time_limit=limit, **kwargs)
            
            self.difficulty = difficulty
            self.title = "にげろ！"
            # テキストはイベント側で "ボタンを連打して..." になっているので、
            # デフォルトは汎用的なものにしておく
            if "text" not in kwargs:
                self.text = "ボタンを れんだして にげきれ！"

        # update, on_mash は MashingMinigame のものをそのまま使う
        # 必要ならオーバーライドして演出を変える
        
        # 既存のイベントコードが check_timing を呼んでいる場合の互換性維持
        # （ただしイベント側が screen escape_minigame を呼んでいるなら、
        #  screen側も対応が必要。screen escape_minigame は minigame.rpy 内にあるので修正する）

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

# =============================================================================
# 各種ゲーム画面（説明画面を内包）
# =============================================================================

# 1. タイミング
screen timing_minigame(game):
    modal True
    
    # まだ始まっていないなら説明を表示
    if not game.started:
        use minigame_intro_overlay(game)
    else:
        # ゲーム本編
        add Solid("#000000AA")
        vbox:
            align (0.5, 0.5)
            spacing 20
            text "タイミングよく押せ！":
                size 40 xalign 0.5 bold True color "#fff" outlines [(2, "#000", 0, 0)]
            fixed:
                xsize game.width + 40 ysize game.height + 40 xalign 0.5
                add Solid("#1a1a3d", xsize=game.width+20, ysize=game.height+20) align (0.5, 0.5)
                add game.bg_displayable align (0.5, 0.5)
                add Solid("#00ff00", xsize=game.good_range*2, ysize=game.height) align (0.5, 0.5) alpha 0.3
                add Solid("#ffff00", xsize=game.perfect_range*2, ysize=game.height) align (0.5, 0.5) alpha 0.6
                add DynamicDisplayable(game.update)
            
            if game.show_result:
                $ res_txt = {"perfect": "PERFECT!!", "good": "GOOD!", "miss": "MISS..."}.get(game.result)
                $ res_clr = {"perfect": "#ff0", "good": "#0f0", "miss": "#f00"}.get(game.result)
                text res_txt size 50 xalign 0.5 color res_clr bold True outlines [(3, "#000", 0, 0)]

        if not game.show_result:
            key game.key action Function(game.check_timing)
        else:
            timer 1.5 action Return(game.result)

# 2. 連打
screen mashing_minigame(game):
    modal True
    
    if not game.started:
        use minigame_intro_overlay(game)
    else:
        # ゲーム本編
        if not game.finished:
            timer 0.05 repeat True action Function(renpy.restart_interaction)
        add Solid("#000000CC")
        vbox:
            align (0.5, 0.5)
            spacing 30
            text "連打しろ！" size 36 xalign 0.5 color "#fff"
            text "のこり: [game.get_remaining():.1f] びょう" size 28 xalign 0.5 color "#ffff00"
            text "[game.current_count] / [game.target_count]" size 60 xalign 0.5 color "#ff6600" bold True
            frame:
                xsize 420 ysize 50 xalign 0.5 background "#444444"
                add DynamicDisplayable(game.update) align (0.0, 0.5)
            
            if game.show_result:
                $ res_txt = {"perfect": "PERFECT!!", "good": "GOOD!", "miss": "じかんぎれ..."}.get(game.result)
                text res_txt size 50 xalign 0.5 color "#fff" bold True

        if not game.show_result:
            key game.key action Function(game.on_mash)
        else:
            timer 1.5 action Return(game.result)

# 3. 脱出
screen escape_minigame(game):
    modal True

    if not game.started:
        use minigame_intro_overlay(game)
    else:
        # ゲーム本編
        if not game.finished:
            timer 0.05 repeat True action Function(renpy.restart_interaction)
            
        add Solid("#220000CC")
        vbox:
            align (0.5, 0.5)
            spacing 25
            text "にげろ！" size 40 xalign 0.5 color "#ff6666" bold True outlines [(3, "#000", 0, 0)]
            
            # 残り時間
            text "のこり: [game.get_remaining():.1f] びょう" size 28 xalign 0.5 color "#ffff00"

            # ゲージ表示 (MashingMinigame.update を利用)
            frame:
                xsize 420 ysize 50 xalign 0.5 background "#440000"
                add DynamicDisplayable(game.update) align (0.0, 0.5)
            
            text "[game.current_count] / [game.target_count]" size 50 xalign 0.5 color "#ffcc00" bold True

            if game.show_result:
                # MashingMinigameは perfect/good/miss を返すが、
                # EscapeMinigameの呼び出し元は success/fail を期待している場合がある
                # クラス側で吸収するか、ここで変換するか。
                # 呼び出し元コード(event_encounter_danger.rpy)は `_return == "success"` を期待している。
                # MashingMinigame.on_mash は perfect/good をセットする。
                # 互換性のため、return値を変換するロジックを入れる。
                
                $ success = (game.result in ["perfect", "good"])
                $ res_txt = "にげきった！" if success else "つかまった..."
                text res_txt size 60 xalign 0.5 color "#fff" bold True outlines [(4, "#f00", 0, 0)]

        if not game.show_result:
            key game.key action Function(game.on_mash)
        else:
            # 呼び出し元が success/fail を期待しているので変換して返す
            $ ret_val = "success" if (game.result in ["perfect", "good"]) else "fail"
            timer 1.5 action Return(ret_val)

# ボタンのスタイル
style confirm_button:
    background Solid("#444")
    padding (40, 20)
    hover_background Solid("#666")

style confirm_button_text:
    color "#fff"
    size 40