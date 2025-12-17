label start:
    # 変数リセット
    $ current_location_id = 'school'
    $ danger_meter = 0
    $ is_stalked = False
    $ knows_safe_house = False
    $ heard_rumor_110 = False
    $ visited_locations = set()
    $ visited_locations.add('school')

    # 地図画像の指定（黄色い線入りのもの）
    $ current_minimap_image = "minimap_guide.png"

    # デッキ作成
    $ deck_suspicious = suspicious_events[:]
    $ deck_safe = safe_events[:]
    $ renpy.random.shuffle(deck_suspicious)
    $ renpy.random.shuffle(deck_safe)

    scene bg school_road_evening
    "下校時刻だ。家に帰ろう！"
    "（右上の地図に書いてある「黄色い線」が通学路だ。）"
    "（自分のアイコンの位置を確認しながら、正しい道を選ぼう。）"

    jump map_game_loop


# ==========================================
# マップ移動メインループ
# ==========================================
label map_game_loop:

    $ visited_locations.add(current_location_id)
    $ loc_info = map_data[current_location_id]
    $ current_bg_image = loc_info['bg']

    scene expression current_bg_image with dissolve
    show screen game_hud

    # 危険度計算
    $ danger_meter += loc_info['danger_add']
    if danger_meter < 0:
        $ danger_meter = 0
    if danger_meter > 100:
        $ danger_meter = 100

    # 110番の家イベント（大通りor住宅街）
    if current_location_id == 'main_road' or current_location_id == 'residential_area':
        if heard_rumor_110 and not knows_safe_house:
            $ knows_safe_house = True
            "通学路を歩いていると、110番の家を見つけた！"
            "（寄り道せずに帰ったおかげですぐ見つかったぞ。）"

    # ゴール判定
    if current_location_id == 'home':
        if not is_stalked:
            jump game_clear
        else:
            hide screen game_hud
            "自宅前。背後に気配が……！"
            menu:
                "鍵を開けて逃げ込む！（危険）":
                    jump scene_climax_lock
                "交番へ走る！（安全）":
                    jump scene_climax_run_police

    # イベント発生
    if loc_info['is_event_spot']:
        call trigger_category_event_deck

    scene expression current_bg_image
    show screen game_hud

    # 移動選択
    call screen move_selector(current_location_id)
    $ current_location_id = _return

    jump map_game_loop


# ==========================================
# イベント抽選ロジック
# ==========================================
label trigger_category_event_deck:
    python:
        encounter_prob = 50 + danger_meter
        
        if renpy.random.randint(1, 100) > encounter_prob:
            target_label = "event_fallback_nothing"
        else:
            if renpy.random.randint(1, 100) <= danger_meter:
                is_danger_type = True
            else:
                is_danger_type = False

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
# ラベル定義
# ==========================================
label event_fallback_nothing:
    return

label scene_climax_lock:
    call screen qte_door_lock
    return

label success_enter_home:
    scene bg_home_indoor
    "間に合った！"
    jump game_clear

label scene_climax_run_police:
    scene bg_koban
    "助かった！"
    jump game_clear

label game_clear:
    hide screen game_hud
    "GAME CLEAR!!"
    return

label game_over_caught:
    hide screen game_hud
    scene black
    "GAME OVER"
    return