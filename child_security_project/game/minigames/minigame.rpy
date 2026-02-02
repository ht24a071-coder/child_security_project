# =============================================================================
# ミニゲーム集
# =============================================================================

init -1 python:
    import math

    # =========================================================================
    # 1. タイミングミニゲーム（既存）
    # =========================================================================
    class TimingMinigame(object):
        def __init__(self, speed=2.0, perfect_range=30, good_range=60, key="K_SPACE",
                     width=600, height=100, bar_width=20,
                     bg_color="#2d2d5f", bar_color="#ff00ff",
                     perfect_color="#ffff00", good_color="#00ff00"):
            self.speed = speed
            self.perfect_range = perfect_range
            self.good_range = good_range
            self.key = key
            self.result = None
            self.position = 0.0
            self.direction = 1
            self.show_result = False
            self.last_st = -1
            self.width = width
            self.height = height
            self.bar_width = bar_width
            self.bar_displayable = Solid(bar_color, xsize=bar_width, ysize=height)
            self.bg_displayable = Solid(bg_color, xsize=width, ysize=height)
            self.border_displayable = Solid("#1a1a3d", xsize=width+20, ysize=height+20)
            self.perfect_displayable = Solid(perfect_color, xsize=perfect_range*2, ysize=height)
            self.good_displayable = Solid(good_color, xsize=good_range*2, ysize=height)

        def update(self, st, at):
            if self.last_st == -1:
                self.last_st = st
            dt = st - self.last_st
            self.last_st = st
            if not self.show_result:
                max_pos = (self.width / 2) - (self.bar_width / 2)
                self.position += self.direction * self.speed * dt * 200
                if self.position >= max_pos:
                    self.position = max_pos
                    self.direction = -1
                elif self.position <= -max_pos:
                    self.position = -max_pos
                    self.direction = 1
            display = Transform(child=self.bar_displayable, xalign=0.5, yalign=0.5, xoffset=int(self.position))
            return display, 0.0

        def check_timing(self):
            if self.show_result:
                return
            distance = abs(self.position)
            if distance <= self.perfect_range:
                self.result = "perfect"
            elif distance <= self.good_range:
                self.result = "good"
            else:
                self.result = "miss"
            self.show_result = True

    # =========================================================================
    # 2. 連打ミニゲーム（新規）
    # =========================================================================
    class MashingMinigame(object):
        def __init__(self, target_count=10, time_limit=3.0, key="K_SPACE",
                     bar_color="#ff6600", bg_color="#333333"):
            self.target_count = target_count
            self.time_limit = time_limit
            self.key = key
            self.current_count = 0
            self.result = None
            self.show_result = False
            self.finished = False  # スクリーン終了フラグ
            self.start_time = None
            self.elapsed = 0.0
            self.bar_color = bar_color
            self.bg_color = bg_color
            self._real_start_time = None

        def get_remaining(self):
            """残り時間をリアルタイムで取得"""
            if self._real_start_time is None:
                return self.time_limit
            elapsed = renpy.get_game_runtime() - self._real_start_time
            return max(0, self.time_limit - elapsed)

        def update(self, st, at):
            if self.start_time is None:
                self.start_time = st
                self._real_start_time = renpy.get_game_runtime()
            self.elapsed = st - self.start_time
            
            # 時間切れチェック
            if not self.show_result and self.elapsed >= self.time_limit:
                self.result = "miss"
                self.show_result = True
                self.finished = True
            
            # 進捗バー
            progress = min(1.0, self.current_count / self.target_count)
            bar_width = int(400 * progress)
            bar = Solid(self.bar_color, xsize=max(1, bar_width), ysize=40)
            return bar, 0.01

        def on_mash(self):
            if self.show_result or self.finished:
                return
            self.current_count += 1
            if self.current_count >= self.target_count:
                if self.elapsed < self.time_limit * 0.5:
                    self.result = "perfect"
                elif self.elapsed < self.time_limit * 0.8:
                    self.result = "good"
                else:
                    self.result = "good"
                self.show_result = True
                self.finished = True

    # =========================================================================
    # 3. 難しい脱出ミニゲーム（新規）
    # =========================================================================
    class EscapeMinigame(object):
        def __init__(self, difficulty="hard", key="K_SPACE"):
            self.difficulty = difficulty
            self.key = key
            self.result = None
            self.show_result = False
            self.position = 0.0
            self.direction = 1
            self.last_st = -1
            
            # 難易度設定
            if difficulty == "easy":
                self.speed = 2.0
                self.target_range = 50
            elif difficulty == "normal":
                self.speed = 3.5
                self.target_range = 35
            else:  # hard
                self.speed = 5.0
                self.target_range = 20
            
            self.width = 500
            self.height = 80
            self.bar_width = 15

        def update(self, st, at):
            if self.last_st == -1:
                self.last_st = st
            dt = st - self.last_st
            self.last_st = st
            
            if not self.show_result:
                max_pos = (self.width / 2) - (self.bar_width / 2)
                self.position += self.direction * self.speed * dt * 250
                if self.position >= max_pos:
                    self.position = max_pos
                    self.direction = -1
                elif self.position <= -max_pos:
                    self.position = -max_pos
                    self.direction = 1
            
            bar = Solid("#ff3333", xsize=self.bar_width, ysize=self.height)
            display = Transform(child=bar, xalign=0.5, yalign=0.5, xoffset=int(self.position))
            return display, 0.0

        def check_timing(self):
            if self.show_result:
                return
            distance = abs(self.position)
            if distance <= self.target_range:
                self.result = "success"
            else:
                self.result = "fail"
            self.show_result = True


