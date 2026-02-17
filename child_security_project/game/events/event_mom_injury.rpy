# =============================================================================
# 不審者イベント：お母さんが怪我したから来て
# =============================================================================

label suspi_e_mom_injury:

    $ setup_stranger("mom_injury")
    "とつぜん、しらない おとなが はなしかけてきた。"
    
    show stranger with dissolve
    
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
    
    "{i}それは わるいおとなの うそでした。{/i}"
    "{i}しらないひとの くるまに のってはいけません。{/i}"
    "{i}「おかあさんが けがをした」といわれても、ついていっては いけません。{/i}"
    
    jump game_over

# -----------------------------------------------------------------------------
# 断る（正解）
# -----------------------------------------------------------------------------
label .refuse_car_mom:
    $ update_score(10)
    
    pc "（しらない ひとには ついていかない！）"
    pc "いきません！"
    
    stranger "えっ？ でも おかあさんが..."
    
    pc "せんせいや パパに れんらくしますから！"
    
    # --- ここから執拗な勧誘 ---
    stranger "いいから こいよ！"
    "ふしんしゃは うでを つかもうとしてきた！"
    
    # 選択肢：大声か逃げる（連打）か
    menu:
        "おおごえを だす":
            # 大声ミニゲーム
            window hide
            # 難易度調整: 閾値0.6, 制限時間8秒
            $ shout_game = ShoutMinigame(threshold=0.6, duration=8.0)
            call screen shout_minigame(shout_game)
            hide screen shout_minigame
            window show
            
            if _return == "perfect":
                jump .escape_success_mom
            else:
                jump .escape_fail_mom
        
        "にげる":
            # 連打ミニゲーム
            window hide
            # 難易度調整: 15回/5秒
            $ mash_game = MashMinigame(target_count=15, time_limit=5.0)
            call screen mash_minigame_screen(mash_game)
            hide screen mash_minigame_screen
            window show
            
            if _return == "perfect" or _return == "good":
                jump .escape_success_mom
            else:
                jump .escape_fail_mom

label .escape_success_mom:
    # 逃走成功
    $ update_score(15)
    pc "やめてー！！"
    "ふしんしゃの てを ふりほどいて にげだした！"
    
    stranger "チッ...！"
    "ふしんしゃは にげていった。"
    hide stranger with dissolve
    
    "{i}よくできた！しらない ひとが [player_name]ちゃんの うでを ひっぱったりしたら、おおごえを だして にげよう！{/i}"
    "{i}かならず ほかの おとなに かくにんしようね。{/i}"
    return

label .escape_fail_mom:
    # 逃走失敗 -> 連れ去り
    pc "はなしてよー！"
    stranger "うるさい！ くるまに のるんだ！"
    
    scene black with fade
    "{i}ふしんしゃに むりやり くるまに のせられてしまった...{/i}"
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
    
    "{i}すばらしい！うそかもしれないと おもって ブザーを ならせたね！{/i}"
    return
