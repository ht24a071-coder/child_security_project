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
        "home_marker": "images/gui/icon_home.png",    # ★追加: お家のアイコン
        "school_marker": "images/gui/icon_school.png", # 学校のアイコン
        "nav_marker": "images/gui/nav_marker.png",    # 移動先マーカー画像（差し替え可能）
        "nav_marker_scale": 0.6, # 移動先マーカーのサイズ倍率（30px*0.6=18px。元のノード(10px)より大きくして目立たせる）
        "zoom": 0.45,           # 通常表示用
        "pin_scale": 0.7,       # ピンのサイズ倍率
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

    # mapdata.json の内容で map_coordinates を更新（永続化対応）
    # init -10 で読み込まれている world_map を利用
    if 'world_map' in globals():
        for k, v in world_map.items():
            if "minimap" in v:
                mx, my = v["minimap"]
                # [0, 0] 以外なら上書き（有効な座標とみなす）
                if mx != 0 or my != 0:
                     map_coordinates[k] = (mx, my)

    # =========================================================================
    # リンクエディタ用ヘルパー関数 (Def Missing Functions Fix)
    # =========================================================================
    def link_editor_rename_node(new_name):
        """ノード名を変更し、リンク参照も更新する"""
        state = _link_editor_state
        old_name = state.get("selected_node")
        
        if not old_name:
            return
            
        if not new_name:
            renpy.notify("名前を入力してください")
            return
        
        if new_name in world_map:
            renpy.notify("その名前は既に使用されています")
            return
            
        # 1. データをコピー
        world_map[new_name] = world_map[old_name]
        
        # 2. 古いデータを削除
        del world_map[old_name]
        
        # 3. 座標マップ更新
        if old_name in map_coordinates:
            map_coordinates[new_name] = map_coordinates[old_name]
            del map_coordinates[old_name]
            
        # 4. 全ノードのリンク参照を更新 (重要)
        count = 0
        for node_id, node_data in world_map.items():
            links = node_data.get("links", {})
            updated_links = {}
            modified = False
            for link_text, dest in links.items():
                if dest == old_name:
                    updated_links[link_text] = new_name
                    count += 1
                    modified = True
                else:
                    updated_links[link_text] = dest
            
            if modified:
                node_data["links"] = updated_links
        
        # 5. 保存
        save_map_data()
        
        # 6. UI状態更新
        state["selected_node"] = new_name
        state["mode"] = "edit_links"
        renpy.notify("リネーム完了: {} -> {} (リンク更新: {}件)".format(old_name, new_name, count))
        renpy.restart_interaction()

    def link_editor_start_rename():
        """リネームモード開始"""
        _link_editor_state["mode"] = "rename_node"
        _link_editor_state["temp_input"] = ""

    def link_editor_start_move():
        """移動モード開始"""
        _link_editor_state["mode"] = "move_node_confirm"
        renpy.notify("移動モード: 新しい位置をクリックしてください")

    def link_editor_set_move_coord(x, y):
        """移動先の座標をセットして保存"""
        global map_coordinates
        node_id = _link_editor_state.get("selected_node")
        
        try:
            if node_id and node_id in world_map:
                world_map[node_id]["minimap"] = [x, y]
                
                # 辞書の変更をScreenに通知するために再代入
                map_coordinates[node_id] = (x, y)
                map_coordinates = map_coordinates.copy()
                
                # save_map_data()
                save_map_data()
                
                msg = "移動完了: ({}, {})".format(x, y)
                renpy.notify(msg)
                _link_editor_state["last_message"] = msg
                _link_editor_state["mode"] = "edit_links"
            else:
                msg = "エラー: ノードなし ({})".format(node_id)
                renpy.notify(msg)
                _link_editor_state["last_message"] = msg
                _link_editor_state["mode"] = "edit_links"
        except Exception as e:
            msg = "移動Ex: " + str(e)
            renpy.notify(msg)
            _link_editor_state["last_message"] = msg
            print("Move Error: " + str(e))

    def link_editor_cancel_move():
        _link_editor_state["mode"] = "edit_links"

    def save_map_data():
        """現在のマップデータを保存（互換性用ラッパー）"""
        try:
            # def_map_editor.rpy の関数を利用
            # まだ定義されていない場合の対策
            if "_load_mapdata" not in globals() or "_save_mapdata" not in globals():
                renpy.notify("保存機能が利用できません（関数未定義）")
                return

            data = _load_mapdata()
            # メモリ上で変更された world_map を反映
            data["world_map"] = world_map
            _save_mapdata(data)
        except Exception as e:
            renpy.notify("保存失敗: " + str(e))
            print("Save Error: " + str(e))

# =============================================================================
# ミニマップスクリーン
# =============================================================================
screen minimap():
    zorder 98
    
    # 設定値を取得
    $ cfg = minimap_config
    $ zoom = cfg["zoom"]
    $ pin_scale = cfg["pin_scale"]
    
    # 現在地の座標を取得（ホバー時はその場所、なければ現在地）
    $ current_pos_node = minimap_hover_node if minimap_hover_node else current_node
    $ pos = map_coordinates.get(current_pos_node, None) if current_pos_node else None
    
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
            
            # 全ノードにマーカーを表示（行き先ノードは色付きマーカーに差し替え）
            for node_id, node_pos in map_coordinates.items():
                if node_pos:
                    # マーカーの中心(0.5, 0.5)を座標に合わせる
                    $ marker_x = int(node_pos[0] * zoom)
                    $ marker_y = int(node_pos[1] * zoom)
                    
                    if node_id in home_nodes:
                        # お家アイコン
                        add cfg["home_marker"]:
                            pos (marker_x, marker_y)
                            anchor (0.5, 0.5)
                            zoom 1.5
                    elif node_id == "start_point":
                        # 学校アイコン
                        add cfg["school_marker"]:
                            pos (marker_x, marker_y)
                            anchor (0.5, 0.5)
                            zoom 1.5
                    elif _nav_color_map and node_id in _nav_color_map:
                        # 行き先ノード → カラーマーカー画像に差し替え
                        $ nav_color, nav_img = _nav_color_map[node_id]
                        if renpy.loadable(nav_img):
                            add nav_img:
                                pos (marker_x, marker_y)
                                anchor (0.30, 0.30)
                                zoom cfg["nav_marker_scale"]
                        else:
                            add Text("\u25cf", size=28, color=nav_color, font=gui.text_font):
                                pos (marker_x, marker_y)
                                anchor (0.5, 0.5)
                    else:
                        # 通常の丸いマーカー
                        add cfg["node_marker"]:
                            pos (marker_x, marker_y)
                            anchor (0.5, 0.5)
                            zoom cfg["marker_scale"]

            # 現在地（またはホバー先）にピン画像を表示
            if pos:
                $ pin_x = int(pos[0] * zoom)
                $ pin_y = int(pos[1] * zoom)
                add cfg["pin_image"]:
                    pos (pin_x, pin_y)
                    anchor (0.5, 1.0)
                    zoom pin_scale

    # ミニマップの下にマップ表示ボタン（コントローラーⒾボタンでも開ける）
    textbutton "🗺 マップ {size=22}{color=#FFE66D}Ⓨ{/color}{/size}":
        xalign 1.0 yalign 0.0
        xoffset -cfg["margin_x"]
        yoffset cfg["margin_y"] + 345
        text_size 28
        text_color "#ffffff"
        background Solid("#00000080")
        padding (18, 10, 18, 10)
        hover_foreground Solid("#ffffff30")
        action Show("fullscreen_map")

    key "K_y" action Show("fullscreen_map")

