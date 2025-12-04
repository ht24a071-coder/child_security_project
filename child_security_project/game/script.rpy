# 初期設定とリスト定義
init python:
    # 不審者が出る確率（％）
    PROB_SUSPICIOUS = 50

    # 不審者イベントのリスト
    suspicious_events = [
        "event_bad_cookie",     # お菓子
        "event_bad_car",        # 車
    ]

    # 安全イベントのリスト
    safe_events = [
        "event_safe_grandma",   # おばあちゃん
        "event_safe_dog",       # 犬
    ]

# ゲーム開始
label start:
    # 変数リセット
    $ current_step = 0
    $ max_steps = 10
    $ has_encountered_suspicious = False # 不審者に会ったかフラグ

    scene bg school_road_evening
    "下校時刻だ。家に帰ろう！"

    # マップループ開始
    while current_step < max_steps:
        
        $ current_step += 1
        "テクテク歩いて、あと [max_steps - current_step] マス..."

        # 抽選システム呼び出し
        call trigger_category_event

    # ループ終了後のクリア処理
    jump game_clear

# 抽選ロジック（強制出現機能付き）
label trigger_category_event:
    python:
        steps_left = max_steps - current_step

        # 【強制出現判定】残り2マス以下 かつ まだ不審者に会っていない場合
        if steps_left <= 2 and not has_encountered_suspicious:
            is_danger = True
            # renpy.notify("強制出現！") # デバッグ用
        
        # 通常の確率計算
        else:
            roll = renpy.random.randint(1, 100)
            if roll <= PROB_SUSPICIOUS:
                is_danger = True
            else:
                is_danger = False

        # イベント決定処理
        if is_danger:
            target_label = renpy.random.choice(suspicious_events)
            has_encountered_suspicious = True # フラグON
        else:
            target_label = renpy.random.choice(safe_events)

    # イベント実行
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