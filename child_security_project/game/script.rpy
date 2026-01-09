label start:
    $ current_step = 0
    $ has_encountered_suspicious = False
    $ flag_know_110 = False

    $ deck_suspicious = list(suspicious_events)
    $ deck_safe = list(safe_events)

    scene bg room
    
    "ゲームを始める前に、あなたのプロフィールを設定してください。"

    # スクリーンを呼び出す
    call screen profile_setup

    # 設定完了後
    pc "よし、これで登録完了だ。"
    pc "俺の名前は [player_name]。これからよろしく頼む。"

    return

    # 最初の背景セット（マネージャー呼び出し）
    call update_walking_background
    
    "下校時刻だ。家に帰ろう！"

    while current_step < MAX_STEPS: 
        
        $ current_step += 1

        # ★変更点1：背景管理マネージャーを呼ぶだけにする
        call update_walking_background

        "テクテク歩いて、あと [MAX_STEPS - current_step] マス..."

        call trigger_category_event
    
    "家の前まで着いた……。"
    "鍵を開けようとしたその時、背後に気配を感じた！"


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
    # ----------------------------------------------------------




label trigger_category_event:
    python:
        steps_left = MAX_STEPS - current_step
        
        # 危険か安全かの判定
        is_danger = False
        
        if steps_left <= 2 and not has_encountered_suspicious:
            is_danger = True
        else:
            if renpy.random.randint(1, 100) <= PROB_SUSPICIOUS:
                is_danger = True

        # イベント抽選と山札処理
        target_label = "event_fallback_nothing"

        if is_danger:
            if len(deck_suspicious) > 0:
                target_label = renpy.random.choice(deck_suspicious)
                deck_suspicious.remove(target_label)
                has_encountered_suspicious = True
            else:
                is_danger = False 

        if not is_danger:
            if len(deck_safe) > 0:
                target_label = renpy.random.choice(deck_safe)
                deck_safe.remove(target_label)
            else:
                target_label = "event_fallback_nothing"

    # 対応表(event_bg_map)に設定があれば背景を切り替える
    if target_label in event_bg_map:
        $ _bg_image = event_bg_map[target_label]
        scene expression _bg_image with fade

    call expression target_label

    return

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

label event_fallback_nothing:
    "特に何も起こらなかった。" 
    return