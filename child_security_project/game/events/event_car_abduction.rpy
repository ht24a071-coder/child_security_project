# =============================================================================
# 不審者イベント：車に乗せようとする（断っても強引なパターンあり）
# =============================================================================

label suspi_e_car:

    $ setup_stranger()
    "くるまが ゆっくり ちかづいてきた。"
    
    "まどが あいて、なかから ひとが こえを かけてきた。"
    
    show stranger with dissolve
    
    $ _v = get_stranger_voice("001")
    if _v:
        voice _v
    stranger "ねえ、きみ、がっこうの かえり？"
    
    # まず挨拶への反応
    menu:
        "はい、そうです":
            pc "はい..."
            stranger "そうか、そうか。"
        
        "...（むしする）":
            pc "..."
            stranger "ねえ、きいてる？"
        
        "（ぼうはんブザーを にぎる）":
            pc "（いつでも ならせるように...）"

    $ _v = get_stranger_voice("002")
    if _v:
        voice _v
    stranger "おうちまで おくってあげようか？"
    stranger "くるまの ほうが はやいよ？"

    menu:
        "のります！":
            jump .get_in_car

        "だいじょうぶです、じぶんで かえれます":
            jump .refuse_car
        
        "（にげる）":
            jump .run_away_car
        
        "ぼうはんブザーを ならす":
            jump .buzzer_car

# -----------------------------------------------------------------------------
# 乗ってしまうルート（GAME OVER）
# -----------------------------------------------------------------------------
label .get_in_car:
    pc "ありがとうございます..."
    stranger "よしよし、こっちだよ..."
    
    hide stranger
    scene black with fade
    
    "{i}しらない ひとの くるまに のってはいけません！{/i}"
    "{i}「いかのおすし」の「の」＝のらない！{/i}"
    
    jump game_over

# -----------------------------------------------------------------------------
# 断るルート（強引に乗せようとしてくる場合あり）
# -----------------------------------------------------------------------------
label .refuse_car:
    $ update_score(10)
    
    pc "だいじょうぶです。じぶんで かえれますから。"
    
    # ランダムで強引パターンか諦めパターンか
    $ forceful = renpy.random.randint(1, 100) <= 40  # 40%の確率で強引
    
    if forceful:
        jump .forceful_attempt
    else:
        stranger "そう...じゃあね..."
        "くるまは さっていった。"
        hide stranger with dissolve
        
        "{i}よくできた！しらない ひとの くるまには のらないでね。{/i}"
        return

# -----------------------------------------------------------------------------
# 強引に乗せようとしてくるパターン
# -----------------------------------------------------------------------------
label .forceful_attempt:
    stranger "えー、いいから いいから！"
    stranger "ちょっとだけだから！"
    
    "ふしんしゃが くるまから おりてきた！"
    
    pc "（やばい…！）"
    
    menu:
        "おおごえを だす":
            jump .forceful_shout
        
        "にげる":
            jump .forceful_run
        
        "ぼうはんブザーを ならす":
            jump .forceful_buzzer
        
        "たたかう":
            jump .forceful_fight

# 大声を出す
label .forceful_shout:
    pc "「たすけてーーー！！」"
    
    "（ほんとうに おおきな こえを だそう！）"
    
    python:
        shout_game = ShoutMinigame(threshold=0.35, duration=3.0, hold_time=0.3)
    
    call screen shout_minigame(shout_game)
    
    if _return != "miss":
        $ update_score(20)
        play audio "audio/buzzer.mp3"
        stranger "ちっ...！"
        "ふしんしゃは くるまに のって にげていった！"
        hide stranger with dissolve
        
        show woman with dissolve
        woman "どうしたの！？ だいじょうぶ！？"
        pc "くるまに のせられそうに...！"
        woman "こわかったね！よく おおごえを だせたね！"
        woman "おまわりさんに れんらくするね。"
        hide woman with dissolve
        
        "{i}すばらしい！おおごえを だして たすけを よべたね！{/i}"
        return
    else:
        stranger "しずかにしろ！"
        hide stranger
        scene black with fade
        "{i}こえが でなかった...{/i}"
        jump game_over

# 逃げる
label .forceful_run:
    pc "（にげなきゃ！）"
    
    python:
        escape_game = EscapeMinigame(difficulty="hard", key="dismiss")
    
    call screen escape_minigame(escape_game)
    
    if _return == "success":
        $ update_score(25)
        hide stranger
        
        "なんとか にげきった！"
        
        if flag_know_110:
            "110ばんの いえに かけこんだ！"
            show officer with dissolve
            officer "どうしたの！？"
            pc "くるまに のせられそうに...！"
            officer "だいじょうぶ、すぐ パトロールする！"
            hide officer with dissolve
            $ update_score(10)
        
        "{i}よく にげられたね！あやしい くるまには ちかづかないようにしよう。{/i}"
        return
    else:
        stranger "つかまえた！"
        hide stranger
        scene black with fade
        "{i}にげられなかった...{/i}"
        jump game_over

# 防犯ブザー
label .forceful_buzzer:
    play audio "audio/buzzer.mp3"
    
    $ update_score(25)
    
    "ピピピピピ！！"
    stranger "うわっ！？"
    
    "ふしんしゃは あわてて くるまに のって にげていった！"
    hide stranger with dissolve
    
    show woman with dissolve
    woman "どうしたの！？ おおきな おとが！"
    pc "くるまに のせられそうに...！"
    woman "よくできたね！ぼうはんブザーを ならしたのは せいかいだよ！"
    woman "おまわりさんに れんらくするね。"
    hide woman with dissolve
    
    "{i}すばらしい！ぼうはんブザーで たすかったね！{/i}"
    return

# たたかう（おすすめしない）
label .forceful_fight:
    pc "やめてください！"
    
    "たたかおうとしたけど..."
    
    stranger "おとなしくしろ！"
    hide stranger
    scene black with fade
    
    "{i}おとなに たたかっても かてないよ...{/i}"
    "{i}にげるか おおごえを だすか ぼうはんブザーを ならそう！{/i}"
    
    jump game_over

# -----------------------------------------------------------------------------
# 逃げるルート
# -----------------------------------------------------------------------------
label .run_away_car:
    pc "（にげよう！）"
    
    $ update_score(15)
    
    python:
        escape_game = EscapeMinigame(difficulty="normal", key="dismiss")
    
    call screen escape_minigame(escape_game)
    
    hide stranger
    
    if _return == "success":
        $ update_score(10)
        "うまく にげられた！"
    else:
        "なんとか にげられた..."
    
    "{i}よくできた！あやしい くるまには ちかづかず、すぐ にげよう！{/i}"
    return

# -----------------------------------------------------------------------------
# 防犯ブザールート
# -----------------------------------------------------------------------------
label .buzzer_car:
    play audio "audio/buzzer.mp3"
    
    $ update_score(20)
    
    "ピピピピピ！！"
    stranger "な、なんだ！？"
    
    "くるまは あわてて はしりさった！"
    hide stranger with dissolve
        
    show woman with dissolve
    woman "どうしたの！？"
    pc "くるまの ひとに こえを かけられて..."
    woman "よくできたね！あやしいと おもったら すぐ ブザーだね！"
    hide woman with dissolve
    
    "{i}すばらしい！あやしいと おもったら すぐに ぼうはんブザーを ならそう！{/i}"
    return
