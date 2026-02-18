# =============================================================================
# 人物遭遇イベント：安全な人（挨拶から始まる＋ミニゲーム付き）
# =============================================================================

label encounter_e_safe_person:

    python:
        h_tag, _unused = get_helper_data()
        _safe_is_teacher = (h_tag == "teacher")
    
    "だれかが ちかづいてきた。"
    
    if _safe_is_teacher:
        show teacher with dissolve
        teacher "こんにちは！"
    else:
        show woman with dissolve
        woman "こんにちは！"
    
    # まず挨拶への反応
    menu:
        "こんにちは！":
            $ update_score(5)
            pc "こんにちは！"
            if _safe_is_teacher:
                teacher "げんきな あいさつだね！"
            else:
                woman "げんきな あいさつだね！"
        
        "...（むしする）":
            pc "..."
            if _safe_is_teacher:
                teacher "あら、はずかしがりやさんね。"
            else:
                woman "あら、はずかしがりやさんね。"
        
        "（ぼうはんブザーを にぎる）":
            pc "（ねんのため...）"
            if _safe_is_teacher:
                teacher "？"
            else:
                woman "？"
    
    if _safe_is_teacher:
        teacher "がっこうの かえり？きを つけてね。"
    else:
        woman "がっこうの かえり？きを つけてね。"
    
    "（そう いって、その ひとは さっていこうとした。）"

    menu:
        "あいさつして みおくる":
            jump .greet_back

        "ぼうはんブザーを ならす":
            jump .buzzer_safe

        "（むしする）":
            jump .ignore_safe

# -----------------------------------------------------------------------------
# 挨拶を返すルート（正解＋ミニゲーム）
# -----------------------------------------------------------------------------
label .greet_back:
    # ミニゲーム：元気よく挨拶
    "（ボタンで タイミングよく あいさつしよう！）"
    
    python:
        greet_game = TimingMinigame(speed=3.0, perfect_range=50, good_range=80, key="K_SPACE")
    
    call screen timing_minigame(greet_game)
    
    if _return == "perfect":
        $ update_score(15)
        pc "さようなら！きを つけます！"
        "PERFECT!! とても げんきな あいさつだ！"
        if _safe_is_teacher:
            teacher "まあ、げんきね！いいこだわ。バイバイ！"
        else:
            woman "まあ、げんきね！いいこだわ。バイバイ！"
    elif _return == "good":
        $ update_score(10)
        pc "さようなら！"
        "GOOD! ちゃんと あいさつできたね！"
        if _safe_is_teacher:
            teacher "いいこね。バイバイ！"
        else:
            woman "いいこね。バイバイ！"
    else:
        $ update_score(5)
        pc "…さようなら"
        if _safe_is_teacher:
            teacher "バイバイ！"
        else:
            woman "バイバイ！"
    
    if _safe_is_teacher:
        hide teacher with dissolve
    else:
        hide woman with dissolve
    
    "{i}よくできました！あいさつは コミュニケーションの きほんだね。{/i}"
    return

# -----------------------------------------------------------------------------
# 防犯ブザールート（お叱り）
# -----------------------------------------------------------------------------
label .buzzer_safe:
    play audio "audio/buzzer.mp3"
    
    "ピピピピピ！！"
    
    if _safe_is_teacher:
        teacher "えっ！？ ちょ、ちょっと！？"
        hide teacher with dissolve
    else:
        woman "えっ！？ ちょ、ちょっと！？"
        hide woman with dissolve

    if _safe_is_teacher:
        show teacher with dissolve
        teacher "どうしたの？"
        pc "あ、あの……"
        teacher "ぼうはんブザーは ほんとうに あぶないときに つかうものだよ。"
        teacher "ふつうの ひとには ならしちゃダメだよ。"
        hide teacher with dissolve
    else:
        show officer with dissolve
        officer "どうしたの？"
        pc "あ、あの……"
        officer "ぼうはんブザーは ほんとうに あぶないときに つかうものだよ。"
        officer "ふつうの ひとには ならしちゃダメだよ。"
        hide officer with dissolve
    
    $ update_score(-5)
    
    "{i}ぼうはんブザーは ほんとうに あぶないときだけ つかおうね。{/i}"
    "{i}でも、あやしいと おもったら つかうゆうきも だいじだよ。{/i}"
    return

# -----------------------------------------------------------------------------
# 無視ルート
# -----------------------------------------------------------------------------
label .ignore_safe:
    pc "……"
    if _safe_is_teacher:
        teacher "あら、シャイな こね。きを つけてね。"
        hide teacher with dissolve
    else:
        woman "あら、シャイな こね。きを つけてね。"
        hide woman with dissolve
    
    "{i}あいさつを かえすと、ちいきの ひとが あなたのことを おぼえてくれるよ。{/i}"
    return
