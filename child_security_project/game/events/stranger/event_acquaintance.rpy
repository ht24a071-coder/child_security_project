# =============================================================================
# 不審者イベント：知り合い（顔見知り）の誘い
# =============================================================================

label suspi_e_acquaintance:


    call show_stranger_wrapper from _call_show_stranger_wrapper_acquaintance

    
    $ _v = get_stranger_voice("003") 
    if _v:
        voice _v
    stranger "おーい、[player_name]ちゃん！"
    stranger "学校おわりかい？ えらいねえ。"

    pc "あ、こんばんは。"
    pc "（優しそうな おじさんだ。知ってる人だし安心かな？）"

    stranger "お母さんは 元気にしてるかい？"
    pc "うん、元気だよ。"
    
    stranger "そうかそうか。実はね、あっちに 可愛い子犬がいるんだ。"
    stranger "[player_name]ちゃん、犬好きだよね？ ちょっと見ていかない？"

    pc "えっ、子犬..."
    pc "（見たいな... 知ってる人だし...）"
    
    # ここで選択肢
    menu:
        "ついていく":
            jump .follow_acquaintance
        
        "ことわる":
            jump .refuse_acquaintance
        
        "ぼうはんブザーを ならす":
            jump .buzzer_acquaintance

# -----------------------------------------------------------------------------
# ついていく（GAME OVER）
# -----------------------------------------------------------------------------
label .follow_acquaintance:
    pc "はーい！なになに？"
    
    stranger "こっちだよ...もっと おくのほう..."
    
    "おじさんは ひと気のない ほうへ あるいていく。"
    
    call hide_stranger_wrapper from _call_hide_stranger_wrapper
    scene black with fade
    
    "{i}しっている ひとでも、かってに ついていってはいけません。{/i}"
    "{i}わるいことを かんがえている 人も いるかもしれません。{/i}"
    "{i}かならず おうちのひとに きいてからに しましょう。{/i}"
    
    jump game_over

# -----------------------------------------------------------------------------
# 断る（正解）
# -----------------------------------------------------------------------------
label .refuse_acquaintance:
    $ update_score(10)
    
    pc "ごめんなさい！いま いそいでるんです！"
    
    stranger "えー、いいじゃないか。ちょっとだけだよ？"
    
    pc "（しつこいな...）"
    pc "ママに おこられるから！"
    
    "あわてて そのばを はなれた。"
    
    call hide_stranger_wrapper(dissolve) from _call_hide_stranger_wrapper_1
    
    "{i}よくできた！しっている ひとでも、ついていってはいけないよ。{/i}"
    "{i}「ちょっとだけ」といわれても、ことわって すぐに はなれよう。{/i}"
    
    return

# -----------------------------------------------------------------------------
# 防犯ブザー（大正解）
# -----------------------------------------------------------------------------
label .buzzer_acquaintance:
    play audio "audio/buzzer.mp3"
    
    $ update_score(15)
    
    "ピピピピピ！！"
    stranger "おいおい！なにをするんだ！"
    
    "おじさんは びっくりして いなくなった。"
    call hide_stranger_wrapper(dissolve) from _call_hide_stranger_wrapper_2
    
    pc "（ちょっと こわかった...）"
    
    "{i}すごい！しっている ひとでも、こわいと おもったら ブザーを ならして いいんだよ。{/i}"
    "{i}じぶんの みを まもるのが いちばん だいじだからね。{/i}"
    
    return
