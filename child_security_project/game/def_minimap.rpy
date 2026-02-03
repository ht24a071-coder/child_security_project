# =============================================================================
# ミニマップ機能（画像ベース）
# マップ画像の上にピンを表示
# =============================================================================

init -5 python:
    # =========================================================================
    # ミニマップ設定
    # =========================================================================
    minimap_config = {
        "image": "images/gui/minimap.jpg",
        "pin_image": "images/gui/pin.png",
        "node_marker": "images/gui/node_marker.png",  # ノードマーカー画像
        "zoom": 0.4,            # 通常表示用
        "pin_scale": 1.0,       # ピンのサイズ倍率
        "marker_scale": 0.5,    # ノードマーカーのサイズ倍率
        "margin_x": 20,         # 画面右端からの余白
        "margin_y": 20,         # 画面上端からの余白
    }

    # =========================================================================
    # 各ノードのマップ上の座標
    # - 座標はオリジナル画像のピクセル位置で指定
    # - デバッグツールで取得した座標（更新済み）
    # =========================================================================
    map_coordinates = {
        # --- ゲームで使用するノードID（world_map と一致）---
        "start_point":       (609, 271),   # 学校
        "school_park":       (580, 276),   # 学校左の公園近く
        "street_1":          (499, 369),   # 学校左の下
        "street_2":          (482, 446),   # そのさらに下
        "street_a":          (382, 451),   # その左
        "street_b":          (280, 453),   # そのさらに左
        "crossing_point":    (212, 454),   # 横断歩道があるところ
        "factory_road":      (240, 377),   # 高校近くの細道
        "narrow_path_entry": (298, 184),   # おじいちゃんたちの細道入口
        "narrow_path_mid":   (374, 177),   # 細道真ん中
        "narrow_path_exit":  (446, 184),   # 細道出口
        "public_hall":       (484, 182),   # 公民館みたい
        # 修正: 公民館→並木→公園→遮断機→下家の順
        "tree_lined_road":   (629, 173),   # 並木道（公民館の近く）
        "danchi_park":       (623, 199),   # 団地中の公園（並木の隣）
        "railway_point":     (835, 442),   # 遮断機（下家の近く）
        
        # ゴール（上下）
        "home_up":           (336, 55),    # 上家
        "home_down":         (930, 602),   # 下家
    }

# =============================================================================
# ミニマップスクリーン
# =============================================================================
screen minimap():
    zorder 98
    
    # 設定値を取得
    $ cfg = minimap_config
    $ zoom = cfg["zoom"]
    $ pin_scale = cfg["pin_scale"]
    
    # 現在地の座標を取得（なければ None）
    $ pos = map_coordinates.get(current_node, None) if current_node else None
    
    frame:
        xalign 1.0 yalign 0.0
        xoffset -cfg["margin_x"]
        yoffset cfg["margin_y"]
        padding (5, 5)
        background "#00000080"
        
        fixed:
            fit_first True
            
            # マップ画像
            add cfg["image"]:
                zoom zoom
            
            # 全ノードにマーカーを表示
            for node_id, node_pos in map_coordinates.items():
                if node_pos:
                    # マーカーの中心(0.5, 0.5)を座標に合わせる
                    $ marker_x = int(node_pos[0] * zoom)
                    $ marker_y = int(node_pos[1] * zoom)
                    add cfg["node_marker"]:
                        pos (marker_x, marker_y)
                        anchor (0.5, 0.5)
                        zoom cfg["marker_scale"]
            
            # 現在地にピン画像を表示
            if pos:
                # ピンの下端中央(0.5, 1.0)を座標に合わせる
                $ pin_x = int(pos[0] * zoom)
                $ pin_y = int(pos[1] * zoom)
                add cfg["pin_image"]:
                    pos (pin_x, pin_y)
                    anchor (0.5, 1.0)
                    zoom pin_scale

# =============================================================================
# 座標デバッグツール（フルスクリーン版）
# ミニマップを画面中央に大きく表示し、クリックで座標を記録
# 使い方：コンソールで renpy.show_screen("minimap_debug")
#         終了は renpy.hide_screen("minimap_debug")
# =============================================================================

