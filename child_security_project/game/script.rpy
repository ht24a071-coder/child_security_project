label start:
    # --- 変数とデッキの初期化 ---
    $ current_location_id = 'school'
    $ danger_meter = 0
    $ is_stalked = False
    $ knows_safe_house = False

    # 既存のリストから山札を作成
    $ deck_suspicious = suspicious_events[:]
    $ deck_safe = safe_events[:]
    
    # シャッフル
    $ renpy.random.shuffle(deck_suspicious)
    $ renpy.random.shuffle(deck_safe)

    scene bg school_road_evening
    "下校時刻だ。家に帰ろう！"

    jump map_game_loop


# ==========================================
# マップ移動メインループ
# ==========================================
label map_game_loop:

    # --- 現在地と背景の更新 ---
    $ loc_info = map_data[current_location_id]
    $ current_bg_image = loc_info['bg']

    scene expression current_bg_image with dissolve
    show screen game_hud

    # --- 危険度の計算 (0-100) ---
    $ danger_meter += loc_info['danger_add']
    if danger_meter < 0:
        $ danger_meter = 0
    if danger_meter > 100:
        $ danger_meter = 100

    # --- 110番の家フラグ ---
    if current_location_id == 'house_110':
        $ knows_safe_house = True
        "「こども110番の家」の旗を見つけた！"

    # --- ゴール判定とクライマックス分岐 ---
    if current_location_id == 'home':
        if not is_stalked:
            jump game_clear
        else:
            # 尾行中の場合
            hide screen game_hud
            "自宅に着いたが、背後に気配を感じる！"
            
            menu:
                "一か八か、鍵を開けて逃げ込む！（危険）":
                    jump scene_climax_lock
                
                "大通りの交番へ走って逃げる！（安全策）":
                    jump scene_climax_run_police

    # --- イベント抽選処理 ---
    call trigger_category_event_deck

    # 背景再描画（イベントで変更された場合のため）
    scene expression current_bg_image
    show screen game_hud

    # --- 次の移動先選択 ---
    call screen move_selector(current_location_id)
    $ current_location_id = _return

    jump map_game_loop


# ==========================================
# イベント抽選システム（山札方式）
# ==========================================
label trigger_category_event_deck:
    python:
        # 発生判定（基本10% + 危険度）
        encounter_prob = 10 + danger_meter
        
        if renpy.random.randint(1, 100) > encounter_prob:
            target_label = "event_fallback_nothing"
        
        else:
            # 危険/安全の種別判定
            if renpy.random.randint(1, 100) <= danger_meter:
                is_danger_type = True
            else:
                is_danger_type = False

            # 山札から取得（空なら補充）
            if is_danger_type:
                if len(deck_suspicious) == 0:
                    deck_suspicious = suspicious_events[:]
                    renpy.random.shuffle(deck_suspicious)
                
                if deck_suspicious:
                    target_label = deck_suspicious.pop()
                else:
                    target_label = "event_fallback_nothing"
            else:
                if len(deck_safe) == 0:
                    deck_safe = safe_events[:]
                    renpy.random.shuffle(deck_safe)
                
                if deck_safe:
                    target_label = deck_safe.pop()
                else:
                    target_label = "event_fallback_nothing"

    if target_label != "event_fallback_nothing":
        call expression target_label

    return

# ==========================================
# システム用ラベル（何もしない、エンド等）
# ==========================================
label event_fallback_nothing:
    return

label scene_climax_lock:
    "急いで鍵を開けろ！"
    call screen qte_door_lock
    return

label success_enter_home:
    scene bg_home_indoor
    "間一髪、家に入れた！"
    jump game_clear

label scene_climax_run_police:
    scene bg_koban
    "交番へ駆け込んだ！助かった！"
    jump game_clear

label game_clear:
    hide screen game_hud
    "無事に家に帰ることができた。"
    "GAME CLEAR!!"
    return

label game_over_caught:
    hide screen game_hud
    scene black
    "つかまってしまった……。"
    "GAME OVER"
    return