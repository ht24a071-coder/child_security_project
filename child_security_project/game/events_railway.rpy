init 2 python:
    # safe_eventsリストに追加
    safe_events.append("safe_e_railway")

label safe_e_railway:
    # 背景指定（マップの自動切り替えを使わない場合はここで指定）
    scene back_railway with dissolve
    play sound "audio/humikiri.mp3" loop

    # pc "あ、{rb}踏切{/rb}{rt}ふみきり{/rt}だ。"
    pc "あ、{rb}踏切{/rb}{rt}ふみきり{/rt}だ。"

    "カンカンカンカン……"
    
    # 警報機、遮断機は難しい言葉なのでルビ必須です
    "{rb}警報機{/rb}{rt}けいほうき{/rt}が{rb}鳴{/rb}{rt}な{/rt}り{rb}始{/rb}{rt}はじ{/rt}め、{rb}遮断機{/rb}{rt}しゃだんき{/rt}が{rb}下{/rb}{rt}お{/rt}りてきた！"

    menu:
        # 選択肢にもルビが使えます
        "{rb}急{/rb}{rt}いそ{/rt}いで{rb}走{/rb}{rt}はし{/rt}り{rb}抜{/rb}{rt}ぬ{/rt}ける！":
            jump .choice_dash

        "{rb}立{/rb}{rt}た{/rt}ち{rb}止{/rb}{rt}ど{/rt}まって{rb}待{/rb}{rt}ま{/rt}つ":
            jump .choice_wait

label .choice_dash:
    # --- バッドルート ---
    pc "{rb}今{/rb}{rt}いま{/rt}ならまだ{rb}間{/rb}{rt}ま{/rt}に{rb}合{/rb}{rt}あ{/rt}うはず……！"
    
    play audio "audio/crash.mp3" 

    "ガタン！！"

    pc "うわっ！？"
    "{rb}転{/rb}{rt}ころ{/rt}んでしまった！"

    # ここで警報音を止める
    stop sound fadeout 1.0

    pc "（{rb}危{/rb}{rt}あぶ{/rt}なかった……。）"
    jump .event_end

label .choice_wait:
    # --- グッドルート ---
    pc "{rb}危{/rb}{rt}あぶ{/rt}ないから{rb}待{/rb}{rt}ま{/rt}っていよう。"

    play sound "audio/train.mp3"

    "……ガタンゴトン、ガタンゴトン……"
    "{rb}目{/rb}{rt}め{/rt}の{rb}前{/rb}{rt}まえ{/rt}を{rb}電車{/rb}{rt}でんしゃ{/rt}が{rb}通{/rb}{rt}とお{/rt}り{rb}過{/rb}{rt}す{/rt}ぎていった。"

    # 音が鳴り終わるのを待つ
    pause 2.0

    stop sound fadeout 1.0

    "{rb}遮断機{/rb}{rt}しゃだんき{/rt}が{rb}上{/rb}{rt}あ{/rt}がった。"
    pc "よし、もう{rb}渡{/rb}{rt}わた{/rt}っても{rb}大丈夫{/rb}{rt}だいじょうぶ{/rt}だね。"
    jump .event_end

label .event_end:
    stop sound fadeout 1.0
    
    "{rb}元{/rb}{rt}もと{/rt}の{rb}道{/rb}{rt}みち{/rt}に{rb}戻{/rb}{rt}もど{/rt}ろう。"
    scene back_town with dissolve
    return