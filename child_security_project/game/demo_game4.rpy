init python:
    import math
    import pygame
    import random

    # --- 地形データ生成 (変更なし) ---
    class TerrainMap:
        def __init__(self, size):
            self.size = size
            self.height_map = [0] * (size * size)
            self.color_map = [(0,0,0)] * (size * size)
            self.generate()

        def generate(self):
            for y in range(self.size):
                for x in range(self.size):
                    nx = x / 64.0; ny = y / 64.0
                    h1 = math.sin(nx) * math.cos(ny) 
                    h2 = math.sin(nx * 3 + 1.5) * math.cos(ny * 2.5) * 0.4
                    h3 = math.sin(nx * 10) * math.cos(ny * 10) * 0.05
                    height = int((h1 + h2 + h3 + 1.5) * 60)
                    if height < 0: height = 0
                    if height > 255: height = 255
                    self.height_map[y * self.size + x] = height
                    
                    if height < 50: self.color_map[y * self.size + x] = (20, 40, height + 120)
                    elif height < 60: self.color_map[y * self.size + x] = (200, 190, 140)
                    elif height < 140:
                        noise = random.randint(-10, 10)
                        self.color_map[y * self.size + x] = (30, min(255, 100+height+noise), 40)
                    elif height < 190:
                        c = height - 20
                        self.color_map[y * self.size + x] = (c, c, c)
                    else: self.color_map[y * self.size + x] = (240, 240, 255)

    # --- Voxel Space エンジン (遠距離対応版) ---
    class VoxelDisplayable(renpy.Displayable):
        def __init__(self, **kwargs):
            super(VoxelDisplayable, self).__init__(**kwargs)
            self.map_size = 512
            self.mask = self.map_size - 1
            self.terrain = TerrainMap(self.map_size)
            
            self.cx = 256.0; self.cy = 256.0
            self.height = 150.0; self.angle = 0.0
            self.horizon = 60
            self.speed = 0.0
            self.last_st = 0
            
            self.keys = {pygame.K_i:False, pygame.K_k:False, pygame.K_j:False, pygame.K_l:False, pygame.K_u:False, pygame.K_o:False, pygame.K_q:False, pygame.K_e:False}

        def render(self, width, height, st, at):
            dt = st - self.last_st
            if dt > 0.1: dt = 0.016
            self.last_st = st
            
            # --- 操作処理 ---
            keys = pygame.key.get_pressed()
            if self.keys[pygame.K_j]: self.angle -= 1.5 * dt
            if self.keys[pygame.K_l]: self.angle += 1.5 * dt
            
            target_speed = 0
            if self.keys[pygame.K_i]: target_speed = 100.0
            if self.keys[pygame.K_k]: target_speed = -30.0
            self.speed += (target_speed - self.speed) * 2.0 * dt
            
            self.cx += math.cos(self.angle) * self.speed * dt
            self.cy += math.sin(self.angle) * self.speed * dt
            
            if self.keys[pygame.K_u]: self.height += 60.0 * dt
            if self.keys[pygame.K_o]: self.height -= 60.0 * dt
            if self.keys[pygame.K_q]: self.horizon -= 120 * dt
            if self.keys[pygame.K_e]: self.horizon += 120 * dt
            
            map_offset = (int(self.cy) & self.mask) * self.map_size + (int(self.cx) & self.mask)
            ground_h = self.terrain.height_map[map_offset]
            if self.height < ground_h + 10: self.height = ground_h + 10


            # --- 描画処理 (遠距離特化チューニング) ---
            render = renpy.Render(width, height)
            canvas = render.canvas()
            
            # 空 (より広く高く)
            sky_h = int(self.horizon + height/2 + 100) # 少し余分に描く
            if sky_h > 0:
                canvas.rect((100, 160, 255), (0, 0, width, min(height, sky_h)))
            
            # 【設定】画質と距離のバランス
            STRIDE = 6 # 4(綺麗)〜8(速い)。6はバランス型
            resolution = int(width / STRIDE)
            
            # 【ここが変更点】描画距離を大幅アップ
            view_distance = 450 # 150 -> 450 (3倍！)
            
            sin_a = math.sin(self.angle); cos_a = math.cos(self.angle)
            y_buffer = [height] * resolution
            
            # 変数キャッシュ
            h_half = height / 2
            cam_h = self.height
            hor = self.horizon
            FOG_R, FOG_G, FOG_B = (200, 230, 255)

            # --- メインループ ---
            dz = 1.0
            z = 1.0
            
            while z < view_distance:
                # 座標計算
                plx = -cos_a * z - sin_a * z
                ply = -sin_a * z + cos_a * z
                prx = cos_a * z - sin_a * z
                pry = sin_a * z + cos_a * z
                
                dx = (prx - plx) / resolution
                dy = (pry - ply) / resolution
                rx = self.cx + plx
                ry = self.cy + ply
                
                inv_z = 1.0 / z
                scale = 220.0 * inv_z 
                
                # 霧の計算（距離が伸びたので計算式も調整）
                fog = z / view_distance 
                # 遠くのフォグを少し強めにかける
                fog = fog * fog # 2乗カーブで手前をクリアに
                if fog > 1.0: fog = 1.0
                inv_fog = 1.0 - fog
                
                # 横ループ
                for i in range(resolution):
                    map_off = (int(ry) & self.mask) * self.map_size + (int(rx) & self.mask)
                    map_h = self.terrain.height_map[map_off]
                    
                    screen_y = int((cam_h - map_h) * scale + hor + h_half)

                    if screen_y < y_buffer[i]:
                        col = self.terrain.color_map[map_off]
                        
                        r = int(col[0] * inv_fog + FOG_R * fog)
                        g = int(col[1] * inv_fog + FOG_G * fog)
                        b = int(col[2] * inv_fog + FOG_B * fog)

                        height_draw = y_buffer[i] - screen_y
                        canvas.rect((r,g,b), (i * STRIDE, screen_y, STRIDE, height_draw))
                        
                        y_buffer[i] = screen_y
                    
                    rx += dx
                    ry += dy
                
                # 【ここが超高速化のキモ】
                # 遠くに行くほど、Zの進み方(dz)を加速度的に大きくする
                # 手前は丁寧に、奥は雑に！
                z += dz
                dz += 0.05 * z # 係数を調整して奥をスキップしまくる

            self.draw_hud(render, width, height)
            renpy.redraw(self, 0)
            return render
        
        def draw_hud(self, render, width, height):
            # HUD
            txt = Text(f"ALT:{int(self.height)} SPD:{int(self.speed)}", color="#0f0", size=20, outlines=[(1,"#000")])
            r = renpy.render(txt, width, height, 0, 0)
            render.blit(r, (20, 20))
            
            # レティクル
            canvas = render.canvas()
            cx, cy = width/2, height/2
            canvas.rect((0,255,0), (cx-10, cy, 20, 2))
            canvas.rect((0,255,0), (cx, cy-10, 2, 20))

        def event(self, ev, x, y, st):
            if ev.type==pygame.KEYDOWN and ev.key in self.keys: self.keys[ev.key]=True
            elif ev.type==pygame.KEYUP and ev.key in self.keys: self.keys[ev.key]=False
            return None

screen voxel_flight():
    add VoxelDisplayable()
    add Solid("#000") alpha 0.1
    vbox:
        align (0.95, 0.05)
        text "LONG DISTANCE MODE" color "#0ff" size 12 xalign 1.0
        text "I/K:Speed J/L:Turn U/O:Alt" color "#aaa" size 15 xalign 1.0

    textbutton "EXIT":
        action Return()
        align (0.95, 0.95)
        text_color "#fff"

label play_minigame4:
    window hide
    $ config.mouse = None
    call screen voxel_flight
    $ config.mouse = None
    window show
    return