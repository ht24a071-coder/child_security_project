# ゲーム開始
label start:
    # 変数のリセット（2周目のために必要）
    $ current_step = 0
    $ has_encountered_suspicious = False
    $ flag_know_110 = False

    scene bg school_road_evening
    "下校時刻だ。家に帰ろう！"

    # マップループ
    while current_step < MAX_STEPS: 
        
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
        
        # 危険イベントか安全イベントかを判定
        # 1. 強制出現判定（残り2マス以下で未遭遇なら必ず危険）
        if steps_left <= 2 and not has_encountered_suspicious:
            is_danger = True
        # 2. それ以外なら確率で判定
        else:
            if renpy.random.randint(1, 100) <= PROB_SUSPICIOUS:
                is_danger = True
            else:
                is_danger = False

        # --- イベント抽選とリスト空チェック ---
        
        if is_danger:
            # 危険イベントリストが空でなければ抽選
            if suspicious_events: 
                target_label = renpy.random.choice(suspicious_events)
                has_encountered_suspicious = True
            else:
                # 危険イベントが空なら安全イベントにフォールバック
                if safe_events:
                    target_label = renpy.random.choice(safe_events)
                else:
                    target_label = "event_fallback_nothing"
        
        else:
            # 安全イベントリストが空でなければ抽選
            if safe_events:
                target_label = renpy.random.choice(safe_events)
            else:
                target_label = "event_fallback_nothing"

    # 抽選結果のイベントへコール
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

# 代替イベント (リストが空だった場合の安全装置)
label event_fallback_nothing:
    "特に何も起こらなかった。" 
    return