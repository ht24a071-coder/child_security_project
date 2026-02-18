# =============================================================================
# 人物遭遇イベント：安全な人（挨拶から始まる＋ミニゲーム付き）
# =============================================================================

label encounter_e_safe_person:

    "だれかが ちかづいてきた。"
    
    show woman with dissolve
    
    woman "こんにちは！"
    
    # まず挨拶への反応
    menu:
        "こんにちは！":
            $ update_score(5)
            pc "こんにちは！"
            woman "げんきな あいさつだね！"
        
        "...（むしする）":
            pc "..."
            woman "あら、はずかしがりやさんね。"
        
        "（ぼうはんブザーを にぎる）":
            pc "（ねんのため...）"
            woman "？"
    
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
        woman "まあ、げんきね！いいこだわ。バイバイ！"
    elif _return == "good":
        $ update_score(10)
        pc "さようなら！"
        "GOOD! ちゃんと あいさつできたね！"
        woman "いいこね。バイバイ！"
    else:
        $ update_score(5)
        pc "…さようなら"
        woman "バイバイ！"
    
    call hide_woman_wrapper from _call_hide_woman_wrapper
    
    "{i}よくできました！あいさつは コミュニケーションの きほんだね。{/i}"
    return

# -----------------------------------------------------------------------------
# 防犯ブザールート（お叱り）
# -----------------------------------------------------------------------------
label .buzzer_safe:
    play audio "audio/buzzer.mp3"
    
    "ピピピピピ！！"
    woman "えっ！？ ちょ、ちょっと！？"
    
    call hide_woman_wrapper from _call_hide_woman_wrapper_1
    
    call show_officer_wrapper from _call_show_officer_wrapper
    officer "どうしたの？"
    pc "あ、あの……"
    officer "ぼうはんブザーは ほんとうに あぶないときに つかうものだよ。"
    officer "ふつうの ひとには ならしちゃダメだよ。"
    
    call hide_officer_wrapper from _call_hide_officer_wrapper
    
    $ update_score(-5)
    
    "{i}ぼうはんブザーは ほんとうに あぶないときだけ つかおうね。{/i}"
    "{i}でも、あやしいと おもったら つかうゆうきも だいじだよ。{/i}"
    return

# -----------------------------------------------------------------------------
# 無視ルート
# -----------------------------------------------------------------------------
label .ignore_safe:
    pc "……"
    woman "あら、シャイな こね。きを つけてね。"
    
    call hide_woman_wrapper from _call_hide_woman_wrapper_2
    
    "{i}あいさつを かえすと、ちいきの ひとが あなたのことを おぼえてくれるよ。{/i}"
    return