# =============================================================================
# フルスクリーンマップ表示
# ミニマップをタップすると大きいマップを表示
# =============================================================================
screen fullscreen_map():
    zorder 150
    modal True

    # 設定値を取得
    $ cfg = minimap_config
    $ fzoom = 0.85
    $ pos = map_coordinates.get(current_node, None) if current_node else None

    # 背景を暗く
    add Solid("#000000CC")

    # タイトル
    text "🗺 マップ" xalign 0.5 yalign 0.02 size 28 color "#ffffff" bold True

    # マップ表示（中央に大きく）
    frame:
        xalign 0.5 yalign 0.5
        padding (8, 8)
        background "#222222DD"

        fixed:
            fit_first True
            # マップ画像のサイズ * ズーム率
            $ p_zoom = 1.0

            # マップ画像
            add cfg["image"]:
                zoom p_zoom

            # 全ノードにマーカーを表示
            for node_id, node_pos in map_coordinates.items():
                if node_pos and (node_pos[0] != 0 or node_pos[1] != 0):
                    $ marker_x = int(node_pos[0] * p_zoom)
                    $ marker_y = int(node_pos[1] * p_zoom)

                    if node_id in home_nodes:
                        add cfg["home_marker"]:
                            pos (marker_x, marker_y)
                            anchor (0.5, 0.5)
                            zoom 1.6
                    elif node_id == "start_point":
                        add cfg["school_marker"]:
                            pos (marker_x, marker_y)
                            anchor (0.5, 0.5)
                            zoom 1.6
                    elif _nav_color_map and node_id in _nav_color_map:
                        # 行き先ノード → カラーマーカー画像に差し替え
                        $ nav_color, nav_img = _nav_color_map[node_id]
                        if renpy.loadable(nav_img):
                            add nav_img:
                                pos (marker_x, marker_y)
                                anchor (0.30, 0.30)
                                zoom cfg["nav_marker_scale"] * 1.6 # 少し大きめに
                        else:
                            add Text("\u25cf", size=48, color=nav_color, font=gui.text_font):
                                pos (marker_x, marker_y)
                                anchor (0.5, 0.5)
                    else:
                        add cfg["node_marker"]:
                            pos (marker_x, marker_y)
                            anchor (0.5, 0.5)
                            zoom 0.8

            # 現在地ピン（最前面）
            if current_node in map_coordinates:
                $ c_pos = map_coordinates[current_node]
                if c_pos:
                    $ pin_x = int(c_pos[0] * p_zoom)
                    $ pin_y = int(c_pos[1] * p_zoom)
                    add cfg["pin_image"]:
                        pos (pin_x, pin_y)
                        anchor (0.5, 1.0)
                        zoom cfg["pin_scale"] * 1.0



    # 閉じるボタン
    textbutton "× とじる":
        text_font gui.text_font
        xalign 0.5 yalign 0.96
        text_size 24
        text_color "#ffffff"
        background Solid("#00000099")
        padding (20, 8, 20, 8)
        hover_foreground Solid("#ffffff30")
        action Hide("fullscreen_map")

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
    # 入力中のノード情報
    _pending_node_name = None
    _pending_bg_name = None
    
    # デバッグ画面モード: "click", "select_bg"
    _debug_mode = "click"
    
    def request_coord_input(x, y):
        """座標を一時保存してから入力画面を呼び出す"""
        global _pending_coord
        _pending_coord = (x, y)
        renpy.call_in_new_context("_node_input_label")
    
    def debug_go_to_bg_select():
        """ノード名入力後にUI画像選択へ"""
        global _debug_mode
        _debug_mode = "select_bg"
        renpy.restart_interaction()
    
    def debug_select_bg_and_save(bg_name):
        """背景を選択して保存"""
        global _pending_coord, _pending_node_name, _pending_bg_name, _debug_mode
        
        if not _pending_coord or not _pending_node_name:
            _debug_mode = "click"
            renpy.restart_interaction()
            return
        
        x, y = _pending_coord
        node_name = _pending_node_name.strip()
        
        # 保存
        try:
            add_node(node_name, bg_name, x, y)
            debug_clicked_coords.append((node_name, x, y))
            renpy.notify("Saved: {} at ({}, {})".format(node_name, x, y))
        except Exception as e:
            renpy.notify("Error: {}".format(str(e)))
        
        # リセット
        _pending_coord = None
        _pending_node_name = None
        _pending_bg_name = None
        _debug_mode = "click"
        renpy.restart_interaction()
    
    def debug_cancel_bg_select():
        """画像選択をキャンセル"""
        global _pending_coord, _pending_node_name, _debug_mode
        _pending_coord = None
        _pending_node_name = None
        _debug_mode = "click"
        renpy.restart_interaction()
    
    def do_save_node_to_json():
        """ノードをJSONに保存（旧方式、UI選択へ遷移）"""
        global _pending_coord, _pending_node_name, _pending_bg_name
        
        if not _pending_coord or not _pending_node_name:
            renpy.notify("保存をキャンセルしました")
            return
        
        # UI選択モードへ遷移
        debug_go_to_bg_select()

# 座標入力用のラベル（ノード名→画像名の順で入力）
label _node_input_label:
    $ _pending_node_name = renpy.input(
        "ノード名を入力（例: street_1）\n座標: ({}, {})".format(_pending_coord[0], _pending_coord[1]),
        default="", length=30)
    
    if _pending_node_name and _pending_node_name.strip():
        # 既存ノードかチェック
        python:
            _existing_node = world_map.get(_pending_node_name.strip())
            if _existing_node:
                _default_bg = _existing_node.get("bg", "back_town")
            else:
                _default_bg = "back_town"
        
        $ _pending_bg_name = renpy.input(
            "背景画像名を入力（例: back_town）\n※既存ノードなら現在値: {}".format(_default_bg),
            default=_default_bg, length=30)
        
        $ do_save_node_to_json()
    else:
        "キャンセルしました"
        python:
            _pending_coord = None
            _pending_node_name = None
            _pending_bg_name = None
    
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
            textbutton "[[Close]" action Hide("minimap_debug") text_color "#ff8888" text_size 18
    
    # 背景画像選択オーバーレイ（select_bgモード時）
    if _debug_mode == "select_bg":
        frame:
            xalign 0.5 yalign 0.5
            padding (20, 20)
            background "#222222EE"
            
            vbox:
                spacing 10
                
                text "[[Select Background]" color "#ffcc00" size 24
                if _pending_node_name:
                    text "Node: [_pending_node_name]" color "#88ff88" size 16
                if _pending_coord:
                    $ _px, _py = _pending_coord
                    text "Coord: ([_px], [_py])" color "#aaaaaa" size 14
                
                null height 10
                
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    xsize 450
                    ysize 350
                    
                    vbox:
                        spacing 8
                        for bg_name in _available_bg_images:
                            frame:
                                background "#333333"
                                padding (10, 5)
                                xfill True
                                
                                hbox:
                                    spacing 15
                                    add bg_name:
                                        zoom 0.12
                                        yalign 0.5
                                    
                                    vbox:
                                        spacing 3
                                        text "[bg_name]" color "#00ffff" size 16
                                        textbutton "[[Select]":
                                            text_size 14
                                            text_color "#00ff00"
                                            action Function(debug_select_bg_and_save, bg_name)
                
                null height 10
                textbutton "[[Cancel]":
                    text_size 16
                    text_color "#ff8888"
                    action Function(debug_cancel_bg_select)

# =============================================================================
# リンクエディタUI
# ノードを選択してリンクを追加・編集
# 使い方：コンソールで renpy.show_screen("link_editor")
# =============================================================================

