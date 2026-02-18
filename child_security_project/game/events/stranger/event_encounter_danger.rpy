# =============================================================================
# 人物遭遇イベント：不審者（挨拶から始まる＋防犯ブザー選択肢追加）
# =============================================================================

label encounter_e_stranger:
    "だれかが ちかづいてきた。"
    
    call show_stranger_wrapper from _call_show_stranger_wrapper_danger
    
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
label .buzzer_stranger:
    # 防犯ブザーを鳴らす
    play audio "audio/防犯ブザー.mp3"
    
    pc "えいっ！！"
    
    "{size=40}ビーーーーーーー！！！{/size}"
    
    stranger "うわっ！ なんだ！？"
    hide stranger with dissolve
    
    "ふしんしゃは おとにおどろいて にげていった！"
    
    $ update_score(20)
    
    show woman with dissolve
    woman "どうしたの！？ すごい おとが したけど！"
    pc "しらない ひとに こえを かけられて……"
    woman "ブザーを ならしたのね。えらいわ！"
    hide woman with dissolve
    
    "{i}よくできた！防犯ブザーは こわいとおもったら すぐにならそう！{/i}"
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
    
    $ update_score(15)
    
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
    
    if _return == "success":
        $ update_score(30)
        "「こども110ばんの いえ」に かけこんだ！"
        show officer with dissolve
        officer "どうしたの！？"
        pc "しらない ひとに つれていかれそうに……！"
        officer "だいじょうぶ、ここは あんぜんだよ。よく にげてきたね！"
        hide officer with dissolve
        "{i}すばらしい！110ばんの いえを おぼえていたから にげられたね！{/i}"
    else:
        $ update_score(10)
        "なんとか にげきった…でも こわかった…"
        "{i}あぶなかったね。さいしょから ついていかないように しよう。{/i}"
    return

# 110番の家を知らない
label .escape_fail_no_110:
    pc "（110ばんの いえって どこ…？）"
    pc "にげなきゃ！"
    

    # ゲーム
    $ game = EscapeMinigame(
        difficulty="hard",
        title="全力疾走！", 
        text="スペースキーを連打して\n駅までダッシュしろ！"
    )
    call screen escape_minigame(game)
    
    hide stranger
    
    if _return == "success":
        $ update_score(5)
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
            $ update_score(5)
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
    
    python:
        shout_game = ShoutMinigame(threshold=0.3, duration=5.0)
    
    call screen shout_minigame(shout_game)
    
    if _return != "miss":
        $ update_score(15)
        play audio "audio/buzzer.mp3"
        stranger "うわっ…！"
        hide stranger with dissolve
        
        show woman with dissolve
        woman "どうしたの！？ だいじょうぶ！？"
        pc "しらない ひとに……"
        woman "こわかったね。よく おおごえを だせたね！"
        hide woman with dissolve
        "{i}よくがんばった！でも さいしょから ついていかないのが いちばんだよ。{/i}"
    else:
        hide stranger
        "{i}こえが でなかった……{/i}"
        
        "（どうしよう…！？）"
        menu:
            "ぼうはんブザーを ならす！":
                jump .buzzer_stranger
            
            "……":
                scene black with fade
                jump game_over
    return

# -----------------------------------------------------------------------------
# 逃げるルート
# -----------------------------------------------------------------------------
label .refuse_stranger:
    $ update_score(15)
    
    pc "ごめんなさい！まっすぐ かえらないといけないんです！"
    stranger "えー、ちょっとだけだよ～"
    pc "いいえ！さようなら！"
    
    "しっかり ことわって、そのばを はなれた。"
    
    hide stranger with dissolve
    
    "{i}よくできた！しらない ひとの さそいは きっぱり ことわろう！{/i}"
    return

# -----------------------------------------------------------------------------
# 大声を出すルート（マイク使用）
# -----------------------------------------------------------------------------
label .shout_stranger:
    pc "「たすけてーー！！」"
    
    "（ほんとうに おおきな こえを だしてみよう！）"
    
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
             "やっぱり こえが でない……"
             "（どうしよう…！？）"
             menu:
                "ぼうはんブザーを ならす！":
                    jump .buzzer_stranger
                
                "……":
                    scene black with fade
                    jump game_over

    stranger "うわっ！ ちょ、ちょっと……！"
    hide stranger with dissolve
    
    "ふしんしゃは にげていった！"
    
    
    show woman with dissolve
    woman "どうしたの！？ だいじょうぶ！？"
    pc "しらない ひとに こえを かけられて……"
    woman "こわかったね。よく おおごえを だせたね！"
    hide woman with dissolve
    
    "{i}すばらしい！おおごえを だすと まわりの ひとが たすけに きてくれるよ！{/i}"
    return

# -----------------------------------------------------------------------------
# 共通結末
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
    
    if _return == "success":
        $ update_score(35)
        "PERFECT!! 「こども110ばんの いえ」に かけこんだ！"
    else:
        $ update_score(20)
        "なんとか にげられた！"
    
    show officer with dissolve
    officer "どうしたの！？"
    pc "しらない ひとに おいかけられて……！"
    officer "だいじょうぶ、ここは あんぜんだよ。よく にげてきたね！"
    hide officer with dissolve
    
    "{i}よくできた！しらない ひとには ぜったいに ついていかないように しよう。{/i}"
    return

# 110番の家を覚えていない → 失敗
label .flee_fail:
    pc "にげなきゃ！"
    "はしりだしたけど……"
    pc "（どこに にげればいいの……！？）"
    
    stranger "まてまて～"
    
    hide stranger
    scene black with fade
    "{i}ふしんしゃに つれさられてしまった...{/i}"
    jump game_over
    




