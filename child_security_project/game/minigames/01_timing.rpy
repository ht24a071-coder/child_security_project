init -1 python:
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


# =============================================================================
# 各種ゲーム画面
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
