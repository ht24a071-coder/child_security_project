init 2 python:
    safe_events.append("safe_e_railway")

label safe_e_railway:
    # -----------------------------------------------------------
    # 踏切イベント
    # -----------------------------------------------------------
    
    # 背景を踏切に切り替え
    scene back_railway with dissolve

    pc "あ、踏切だ。"

    # 音を鳴らす（SEがあれば）
    # play audio "audio/se_crossing.mp3"
    "カンカンカンカン……"

    "警報機が鳴り始め、遮断機が下りてきた！"

    menu:
        "急いで走り抜ける！":
            jump .choice_dash

        "立ち止まって待つ":
            jump .choice_wait

label .choice_dash:
    # --- バッドルート（危険） ---
    pc "今ならまだ間に合うはず……！"
    
    scene back_railway with vpunch # 画面を揺らす演出
    "ガタン！！"

    pc "うわっ！？"

    "慌てて走ろうとして、足がもつれて転んでしまった！"
    "目の前を電車が轟音を立てて通過していく……。"

    pc "（は、ひかれたかと思った……。）"
    pc "（無理に通るのは危ないな……。）"

    # ペナルティとしてスコアを下げるなどしてもOK
    # $ current_score -= 10 

    jump .event_end

label .choice_wait:
    # --- グッドルート（安全） ---
    pc "危ないから待っていよう。"

    "……ガタンゴトン、ガタンゴトン……"
    
    "電車が通り過ぎるのを静かに待った。"
    "遮断機が上がった。"

    pc "よし、もう渡っても大丈夫だね。"
    
    # ご褒美（スコアアップなど）
    # $ current_score += 10

    jump .event_end

label .event_end:
    "元の道に戻ろう。"
    # 元の背景に戻す（共通処理があるなら不要ですが、念のため）
    scene back_town with dissolve
    
    return