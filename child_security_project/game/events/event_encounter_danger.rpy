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
    
    pc "（つかまる！）"

    menu:
        "おおごえを だす":
            jump .shout_stranger

        "にげる":
            jump .flee_stranger

# -----------------------------------------------------------------------------
# 大声を出すルート
# -----------------------------------------------------------------------------
label .shout_stranger:
    pc "「たすけてーーー！！」"
    
    python:
        shout_game = ShoutMinigame(threshold=0.3, duration=5.0)
    
    call screen shout_minigame(shout_game)
    
    if _return != "miss":
        # 成功
        jump .stranger_repelled
    else:
        # 失敗 -> ブザーチャンス
        call fallback_buzzer_sequence
        if _return == "success":
            $ update_score(10)
            jump .stranger_repelled_buzzer
        else:
            jump .stranger_gameover

# -----------------------------------------------------------------------------
# 逃げるルート
# -----------------------------------------------------------------------------
label .flee_stranger:
    pc "（にげなきゃ！）"
    
    python:
        # 連打ゲーム (または逃走ゲーム)
        escape_game = EscapeMinigame(difficulty="normal", key="dismiss")
    
    call screen escape_minigame(escape_game)
    
    if _return == "success":
        # 成功
        jump .stranger_escaped
    else:
        # 失敗 -> ブザーチャンス
        call fallback_buzzer_sequence
        if _return == "success":
            $ update_score(10)
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
    