init python:
    # クリックされた座標を記録するリスト
    debug_clicked_coords = []
    # 一時的に座標を保存
    _pending_coord = None
    
    def request_coord_input(x, y):
        """座標を一時保存してから入力画面を呼び出す"""
        global _pending_coord
        _pending_coord = (x, y)
        renpy.call_in_new_context("_coord_input_label")
    
    def do_save_coord(node_name):
        """実際に座標を保存"""
        import os
        global _pending_coord
        x, y = _pending_coord
        
        if not node_name or not node_name.strip():
            node_name = "unnamed_{}".format(len(debug_clicked_coords) + 1)
        else:
            node_name = node_name.strip()
        
        debug_clicked_coords.append((node_name, x, y))
        log_path = os.path.join(config.gamedir, "coordinate_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write('"{}": ({}, {}),\n'.format(node_name, x, y))
        renpy.notify("{}: ({}, {}) を記録！".format(node_name, x, y))
        _pending_coord = None

# 座標入力用のラベル
label _coord_input_label:
    $ _node_name = renpy.input("このポイントの名前は？（例: street_1）", default="", length=30)
    $ do_save_coord(_node_name)
    return

screen minimap_debug():
    zorder 200
    modal True
    
    # リアルタイムでマウス位置を更新するためのタイマー
    timer 0.05 repeat True action renpy.restart_interaction
    
    # デバッグ用のズーム（大きく表示）
    $ debug_zoom = 1.0
    $ cfg = minimap_config
    
    # マウス位置
    $ mx, my = renpy.get_mouse_pos()
    
    # 画像サイズ
    $ map_img = renpy.image_size(cfg["image"])
    $ map_w = int(map_img[0] * debug_zoom)
    $ map_h = int(map_img[1] * debug_zoom)
    
    # マップの左上座標（中央配置）
    $ map_left = (config.screen_width - map_w) // 2
    $ map_top = (config.screen_height - map_h) // 2
    
    # マップ内での相対座標
    $ rel_x = mx - map_left
    $ rel_y = my - map_top
    
    # オリジナル画像上の座標
    $ orig_x = int(rel_x / debug_zoom)
    $ orig_y = int(rel_y / debug_zoom)
    
    # マップ内判定
    $ in_map = (0 <= rel_x <= map_w and 0 <= rel_y <= map_h)
    
    # 背景を暗く
    add "#000000AA"
    
    # マップ画像（中央に大きく・クリック可能）
    frame:
        xalign 0.5 yalign 0.5
        padding (5, 5)
        background "#333333"
        
        fixed:
            fit_first True
            
            # クリック可能なマップ画像
            imagebutton:
                idle cfg["image"]
                action Function(request_coord_input, orig_x, orig_y)
                focus_mask True
            
            # 全ノードにマーカーを表示
            for node_id, node_pos in map_coordinates.items():
                if node_pos:
                    $ marker_x = int(node_pos[0] * debug_zoom)
                    $ marker_y = int(node_pos[1] * debug_zoom)
                    add cfg["node_marker"]:
                        pos (marker_x, marker_y)
                        anchor (0.5, 0.5)
                        zoom 1.0
    
    # クロスヘア（十字線）- マウス位置を正確に表示
    if in_map:
        # 縦線
        add Solid("#ff0000", xsize=2, ysize=30):
            pos (mx - 1, my - 15)
        # 横線
        add Solid("#ff0000", xsize=30, ysize=2):
            pos (mx - 15, my - 1)
        # 中心点
        add Solid("#ffff00", xsize=4, ysize=4):
            pos (mx - 2, my - 2)
    
    # 座標表示（画面左上）
    frame:
        xalign 0.0 yalign 0.0
        xoffset 10
        yoffset 10
        padding (10, 10)
        background "#000000DD"
        
        vbox:
            spacing 5
            text "【座標デバッグモード】" color "#ffff00" size 20
            text "クリックで座標を記録！" color "#88ff88" size 16
            
            null height 5
            text "マウス座標: ([mx], [my])" color "#ffffff" size 14
            
            if in_map:
                text "★ マップ内 ★" color "#00ff00" size 18
                text "画像座標: ([orig_x], [orig_y])" color "#00ffff" size 24 bold True
            else:
                text "（マップ外）" color "#888888" size 16
            
            null height 10
            text "記録数: [len(debug_clicked_coords)]" color "#ffcc00" size 16
            text "ログ: game/coordinate_log.txt" color "#aaaaaa" size 12
            
            null height 10
            textbutton "【閉じる】" action Hide("minimap_debug") text_color "#ff8888" text_size 18
