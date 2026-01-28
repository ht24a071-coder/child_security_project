# =============================================================================
# 人物遭遇イベント：不審者（挨拶から始まる＋防犯ブザー選択肢追加）
# =============================================================================

label encounter_e_stranger:
    scene back_dark with dissolve

    "だれかが ちかづいてきた。"
    
    show stranger with dissolve
    
    stranger "こんにちは～"
    
    # まず挨拶への反応
    menu:
        "こんにちは":
            pc "こんにちは..."
            stranger "いいこだね～"
        
        "...（むしする）":
            pc "..."
        
        "（ぼうはんブザーを にぎる）":
            pc "（なにかあったら すぐ ならそう...）"
    
    pause 0.3
    stranger "ねえねえ、おいしい おかしが あるんだけど、たべない？"
    stranger "こっちに おいでよ。"

    menu:
        "ついていく":
            jump .follow_stranger

        "ことわって はなれる":
            jump .refuse_stranger

        "おおごえを だす":
            jump .shout_stranger

        "にげる":
            jump .flee_stranger
        
        "ぼうはんブザーを ならす":
            jump .buzzer_stranger

# -----------------------------------------------------------------------------
# 防犯ブザールート（追加）
# -----------------------------------------------------------------------------
label .buzzer_stranger:
    play audio "audio/buzzer.mp3"
    
    "ピピピピピ！！"
    stranger "うわっ！？なんだ！？"
    
    "ふしんしゃは あわてて にげていった！"
    hide stranger with dissolve
    
    $ total_score += 20
    
    scene back_town with dissolve
    
    show woman with dissolve
    woman "どうしたの！？ おおきな おとが したけど..."
    pc "しらない ひとに こえを かけられて..."
    woman "よくできたね！ぼうはんブザーを ならすのは とてもいい はんだんだよ！"
    hide woman with dissolve
    
    "{i}すばらしい！あやしいと おもったら すぐに ぼうはんブザーを ならそう！{/i}"
    return

# -----------------------------------------------------------------------------
# ついていくルート（危険→逃げる選択肢）
# -----------------------------------------------------------------------------
label .follow_stranger:
    pc "おかし……？ いく！"
    stranger "いいこだね～ こっちこっち……"
    
    hide stranger
    scene black with fade
    
    "…しばらく あるいたあと…"
    
    scene back_tunnel with fade
    show stranger with dissolve
    
    stranger "さあ、もうすこしだよ…"
    
    "（なんだか こわくなってきた…）"
    
    menu:
        "110ばんの いえに にげる":
            if flag_know_110:
                jump .escape_110
            else:
                jump .escape_fail_no_110
        
        "いえに はしる":
            jump .escape_home
        
        "おおごえを だして にげる":
            jump .escape_shout
        
        "ぼうはんブザーを ならす":
            jump .escape_buzzer

# 防犯ブザーで逃げる（ついていった後）
label .escape_buzzer:
    play audio "audio/buzzer.mp3"
    
    "ピピピピピ！！"
    stranger "うわっ！？"
    
    hide stranger with dissolve
    scene back_town with dissolve
    
    $ total_score += 15
    
    show woman with dissolve
    woman "どうしたの！？"
    pc "しらない ひとに つれていかれそうに..."
    woman "よくできたね！でも さいしょから ついていかないように しようね。"
    hide woman with dissolve
    
    "{i}ぼうはんブザーで にげられた！でも さいしょから ついていかないのが いちばんだよ。{/i}"
    return

# 110番の家に逃げる（フラグあり→成功）
label .escape_110:
    pc "（あそこに「110ばんの いえ」があった！）"
    pc "にげろーー！"
    
    python:
        escape_game = EscapeMinigame(difficulty="normal", key="K_SPACE")
    
    call screen escape_minigame(escape_game)
    
    hide stranger
    scene back_town with dissolve
    
    if _return == "success":
        $ total_score += 30
        "「こども110ばんの いえ」に かけこんだ！"
        show officer with dissolve
        officer "どうしたの！？"
        pc "しらない ひとに つれていかれそうに……！"
        officer "だいじょうぶ、ここは あんぜんだよ。よく にげてきたね！"
        hide officer with dissolve
        "{i}すばらしい！110ばんの いえを おぼえていたから にげられたね！{/i}"
    else:
        $ total_score += 10
        "なんとか にげきった…でも こわかった…"
        "{i}あぶなかったね。さいしょから ついていかないように しよう。{/i}"
    return

# 110番の家を知らない
label .escape_fail_no_110:
    pc "（110ばんの いえって どこ…？）"
    pc "にげなきゃ！"
    
    python:
        escape_game = EscapeMinigame(difficulty="hard", key="K_SPACE")
    
    call screen escape_minigame(escape_game)
    
    hide stranger
    
    if _return == "success":
        $ total_score += 5
        scene back_town with dissolve
        "なんとか にげきった……"
        "{i}あぶなかったね。「110ばんの いえ」を おぼえておけば もっと あんぜんだよ。{/i}"
        return
    else:
        scene black with fade
        "{i}にげられなかった……{/i}"
        "{i}「こども110ばんの いえ」を みつけたら、ばしょを おぼえておこう！{/i}"
        jump game_over

