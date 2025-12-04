# ゲーム開始
label start:
    # 変数のリセット（2周目のために必要）
    $ current_step = 0
    $ has_encountered_suspicious = False
    $ flag_know_110 = False

    scene bg school_road_evening
    "下校時刻だ。家に帰ろう！"

    # マップループ
    while current_step < MAX_STEPS: # defineした定数はそのまま使える
        
        $ current_step += 1
        "テクテク歩いて、あと [MAX_STEPS - current_step] マス..."

        # 抽選システム呼び出し
        call trigger_category_event

    # クリア
    jump game_clear

# 抽選ロジック
label trigger_category_event:
    python:
        steps_left = MAX_STEPS - current_step

        # 強制出現判定
        if steps_left <= 2 and not has_encountered_suspicious:
            is_danger = True
        else:
            if renpy.random.randint(1, 100) <= PROB_SUSPICIOUS:
                is_danger = True
            else:
                is_danger = False

        # イベント決定
        if is_danger:
            target_label = renpy.random.choice(suspicious_events)
            has_encountered_suspicious = True
        else:
            target_label = renpy.random.choice(safe_events)

    call expression target_label
    return

# エンディング類
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