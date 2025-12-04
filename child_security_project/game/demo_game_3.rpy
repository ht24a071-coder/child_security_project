init python:
    import math
    import pygame
    import random

    # --- ランダムマップ生成 (変更なし) ---
    class MapGenerator:
        def generate(self, width, height):
            grid = [[1 for _ in range(width)] for _ in range(height)]
            start_x, start_y = 1, 1
            grid[start_y][start_x] = 0
            walls = []
            self.add_walls(start_x, start_y, width, height, walls)
            while walls:
                wx, wy, dx, dy = random.choice(walls)
                walls.remove((wx, wy, dx, dy))
                nx, ny = wx + dx, wy + dy
                if 1 <= nx < width-1 and 1 <= ny < height-1:
                    if grid[ny][nx] == 1:
                        grid[wx][wy] = 0; grid[ny][nx] = 0
                        self.add_walls(nx, ny, width, height, walls)
            for y in range(1, height-1):
                for x in range(1, width-1):
                    if grid[y][x] == 1:
                        if random.random() < 0.3: grid[y][x] = 2
                        elif random.random() < 0.2: grid[y][x] = 3
            self.goal_pos = (1.5, 1.5)
            max_dist = 0
            for y in range(height):
                for x in range(width):
                    if grid[y][x] == 0:
                        dist = (x-start_x)**2 + (y-start_y)**2
                        if dist > max_dist:
                            max_dist = dist
                            self.goal_pos = (x + 0.5, y + 0.5)
            return grid
        def add_walls(self, x, y, w, h, walls):
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in directions:
                nx, ny = x + dx*2, y + dy*2
                if 1 <= nx < w-1 and 1 <= ny < h-1: walls.append((x+dx, y+dy, dx, dy))

    # --- ゲームエンジン ---
    class FPSDisplayable(renpy.Displayable):
        def __init__(self, **kwargs):
            super(FPSDisplayable, self).__init__(**kwargs)
            self.map_w = 16; self.map_h = 16
            generator = MapGenerator()
            self.world_map = generator.generate(self.map_w, self.map_h)
            self.goal_pos = generator.goal_pos
            self.pos_x = 1.5; self.pos_y = 1.5
            self.dir_x = -1.0; self.dir_y = 0.0
            
            # 【調整1】視野角(FOV)を広げる
            # planeの値を大きくすると広角になります (0.66 -> 0.85)
            self.plane_x = 0.0; self.plane_y = 0.85 
            
            self.last_st = 0
            self.keys = {pygame.K_i:False, pygame.K_k:False, pygame.K_j:False, pygame.K_l:False}
            self.win_state = False
            
            # 物理演算用変数
            self.vel_move = 0.0 # 現在の移動速度
            self.vel_rot = 0.0  # 現在の回転速度
            self.walk_timer = 0.0 # ヘッドボブ用タイマー

            # テクスチャ色
            self.tex_colors = {}
            for id in [1, 2, 3]:
                colors = []
                for i in range(16):
                    if id == 1: c = random.randint(100, 140); col = (c,c,c)
                    elif id == 2: c = random.randint(-10,10); col = (120+c, 80+c, 50+c)
                    elif id == 3: c = random.randint(-15,15); col = (140+c, 70+c, 60+c)
                    colors.append(col)
                self.tex_colors[id] = colors

        def render(self, width, height, st, at):
            if self.win_state:
                r = renpy.Render(width, height)
                t = Text("GOAL REACHED", size=80, color="#fff", outlines=[(4,"#000")])
                tr = renpy.render(t, width, height, st, at)
                r.blit(tr, (width/2-tr.width/2, height/2-tr.height/2))
                return r

            dt = st - self.last_st
            if dt > 0.1: dt = 0.016 # ラグ対策
            self.last_st = st
            
            keys = pygame.key.get_pressed()

            # --- 【調整2】物理挙動 (慣性と摩擦) ---
            # パラメータ設定
            MAX_SPEED = 4.0      # 最高速度
            ACCEL = 10.0         # 加速度（動き出しの速さ）
            FRICTION = 8.0       # 摩擦（止まりやすさ）
            
            MAX_ROT = 3.0        # 回転最高速度
            ROT_ACCEL = 8.0      # 回転加速度
            ROT_FRICTION = 10.0  # 回転摩擦

            # 1. 回転の計算
            target_rot = 0
            if self.keys[pygame.K_l]: target_rot = -MAX_ROT
            if self.keys[pygame.K_j]: target_rot = MAX_ROT
            
            # 線形補間(Lerp)っぽく速度を変化させる
            if target_rot != 0:
                # 加速
                if self.vel_rot < target_rot: self.vel_rot += ROT_ACCEL * dt
                if self.vel_rot > target_rot: self.vel_rot -= ROT_ACCEL * dt
            else:
                # 減速（摩擦）
                if self.vel_rot > 0: self.vel_rot -= ROT_FRICTION * dt; self.vel_rot = max(0, self.vel_rot)
                if self.vel_rot < 0: self.vel_rot += ROT_FRICTION * dt; self.vel_rot = min(0, self.vel_rot)

            # 実際に回転させる
            if self.vel_rot != 0:
                rot_step = self.vel_rot * dt
                old_dx = self.dir_x
                self.dir_x = self.dir_x*math.cos(rot_step) - self.dir_y*math.sin(rot_step)
                self.dir_y = old_dx*math.sin(rot_step) + self.dir_y*math.cos(rot_step)
                old_px = self.plane_x
                self.plane_x = self.plane_x*math.cos(rot_step) - self.plane_y*math.sin(rot_step)
                self.plane_y = old_px*math.sin(rot_step) + self.plane_y*math.cos(rot_step)

            # 2. 移動の計算
            target_move = 0
            if self.keys[pygame.K_i]: target_move = MAX_SPEED
            if self.keys[pygame.K_k]: target_move = -MAX_SPEED
            
            # 加速・減速
            if target_move > 0:
                if self.vel_move < target_move: self.vel_move += ACCEL * dt
            elif target_move < 0:
                if self.vel_move > target_move: self.vel_move -= ACCEL * dt
            else:
                # 摩擦で停止
                if self.vel_move > 0: self.vel_move -= FRICTION * dt; self.vel_move = max(0, self.vel_move)
                if self.vel_move < 0: self.vel_move += FRICTION * dt; self.vel_move = min(0, self.vel_move)

            # 実際に移動させる
            if self.vel_move != 0:
                move_step = self.vel_move * dt
                nx = self.pos_x + self.dir_x * move_step
                ny = self.pos_y + self.dir_y * move_step
                
                # 壁判定（滑り処理）
                # X軸方向のみ移動してみて壁がなければ更新
                if self.world_map[int(self.pos_y)][int(nx)] == 0: self.pos_x = nx
                # Y軸方向のみ移動してみて壁がなければ更新
                if self.world_map[int(ny)][int(self.pos_x)] == 0: self.pos_y = ny
                
                # ゴール判定
                gx, gy = self.goal_pos
                if (self.pos_x - gx)**2 + (self.pos_y - gy)**2 < 0.6:
                    self.win_state = True; renpy.timeout(2.0); renpy.jump("game_cleared_label")

            # --- 【調整3】ヘッドボブ（歩行揺れ） ---
            # 移動速度に応じて揺れの速さと大きさを変える
            walk_speed = abs(self.vel_move)
            self.walk_timer += dt * walk_speed * 3.0 # 歩くリズム
            # サイン波で上下の揺れ(Z軸オフセット)を作る
            bob_z = math.sin(self.walk_timer) * 10.0 * (walk_speed / MAX_SPEED)


            # --- 描画 ---
            render = renpy.Render(width, height)
            canvas = render.canvas()
            
            FOG_COLOR = (25, 25, 30)
            canvas.rect(FOG_COLOR, (0,0,width,height))

            FLOOR_STEP = 4
            horizon = height / 2 + bob_z # 地平線も揺らす
            
            # 床描画
            for y in range(int(horizon), height, FLOOR_STEP):
                if y >= height: break
                ratio = (y - horizon) / (height - horizon)
                floor_r = int(FOG_COLOR[0]*(1-ratio) + 60*ratio)
                floor_g = int(FOG_COLOR[1]*(1-ratio) + 55*ratio)
                floor_b = int(FOG_COLOR[2]*(1-ratio) + 50*ratio)
                canvas.rect((floor_r, floor_g, floor_b), (0, y, width, FLOOR_STEP))
            
            canvas.rect((15, 15, 20), (0, 0, width, horizon))

            PIXEL_SIZE = 8 
            cols = int(width / PIXEL_SIZE)
            z_buffer = [0.0] * cols 

            for i in range(cols):
                x = i * PIXEL_SIZE
                camera_x = 2 * i / float(cols) - 1
                ray_dir_x = self.dir_x + self.plane_x * camera_x
                ray_dir_y = self.dir_y + self.plane_y * camera_x
                map_x, map_y = int(self.pos_x), int(self.pos_y)
                delta_x = abs(1/ray_dir_x) if ray_dir_x!=0 else 1e30
                delta_y = abs(1/ray_dir_y) if ray_dir_y!=0 else 1e30
                step_x=0; step_y=0; side_x=0; side_y=0
                if ray_dir_x<0: step_x=-1; side_x=(self.pos_x-map_x)*delta_x
                else: step_x=1; side_x=(map_x+1.0-self.pos_x)*delta_x
                if ray_dir_y<0: step_y=-1; side_y=(self.pos_y-map_y)*delta_y
                else: step_y=1; side_y=(map_y+1.0-self.pos_y)*delta_y
                hit=0; side=0; wall_type=1; loop=100
                while hit==0 and loop>0:
                    if side_x < side_y: side_x+=delta_x; map_x+=step_x; side=0
                    else: side_y+=delta_y; map_y+=step_y; side=1
                    if map_x<0 or map_x>=self.map_w or map_y<0 or map_y>=self.map_h: hit=1
                    elif self.world_map[map_y][map_x] > 0: hit=1; wall_type=self.world_map[map_y][map_x]
                    loop-=1
                if side==0: perp_dist=(side_x-delta_x)
                else: perp_dist=(side_y-delta_y)
                if perp_dist<0.1: perp_dist=0.1
                z_buffer[i] = perp_dist

                line_h = int(height / perp_dist)
                # 上下の揺れを壁の描画位置にも反映
                draw_start = int(-line_h / 2 + height / 2 + bob_z)
                draw_end = int(line_h / 2 + height / 2 + bob_z)
                
                wall_x = self.pos_y + perp_dist * ray_dir_y if side == 0 else self.pos_x + perp_dist * ray_dir_x
                wall_x -= math.floor(wall_x)
                tex_x = int(wall_x * 16)
                col = self.tex_colors.get(wall_type, self.tex_colors[1])[tex_x]
                if side==1: col = (int(col[0]*0.7), int(col[1]*0.7), int(col[2]*0.7))
                
                fog = perp_dist / 8.0; 
                if fog>1.0: fog=1.0

                y_start = max(0, draw_start)
                y_end = min(height, draw_end)
                wall_height = y_end - y_start
                if wall_height > 0:
                    r = int(col[0]*(1-fog)*1.1 + FOG_COLOR[0]*fog)
                    g = int(col[1]*(1-fog)*1.1 + FOG_COLOR[1]*fog)
                    b = int(col[2]*(1-fog)*1.1 + FOG_COLOR[2]*fog)
                    canvas.rect((min(255,r),min(255,g),min(255,b)), (x, y_start, PIXEL_SIZE, wall_height/2))
                    r = int(col[0]*(1-fog) + FOG_COLOR[0]*fog)
                    g = int(col[1]*(1-fog) + FOG_COLOR[1]*fog)
                    b = int(col[2]*(1-fog) + FOG_COLOR[2]*fog)
                    canvas.rect((r,g,b), (x, y_start + wall_height/2, PIXEL_SIZE, wall_height - wall_height/2))

            gx, gy = self.goal_pos
            sprite_x = gx - self.pos_x; sprite_y = gy - self.pos_y
            inv_det = 1.0 / (self.plane_x * self.dir_y - self.dir_x * self.plane_y)
            transform_x = inv_det * (self.dir_y * sprite_x - self.dir_x * sprite_y)
            transform_y = inv_det * (-self.plane_y * sprite_x + self.plane_x * sprite_y)

            if transform_y > 0:
                screen_x = int((width / 2) * (1 + transform_x / transform_y))
                sprite_size = abs(int(height / transform_y)) / 3 
                rot_angle = st * 2 
                front_w = abs(math.cos(rot_angle)) * sprite_size
                side_w = abs(math.sin(rot_angle)) * sprite_size
                total_w = front_w + side_w
                if total_w < 4: total_w = 4

                # アイテムも揺れに合わせて上下させる
                float_y = math.sin(st * 3) * 15 / transform_y + bob_z 
                
                start_y = -sprite_size / 2 + height / 2 + float_y
                start_x = int(screen_x - total_w / 2)

                pulse = (math.sin(st*5)+1)/2 * 55
                front_col = (150+pulse, 255, 255) 
                side_col = (100+pulse, 200, 255) 

                center_idx = int(screen_x / PIXEL_SIZE)
                if 0 <= center_idx < cols and transform_y < z_buffer[center_idx]:
                    if side_w > 1: canvas.rect(side_col, (start_x, start_y, side_w, sprite_size))
                    if front_w > 1: canvas.rect(front_col, (start_x + side_w, start_y, front_w, sprite_size))

            renpy.redraw(self, 0)
            return render
            
        def event(self, ev, x, y, st):
            if self.win_state: return None
            if ev.type==pygame.KEYDOWN and ev.key in self.keys: self.keys[ev.key]=True
            elif ev.type==pygame.KEYUP and ev.key in self.keys: self.keys[ev.key]=False
            return None

screen fps_dungeon():
    add FPSDisplayable()
    add Solid("#000") alpha 0.15
    frame:
        background None
        align (0.5, 0.95)
        text "FIND THE CUBE" color "#aaa" size 18 font "DejaVuSans.ttf"
    
    textbutton "EXIT":
        action Return()
        align (0.95, 0.95)
        text_color "#fff"

label game_cleared_label:
    $ config.mouse = None
    window show
    "キューブに触れた。"
    "視界が白く染まっていく..."
    return

label play_minigame3:
    window hide
    $ config.mouse = None
    call screen fps_dungeon
    $ config.mouse = None
    window show
    return