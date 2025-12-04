init python:
    import math
    import pygame

    # --- 1. 3D数学クラス ---
    class Point3D:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    # --- 2. 3Dエンジンシステム (CDD) ---
    class Cyber3DDisplayable(renpy.Displayable):
        def __init__(self, **kwargs):
            super(Cyber3DDisplayable, self).__init__(**kwargs)
            
            # 立方体の頂点定義 (中心からの距離)
            s = 150 # サイズ
            self.vertices = [
                Point3D(-s, -s, -s), Point3D( s, -s, -s),
                Point3D( s,  s, -s), Point3D(-s,  s, -s),
                Point3D(-s, -s,  s), Point3D( s, -s,  s),
                Point3D( s,  s,  s), Point3D(-s,  s,  s)
            ]

            # 頂点を繋ぐ線（辺）の定義
            self.edges = [
                (0,1), (1,2), (2,3), (3,0), # 奥の面
                (4,5), (5,6), (6,7), (7,4), # 手前の面
                (0,4), (1,5), (2,6), (3,7)  # 繋ぎ
            ]

            self.angle_x = 0
            self.angle_y = 0
            self.last_st = 0
            
            # グリッド（地面）の動き用
            self.grid_z_offset = 0

        def rotate(self, point, theta_x, theta_y):
            # X軸回転
            y = point.y * math.cos(theta_x) - point.z * math.sin(theta_x)
            z = point.y * math.sin(theta_x) + point.z * math.cos(theta_x)
            
            # Y軸回転
            x = point.x * math.cos(theta_y) - z * math.sin(theta_y)
            z_final = point.x * math.sin(theta_y) + z * math.cos(theta_y)
            
            return Point3D(x, y, z_final)

        def project(self, point, width, height):
            # 透視投影 (3D座標 -> 2Dスクリーン座標)
            fov = 400 # 視野角的な係数
            camera_dist = 600 # カメラと物体の距離
            
            # カメラより後ろにある点は描画しない
            if point.z + camera_dist <= 0:
                return None

            scale = fov / (point.z + camera_dist)
            
            x_2d = point.x * scale + width / 2
            y_2d = point.y * scale + height / 2
            return (x_2d, y_2d)

        def render(self, width, height, st, at):
            dt = st - self.last_st
            self.last_st = st
            
            render = renpy.Render(width, height)
            canvas = render.canvas()

            # --- 背景：流れるグリッドライン (サイバー空間演出) ---
            # グリッドを手前に移動させる
            speed = 800
            self.grid_z_offset -= speed * dt
            if self.grid_z_offset < -200:
                self.grid_z_offset += 200

            # 地面と天井のグリッド線を描画
            grid_color = (0, 255, 255, 80) # Cyan, 半透明
            horizon_y = height / 2
            
            # 放射状の線
            for x in range(-800, 2000, 200):
                # 簡易的な遠近法
                start_point = (width/2 + (x - width/2)*0.1, horizon_y)
                end_point = (x, height)
                canvas.line(grid_color, start_point, end_point, 2)
                
                # 天井側
                end_point_top = (x, 0)
                canvas.line(grid_color, start_point, end_point_top, 2)

            # 横線（奥から手前へ迫ってくる線）
            for z in range(10):
                # Z距離を擬似的にY座標に変換
                z_pos = z * 200 + self.grid_z_offset
                
                # 【修正ポイント】距離(dist)を計算
                dist = z_pos + 100
                
                # ★安全装置: カメラに近すぎる(10未満)なら描画をスキップ
                # これで無限大になるのを防ぎます
                if dist < 10: 
                    continue

                scale = 200 / dist 
                
                line_y_bottom = horizon_y + 200 * scale
                line_y_top = horizon_y - 200 * scale
                
                # 線の太さを手前ほど太く（最大値を20pxに制限してエラー防止）
                width_line = max(1, int(scale * 3))
                if width_line > 20: width_line = 20 

                alpha = min(255, int(255 * scale))
                
                # 色の作成
                if alpha > 0:
                    col = (0, 255, 255, alpha)
                    canvas.line(col, (0, line_y_bottom), (width, line_y_bottom), width_line)
                    canvas.line(col, (0, line_y_top), (width, line_y_top), width_line)

            # --- メイン：回転する3Dキューブ ---
            # マウス位置で回転速度を変える
            mx, my = renpy.get_mouse_pos()
            target_rot_x = (my - height/2) * 0.005
            target_rot_y = (mx - width/2) * 0.005
            
            self.angle_x += target_rot_x * dt
            self.angle_y += target_rot_y * dt

            # 頂点の計算と投影
            projected_points = []
            for v in self.vertices:
                # 1. 回転
                rotated = self.rotate(v, self.angle_x, self.angle_y)
                # 2. 投影
                proj = self.project(rotated, width, height)
                projected_points.append(proj)

            # 辺の描画
            cube_color = (255, 0, 128, 255) # Magenta
            for edge in self.edges:
                p1 = projected_points[edge[0]]
                p2 = projected_points[edge[1]]
                
                if p1 and p2:
                    # ネオンのような発光感を出すために線を重ねる
                    # 太い半透明の線
                    canvas.line((255, 0, 128, 100), p1, p2, 6)
                    # 細い高輝度の線
                    canvas.line((255, 200, 200, 255), p1, p2, 2)

            # --- UI的な飾り（ハッカー画面風） ---
            # 頂点にドットを打つ
            for p in projected_points:
                if p:
                    canvas.circle((255, 255, 255, 255), p, 3)

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            return None

screen cyber_demo():
    add Solid("#000510") # 濃紺の宇宙
    
    default cyber_system = Cyber3DDisplayable()
    add cyber_system
    
    # HUD (Head Up Display)
    frame:
        background None
        xalign 0.5 yalign 0.1
        text "SYSTEM: ONLINE" size 50 color "#0ff" outlines [(2, "#00aaaa", 0, 0)] at blink_effect

    vbox:
        align (0.05, 0.95)
        text "ROTATION X: ACTIVATED" size 20 color "#f0f" font "DejaVuSans.ttf"
        text "ROTATION Y: ACTIVATED" size 20 color "#f0f" font "DejaVuSans.ttf"
        text "RENDER: WIREFRAME" size 20 color "#f0f" font "DejaVuSans.ttf"

    textbutton "LOGOUT":
        action Return()
        align (0.95, 0.05)
        text_color "#fff"
        text_hover_color "#0ff"

# 点滅エフェクト
transform blink_effect:
    alpha 1.0
    linear 0.5 alpha 0.5
    linear 0.5 alpha 1.0
    repeat

label play_minigame2:
    window hide
    call screen cyber_demo
    window show
    return