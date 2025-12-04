init python:
    import math
    import random
    import pygame

    # --- 1. パーティクル単体の定義 ---
    class NeonParticle:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            # 速度（ランダムに散らす）
            angle = random.uniform(0, 6.28)
            speed = random.uniform(2, 10)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            
            # 色（寿命とともに変化させるためHSV的な管理）
            self.hue = random.uniform(0, 1)
            self.life = 1.0 # 1.0(生きている) -> 0.0(消滅)
            self.decay = random.uniform(0.005, 0.015) # 寿命の減る速さ
            self.size = random.uniform(2, 5)

    # --- 2. メインシステム (CDD) ---
    class ParticleSystemDisplayable(renpy.Displayable):
        def __init__(self, **kwargs):
            super(ParticleSystemDisplayable, self).__init__(**kwargs)
            self.particles = []
            self.last_st = 0
            self.mouse_x = 0
            self.mouse_y = 0
            self.is_mouse_pressed = False
            
            # 初期パーティクル生成（爆発させる）
            self.spawn_particles(640, 360, 200)

        def spawn_particles(self, x, y, count):
            # 一気に大量生成
            for _ in range(count):
                self.particles.append(NeonParticle(x, y))

        def render(self, width, height, st, at):
            # 経過時間計算
            dt = st - self.last_st
            if dt > 0.1: dt = 0.016
            self.last_st = st

            # キャンバスを作成（ここに直接お絵かきする）
            render = renpy.Render(width, height)
            canvas = render.canvas()

            # --- 物理演算と描画ループ ---
            # Pythonのリスト処理は遅いので、なるべく高速化を意識
            
            # マウスの位置を取得（イベント外でも滑らかに取るため）
            mx, my = renpy.get_mouse_pos()

            # 生き残るパーティクル用リスト
            alive_particles = []

            for p in self.particles:
                # 1. マウスへの引力/斥力（ブラックホール効果）
                dx = mx - p.x
                dy = my - p.y
                dist_sq = dx*dx + dy*dy + 0.1 # 0除算防止
                dist = math.sqrt(dist_sq)

                if self.is_mouse_pressed:
                    # クリック中は「強力な吸引」
                    force = 10000 / dist_sq
                    p.vx += (dx / dist) * force * dt
                    p.vy += (dy / dist) * force * dt
                else:
                    # 普段は「マウスを避ける（斥力）」
                    if dist < 150:
                        force = -5000 / dist_sq
                        p.vx += (dx / dist) * force * dt
                        p.vy += (dy / dist) * force * dt

                # 2. 摩擦（空気抵抗）
                p.vx *= 0.96
                p.vy *= 0.96

                # 3. 座標更新
                p.x += p.vx
                p.y += p.vy

                # 4. 壁での跳ね返り
                if p.x < 0:
                    p.x = 0; p.vx *= -0.8
                elif p.x > width:
                    p.x = width; p.vx *= -0.8
                
                if p.y < 0:
                    p.y = 0; p.vy *= -0.8
                elif p.y > height:
                    p.y = height; p.vy *= -0.8

                # 5. 寿命更新
                p.life -= p.decay
                
                # 描画 (Canvasに直接描く)
                if p.life > 0:
                    # 色の計算 (RGB)
                    # 速度が速いほど白く光らせる演出
                    speed = math.sqrt(p.vx*p.vx + p.vy*p.vy)
                    r = min(255, int(255 * p.life + speed * 5))
                    g = min(255, int(100 * p.life + speed * 2))
                    b = min(255, int(50 * p.life))
                    color = (r, g, b, int(255 * p.life)) # Alphaあり

                    # 円を描画
                    canvas.circle(color, (p.x, p.y), p.size)
                    alive_particles.append(p)
            
            # 死んだパーティクルを削除したリストに更新
            self.particles = alive_particles

            # パーティクルが減りすぎたら自動補給（賑やかし）
            if len(self.particles) < 300:
                self.spawn_particles(random.randint(0, width), random.randint(0, height), 5)

            # 常に全力で再描画
            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            # マウス入力の状態管理
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.is_mouse_pressed = True
                # クリックした瞬間に爆発生成
                self.spawn_particles(x, y, 100)
                raise renpy.IgnoreEvent()
            
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.is_mouse_pressed = False
            
            return None

# --- スクリーン定義 ---
screen technical_demo():
    # 背景を真っ黒に（光を際立たせるため）
    add Solid("#050505")
    
    # パーティクルシステム配置
    default system = ParticleSystemDisplayable()
    add system
    
    # UIレイヤー
    vbox:
        align (0.05, 0.05)
        text "Ren'Py Particle Physics Demo" size 40 color "#fff" outlines [(2, "#000")]
        text "Mouse Click: Attract & Spawn" size 24 color "#aaa"
        text "Mouse Hover: Repel" size 24 color "#aaa"

    textbutton "EXIT":
        action Return()
        align (0.95, 0.05)
        text_color "#fff"
        text_hover_color "#f00"

# --- 呼び出し用ラベル ---
label play_minigame:
    window hide
    call screen technical_demo
    window show
    return