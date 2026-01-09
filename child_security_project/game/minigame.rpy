## timing_minigame_fixed.rpy
## デザイン拡張版

init -1 python:
    import math

    class TimingMinigame(object):
        def __init__(self, 
            # --- ゲームバランス設定 ---
            speed=2.0, 
            perfect_range=30, 
            good_range=60, 
            key="K_SPACE",
            
            # --- デザイン設定（サイズ） ---
            width=600,
            height=100,
            bar_width=20,
            
            # --- デザイン設定（色・見た目） ---
            # 画像ファイルパスを指定すれば画像になり、Noneなら単色(Solid)になります
            bg_color="#2d2d5f",
            bg_image=None,
            
            border_color="#1a1a3d",
            border_image=None,
            
            bar_color="#ff00ff",
            bar_image=None,
            
            perfect_color="#ffff00", # 判定ゾーンの色
            good_color="#00ff00"
        ):
            """
            デザイン変更可能なタイミングミニゲーム
            """
            # バランス設定
            self.speed = speed
            self.perfect_range = perfect_range
            self.good_range = good_range
            self.key = key
            
            # 状態管理
            self.result = None
            self.position = 0.0
            self.direction = 1
            self.show_result = False
            self.last_st = -1
            
            # デザイン設定の保存
            self.width = width
            self.height = height
            self.bar_width = bar_width
            
            # --- Displayable（表示物）の生成 ---
            # 画像が指定されていれば画像を読み込み、なければ単色(Solid)を作ります
            
            # 1. 移動するバー
            if bar_image:
                self.bar_displayable = Image(bar_image)
            else:
                self.bar_displayable = Solid(bar_color, xsize=bar_width, ysize=height)
                
            # 2. 背景（ゲージ部分）
            if bg_image:
                self.bg_displayable = Image(bg_image)
            else:
                self.bg_displayable = Solid(bg_color, xsize=width, ysize=height)

            # 3. 外枠（ボーダー）
            if border_image:
                self.border_displayable = Image(border_image)
            else:
                # 外枠はメイン領域より少し大きくする
                self.border_displayable = Solid(border_color, xsize=width+20, ysize=height+20)

            # 4. 判定ゾーン（通常は半透明の色）
            self.perfect_displayable = Solid(perfect_color, xsize=perfect_range*2, ysize=height)
            self.good_displayable = Solid(good_color, xsize=good_range*2, ysize=height)


        def update(self, st, at):
            if self.last_st == -1:
                self.last_st = st
            
            dt = st - self.last_st
            self.last_st = st

            if not self.show_result:
                # 移動範囲は width の半分から bar_widthの半分を引いたもの
                max_pos = (self.width / 2) - (self.bar_width / 2)
                
                self.position += self.direction * self.speed * dt * 200

                if self.position >= max_pos:
                    self.position = max_pos
                    self.direction = -1
                elif self.position <= -max_pos:
                    self.position = -max_pos
                    self.direction = 1

            # --- 描画 ---
            # バーの位置を更新して返す
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


screen timing_minigame(game):
    modal True
    
    # 全画面暗転
    add Solid("#000000AA")
    
    # メインウィンドウ
    frame:
        xalign 0.5
        yalign 0.5
        # 全体サイズはゲージサイズに合わせて自動調整させるため固定値を廃止しても良いが
        # ここでは余裕を持たせたサイズにしておく
        padding (50, 50)
        background "#00000000" # ウィンドウ自体は透明に（中のパーツで表現）
        
        vbox:
            spacing 20
            xalign 0.5
            
            # タイトル
            text " [game.key.upper()] を押して振りほどこう!":
                size 40
                xalign 0.5
                color "#ffffff"
                bold True
                outlines [(3, "#000000", 0, 0)]
            
            # ゲーム本体エリア
            fixed:
                xsize game.width + 40 # 外枠分余裕をもたせる
                ysize game.height + 40
                xalign 0.5
                
                # 1. 外枠
                add game.border_displayable:
                    xalign 0.5
                    yalign 0.8
                
                # 2. 背景（ゲージ）
                add game.bg_displayable:
                    xalign 0.5
                    yalign 0.5
                
                # 3. Goodゾーン（広い）
                add game.good_displayable:
                    xalign 0.5
                    yalign 0.5
                    at transform:
                        alpha 0.3
                
                # 4. Perfectゾーン（狭い）
                add game.perfect_displayable:
                    xalign 0.5
                    yalign 0.5
                    at transform:
                        alpha 0.6
                
                # 5. 中央線（センターマーカー）
                frame:
                    xalign 0.5
                    yalign 0.5
                    xsize 2
                    ysize game.height + 10
                    background "#ffffff"

                # 6. ビジュアル
                text "- Press Space -":
                    size 50
                    color "#ffffff"
                    bold True
                    outlines [(4, "#000000", 0, 0)]
                    xalign 0.5
                    yalign -0.2
                
                # 6. 動くバー
                add DynamicDisplayable(game.update)
            
            # 結果表示エリア
            frame:
                background None
                ysize 60
                xalign 0.5
                
                if game.show_result:
                    if game.result == "perfect":
                        text "PERFECT!!":
                            size 50
                            color game.perfect_displayable.color # ゾーンと同じ色にする
                            bold True
                            outlines [(3, "#000000", 0, 0)]
                            xalign 0.5
                    elif game.result == "good":
                        text "GOOD!":
                            size 40
                            color game.good_displayable.color
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

    # 入力処理
    if not game.show_result:
        key game.key action Function(game.check_timing)
    else:
        timer 1.5 action Return(game.result)