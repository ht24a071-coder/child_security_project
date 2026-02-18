# =============================================================================
# 人物遭遇イベント：不審者（挨拶から始まる＋防犯ブザー選択肢追加）
# =============================================================================

label encounter_e_stranger:
    "だれかが ちかづいてきた。"
    
    $ setup_stranger()
    show stranger with dissolve
    
    $ _v = get_stranger_voice("003")
    if _v:
        voice _v
    stranger "こんにちは～"
    
    # まず挨拶への反応
    menu:
        "こんにちは":
            pc "こんにちは..."
            stranger "いいこだね～"
        
        "...（むしする）":
            pc "..."
    
    pause 0.3
    stranger "ねえねえ、おいしい おかしが あるんだけど、たべない？"
    stranger "こっちに おいでよ。"

    pc "いりません！"
    
    # 強制イベント化
    stranger "いいから おいでよ！"
    "ふしんしゃは うでを つかもうとしてきた！"
    
    # -------------------------------------------------------------------------
    # 第1段階: 「おおごえ」のみ
    # -------------------------------------------------------------------------
    pc "（つかまる！ おおごえを ださなきゃ！）"
    
    # UI一時非表示
    hide screen minimap
    hide screen score_hud
    
    # 強制的に大声ミニゲーム
    python:
        shout_game = ShoutMinigame(threshold=0.3, duration=5.0)
    
    call screen shout_minigame(shout_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    
    if _return != "miss":
        jump .stranger_repelled
    else:
        # 失敗 -> 第2段階へ
        jump .stage2_choice

# -----------------------------------------------------------------------------
# 第2段階: 「おおごえ」or「にげる」
# -----------------------------------------------------------------------------
label .stage2_choice:
    stranger "うるさい ガキだな！"
    "ふしんしゃは まだ てを はなさない！"
    
    pc "（まだ つかまってる...！）"
    
    menu:
        "おおごえを だす":
            jump .stage2_shout
            
        "にげる":
            jump .stage2_run

label .stage2_shout:
    # UI一時非表示
    hide screen minimap
    hide screen score_hud

    python:
        # 少し難易度アップ？現状は同じ設定
        shout_game = ShoutMinigame(threshold=0.3, duration=5.0)
    
    call screen shout_minigame(shout_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud

    if _return != "miss":
        jump .stranger_repelled
    else:
        jump .stage3_choice

label .stage2_run:
    # UI一時非表示
    hide screen minimap
    hide screen score_hud

    python:
        escape_game = EscapeMinigame(difficulty="normal", key="dismiss")
    
    call screen escape_minigame(escape_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud

    if _return == "success":
        jump .stranger_escaped
    else:
        jump .stage3_choice

# -----------------------------------------------------------------------------
# 第3段階: 「おおごえ」or「にげる」or「防犯ブザー」
# -----------------------------------------------------------------------------
label .stage3_choice:
    stranger "いいかげんに しろ！"
    "ふしんしゃが つよく うでを 引っ張った！"
    
    pc "（もう だめかも... でも ぼうはんブザーが ある！）"
    
    menu:
        "おおごえを だす":
            jump .stage3_shout
            
        "にげる":
            jump .stage3_run
            
        "ぼうはんブザー":
            jump .stage3_buzzer

label .stage3_shout:
    # UI一時非表示
    hide screen minimap
    hide screen score_hud

    python:
        shout_game = ShoutMinigame(threshold=0.3, duration=5.0)
    call screen shout_minigame(shout_game)

    show screen minimap
    show screen score_hud

    if _return != "miss":
        jump .stranger_repelled
    else:
        jump .stranger_gameover

label .stage3_run:
    # UI一時非表示
    hide screen minimap
    hide screen score_hud

    python:
        escape_game = EscapeMinigame(difficulty="normal", key="dismiss")
    call screen escape_minigame(escape_game)
    
    show screen minimap
    show screen score_hud

    if _return == "success":
        jump .stranger_escaped
    else:
        jump .stranger_gameover

label .stage3_buzzer:
    # UI一時非表示
    hide screen minimap
    hide screen score_hud

    # 既存の fallback_buzzer_sequence の中身を少し改変して利用するか、
    # 単に演出としてブザーチャンスを呼ぶ
    call screen buzzer_chance_screen
    $ result = _return
    
    show screen minimap
    show screen score_hud
    
    if result == "success":
        jump .stranger_repelled_buzzer
    else:
        jump .stranger_gameover

# -----------------------------------------------------------------------------
# 共通結末
# -----------------------------------------------------------------------------
label .stranger_repelled:
    $ update_score(20)
    play audio "audio/buzzer.mp3"
    stranger "ちっ...！"
    "ふしんしゃは おおごえに おどろいて にげていった！"
    hide stranger with dissolve
    jump .stranger_safe_end

label .stranger_repelled_buzzer:
    # ブザーで撃退した場合
    $ update_score(20)
    play audio "audio/buzzer.mp3"
    scene flash_white
    "ピピピピピ！！"
    "おおきな おとが なった！"
    
    stranger "うわっ、なんだ！！"
    "ふしんしゃは ひるんで にげていった！"
    
    hide stranger with dissolve
    jump .stranger_safe_end

label .stranger_escaped:
    $ update_score(20)
    hide stranger
    "なんとか にげきった！"
    jump .stranger_safe_end

label .stranger_safe_end:
    # 助けに来る人をランダム決定（警察官か先生）
    $ is_officer = renpy.random.choice([True, False])
    
    if is_officer:
        show officer with dissolve
        officer "どうしたの！？ だいじょうぶ！？"
        pc "しらない ひとに つれていかれそうに..."
        officer "こわかったね！よく がんばったね！"
        officer "すぐ パトロールに いってくるよ。"
        hide officer with dissolve
    else:
        show teacher with dissolve
        teacher "どうしたの！？ だいじょうぶ！？"
        pc "しらない ひとに つれていかれそうに..."
        teacher "こわかったわね！よく がんばったわね！"
        teacher "先生から おまわりさんに れんらくしておくわね。"
        hide teacher with dissolve
    
    "{i}よくできた！しらない ひとには ぜったいに ついていかないように しよう。{/i}"
    return

label .stranger_gameover:
    stranger "つかまえた！"
    hide stranger
    scene black with fade
    "{i}ふしんしゃに つれさられてしまった...{/i}"
    jump game_over
    