init python:
    # リンクエディタの状態管理
    _link_editor_state = {
        "selected_node": None,
        "mode": "select_node",  # select_node, confirm_node, edit_links, ruby_edit, select_dest
        "link_text": "",
        "dest_node": None,
        "hover_node": None,      # ホバー中のノード
        "pending_node": None,    # 確認待ちのノード
        "hover_dest_node": None, # 遷移先選択時にホバー中のノード（マップ上でハイライト用）
    }
    
    def link_editor_hover_node(node_name):
        """ノードにホバー"""
        _link_editor_state["hover_node"] = node_name
        renpy.restart_interaction()
    
    def link_editor_hover_dest(node_name):
        """遷移先リストでホバー（マップ上のノードをハイライト）"""
        _link_editor_state["hover_dest_node"] = node_name
        renpy.restart_interaction()
    
    def link_editor_click_node(node_name):
        """ノードをクリック→確認モードへ"""
        _link_editor_state["pending_node"] = node_name
        _link_editor_state["mode"] = "confirm_node"
        renpy.restart_interaction()
    
    def link_editor_confirm_node():
        """ノード選択を確定"""
        node = _link_editor_state["pending_node"]
        if node:
            _link_editor_state["selected_node"] = node
            _link_editor_state["pending_node"] = None
            _link_editor_state["hover_dest_node"] = None  # ハイライトをクリア
            _link_editor_state["mode"] = "edit_links"
        renpy.restart_interaction()
    
    def link_editor_cancel_confirm():
        """ノード選択確認をキャンセル"""
        _link_editor_state["pending_node"] = None
        _link_editor_state["mode"] = "select_node"
        renpy.restart_interaction()
    
    # =========================================================================
    # Create Node モード（フルスクリーンマップ + クロスヘア）
    # =========================================================================
    _create_node_state = {
        "name": "",
        "bg": "back_town",
        "coord_x": 0,
        "coord_y": 0,
        "step": "coord",  # coord -> name -> bg -> done
    }
    
    def start_create_node_mode():
        """Create Nodeモードを開始"""
        _create_node_state["name"] = ""
        _create_node_state["bg"] = "back_town"
        _create_node_state["coord_x"] = 0
        _create_node_state["coord_y"] = 0
        _create_node_state["step"] = "coord"
        _link_editor_state["mode"] = "create_node"
        renpy.restart_interaction()
    
    def create_node_set_coord(x, y):
        """座標を確定してノード名入力へ"""
        _create_node_state["coord_x"] = x
        _create_node_state["coord_y"] = y
        _create_node_state["step"] = "name"
        renpy.call_in_new_context("_create_node_name_input")
    
    def create_node_select_bg(bg_name):
        """背景を選択して保存"""
        _create_node_state["bg"] = bg_name
        # ノードを実際に保存
        name = _create_node_state["name"]
        x = _create_node_state["coord_x"]
        y = _create_node_state["coord_y"]
        if name:
            add_node(name, bg_name, x, y)
            renpy.notify("Created: {} at ({}, {})".format(name, x, y))
        _link_editor_state["mode"] = "select_node"
        renpy.restart_interaction()
    
    def cancel_create_node():
        """Create Nodeモードをキャンセル"""
        _create_node_state["step"] = "coord"
        _link_editor_state["mode"] = "select_node"
        renpy.restart_interaction()

# Create Node用ノード名入力ラベル
label _create_node_name_input:
    $ _cx = _create_node_state["coord_x"]
    $ _cy = _create_node_state["coord_y"]
    $ _node_name = renpy.input(
        "Enter node name\nCoord: ({}, {})".format(_cx, _cy),
        default="", length=30)
    
    if _node_name and _node_name.strip():
        python:
            _name = _node_name.strip()
            _existing = world_map.get(_name)
            if _existing:
                _create_node_state["bg"] = _existing.get("bg", "back_town")
            _create_node_state["name"] = _name
            _create_node_state["step"] = "bg"
            _link_editor_state["mode"] = "create_node_bg"
    else:
        python:
            _link_editor_state["mode"] = "create_node"
    
    return

init python:
    
    def link_editor_select_node(node_name):
        """ノードを直接選択（リストから）"""
        _link_editor_state["selected_node"] = node_name
        _link_editor_state["mode"] = "edit_links"
        renpy.restart_interaction()
    
    def link_editor_start_add():
        """リンク追加モードを開始"""
        _link_editor_state["mode"] = "add_link"
        _link_editor_state["link_text"] = ""
        _link_editor_state["dest_node"] = None
        renpy.call_in_new_context("_link_input_label")
    
    def link_editor_delete_link(text):
        """リンクを削除"""
        node = _link_editor_state["selected_node"]
        if node:
            remove_link(node, text)
            renpy.restart_interaction()
    
    def link_editor_start_delete_node():
        """ノード削除確認モードへ"""
        _link_editor_state["mode"] = "confirm_delete"
        renpy.restart_interaction()
    
    def link_editor_confirm_delete_node():
        """ノードを削除"""
        node = _link_editor_state["selected_node"]
        if node:
            delete_node(node)
            _link_editor_state["selected_node"] = None
            _link_editor_state["mode"] = "select_node"
            renpy.notify("Node deleted: {}".format(node))
        renpy.restart_interaction()
    
    def link_editor_cancel_delete():
        """削除キャンセル"""
        _link_editor_state["mode"] = "edit_links"
        renpy.restart_interaction()
    
    def link_editor_back():
        """前の画面に戻る"""
        if _link_editor_state["mode"] == "edit_links":
            _link_editor_state["selected_node"] = None
            _link_editor_state["mode"] = "select_node"
        elif _link_editor_state["mode"] == "add_link":
            _link_editor_state["mode"] = "edit_links"
        renpy.restart_interaction()
    
    # =========================================================================
    # 背景画像選択
    # =========================================================================
    # 利用可能な背景画像リスト（images/back/フォルダ内の全画像を動的に取得）
    _available_bg_images = []
    for fn in renpy.list_files():
        if fn.startswith("images/back/") and fn.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            # 拡張子を除去し、パスの最後の部分（ファイル名）のみを取得
            # 例: images/back/back_town.png -> back_town
            name = fn.rsplit(".", 1)[0].split("/")[-1]
            _available_bg_images.append(name)
    
    _available_bg_images.sort()
    
    _bg_selector_state = {
        "selected_bg": None,
        "callback": None,  # 選択後のコールバック
    }
    
    def show_bg_selector(callback_mode):
        """背景選択画面を表示"""
        _link_editor_state["mode"] = "select_bg"
        _bg_selector_state["callback"] = callback_mode
        renpy.restart_interaction()
    
    def select_bg_image(bg_name):
        """背景画像を選択"""
        _bg_selector_state["selected_bg"] = bg_name
        
        callback = _bg_selector_state.get("callback")
        
        if callback == "new_node":
            # 新規ノード作成 - 座標クリック待ちへ
            _new_node_state["bg"] = bg_name
            _link_editor_state["mode"] = "new_node_coord"
            renpy.notify("bg: {} - Click map to set coordinates".format(bg_name))
        else:
            # 既存ノードのbg更新
            node = _link_editor_state["selected_node"]
            if node and node in world_map:
                data = _load_mapdata()
                data["world_map"][node]["bg"] = bg_name
                _save_mapdata(data)
                renpy.notify("bg changed to: {}".format(bg_name))
            _link_editor_state["mode"] = "edit_links"
        
        renpy.restart_interaction()
    
    # =========================================================================
    # 新規ノード作成
    # =========================================================================
    _new_node_state = {
        "name": "",
        "bg": "back_town",
        "coord": None,
    }
    
    def start_new_node():
        """新規ノード作成開始"""
        _new_node_state["name"] = ""
        _new_node_state["bg"] = "back_town"
        _new_node_state["coord"] = None
        renpy.call_in_new_context("_new_node_name_input")
    
    def set_new_node_coord(x, y):
        """新規ノードの座標をセット"""
        _new_node_state["coord"] = (x, y)
        # ノードを作成
        name = _new_node_state["name"]
        bg = _new_node_state["bg"]
        if name:
            add_node(name, bg, x, y)
            renpy.notify("Created: {} at ({}, {})".format(name, x, y))
            _link_editor_state["mode"] = "select_node"
        renpy.restart_interaction()
    
    def cancel_new_node():
        """新規ノード作成キャンセル"""
        _new_node_state["name"] = ""
        _new_node_state["coord"] = None
        _link_editor_state["mode"] = "select_node"
        renpy.restart_interaction()
    
    def link_editor_map_click_new_node():
        """マップクリックで座標を取得（new_node_coordモード用）"""
        # マウス座標を取得
        x, y = renpy.get_mouse_pos()
        # マップフレームのオフセットを考慮（左側フレーム幅10 + padding 10）
        frame_offset_x = 20
        frame_offset_y = 60  # vbox spacing + text height
        
        # 座標補正（zoom 0.65 を逆変換）
        map_x = int((x - frame_offset_x) / 0.65)
        map_y = int((y - frame_offset_y) / 0.65)
        
        # 範囲チェック
        if map_x < 0:
            map_x = 0
        if map_y < 0:
            map_y = 0
        if map_x > 1000:
            map_x = 1000
        if map_y > 754:
            map_y = 754
        
        set_new_node_coord(map_x, map_y)
    
    def link_editor_map_click_for_new_node():
        """マップクリックで座標を取得してノード追加を開始（統合版）"""
        # マウス座標を取得
        x, y = renpy.get_mouse_pos()
        frame_offset_x = 20
        frame_offset_y = 60
        
        # 座標補正（zoom 0.65 を逆変換）
        map_x = int((x - frame_offset_x) / 0.65)
        map_y = int((y - frame_offset_y) / 0.65)
        
        # 範囲チェック
        map_x = max(0, min(map_x, 1000))
        map_y = max(0, min(map_y, 754))
        
        if _link_editor_state["mode"] == "new_node_coord":
            # 既にノード名入力済み - 座標セットして保存
            set_new_node_coord(map_x, map_y)
        else:
            # select_nodeモード - 座標を保存してノード名入力へ
            _new_node_state["coord"] = (map_x, map_y)
            renpy.call_in_new_context("_new_node_from_map_click")

