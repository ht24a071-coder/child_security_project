label safe_e_railway:
    # -----------------------------------------------------------
    # 踏切イベント（SE付きバージョン）
    # -----------------------------------------------------------
    
    # 背景呼び出し（一括管理パターンなら、この行はなくてもOK）
    # scene expression event_bg_map["safe_e_railway"] with dissolve

    # ★警報音を再生（loop をつけると鳴り続けます）
    # "sound" チャンネルを使います
    play sound "audio/humikiri.mp3" loop

    pc "あ、踏切だ。"

    "カンカンカンカン……"
    "警報機が鳴り始め、遮断機が下りてきた！"

    menu:
        "急いで走り抜ける！":
            jump .choice_dash

        "立ち止まって待つ":
            jump .choice_wait

label .choice_dash:
    # --- バッドルート ---
    pc "今ならまだ間に合うはず……！"
    
    play audio "audio/se_crash.mp3" 

    scene expression event_bg_map["safe_e_railway"] with vpunch
    "ガタン！！"

    pc "うわっ！？"
    "転んでしまった！"

    # ここで警報音を止める
    stop sound fadeout 1.0

    pc "（危なかった……。）"
    jump .event_end

label .choice_wait:
    # --- グッドルート ---
    pc "危ないから待っていよう。"

    # 電車の通過音を再生（play sound は前の音(警報)を上書きして消します）
    # 警報音から電車の音に切り替わる演出
    play sound "audio/se_train_pass.mp3"

    "……ガタンゴトン、ガタンゴトン……"
    "目の前を電車が通り過ぎていった。"

    # 音が鳴り終わるのを待つ（演出として）
    pause 2.0

    # 音を止める（念のため）
    stop sound fadeout 1.0

    "遮断機が上がった。"
    pc "よし、もう渡っても大丈夫だね。"
    jump .event_end

label .event_end:
    # イベント終了時、念の為音を完全に消す
    stop sound fadeout 1.0
    
    "元の道に戻ろう。"
    scene back_town with dissolve
    return