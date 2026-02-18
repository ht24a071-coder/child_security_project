# =============================================================================
# 不審者イベント：お母さんが怪我したから来て
# =============================================================================

label suspi_e_mom_injury:

    call show_stranger_wrapper from _call_show_stranger_wrapper_mom
    
    $ _v = get_stranger_voice("003") # Hello的なボイスがあれば
    if _v:
        voice _v
    stranger "ねえ、キミ！たいへんだよ！"
    stranger "キミの おかあさんが けがをして びょういんに はこばれたんだ！"

    pc "えっ！？ ママが！？"
    
    stranger "そうなんだ！いまから くるまで びょういんに つれていってあげるよ！"
    stranger "さあ、はやく のって！"
    
    # 選択肢
    menu:
        "くるまに のる":
            jump .get_in_car_mom
        
        "のらない":
            jump .refuse_car_mom
        
        "ぼうはんブザーを ならす":
            jump .buzzer_car_mom
            
# -----------------------------------------------------------------------------
# 車に乗る（GAME OVER）
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
# のらない（正しい判断）
# -----------------------------------------------------------------------------
label .refuse_car_mom:
    $ update_score(15)
    
    pc "いきません！"
    
    stranger "えっ？ でも おかあさんが..."
    
    pc "せんせいや パパに れんらくしますから！"
    
    # --- ここから執拗な勧誘 ---
    stranger "いいから こいよ！"
    "ふしんしゃは うでを つかもうとしてきた！"
    
    menu:
        "おおごえを だす":
            jump .forceful_mom_shout 
        
        "にげる":
            jump .forceful_mom_run

label .forceful_mom_shout:
    # 大声ミニゲーム
    window hide
    # UI一時非表示
    hide screen minimap
    hide screen score_hud
    
    # 難易度調整: 閾値0.6, 制限時間8秒
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
        call fallback_buzzer_sequence
        if _return == "success":
                jump .escape_success_mom_buzzer
        else:
                jump .escape_fail_mom

label .forceful_mom_run:
    # 連打ミニゲーム
    window hide
    # UI一時非表示
    hide screen minimap
    hide screen score_hud
    
    # 難易度調整: 15回/5秒
    $ game = MashingMinigame(
        target_count=15, 
        time_limit=5.0, 
        title="にげろ", 
        text="ボタンを連打して\nダッシュしろ！"
    )
    call screen mashing_minigame(game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    window show
    
    if _return == "perfect" or _return == "good":
        jump .escape_success_mom_run
    else:
                call fallback_buzzer_sequence
                if _return == "success":
                     jump .escape_success_mom_buzzer
                else:
                     jump .escape_fail_mom

label .escape_success_mom_shout:
    # 大声成功
    $ update_score(25)
    pc "やめてー！！"
    "ふしんしゃの てを ふりほどいて にげだした！"
    
    stranger "チッ...！"
    "ふしんしゃは にげていった。"
    call hide_stranger_wrapper(dissolve) from _call_hide_stranger_wrapper_shout
    jump .escape_rescued_mom

label .escape_success_mom_run:
    # 逃走成功
    $ update_score(15)
    "なんとか にげきった！"
    
    stranger "チッ...！"
    "ふしんしゃは にげていった。"
    call hide_stranger_wrapper(dissolve) from _call_hide_stranger_wrapper_run
    jump .escape_rescued_mom

label .escape_rescued_mom:
    
    # 助けに来る人をランダム決定
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
    # ブザー成功時
    $ update_score(15)
    "ピピピピピ！！"
    stranger "うわっ、なんだ！！"
    "ふしんしゃは あわてて にげだした！"
    hide stranger with dissolve
    
    # 助けに来る人をランダム決定
    $ is_officer = renpy.random.choice([True, False])
    
    if is_officer:
         show officer with dissolve
         officer "だいじょうぶ！？"
         pc "しらないひとに つれていかれそうになって..."
         officer "ブザーを ならせて えらかったね！"
         hide officer with dissolve
    else:
         show teacher with dissolve
         teacher "だいじょうぶ！？"
         pc "しらないひとに つれていかれそうになって..."
         teacher "ブザーを ならせて えらかったわね！"
         hide teacher with dissolve

    return

label .escape_fail_mom:
    # 逃走失敗 -> 連れ去り
    pc "はなしてよー！"
    stranger "うるさい！ くるまに のるんだ！"
    
    scene black with fade
    call show_feedback("captured_mom") from _call_fb_mom_3
    jump game_over

# -----------------------------------------------------------------------------
# 防犯ブザー（大正解）
# -----------------------------------------------------------------------------
label .buzzer_car_mom:
    play audio "audio/buzzer.mp3"
    
    $ update_score(20)
    
    "ピピピピピ！！"
    stranger "うわっ！？"
    
    "ふしんしゃは あわてて にげていった！"
    hide stranger with dissolve
    
    show woman with dissolve
    woman "だいじょうぶ！？"
    pc "おかあさんが けがをしたって..."
    woman "それは うそかもしれないよ。おうちのひとに でんわしてみようか？"
    
    "（かくにんしたら、ママは 元気でした）"
    
    woman "よかったね！あやしいと おもったら すぐ ブザーだね！"
    hide woman with dissolve
    
    call show_feedback("buzzer_success_mom_injury") from _call_fb_mom_4
    return