# 新規ノード名入力ラベル
label _new_node_name_input:
    $ _new_node_name = renpy.input(
        "Enter new node name (e.g. street_1)",
        default="", length=30)
    
    if _new_node_name and _new_node_name.strip():
        # 既存チェック
        if _new_node_name.strip() in world_map:
            "Node '[_new_node_name]' already exists"
            python:
                _link_editor_state["mode"] = "select_node"
        else:
            python:
                _new_node_state["name"] = _new_node_name.strip()
                _bg_selector_state["callback"] = "new_node"
                _link_editor_state["mode"] = "select_bg"
    else:
        "Cancelled"
        python:
            _link_editor_state["mode"] = "select_node"
    
    return

# マップ直接クリックでノード追加（座標は既に_new_node_stateに保存済み）
label _new_node_from_map_click:
    $ _coords = _new_node_state.get("coord", (0, 0))
    $ _new_node_name = renpy.input(
        "Node name (coord: {}, {})".format(_coords[0], _coords[1]),
        default="", length=30)
    
    if _new_node_name and _new_node_name.strip():
        python:
            _node_name = _new_node_name.strip()
            _existing = world_map.get(_node_name)
            if _existing:
                # 既存ノード - 座標を更新
                _new_node_state["name"] = _node_name
                _new_node_state["bg"] = _existing.get("bg", "back_town")
                _bg_selector_state["callback"] = "new_node"
                _link_editor_state["mode"] = "select_bg"
            else:
                # 新規ノード - bg選択へ
                _new_node_state["name"] = _node_name
                _bg_selector_state["callback"] = "new_node"
                _link_editor_state["mode"] = "select_bg"
    else:
        python:
            _new_node_state["coord"] = None
            _link_editor_state["mode"] = "select_node"
    
    return

init python:
    def _apply_ruby_to_text(text):
        """ルビ記法を適用: 道(みち) → {rb}道{/rb}{rt}みち{/rt}"""
        return ruby(text)
    
    def _do_add_link_from_input(link_text, dest_node):
        """リンクを実際に追加"""
        node = _link_editor_state["selected_node"]
        if node and link_text and dest_node:
            # ルビはすでに適用済みのテキストをそのまま使用
            add_link(node, link_text, dest_node)
            _link_editor_state["mode"] = "edit_links"
            _link_editor_state["pending_link_text"] = None
            _ruby_editor_state["text"] = ""
            _ruby_editor_state["ruby_ranges"] = []
            renpy.notify("リンクを追加しました！")
    
    def link_editor_select_dest(dest_node):
        """遷移先を選択してリンクを保存"""
        link_text = _link_editor_state.get("pending_link_text", "")
        if link_text:
            _do_add_link_from_input(link_text, dest_node)
        _link_editor_state["hover_dest_node"] = None  # ハイライトをクリア
        renpy.restart_interaction()
    
    def strip_ruby_tags(text):
        """ルビタグを除去してプレーンテキストを返す（表示用）"""
        import re
        # {rb}漢字{/rb}{rt}ふりがな{/rt} → 漢字(ふりがな)
        pattern = r'\{rb\}([^{]+)\{/rb\}\{rt\}([^{]+)\{/rt\}'
        return re.sub(pattern, r'\1(\2)', text)

    def parse_ruby_text(tagged_text):
        """ルビ付きテキストを解析して、ベーステキストとルビ範囲を返す"""
        import re
        pattern = r'\{rb\}([^{]+)\{/rb\}\{rt\}([^{]+)\{/rt\}'
        base_text = ""
        ruby_ranges = []
        last_end = 0
        for m in re.finditer(pattern, tagged_text):
            # マッチ前のプレーンテキスト
            base_text += tagged_text[last_end:m.start()]
            # ルビ対象のテキスト
            target = m.group(1)
            ruby = m.group(2)
            start_idx = len(base_text)
            base_text += target
            end_idx = len(base_text)
            ruby_ranges.append((start_idx, end_idx, ruby))
            last_end = m.end()
        # 残りのテキスト
        base_text += tagged_text[last_end:]
        return base_text, ruby_ranges
    
    # =========================================================================
    # インタラクティブルビエディタ
    # =========================================================================
    _ruby_editor_state = {
        "text": "",           # 元のテキスト
        "ruby_ranges": [],    # [(start, end, ruby_text), ...]
        "selecting": False,
        "select_start": -1,
    }
    
    def ruby_editor_set_text(text):
        """テキストを設定"""
        _ruby_editor_state["text"] = text
        _ruby_editor_state["ruby_ranges"] = []
        renpy.restart_interaction()
    
    def ruby_editor_toggle_char(index):
        """文字をクリックして選択/解除"""
        state = _ruby_editor_state
        if not state["selecting"]:
            # 選択開始
            state["selecting"] = True
            state["select_start"] = index
        else:
            # 選択終了 → ルビ入力
            start = min(state["select_start"], index)
            end = max(state["select_start"], index) + 1
            state["selecting"] = False
            state["select_start"] = -1
            
            # ルビ入力を呼び出す
            renpy.call_in_new_context("_ruby_range_input", start, end)
    
    def ruby_editor_add_ruby(start, end, ruby_text):
        """指定範囲にルビを追加"""
        if ruby_text and ruby_text.strip():
            # 重複チェック・上書き
            _ruby_editor_state["ruby_ranges"] = [
                r for r in _ruby_editor_state["ruby_ranges"]
                if not (r[0] < end and r[1] > start)  # 重複しないものだけ残す
            ]
            _ruby_editor_state["ruby_ranges"].append((start, end, ruby_text.strip()))
            _ruby_editor_state["ruby_ranges"].sort(key=lambda x: x[0])
        renpy.restart_interaction()
    
    def ruby_editor_remove_ruby(start, end):
        """指定範囲のルビを削除"""
        _ruby_editor_state["ruby_ranges"] = [
            r for r in _ruby_editor_state["ruby_ranges"]
            if not (r[0] == start and r[1] == end)
        ]
        renpy.restart_interaction()
    
    def ruby_editor_get_result():
        """ルビ適用済みテキストを取得"""
        state = _ruby_editor_state
        text = state["text"]
        ranges = sorted(state["ruby_ranges"], key=lambda x: x[0], reverse=True)
        
        result = text
        for start, end, ruby_text in ranges:
            target = text[start:end]
            replacement = "{{rb}}{}{{/rb}}{{rt}}{}{{/rt}}".format(target, ruby_text)
            result = result[:start] + replacement + result[end:]
        
        return result
    
    def ruby_editor_confirm():
        """確定して遷移先選択へ"""
        result = ruby_editor_get_result()
        _link_editor_state["pending_link_text"] = result
        _link_editor_state["mode"] = "select_dest"
        renpy.restart_interaction()
    
    def ruby_editor_cancel():
        """キャンセル"""
        _ruby_editor_state["text"] = ""
        _ruby_editor_state["ruby_ranges"] = []
        _link_editor_state["mode"] = "edit_links"
        renpy.restart_interaction()

