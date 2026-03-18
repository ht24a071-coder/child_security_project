# =============================================================================
# ふしんしゃイベント：おかあさんが怪我したから来て
# =============================================================================

label suspi_e_mom_injury:

    call show_stranger_wrapper from _call_show_stranger_wrapper_mom

    # 特徴を表示
    $ current_trait = next((e['trait'] for e in encountered_events if e['event_name'] == 'mom_injury'), "")
    if current_trait:
        "（[current_trait] ひとのようだ。）"
    
    $ play_voice() # おかあさんの怪我という緊急性はセリフで表現し、ボイスは標準的なものを使用
    stranger "ねえ、キミ！たいへんだよ！"
    stranger "キミの おかあさんが けがをして びょういんに はこばれたんだ！"

    pc "えっ！？ ママが！？"
    
    stranger "そうなんだ！いまから くるまで びょういんに つれていってあげるよ！"
    stranger "さあ、はやく のって！"
    
    # せんたく肢
    menu:
        "くるまに のる":
            $ play_se("decide")
            jump .get_in_car_mom
        
        "のらない":
            $ play_se("decide")
            jump .refuse_car_mom
        
        "ぼうはんブザーを ならす":
            $ play_se("decide")
            jump .buzzer_car_mom
            
        "むしして にげる":
            $ play_se("decide")
            $ update_score(20, "むしして にげた")
            jump .forceful_run_mom_dash
            
# -----------------------------------------------------------------------------
# くるまに乗る（GAME OVER）
# -----------------------------------------------------------------------------
label .get_in_car_mom:
    pc "ママが しんぱいだ...！"
    pc "わかりました、つれていってください！"
    
    stranger "よしよし、いいこだね..."
    
    hide stranger
    scene black with fade
    
    call show_feedback("got_in_car_mom") from _call_fb_mom_1
    
    jump game_over

# -----------------------------------------------------------------------------
# のらない（ただしい判断）
# -----------------------------------------------------------------------------
label .refuse_car_mom:
    $ update_score(15, "はっきりと ことわった")
    
    pc "いきません！"
    
    stranger "えっ？ でも おかあさんが..."
    
    pc "せんせいや パパに れんらくしますから！"
    
    # --- ここから執拗な勧誘 ---
    play music "audio/Pinch!!.mp3" fadein 1.0 volume 1.0 # ここで流す！
    stranger "いいから こいよ！"
    "ふしんしゃは うでを つかもうとしてきた！"
    
    menu:
        "おおごえを だす":
            $ play_se("decide")
            jump .forceful_run_mom_shout 
        
        "にげる":
            $ play_se("decide")
            jump .forceful_run_mom_dash

label .forceful_run_mom_shout:
    # おおごえミニゲーム
    window hide
    # UI一じ非表示
    hide screen minimap
    hide screen score_hud
    
    # 難易度調整: 閾値0.6, 制限じかん8びょう
    $ shout_game = ShoutMinigame(threshold=0.6, duration=8.0)
    call screen shout_minigame(shout_game)
    hide screen shout_minigame
    
    # UI復帰
    show screen minimap
    show screen score_hud
    window show
    
    if _return == "perfect":
        jump .escape_success_mom_shout
    else:
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_11
        if _return == "success":
                jump .escape_success_mom_buzzer
        else:
                jump .escape_fail_mom