# 家に走るルート（とても難しい）
label .escape_home:
    pc "いえに にげよう！"
    
    python:
        escape_game = EscapeMinigame(difficulty="hard", key="K_SPACE")
    
    call screen escape_minigame(escape_game)
    
    hide stranger
    
    if _return == "success":
        scene back_town with dissolve
        "なんとか にげきった……"
        
        "いえの まえに ついた！"
        "（いそいで かぎを あけなきゃ！）"
        
        python:
            key_game = TimingMinigame(speed=6.0, perfect_range=15, good_range=25, key="K_SPACE")
        
        call screen timing_minigame(key_game)
        
        if _return == "miss":
            "かぎが あかない…！"
            stranger "まてまて～"
            scene black with fade
            "{i}かぎを あけるのに てまどってしまった…{/i}"
            "{i}いえに にげるより、110ばんの いえや おみせに にげるほうが あんぜんだよ。{/i}"
            jump game_over
        else:
            $ total_score += 5
            "なんとか いえに にげこめた…"
            "{i}あぶなかったね。つぎからは さいしょから ついていかないようにね。{/i}"
            return
    else:
        scene black with fade
        "{i}にげられなかった……{/i}"
        "{i}さいしょから しらない ひとに ついていかないように しよう。{/i}"
        jump game_over

# 大声を出して逃げる（マイク使用）
label .escape_shout:
    pc "「たすけてーーー！！」"
    
    "（おおきな こえを だそう！）"
    
    python:
        shout_game = ShoutMinigame(threshold=0.25, duration=3.0, hold_time=0.4)
    
    call screen shout_minigame(shout_game)
    
    if _return != "miss":
        $ total_score += 15
        play audio "audio/buzzer.mp3"
        stranger "うわっ…！"
        hide stranger with dissolve
        
        scene back_town with dissolve
        show woman with dissolve
        woman "どうしたの！？ だいじょうぶ！？"
        pc "しらない ひとに……"
        woman "こわかったね。よく おおごえを だせたね！"
        hide woman with dissolve
        "{i}よくがんばった！でも さいしょから ついていかないのが いちばんだよ。{/i}"
    else:
        hide stranger
        scene black with fade
        "{i}こえが でなかった……{/i}"
        jump game_over
    return

# -----------------------------------------------------------------------------
# 断って離れるルート（正解）
# -----------------------------------------------------------------------------
label .refuse_stranger:
    $ total_score += 15
    
    pc "ごめんなさい！まっすぐ かえらないといけないんです！"
    stranger "えー、ちょっとだけだよ～"
    pc "いいえ！さようなら！"
    
    "しっかり ことわって、そのばを はなれた。"
    
    hide stranger with dissolve
    scene back_town with dissolve
    
    "{i}よくできた！しらない ひとの さそいは きっぱり ことわろう！{/i}"
    return

# -----------------------------------------------------------------------------
# 大声を出すルート（マイク使用）
# -----------------------------------------------------------------------------
label .shout_stranger:
    pc "「たすけてーー！！」"
    
    "（ほんとうに おおきな こえを だしてみよう！）"
    
    python:
        shout_game = ShoutMinigame(threshold=0.3, duration=3.5, hold_time=0.5)
    
    call screen shout_minigame(shout_game)
    
    if _return == "perfect":
        $ total_score += 25
        play audio "audio/buzzer.mp3"
        "「たすけてーーー！！！」"
        "PERFECT!! ものすごく おおきな こえが でた！"
    elif _return == "good":
        $ total_score += 20
        play audio "audio/buzzer.mp3"
        "GOOD! おおきな こえが でた！"
    else:
        $ total_score += 10
        "こえは ちいさかったけど、がんばった！"
    
    stranger "うわっ！ ちょ、ちょっと……！"
    hide stranger with dissolve
    
    "ふしんしゃは にげていった！"
    
    scene back_town with dissolve
    
    show woman with dissolve
    woman "どうしたの！？ だいじょうぶ！？"
    pc "しらない ひとに こえを かけられて……"
    woman "こわかったね。よく おおごえを だせたね！"
    hide woman with dissolve
    
    "{i}すばらしい！おおごえを だすと まわりの ひとが たすけに きてくれるよ！{/i}"
    return

# -----------------------------------------------------------------------------
# 逃げるルート（フラグ判定）
# -----------------------------------------------------------------------------
label .flee_stranger:
    if flag_know_110:
        jump .flee_success
    else:
        jump .flee_fail

# 110番の家を覚えている → 成功
label .flee_success:
    pc "（あそこに「110ばんの いえ」があった！）"
    pc "にげろーー！"
    
    python:
        flee_game = EscapeMinigame(difficulty="normal", key="K_SPACE")
    
    call screen escape_minigame(flee_game)
    
    hide stranger
    scene back_town with dissolve
    
    if _return == "success":
        $ total_score += 35
        "PERFECT!! 「こども110ばんの いえ」に かけこんだ！"
    else:
        $ total_score += 20
        "なんとか にげられた！"
    
    show officer with dissolve
    officer "どうしたの！？"
    pc "しらない ひとに おいかけられて……！"
    officer "だいじょうぶ、ここは あんぜんだよ。よく にげてきたね！"
    hide officer with dissolve
    
    "{i}すばらしい！110ばんの いえを おぼえていたから にげられたね！{/i}"
    return

# 110番の家を覚えていない → 失敗
label .flee_fail:
    pc "にげなきゃ！"
    "はしりだしたけど……"
    pc "（どこに にげればいいの……！？）"
    
    stranger "まてまて～"
    
    hide stranger
    scene black with fade
    
    "{i}にげばしょが わからなかった……{/i}"
    "{i}「こども110ばんの いえ」を みつけたら、ばしょを おぼえておこう！{/i}"
    
    jump game_over
