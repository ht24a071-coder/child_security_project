init -1 python:
    # 2. 連打ミニゲーム (統合版)
    # Logic based on minigame_mash.rpy (better visuals), Structure based on BaseMinigame
    class MashingMinigame(BaseMinigame):
        def __init__(self, target_count=10, time_limit=8.0, **kwargs):
            # デフォルトタイトル・テキストを設定（引数で上書き可能）
            if "title" not in kwargs: kwargs["title"] = "れんだミニゲーム"
            if "text" not in kwargs: kwargs["text"] = "スペースキーを れんだしろ！"
            
            super(MashingMinigame, self).__init__(**kwargs)
            
            self.target_count = target_count
            self.time_limit = time_limit
            self.current_count = 0
            self._real_start_time = None
            
            # 演出用 (from minigame_mash.rpy)
            self.last_press_time = 0.0
            self.shake_offset = (0, 0)

        def get_remaining(self):
            # まだ始まってない、あるいは開始時刻が決まってないなら制限時間をそのまま返す
            if not self.started or self._real_start_time is None: 
                return self.time_limit
            
            elapsed = renpy.get_game_runtime() - self._real_start_time
            return max(0, self.time_limit - elapsed)

        def update(self, st, at):
            if not self.started:
                # 始まってない時は空の更新を返す
                return Solid("#00000000", xsize=1, ysize=40), 0.1

            # 開始直後に現在時刻を記録
            if self._real_start_time is None: 
                self._real_start_time = renpy.get_game_runtime()

            # 時間切れ判定
            if not self.show_result and self.get_remaining() <= 0:
                self.result, self.show_result, self.finished = "miss", True, True
            
            # シェイク減衰
            if renpy.get_game_runtime() - self.last_press_time > 0.1:
                self.shake_offset = (0, 0)

            # ゲージ表示更新
            progress = min(1.0, float(self.current_count) / self.target_count)
            
            # 色の変化 (from minigame_mash.rpy)
            bar_color = "#ff0000" if progress < 0.3 else "#ffff00" if progress < 0.7 else "#00ff00"
            
            return Solid(bar_color, xsize=max(1, int(400 * progress)), ysize=40), 0.05

        def on_mash(self):
            if not self.started or self.show_result or self.finished: return
            
            self.current_count += 1
            self.last_press_time = renpy.get_game_runtime()
            
            # 演出：振動
            import random
            self.shake_offset = (random.randint(-5, 5), random.randint(-5, 5))
            
            if self.current_count >= self.target_count:
                rem = self.get_remaining()
                self.result = "perfect" if rem > self.time_limit * 0.5 else "good"
                self.show_result = self.finished = True
            
    class EscapeMinigame(MashingMinigame):
        def __init__(self, difficulty="normal", **kwargs):
            # 難易度に応じた設定
            settings = {
                "easy":   {"target_count": 10, "time_limit": 5.0},
                "normal": {"target_count": 15, "time_limit": 5.0},
                "hard":   {"target_count": 25, "time_limit": 5.0} # 5秒で25回=連打力5/s
            }
            params = settings.get(difficulty, settings["normal"])
            
            # タイトル等のデフォルト
            if "title" not in kwargs: kwargs["title"] = "にげろ！"
            if "text" not in kwargs: kwargs["text"] = "ボタンを れんだして にげきれ！"
            
            super(EscapeMinigame, self).__init__(
                target_count=params["target_count"], 
                time_limit=params["time_limit"], 
                **kwargs
            )
            # get_remaining, update, on_mash は親クラス MashingMinigame から継承


# -----------------------------------------------------------------------------
# 連打ミニゲーム画面
# -----------------------------------------------------------------------------
screen mashing_minigame(game):
    modal True
    
    # Intro overlay support
    if not game.started:
        use minigame_intro_overlay(game)
    else:
        # ゲーム本編
        if not game.finished:
            timer 0.05 repeat True action Function(renpy.restart_interaction)
        add Solid("#000000CC")

        # ---------------------------------------------------------------
        # 背景アニメーション（ゲーム中演出）
        # ---------------------------------------------------------------
        # 左右から流れ込む斜め帯（赤・オレンジ系）
        add Solid("#ff2200", xsize=800, ysize=60) rotate -20 alpha 0.08:
            align (0.5, 0.2)
            at mg_bg_drift(delay=0.0, dist=80, period=3.0)
        add Solid("#ff6600", xsize=800, ysize=60) rotate -20 alpha 0.08:
            align (0.5, 0.5)
            at mg_bg_drift(delay=0.8, dist=-80, period=3.2)
        add Solid("#ffaa00", xsize=800, ysize=60) rotate -20 alpha 0.08:
            align (0.5, 0.8)
            at mg_bg_drift(delay=1.6, dist=60, period=2.8)

        # 上昇するパーティクル（左・中・右）
        add Solid("#ff4400", xsize=8, ysize=8) alpha 0.5:
            align (0.2, 1.0)
            at mg_particle_rise(delay=0.0, rise=700, period=2.5)
        add Solid("#ff8800", xsize=6, ysize=6) alpha 0.5:
            align (0.5, 1.0)
            at mg_particle_rise(delay=0.9, rise=700, period=3.0)
        add Solid("#ffcc00", xsize=10, ysize=10) alpha 0.5:
            align (0.75, 1.0)
            at mg_particle_rise(delay=1.7, rise=700, period=2.2)
        add Solid("#ff2200", xsize=7, ysize=7) alpha 0.5:
            align (0.35, 1.0)
            at mg_particle_rise(delay=0.4, rise=700, period=2.8)
        add Solid("#ff6600", xsize=9, ysize=9) alpha 0.5:
            align (0.88, 1.0)
            at mg_particle_rise(delay=1.3, rise=700, period=3.3)

        # 連打ヒット時のフラッシュ（shake_offset が非ゼロのとき光る）
        if game.shake_offset != (0, 0):
            add Solid("#ff4400", xsize=1920, ysize=1080) alpha 0.1:
                at mg_flash_in

        # ---------------------------------------------------------------
        frame:
            xalign 0.5 yalign 0.5
            xsize 600 ysize 500
            background None
            # Shake effect applied to the whole frame
            xoffset game.shake_offset[0]
            yoffset game.shake_offset[1]
            
            vbox:
                spacing 30
                xalign 0.5
                
                # タイトルや説明はIntroで出たので、ここではゲーム進行に集中
                text "れんだしろ！" size 40 xalign 0.5 color "#ff0000" bold True outlines [(2, "#fff", 0, 0)]
                
                text "のこり: [game.get_remaining():.1f] びょう" size 28 xalign 0.5 color "#ffff00"
                
                text "[game.current_count] / [game.target_count]" size 60 xalign 0.5 color "#ff6600" bold True
                
                frame:
                    xsize 420 ysize 50 xalign 0.5 background "#444444"
                    add DynamicDisplayable(game.update) align (0.0, 0.5)
                
                if game.show_result:
                    $ res_txt = {"perfect": "PERFECT!!", "good": "GOOD!", "miss": "じかんぎれ..."}.get(game.result)
                    $ res_clr = {"perfect": "#ff0", "good": "#0f0", "miss": "#888"}.get(game.result)
                    text res_txt size 50 xalign 0.5 color res_clr bold True outlines [(3, "#000", 0, 0)]
                else:
                     # ボタン案内
                    text "\u24B6" size 80 color "#00ffff" bold True outlines [(3, "#000", 0, 0)] xalign 0.5 font gui.interface_text_font

        if not game.show_result:
            key game.key action Function(game.on_mash)
        else:
            timer 1.5 action Return(game.result)
