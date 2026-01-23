label start:
    # --- 変数の初期化 ---
    $ current_node = "start_point"
    $ previous_node = None
    
    # 時間制限のスクリーンの表示
    show screen inactivity_guard
    $ current_step = 0
    $ used_events = set() # 一度起きたイベントを記録

    scene black

    # プロフ設定-----------------------
    "ゲームを始める前に、あなたのプロフィールを設定してください。"

    # スクリーンを呼び出す

    call screen profile_setup
    # -------------------------------

    
    # メイン移動ループへ
    jump travel_loop

label travel_loop:
    # 1. 現在地のデータを取得
    $ node_data = world_map.get(current_node)
    $ current_bg = node_data["bg"]
    
    # 2. 背景の更新
    scene expression current_bg with fade
    
    # 3. ゴール判定（家の前に着いたらループ終了）
    if current_node == "home_front":
        jump arrival_home

    # 4. 歩数カウントとイベント抽選
    $ current_step += 1
    call trigger_node_event(node_data)

    # 5. 移動選択肢の生成
    python:
        # 選択肢のリストを作成
        menu_items = []
        
        # マップデータにあるリンクを順に追加
        for label_text, target_id in node_data["links"].items():
            menu_items.append((label_text, target_id))
        
        # 「戻る」選択肢を自動追加（前の地点がある場合）
        if previous_node:
            menu_items.append(("一つ前の場所に戻る", previous_node))
            
        # Ren'Pyのメニューを呼び出し
        next_location = renpy.display_menu(menu_items)

    # 6. 移動処理
    $ previous_node = current_node
    $ current_node = next_location
    jump travel_loop

# --- イベント抽選サブロジック ---
label trigger_node_event(data):
    python:
        group_name = data["group"]
        chance = data["chance"]
        target_event = None

        # 確率判定とグループの存在確認
        if renpy.random.randint(1, 100) <= chance and group_name in event_pools:
            # まだ使っていないイベントだけを抽出
            available = [e for e in event_pools[group_name] if e not in used_events]
            
            if available:
                target_event = renpy.random.choice(available)
                used_events.add(target_event) # 使用済みリストに追加

    # イベントが当選していれば呼び出し
    if target_event:
        call expression target_event
    return

label arrival_home:
    "ようやく家の前に着いた……。"
    # ミニゲーム-----------------------------------------------
    python:
        # 難易度設定: 速度4.0、判定は少し厳しめに設定してみる
        # speed: バーの速さ
        # perfect_range: 黄色の幅（ピクセル）
        # good_range: 緑の幅（ピクセル）
        lock_game = TimingMinigame(speed=4.0, perfect_range=25, good_range=60, key="K_SPACE")

    "（タイミングよくスペースキーを押せ！）"

    # スクリーンを呼び出し（結果は _return に入ります）
    call screen timing_minigame(lock_game)

    if (_return == "miss"):
        jump game_over
    else:
        jump game_clear

    # ---------------------------------------------------


label game_clear:

    "「ただいまー！」"

    "無事に家に到着した。"

    "GAME CLEAR!!"

    return



label game_over:

    scene bg black

    "連れ去られてしまった..."

    "GAME OVER..."

    return