label .forceful_run_mom_dash:
    # れんだミニゲーム
    window hide
    # UI一じ非表示
    hide screen minimap
    hide screen score_hud
    
    # 難易度調整: 15回/5びょう
    $ game = MashingMinigame(
        target_count=15, 
        time_limit=5.0, 
        title="にげろ", 
        text="ボタンをれんだして\nダッシュしろ！"
    )
    call screen mashing_minigame(game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    window show
    
    if _return == "perfect" or _return == "good":
        jump .escape_success_mom_run
    else:
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_12
        if _return == "success":
            jump .escape_success_mom_buzzer
        else:
            jump .escape_fail_mom

label .escape_success_mom_shout:
    # おおごえせいこう
    $ update_score(25, "おおごえで げきたい")
    $ play_se("buzzer")
    pc "やめてー！！"
    "ふしんしゃの てを ふりほどいて にげだした！"
    
    stranger "チッ...！"
    "ふしんしゃは にげていった。"
    call hide_stranger_wrapper(dissolve) from _call_hide_stranger_wrapper_shout
    jump .escape_rescued_mom

label .escape_success_mom_run:
    # 逃走せいこう
    $ update_score(15, "なんとか にげきった")
    "なんとか にげきった！"
    
    stranger "チッ...！"
    "ふしんしゃは にげていった。"
    call hide_stranger_wrapper(dissolve) from _call_hide_stranger_wrapper_run
label .escape_rescued_mom:
    hide stranger with dissolve
    
    # 助けに来るひとをランダムけってい
    $ is_officer = renpy.random.choice([True, False])
    
    if is_officer:
        show officer with dissolve
        officer "どうしたの！？"
        pc "しらない ひとに つれていかれそうに..."
        officer "こわかったね！よく がんばったね！"
        hide officer with dissolve
    else:
        show teacher with dissolve
        teacher "どうしたの！？"
        pc "しらない ひとに つれていかれそうに..."
        teacher "こわかったわね！よく がんばったわね！"
        hide teacher with dissolve
    
    call show_feedback("escape_success_mom") from _call_fb_mom_2
    return

label .escape_success_mom_buzzer:
    # ブザーせいこうじ
    $ update_score(15, "ぼうはんブザーで げきたい")
    $ play_se("buzzer")
    "ピピピピピ！！"
    stranger "うわっ、なんだ！！"
    "ふしんしゃは あわてて にげだした！"
    hide stranger with dissolve
    
    # 助けに来るひとをランダムけってい
    $ is_officer = renpy.random.choice([True, False])
    
    if is_officer:
        show officer with dissolve
        officer "だいじょうぶ！？"
        pc "しらないひとに つれていかれそうになって..."
        officer "ブザーを ならせて えらかったね！"
        hide officer with dissolve
    else:
        show teacher with dissolve
        teacher "だいだいじょうぶ！？"
        pc "しらないひとに つれていかれそうになって..."
        teacher "ブザーを ならせて えらかったわね！"
        hide teacher with dissolve

    return

label .escape_fail_mom:
    # 逃走しっぱい -> 連れ去り
    pc "はなしてよー！"
    stranger "うるさい！ くるまに のるんだ！"
    
    scene black with fade
    call show_feedback("captured_mom") from _call_fb_mom_3
    jump game_over

# -----------------------------------------------------------------------------
# ぼうはんブザー（大正解）
# -----------------------------------------------------------------------------
label .buzzer_car_mom:
    $ play_se("buzzer")
    
    $ update_score(20, "ぼうはんブザーで げきたい")
    
    "ピピピピピ！！"
    stranger "うわっ！？"
    
    "ふしんしゃは あわてて にげていった！"
    hide stranger with dissolve
    python:
        h_tag, h_name = get_helper_data()
        _is_teacher = (h_tag == "teacher")

    if _is_teacher:
        show teacher with dissolve
        teacher "だいじょうぶ！？"
        pc "おかあさんが けがをしたって..."
        teacher "それは うそかもしれないよ。おうちのひとに でんわしてみようか？"
        
        "（かくにんしたら、ママは げんきでした）"
        
        teacher "よかったね！あやしいと おもったら すぐ ブザーだね！"
        hide teacher with dissolve
    else:
        show officer with dissolve
        officer "だいじょうぶ！？"
        pc "おかあさんが けがをしたって..."
        officer "それは うそかもしれないよ。おうちのひとに でんわしてみようか？"
        
        "（かくにんしたら、ママは げんきでした）"
        
        officer "よかったね！あやしいと おもったら すぐ ブザーだね！"
        hide officer with dissolve
    
    call show_feedback("buzzer_success_mom_injury") from _call_fb_mom_4
    return
