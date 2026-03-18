# =============================================================================
# ふしんしゃイベント：くるまに乗せようとする（断っても強引なパターンあり）
# =============================================================================

label suspi_e_car:
    $ setup_stranger("suspi_e_car")
    play music "audio/Pinch!!.mp3" fadein 1.0  # ここで流す
    "くるまが ゆっくり ちかづいてきた。"
    
    "まどが あいて、なかから ひとが こえを かけてきた。"
    
    show stranger with dissolve
    
    # 特徴を表示
    $ current_trait = next((e['trait'] for e in encountered_events if e['event_name'] == 'suspi_e_car'), "")
    if current_trait:
        "（{color=#ff0000}[current_trait]{/color} ひとのようだ。）"
    
    if game_mode == "going_home":
        $ play_voice("kaeri")
        stranger "ねえ、きみ、がっこうの かえり？"
    else:
        $ play_voice("hello")
        stranger "ねえ、きみ、がっこうに いくの？"
    
    # まず挨拶への反応
    menu:
        "はい、なんですか？":
            $ play_se("decide")
            pc "はい、なんですか？"
            stranger "そうか、そうか。"
        
        "...（むしする）":
            pc "..."
            stranger "ねえ、きいてる？"

    $ play_voice("okuru")
    $ s_text = get_commute_text("おうちまで おくってあげようか？", "がっこうまで おくってあげようか？")
    stranger "{color=#ff0000}[s_text]{/color}"
    $ player_destination = get_commute_text("かえれ", "いけ")
    stranger "くるまの ほうが はやいよ？"

    menu:
        "のります！":
            jump .get_in_car

        "だいじょうぶです、[player_destination]れます":
            jump .refuse_car
        
        "（にげる）":
            $ play_se("decide")
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
    
    call show_feedback("got_in_car") from _call_fb_car_1
    
    jump game_over

# -----------------------------------------------------------------------------
# 断るルート（強引に乗せようとしてくる場合あり）
# -----------------------------------------------------------------------------
label .refuse_car:
    $ player_destination = get_commute_text("かえれ", "いけ")
    pc "だいじょうぶです。じぶんで [player_destination]ますから。"
    
    # かならずごういんなてだんにでる
    jump .forceful_attempt

# -----------------------------------------------------------------------------
# 強引に乗せようとしてくるパターン
# -----------------------------------------------------------------------------
label .forceful_attempt:
    stranger "いいから のりなよ！"
    stranger "ちょっとだけだから！"
    
    "ふしんしゃが くるまから おりてきた！"
    
    pc "（やばい…！）"
    
    menu:
        "おおごえを だす":
            jump .forceful_shout
        
        "にげる":
            jump .forceful_run

# おおごえを出す
label .forceful_shout:
    pc "「たすけてーーー！！」"
    
    "（ほんとうに おおきな こえを だそう！）"
    
    # UI一じ非表示
    hide screen minimap
    hide screen score_hud

    python:
        shout_game = ShoutMinigame(threshold=0.35, duration=8.0)
    
    call screen shout_minigame(shout_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    
    if _return != "miss":
        $ update_score(25, "おおごえで げきたい")
        $ play_se("buzzer")
        stranger "ちっ...！"
        "ふしんしゃは くるまに のって にげていった！"
        hide stranger with dissolve
        
        # 助けに来るひとをランダムけってい
        $ is_officer = renpy.random.choice([True, False])
        
        if is_officer:
            hide stranger
            show officer with dissolve
            officer "どうしたの！？ だいじょうぶ！？"
            pc "くるまに のせられそうに...！"
            officer "こわかったね！よく おおごえを だせたね！"
            officer "すぐ パトロールに いってくるよ。"
            hide officer with dissolve
        else:
            hide stranger
            show teacher with dissolve
            teacher "どうしたの！？ だいじょうぶ！？"
            pc "くるまに のせられそうに...！"
            teacher "こわかったわね！よく おおごえを だせたわね！"
            teacher "せんせいから おまわりさんに れんらくしておくわね。"
            hide teacher with dissolve
        
        call show_feedback("shout_success") from _call_fb_car_2
        return
    else:
        # しっぱい -> ブザーチャンス
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence
        if _return == "success":
            $ update_score(15)
            jump .car_repelled_buzzer
        else:
            jump .car_gameover

# にげる
label .forceful_run:
    pc "（にげなきゃ！）"
    
    # UI一じ非表示
    hide screen minimap
    hide screen score_hud

    python:
        escape_game = EscapeMinigame(difficulty="hard", key="dismiss")
    
    call screen mashing_minigame(escape_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud

    if _return == "success":
        $ update_score(15, "なんとか にげきった")
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
        
        call show_feedback("run_success_car") from _call_fb_car_3
        return
    else:
        # しっぱい -> ブザーチャンス
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_1
        if _return == "success":
            $ update_score(15)
            jump .car_repelled_buzzer
        else:
            jump .car_gameover

label .car_repelled_buzzer:
    "ふしんしゃは ブザーの おとに おどろいて にげていった！"
    hide stranger with dissolve
    
    # 助けに来るひとをランダムけってい
    $ is_officer = renpy.random.choice([True, False])
    
    if is_officer:
        hide stranger
        show officer with dissolve
        officer "どうしたの！？ だいじょうぶ！？"
        pc "くるまに のせられそうに...！"
        officer "こわかったね！よく ブザーを ならせて えらかったね！"
        hide officer with dissolve
    else:
        hide stranger
        show teacher with dissolve
        teacher "どうしたの！？ だいじょうぶ！？"
        pc "くるまに のせられそうに...！"
        teacher "こわかったわね！よく ブザーを ならせわね！"
        hide teacher with dissolve
    
    return

label .car_gameover:
    stranger "つかまえた！"
    hide stranger
    scene black with fade
    call show_feedback("captured") from _call_fb_car_4
    jump game_over



# -----------------------------------------------------------------------------
# にげるルート
# -----------------------------------------------------------------------------
label .run_away_car:
    pc "（にげよう！）"
    
    $ update_score(15)
    
    # UI一じ非表示
    hide screen minimap
    hide screen score_hud

    python:
        escape_game = EscapeMinigame(difficulty="normal", key="dismiss")
    
    call screen mashing_minigame(escape_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    
    hide stranger
    
    if _return == "success":
        $ update_score(10, "うまく にげられた")
        "うまく にげられた！"
    else:
        "なんとか にげられた..."
    
    call show_feedback("run_car_success") from _call_fb_car_5
    return

# -----------------------------------------------------------------------------
# ぼうはんブザールート
# -----------------------------------------------------------------------------
label .buzzer_car:
    $ play_se("buzzer")
    
    $ update_score(20, "ぼうはんブザーで げきたい")
    
    "ピピピピピ！！"
    stranger "な、なんだ！？"
    
    python:
        h_tag, h_name = get_helper_data()
        _is_teacher = (h_tag == "teacher")

    if _is_teacher:
        hide stranger
        show teacher with dissolve
        teacher "どうしたの！？"
        pc "くるまの ひとに こえを かけられて..."
        teacher "よくできたね！あやしいと おもったら すぐ ブザーだね！"
        hide teacher with dissolve
    else:
        hide stranger
        show officer with dissolve
        officer "どうしたの！？"
        pc "くるまの ひとに こえを かけられて..."
        officer "よくできたね！あやしいと おもったら すぐ ブザーだね！"
        hide officer with dissolve
    
    call show_feedback("buzzer_success_car") from _call_fb_car_6
    return