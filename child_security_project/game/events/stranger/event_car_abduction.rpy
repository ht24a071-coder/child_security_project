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
    
    # かならず強引な手段に出る
    jump .forceful_attempt

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

# 大声を出す
label .forceful_shout:
    pc "「たすけてーーー！！」"
    
    "（ほんとうに おおきな こえを だそう！）"
    
    # UI一時非表示
    hide screen minimap
    hide screen score_hud

    python:
        shout_game = ShoutMinigame(threshold=0.35, duration=8.0)
    
    call screen shout_minigame(shout_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    
    if _return != "miss":
        $ update_score(20)
        play audio "audio/buzzer.mp3"
        stranger "ちっ...！"
        "ふしんしゃは くるまに のって にげていった！"
        hide stranger with dissolve
        
        # 助けに来る人をランダム決定
        $ is_officer = renpy.random.choice([True, False])
        
        if is_officer:
             show officer with dissolve
             officer "どうしたの！？ だいじょうぶ！？"
             pc "くるまに のせられそうに...！"
             officer "こわかったね！よく おおごえを だせたね！"
             officer "すぐ パトロールに いってくるよ。"
             hide officer with dissolve
        else:
             show teacher with dissolve
             teacher "どうしたの！？ だいじょうぶ！？"
             pc "くるまに のせられそうに...！"
             teacher "こわかったわね！よく おおごえを だせたわね！"
             teacher "先生から おまわりさんに れんらくしておくわね。"
             hide teacher with dissolve
        
        "{i}すばらしい！おおごえを だして たすけを よべたね！{/i}"
        return
    else:
        # 失敗 -> ブザーチャンス
        call fallback_buzzer_sequence
        if _return == "success":
            $ update_score(15)
            jump .car_repelled_buzzer
        else:
            jump .car_gameover

# 逃げる
label .forceful_run:
    pc "（にげなきゃ！）"
    
    # UI一時非表示
    hide screen minimap
    hide screen score_hud

    python:
        escape_game = EscapeMinigame(difficulty="hard", key="dismiss")
    
    call screen escape_minigame(escape_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud

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
        # 失敗 -> ブザーチャンス
        call fallback_buzzer_sequence
        if _return == "success":
            $ update_score(15)
            jump .car_repelled_buzzer
        else:
            jump .car_gameover

label .car_repelled_buzzer:
    "ふしんしゃは ブザーの おとに おどろいて にげていった！"
    hide stranger with dissolve
    
    # 助けに来る人をランダム決定
    $ is_officer = renpy.random.choice([True, False])
    
    if is_officer:
         show officer with dissolve
         officer "どうしたの！？ だいじょうぶ！？"
         pc "くるまに のせられそうに...！"
         officer "こわかったね！よく ブザーを ならせたね！"
         hide officer with dissolve
    else:
         show teacher with dissolve
         teacher "どうしたの！？ だいじょうぶ！？"
         pc "くるまに のせられそうに...！"
         teacher "こわかったわね！よく ブザーを ならせたわね！"
         hide teacher with dissolve

    return

label .car_gameover:
    stranger "つかまえた！"
    hide stranger
    scene black with fade
    "{i}ふしんしゃに つれさられてしまった...{/i}"
    jump game_over



# -----------------------------------------------------------------------------
# 逃げるルート
# -----------------------------------------------------------------------------
label .run_away_car:
    pc "（にげよう！）"
    
    $ update_score(15)
    
    # UI一時非表示
    hide screen minimap
    hide screen score_hud

    python:
        escape_game = EscapeMinigame(difficulty="normal", key="dismiss")
    
    call screen escape_minigame(escape_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    
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