# ルビ範囲入力用ラベル
label _ruby_range_input(start, end):
    $ _selected_text = _ruby_editor_state["text"][start:end]
    $ _ruby_input = renpy.input(
        "「{}」のふりがなを入力".format(_selected_text),
        default="", length=20)
    $ ruby_editor_add_ruby(start, end, _ruby_input)
    return

# リンクテキスト入力用ラベル
label _link_input_label:
    $ _link_text_input = renpy.input(
        "リンクテキストを入力\n（後でルビを追加できます）",
        default="", length=50)
    
    if _link_text_input and _link_text_input.strip():
        # ルビエディタモードへ
        python:
            ruby_editor_set_text(_link_text_input.strip())
            _link_editor_state["mode"] = "ruby_edit"
    else:
        "キャンセルしました"
        python:
            _link_editor_state["mode"] = "edit_links"
    
    return

screen link_editor():
    zorder 200
    modal True
    
    $ state = _link_editor_state
    $ cfg = minimap_config
    
    # 背景
    add "#000000DD"


    
    # 共通: マップ描画 (create_node系モード または move_node_confirm 用)
    if state["mode"] in ["create_node", "create_node_bg", "move_node_confirm"]:
        # マウス座標計算
        python:
            _mx, _my = renpy.get_mouse_pos()
            # マップサイズ（固定値ベース）
            _map_base_w = 1000
            _map_base_h = 754
            _zoom_factor = 0.9
            _map_w = int(_map_base_w * _zoom_factor)
            _map_h = int(_map_base_h * _zoom_factor)
            
            # マップの左上座標（画面中央配置時の計算）
            _map_left = (config.screen_width - _map_w) // 2
            _map_top = (config.screen_height - _map_h) // 2
            
            # 相対座標
            _rel_x = _mx - _map_left
            _rel_y = _my - _map_top
            
            # オリジナル座標への変換
            _orig_x = int(_rel_x / _zoom_factor)
            _orig_y = int(_rel_y / _zoom_factor)
            
            # マップ内判定
            _in_map = (0 <= _rel_x < _map_w and 0 <= _rel_y < _map_h)
        
        # 背景フレーム（装飾）
        frame:
            align (0.5, 0.5)
            xsize _map_w + 20
            ysize _map_h + 20
            background "#333333"
        
        # マップコンテナ
        fixed:
            align (0.5, 0.5)
            xsize _map_w
            ysize _map_h
            
            # リアルタイム更新用タイマー
            timer 0.05 repeat True action Function(renpy.restart_interaction)
            
            # マップ画像表示
            add cfg["image"]:
                align (0.0, 0.0)
                zoom _zoom_factor
            
            # クリック可能エリア
            python:
                if _in_map:
                    if state["mode"] == "move_node_confirm":
                         _click_action = Function(link_editor_set_move_coord, _orig_x, _orig_y)
                    else:
                         _click_action = Function(create_node_set_coord, _orig_x, _orig_y)
                else:
                    _click_action = NullAction()
            
            imagebutton:
                align (0.0, 0.0)
                idle Solid("#00000001")
                xsize _map_w
                ysize _map_h
                action _click_action
            
            # 既存ノードマーカー表示
            for node_id, node_pos in map_coordinates.items():
                if node_pos:
                    $ _nx = int(node_pos[0] * _zoom_factor)
                    $ _ny = int(node_pos[1] * _zoom_factor)
                    # 移動中は選択中のノードをズーム変え
                    python:
                        if state["mode"] == "move_node_confirm" and node_id == state["selected_node"]:
                            _m_zoom = 0.6
                            _m_alpha = 1.0
                        else:
                            _m_zoom = cfg["marker_scale"]  # ミニマップと同じ 0.5
                            _m_alpha = 0.8

                    add cfg["node_marker"]:
                        pos (_nx, _ny)
                        anchor (0.5, 0.5)
                        zoom _m_zoom
                        alpha _m_alpha
            
            # クロスヘア描画
            if _in_map:
                # 縦線
                add Solid("#00ff00"):
                    pos (_rel_x, 0)
                    xsize 2
                    ysize _map_h
                # 横線
                add Solid("#00ff00"):
                    pos (0, _rel_y)
                    xsize _map_w
                    ysize 2
        
        # UIオーバーレイ (モード別)
        if state["mode"] == "create_node":
            # 上部情報パネル
            frame:
                xalign 0.5 yalign 0.0
                yoffset 10
                padding (20, 10)
                background "#000000CC"
                
                hbox:
                    spacing 30
                    text "【ノード作成モード】" color "#00ff00" size 24
                    if _in_map:
                        text "座標: ([_orig_x], [_orig_y])" color "#00ffff" size 24
                    else:
                        text "マップ上にカーソルを移動してください" color "#888888" size 20
                    text "クリックして決定" color "#aaaaaa" size 16
            
            # キャンセルボタン
            frame:
                xalign 0.5 yalign 1.0
                yoffset -20
                padding (20, 10)
                background "#000000CC"
                
                textbutton "【キャンセル】":
                    text_size 20
                    text_color "#ff8888"
                    action Function(cancel_create_node)

        elif state["mode"] == "create_node_bg":
            # 背景選択パネル
            frame:
                xalign 0.5 yalign 0.5
                padding (20, 20)
                background "#222222EE"
                
                vbox:
                    spacing 10
                    
                    text "【背景画像を選択】" color "#ffcc00" size 24
                    $ _cn = _create_node_state
                    text "ノード名: [_cn['name']]" color "#88ff88" size 16
                    text "座標: ([_cn['coord_x']], [_cn['coord_y']])" color "#aaaaaa" size 14
                    
                    null height 10
                    
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        xsize 500
                        ysize 450
                        
                        vbox:
                            spacing 8
                            for bg_name in _available_bg_images:
                                frame:
                                    background "#333333"
                                    padding (10, 5)
                                    xfill True
                                    
                                    hbox:
                                        spacing 15
                                        add bg_name:
                                            zoom 0.15
                                            yalign 0.5
                                        
                                        vbox:
                                            spacing 3
                                            text "[bg_name]" color "#00ffff" size 16
                                            textbutton "【選択】":
                                                text_size 14
                                                text_color "#00ff00"
                                                action Function(create_node_select_bg, bg_name)
                    
                    null height 10
                    textbutton "【キャンセル】":
                        text_size 16
                        text_color "#ff8888"
                        action Function(cancel_create_node)

        elif state["mode"] == "move_node_confirm":
            # 移動モードのオーバーレイ
            $ m_node = state["selected_node"]
            frame:
                 xalign 0.5 yalign 0.0
                 yoffset 10
                 padding (20, 10)
                 background "#000000CC"
                 
                 vbox:
                     spacing 5
                     text "【ノード移動モード】: [m_node]" color "#ffff00" size 24
                     if _in_map:
                         text "新座標: ([_orig_x], [_orig_y])" color "#00ffff" size 20
                     else:
                         text "新しい位置をクリックしてください" color "#aaaaaa" size 16
            
            frame:
                xalign 0.5 yalign 1.0
                yoffset -20
                padding (20, 10)
                background "#000000CC"
                textbutton "【キャンセル】":
                     text_size 20
                     text_color "#ff8888"
                     action Function(link_editor_cancel_move)
    
    else:
        # 通常モード（既存のhbox UI）
        hbox:
            xfill True
            yfill True
            spacing 20
            
            # 左側: マップ表示（ノードクリック可能）
            frame:
                xsize 780
                yfill True
                background "#222222"
                padding (10, 10)
                
                # マウス座標計算（フレーム内座標を正しく計算）
                python:
                    _mx, _my = renpy.get_mouse_pos()
                    # フレームの左上座標を考慮（padding 10 + 10）
                    _frame_offset_x = 20
                    _frame_offset_y = 20
                    _zoom = 0.75  # 拡大して余白を減らす
                    # ズームを逆変換してオリジナル座標を取得
                    _map_x = int((_mx - _frame_offset_x) / _zoom)
                    _map_y = int((_my - _frame_offset_y) / _zoom)
                    _in_map = (0 <= _map_x <= 1000 and 0 <= _map_y <= 754)
                
                # マップ表示エリア（すべてfixed内に配置）
                fixed:
                    fit_first True
                    
                    add cfg["image"]:
                        zoom _zoom
                    
                    # マップクリック可能エリア（空いている場所をクリックでノード追加）
                    # select_nodeモードまたはnew_node_coordモードでマップクリック有効
                    if state["mode"] in ["select_node", "new_node_coord"]:
                        $ _map_w = int(1000 * _zoom)
                        $ _map_h = int(754 * _zoom)
                        imagebutton:
                            idle Solid("#00000001")
                            xsize _map_w
                            ysize _map_h
                            action Function(link_editor_map_click_for_new_node)
                    
                    # 各ノードをクリック可能なボタンとして表示
                    # ミニマップと同じ方法で node_marker 画像を使用
                    for node_id, node_pos in map_coordinates.items():
                        if node_pos:
                            $ btn_x = int(node_pos[0] * _zoom)
                            $ btn_y = int(node_pos[1] * _zoom)
                            $ is_selected = (state["selected_node"] == node_id)
                            $ is_pending = (state.get("pending_node") == node_id)
                            $ is_hover = (state.get("hover_node") == node_id)
                            $ is_dest_hover = (state.get("hover_dest_node") == node_id)  # 遷移先ホバー
                            
                            # マーカーズームを状態に応じて変更
                            python:
                                if is_pending:
                                    _marker_zoom = 0.7
                                elif is_selected:
                                    _marker_zoom = 0.65
                                elif is_hover or is_dest_hover:
                                    _marker_zoom = 0.6
                                else:
                                    _marker_zoom = cfg["marker_scale"]  # ミニマップと同じ 0.5
                            
                            # ミニマップと同じ方法で配置（add + pos + anchor）
                            add cfg["node_marker"]:
                                pos (btn_x, btn_y)
                                anchor (0.5, 0.5)
                                zoom _marker_zoom
                            
                            # 遷移先ホバー時はノード名を表示
                            if is_dest_hover:
                                frame:
                                    pos (btn_x + 10, btn_y - 20)
                                    background "#000000CC"
                                    padding (5, 2)
                                    text "[node_id]" color "#ffff00" size 12
                            
                            # クリック可能領域（透明ボタン）
                            # select_dest モードでは遷移先として選択
                            python:
                                if state["mode"] == "select_dest":
                                    if node_id != state["selected_node"]:
                                        _node_action = Function(link_editor_select_dest, node_id)
                                    else:
                                        _node_action = NullAction()
                                else:
                                    _node_action = Function(link_editor_click_node, node_id)
                            
                            imagebutton:
                                pos (btn_x - 15, btn_y - 15)
                                idle Solid("#00000001")
                                xsize 30
                                ysize 30
                                hovered Function(link_editor_hover_node, node_id)
                                unhovered Function(link_editor_hover_node, None)
                                action _node_action
                    
                    # 座標・ホバー情報をオーバーレイで表示（マップ上部）
                    frame:
                        pos (0, 0)
                        background "#000000AA"
                        padding (8, 5)
                        
                        hbox:
                            spacing 15
                            if _in_map:
                                text "座標: ([_map_x], [_map_y])" color "#00ffff" size 14
                            else:
                                text "マップ外" color "#888888" size 14
                            
                            if state.get("hover_node"):
                                text "| Hover: [state['hover_node']]" color "#ffcc00" size 14
                            elif state.get("pending_node"):
                                text "| Selected: [state['pending_node']]" color "#00ff00" size 14
                            elif _in_map:
                                text "| クリックでノード追加" color "#88ff88" size 14
            
            # 右側: ノード情報とリンク編集
            frame:
                xfill True
                yfill True
                background "#333333"
                padding (15, 15)
                
                vbox:
                    spacing 10
                    
                    if state["mode"] == "rename_node":
                        # 名前変更モード
                        text "【ノード名の変更】" color "#00ffff" size 24
                        text "新しい名前を入力してください" color "#aaaaaa" size 16
                        
                        null height 20
                        
                        input:
                            value DictInputValue(_link_editor_state, "temp_input")
                            size 24
                            color "#ffffff"
                        
                        null height 20
                        
                        hbox:
                            spacing 20
                            textbutton "【変更する】":
                                text_size 18
                                text_color "#00ff00"
                                action Function(link_editor_rename_node, _link_editor_state["temp_input"])
                            textbutton "【キャンセル】":
                                text_size 18
                                text_color "#ff8888"
                                action SetDict(_link_editor_state, "mode", "edit_links")

                    elif state["mode"] == "confirm_node":
                        # ノード選択確認モード
                        $ pending = state.get("pending_node", "")
                        $ pending_data = world_map.get(pending, {})
                        
                        text "【確認】" color "#00ffff" size 24
                        text "このノードを選択しますか？" color "#aaaaaa" size 16
                        
                        null height 15
                        
                        frame:
                            background "#222222"
                            padding (10, 10)
                            xfill True
                            
                            vbox:
                                spacing 5
                                text "[pending]" color "#00ffff" size 20
                                text "bg: [pending_data.get('bg', '?')]" color "#aaaaaa" size 14
                                $ _lc = len(pending_data.get('links', {}))
                                text "links: [_lc]" color "#aaaaaa" size 14
                        
                        null height 15
                        
                        hbox:
                            spacing 20
                            textbutton "【OK】":
                                text_size 18
                                text_color "#00ff00"
                                action Function(link_editor_confirm_node)
                            textbutton "【キャンセル】":
                                text_size 18
                                text_color "#ff8888"
                                action Function(link_editor_cancel_confirm)
                
                    elif state["mode"] == "select_node" or (not state["selected_node"] and state["mode"] not in ("event_editor", "event_ruby_edit")):
                        # ノード未選択
                        text "【リンクエディタ】" color "#ffff00" size 24
                        text "マップ上のノードをクリックして選択" color "#aaaaaa" size 16
                        
                        null height 20
                        text "ノードリスト:" color "#88ff88" size 18
                        text "(ホバーでマップ上にハイライト)" color "#888888" size 12
                        
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            ysize 400
                            
                            vbox:
                                spacing 5
                                for node_id in sorted(world_map.keys()):
                                    $ node_data = world_map[node_id]
                                    $ link_count = len(node_data.get("links", {}))
                                    textbutton "[node_id] (links: [link_count])":
                                        text_size 14
                                        text_color "#ffffff"
                                        hovered Function(link_editor_hover_dest, node_id)
                                        unhovered Function(link_editor_hover_dest, None)
                                        action Function(link_editor_select_node, node_id)
                        
                        null height 15
                        textbutton "【新規ノード作成】":
                            text_size 16
                            text_color "#00ff00"
                            action Function(start_create_node_mode)
                        
                        null height 10
                        hbox:
                            spacing 15
                            textbutton "【閉じる】":
                                text_size 18
                                text_color "#ff8888"
                                action Hide("link_editor")
                            textbutton "【イベント編集】":
                                text_size 18
                                text_color "#ff88ff"
                                action Function(event_editor_open)
                    
                    elif state["mode"] == "event_editor":
                        # イベントセリフエディタ
                        $ ev_state = _event_editor_state
                        
                        if ev_state["mode"] == "file_list":
                            text "【イベント編集】" color "#ff88ff" size 24
                            text "ファイルを選択" color "#aaaaaa" size 14
                            
                            null height 10
                            viewport:
                                scrollbars "vertical"
                                mousewheel True
                                ysize 500
                                
                                vbox:
                                    spacing 5
                                    for ev_fname, ev_fpath in ev_state["files"]:
                                        textbutton "📄 [ev_fname]":
                                            text_size 16
                                            text_color "#00ffff"
                                            action Function(event_editor_select_file, ev_fname, ev_fpath)
                            
                            null height 15
                            textbutton "【戻る】":
                                text_size 16
                                text_color "#ff8888"
                                action Function(event_editor_close)
                        
                        elif ev_state["mode"] == "line_list":
                            text "【[ev_state['selected_filename']]】" color "#ff88ff" size 20
                            $ _ev_line_count = len(ev_state["lines"])
                            text "セリフ: [_ev_line_count]件" color "#aaaaaa" size 14
                            
                            null height 10
                            viewport:
                                scrollbars "vertical"
                                mousewheel True
                                ysize 450
                                
                                vbox:
                                    spacing 8
                                    for ev_line in ev_state["lines"]:
                                        frame:
                                            background "#222222"
                                            padding (8, 5)
                                            xfill True
                                            
                                            $ _ev_ln = ev_line["line_no"]
                                            $ _ev_sp = ev_line["speaker"]
                                            $ _ev_tx = strip_ruby_tags(ev_line["text"])
                                            $ _ev_tp = ev_line["type"]
                                            $ _ev_has_ruby = "{rb}" in ev_line["text"]
                                            
                                            hbox:
                                                spacing 8
                                                # 行番号
                                                text "L[_ev_ln]" color "#666666" size 12 yalign 0.5 min_width 40
                                                # タイプ表示
                                                if _ev_tp == "menu":
                                                    text "選択" color "#ffcc00" size 12 yalign 0.5
                                                elif _ev_sp:
                                                    text "[_ev_sp]" color "#88ccff" size 12 yalign 0.5
                                                else:
                                                    text "narr" color "#888888" size 12 yalign 0.5
                                                # セリフテキスト（ルビ付きは緑で表示）
                                                if _ev_has_ruby:
                                                    text "[_ev_tx]" color "#00ff00" size 14 yalign 0.5
                                                else:
                                                    text "[_ev_tx]" color "#cccccc" size 14 yalign 0.5
                                                # 編集ボタン
                                                textbutton "✏":
                                                    text_size 16
                                                    text_color "#ff88ff"
                                                    yalign 0.5
                                                    action Function(event_editor_edit_line, ev_line)
                            
                            null height 10
                            textbutton "【← ファイル一覧】":
                                text_size 16
                                text_color "#ffcc00"
                                action Function(event_editor_back)
                    
                    elif state["mode"] == "event_ruby_edit":
                        # イベントセリフのルビ編集
                        $ ruby_state = _ruby_editor_state
                        $ base_text = ruby_state["text"]
                        $ ruby_ranges = ruby_state["ruby_ranges"]
                        $ is_selecting = ruby_state["selecting"]
                        $ select_start = ruby_state["select_start"]
                        $ _ev_editing = _event_editor_state["editing_line"]
                        
                        text "【ルビ編集】" color "#ff88ff" size 24
                        if _ev_editing:
                            $ _ev_sp2 = _ev_editing.get("speaker", "")
                            $ _ev_ln2 = _ev_editing["line_no"]
                            if _ev_sp2:
                                text "[_ev_sp2] (L[_ev_ln2])" color "#aaaaaa" size 14
                            else:
                                text "ナレーション (L[_ev_ln2])" color "#aaaaaa" size 14
                        
                        if is_selecting:
                            text "★ 選択中... 終了位置をクリック" color "#ffff00" size 16
                        else:
                            text "文字をクリックして選択開始/終了" color "#aaaaaa" size 14
                        
                        null height 10
                        
                        # 文字を1つずつクリック可能に表示
                        frame:
                            background "#222222"
                            padding (10, 10)
                            xfill True
                            
                            hbox:
                                spacing 2
                                for i, char in enumerate(base_text):
                                    python:
                                        _has_ruby = False
                                        _ruby_text = ""
                                        for rs, re, rt in ruby_ranges:
                                            if rs <= i < re:
                                                _has_ruby = True
                                                _ruby_text = rt
                                                break
                                        _is_select_start = (is_selecting and select_start == i)
                                        if _has_ruby:
                                            _char_color = "#00ff00"
                                        elif _is_select_start:
                                            _char_color = "#ffff00"
                                        else:
                                            _char_color = "#ffffff"
                                    
                                    textbutton "[char]":
                                        text_size 24
                                        text_color _char_color
                                        action Function(ruby_editor_toggle_char, i)
                        
                        null height 10
                        
                        # ルビ一覧
                        if ruby_ranges:
                            text "追加済みルビ:" color "#88ff88" size 14
                            viewport:
                                scrollbars "vertical"
                                mousewheel True
                                ysize 60
                                
                                vbox:
                                    spacing 3
                                    for rs, re, rt in ruby_ranges:
                                        $ _target = base_text[rs:re]
                                        hbox:
                                            spacing 10
                                            text "[_target]([rt])" color "#aaaaaa" size 14
                                            textbutton "x":
                                                text_size 12
                                                text_color "#ff6666"
                                                action Function(ruby_editor_remove_ruby, rs, re)
                        
                        null height 10
                        
                        # プレビュー
                        text "プレビュー:" color "#88ff88" size 14
                        frame:
                            background "#222222"
                            padding (8, 5)
                            xfill True
                            $ _preview = ruby_editor_get_result()
                            text "[_preview]" color "#00ffff" size 16
                        
                        null height 15
                        
                        hbox:
                            spacing 15
                            textbutton "【保存】":
                                text_size 16
                                text_color "#00ff00"
                                action Function(event_editor_save_ruby)
                            textbutton "【キャンセル】":
                                text_size 16
                                text_color "#ff8888"
                                action Function(event_editor_cancel_ruby)
                    
                    elif state["mode"] == "new_node_coord":
                        # 座標クリック待ちモード
                        $ new_name = _new_node_state.get("name", "")
                        $ new_bg = _new_node_state.get("bg", "")
                        
                        text "【マップをクリック】" color "#00ffff" size 24
                        text "新規ノードの座標を選択してください" color "#aaaaaa" size 14
                        
                        null height 10
                        frame:
                            background "#113322"
                            padding (10, 8)
                            xfill True
                            
                            vbox:
                                spacing 3
                                text "名前: [new_name]" color "#88ff88" size 16
                                text "bg: [new_bg]" color "#aaaaaa" size 14
                        
                        null height 15
                        textbutton "【キャンセル】":
                            text_size 16
                            text_color "#ff8888"
                            action Function(cancel_new_node)
                    
                    elif state["mode"] == "confirm_delete":
                        # ノード削除確認モード
                        $ del_node = state["selected_node"]
                        $ del_data = world_map.get(del_node, {})
                        $ del_links = len(del_data.get("links", {}))
                        
                        text "【ノード削除】" color "#ff4444" size 24
                        text "このノードを本当に削除しますか？" color "#ffaaaa" size 16
                        
                        null height 15
                        
                        frame:
                            background "#441111"
                            padding (15, 10)
                            xfill True
                            
                            vbox:
                                spacing 5
                                text "[del_node]" color "#ff6666" size 20
                                text "bg: [del_data.get('bg', '?')]" color "#aaaaaa" size 14
                                text "links: [del_links]" color "#aaaaaa" size 14
                        
                        null height 20
                        
                        hbox:
                            spacing 20
                            textbutton "【削除する】":
                                text_size 18
                                text_color "#ff0000"
                                action Function(link_editor_confirm_delete_node)
                            textbutton "【キャンセル】":
                                text_size 18
                                text_color "#88ff88"
                                action Function(link_editor_cancel_delete)
                    
                    elif state["mode"] == "select_bg":
                        # 背景画像選択モード
                        text "【背景画像を選択】" color "#ffcc00" size 24
                        text "クリックしてプレビュー・選択" color "#aaaaaa" size 14
                        
                        null height 10
                        
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            ysize 700
                            
                            vbox:
                                spacing 8
                                for bg_name in _available_bg_images:
                                    frame:
                                        background "#222222"
                                        padding (10, 5)
                                        xfill True
                                        
                                        hbox:
                                            spacing 15
                                            # サムネイル表示
                                            add bg_name:
                                                zoom 0.15
                                                yalign 0.5
                                            
                                            vbox:
                                                spacing 3
                                                text "[bg_name]" color "#00ffff" size 16
                                                textbutton "【選択】":
                                                    text_size 14
                                                    text_color "#00ff00"
                                                    action Function(select_bg_image, bg_name)
                        
                        null height 10
                        textbutton "【キャンセル】":
                            text_size 16
                            text_color "#ff8888"
                            action [SetDict(_link_editor_state, "mode", "edit_links")]
                    
                    elif state["mode"] == "ruby_edit":
                        # ルビ編集モード
                        $ ruby_state = _ruby_editor_state
                        $ base_text = ruby_state["text"]
                        $ ruby_ranges = ruby_state["ruby_ranges"]
                        $ is_selecting = ruby_state["selecting"]
                        $ select_start = ruby_state["select_start"]
                        
                        text "【ルビ編集】" color "#ff88ff" size 24
                        text "文字をクリックして選択開始/終了" color "#aaaaaa" size 14
                        
                        if is_selecting:
                            text "★ 選択中... 終了位置をクリック" color "#ffff00" size 16
                        
                        null height 10
                        
                        # 文字を1つずつクリック可能に表示
                        frame:
                            background "#222222"
                            padding (10, 10)
                            xfill True
                            
                            hbox:
                                spacing 2
                                for i, char in enumerate(base_text):
                                    # ルビが付いているかチェック
                                    python:
                                        _has_ruby = False
                                        _ruby_text = ""
                                        for rs, re, rt in ruby_ranges:
                                            if rs <= i < re:
                                                _has_ruby = True
                                                _ruby_text = rt
                                                break
                                        _is_select_start = (is_selecting and select_start == i)
                                        if _has_ruby:
                                            _char_color = "#00ff00"
                                        elif _is_select_start:
                                            _char_color = "#ffff00"
                                        else:
                                            _char_color = "#ffffff"
                                    
                                    textbutton "[char]":
                                        text_size 24
                                        text_color _char_color
                                        action Function(ruby_editor_toggle_char, i)
                        
                        null height 10
                        
                        # ルビ一覧
                        if ruby_ranges:
                            text "追加済みルビ:" color "#88ff88" size 14
                            viewport:
                                scrollbars "vertical"
                                mousewheel True
                                ysize 80
                                
                                vbox:
                                    spacing 3
                                    for rs, re, rt in ruby_ranges:
                                        $ _target = base_text[rs:re]
                                        hbox:
                                            spacing 10
                                            text "[_target]([rt])" color "#aaaaaa" size 14
                                            textbutton "x":
                                                text_size 12
                                                text_color "#ff6666"
                                                action Function(ruby_editor_remove_ruby, rs, re)
                        
                        null height 15
                        
                        # プレビュー
                        text "プレビュー:" color "#88ff88" size 14
                        frame:
                            background "#222222"
                            padding (8, 5)
                            xfill True
                            $ _preview = ruby_editor_get_result()
                            text "[_preview]" color "#00ffff" size 16
                        
                        null height 15
                        
                        hbox:
                            spacing 15
                            textbutton "【確定 → 遷移先選択】":
                                text_size 16
                                text_color "#00ff00"
                                action Function(ruby_editor_confirm)
                            textbutton "【キャンセル】":
                                text_size 16
                                text_color "#ff8888"
                                action Function(ruby_editor_cancel)
                    
                    elif state["mode"] == "select_dest":
                        # 遷移先選択モード
                        $ sel_node = state["selected_node"]
                        $ pending_text = state.get("pending_link_text", "")
                        $ display_text = strip_ruby_tags(pending_text) if pending_text else ""
                        
                        text "【遷移先を選択】" color "#ff88ff" size 24
                        text "From: [sel_node]" color "#aaaaaa" size 14
                        text "Text: [display_text]" color "#88ff88" size 14
                        
                        null height 10
                        text "リストまたはマップから選択:" color "#ffff00" size 16
                        text "(ホバーでマップ上にハイライト)" color "#888888" size 12
                        
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            ysize 280
                            
                            vbox:
                                spacing 5
                                for node_id in sorted(world_map.keys()):
                                    if node_id != sel_node:
                                        textbutton "→ [node_id]":
                                            text_size 16
                                            text_color "#00ffff"
                                            hovered Function(link_editor_hover_dest, node_id)
                                            unhovered Function(link_editor_hover_dest, None)
                                            action Function(link_editor_select_dest, node_id)
                        
                        null height 10
                        textbutton "【キャンセル】":
                            text_size 16
                            text_color "#ff8888"
                            action [SetDict(_link_editor_state, "mode", "edit_links"), SetDict(_link_editor_state, "pending_link_text", None), SetDict(_link_editor_state, "hover_dest_node", None)]
                    
                    else:
                        # ノード選択済み - リンク編集モード
                        $ sel_node = state["selected_node"]
                        $ node_data = world_map.get(sel_node, {})
                        $ node_links = node_data.get("links", {})
                        
                        text "【[sel_node]】" color "#00ffff" size 24
                        
                        # bg表示と変更ボタン
                        hbox:
                            spacing 10
                            text "bg: [node_data.get('bg', '?')]" color "#aaaaaa" size 18
                            textbutton "【変更】":
                                text_size 18
                                text_color "#ffcc00"
                                action Function(show_bg_selector, "edit")
                        
                        # 名前の変更と移動
                        hbox:
                            spacing 15
                            textbutton "【名前変更】":
                                text_size 18
                                text_color "#00ffff"
                                action Function(link_editor_start_rename)
                            textbutton "【位置移動】":
                                text_size 18
                                text_color "#00ffff"
                                action Function(link_editor_start_move)
                        
                        null height 10
                        text "リンク一覧:" color "#88ff88" size 18
                        
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            ysize 200
                            
                            vbox:
                                spacing 8
                                if node_links:
                                    for link_text, dest in node_links.items():
                                        $ _disp_text = strip_ruby_tags(link_text)
                                        hbox:
                                            spacing 10
                                            text "-> [dest]" color "#ffffff" size 18
                                            textbutton "x":
                                                text_size 18
                                                text_color "#ff6666"
                                                action Function(link_editor_delete_link, link_text)
                                        text "   [_disp_text]" color "#aaaaaa" size 16
                                else:
                                    text "(リンクなし)" color "#888888" size 18
                        
                        null height 15
                        
                        hbox:
                            spacing 15
                            textbutton "【+ リンク追加】":
                                text_size 16
                                text_color "#00ff00"
                                action Function(link_editor_start_add)
                            
                            textbutton "【戻る】":
                                text_size 16
                                text_color "#ffcc00"
                                action Function(link_editor_back)
                        
                        null height 10
                        hbox:
                            spacing 15
                            textbutton "【ノード削除】":
                                text_size 18
                                text_color "#ff4444"
                                action Function(link_editor_start_delete_node)
                            textbutton "【イベント編集】":
                                text_size 18
                                text_color "#ff88ff"
                                action Function(event_editor_open)
                        
                        null height 20
                        textbutton "【閉じる】":
                            text_size 18
                            text_color "#ff8888"
                            action Hide("link_editor")

    # デバッグメッセージ表示エリア (最前面)
    if _link_editor_state.get("last_message"):
        text _link_editor_state["last_message"]:
            align (0.5, 0.1)
            color "#ffff00"
            size 30
            outlines [(2, "#000000", 0, 0)]