# =============================================================================
# タイミングミニゲーム画面
# =============================================================================
screen timing_minigame(game):
    modal True
    add Solid("#000000AA")
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (50, 50)
        background "#00000000"
        
        vbox:
            spacing 20
            xalign 0.5
            
            text "スペースキー を おせ!":
                size 40
                xalign 0.5
                color "#ffffff"
                bold True
                outlines [(3, "#000000", 0, 0)]
            
            fixed:
                xsize game.width + 40
                ysize game.height + 40
                xalign 0.5
                
                add game.border_displayable:
                    xalign 0.5
                    yalign 0.8
                
                add game.bg_displayable:
                    xalign 0.5
                    yalign 0.5
                
                add game.good_displayable:
                    xalign 0.5
                    yalign 0.5
                    at transform:
                        alpha 0.3
                
                add game.perfect_displayable:
                    xalign 0.5
                    yalign 0.5
                    at transform:
                        alpha 0.6
                
                frame:
                    xalign 0.5
                    yalign 0.5
                    xsize 2
                    ysize game.height + 10
                    background "#ffffff"
                
                add DynamicDisplayable(game.update)
            
            frame:
                background None
                ysize 60
                xalign 0.5
                
                if game.show_result:
                    if game.result == "perfect":
                        text "PERFECT!!":
                            size 50
                            color "#ffff00"
                            bold True
                            outlines [(3, "#000000", 0, 0)]
                            xalign 0.5
                    elif game.result == "good":
                        text "GOOD!":
                            size 40
                            color "#00ff00"
                            bold True
                            outlines [(3, "#000000", 0, 0)]
                            xalign 0.5
                    else:
                        text "MISS...":
                            size 40
                            color "#ff0000"
                            bold True
                            outlines [(3, "#000000", 0, 0)]
                            xalign 0.5

    if not game.show_result:
        key game.key action Function(game.check_timing)
    else:
        timer 1.5 action Return(game.result)


# =============================================================================
# 連打ミニゲーム画面
# =============================================================================
screen mashing_minigame(game):
    modal True
    
    # 画面を定期的に再描画（残り時間を更新するため）
    # 結果表示後は停止
    if not game.finished:
        timer 0.05 repeat True action Function(renpy.restart_interaction)
    
    add Solid("#000000CC")
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (60, 60)
        background "#222222"
        
        vbox:
            spacing 30
            xalign 0.5
            
            text "れんだ！スペースキーを れんだしろ！":
                size 36
                xalign 0.5
                color "#ffffff"
                bold True
            
            # 残り時間
            $ remaining = game.get_remaining()
            text "のこり: [remaining:.1f] びょう":
                size 28
                xalign 0.5
                color "#ffff00"
            
            # カウント表示
            text "[game.current_count] / [game.target_count]":
                size 60
                xalign 0.5
                color "#ff6600"
                bold True
            
            # 進捗バー
            frame:
                xsize 420
                ysize 50
                xalign 0.5
                background "#444444"
                
                add DynamicDisplayable(game.update):
                    xalign 0.0
                    yalign 0.5
            
            # 結果
            if game.show_result:
                if game.result == "perfect":
                    text "PERFECT!!":
                        size 50
                        color "#ffff00"
                        bold True
                        xalign 0.5
                elif game.result == "good":
                    text "GOOD!":
                        size 40
                        color "#00ff00"
                        bold True
                        xalign 0.5
                else:
                    text "じかんぎれ...":
                        size 40
                        color "#ff0000"
                        bold True
                        xalign 0.5

    if not game.show_result:
        key game.key action Function(game.on_mash)
    else:
        timer 1.5 action Return(game.result)


# =============================================================================
# 難しい脱出ミニゲーム画面
# =============================================================================
screen escape_minigame(game):
    modal True
    add Solid("#220000CC")
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (50, 50)
        background "#330000"
        
        vbox:
            spacing 25
            xalign 0.5
            
            text "にげろ！タイミングよく スペースキー！":
                size 36
                xalign 0.5
                color "#ff6666"
                bold True
            
            if game.difficulty == "hard":
                text "むずかしい！":
                    size 24
                    xalign 0.5
                    color "#ff0000"
            
            fixed:
                xsize game.width + 40
                ysize game.height + 40
                xalign 0.5
                
                add Solid("#1a0000", xsize=game.width+20, ysize=game.height+20):
                    xalign 0.5
                    yalign 0.5
                
                add Solid("#330000", xsize=game.width, ysize=game.height):
                    xalign 0.5
                    yalign 0.5
                
                # ターゲットゾーン
                add Solid("#00ff00", xsize=game.target_range*2, ysize=game.height):
                    xalign 0.5
                    yalign 0.5
                    at transform:
                        alpha 0.4
                
                frame:
                    xalign 0.5
                    yalign 0.5
                    xsize 2
                    ysize game.height + 10
                    background "#ffffff"
                
                add DynamicDisplayable(game.update)
            
            frame:
                background None
                ysize 60
                xalign 0.5
                
                if game.show_result:
                    if game.result == "success":
                        text "にげきった！":
                            size 50
                            color "#00ff00"
                            bold True
                            xalign 0.5
                    else:
                        text "つかまった...":
                            size 50
                            color "#ff0000"
                            bold True
                            xalign 0.5

    if not game.show_result:
        key game.key action Function(game.check_timing)
    else:
        timer 1.5 action Return(game.result)