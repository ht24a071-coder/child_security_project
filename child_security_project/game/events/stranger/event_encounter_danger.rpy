# =============================================================================
# ひと物遭遇イベント：ふしんしゃ（挨拶から始まる＋ぼうはんブザーせんたく肢追加）
# =============================================================================

label encounter_e_stranger:
    play music "audio/Pinch!!.mp3" fadein 1.0
    "だれかが ちかづいてきた。"
    
    call show_stranger_wrapper("encounter_e_stranger") from _call_show_stranger_wrapper_danger

    # 特徴を表示
    $ current_trait = next((e['trait'] for e in encountered_events if e['event_name'] == 'encounter_e_stranger'), "")
    if current_trait:
        "（{color=#ff0000}[current_trait]{/color} ひとのようだ。）"
    
    $ play_voice("hello")
        
    stranger "こんにちは～"
    
    # まず挨拶への反応
    # まず呼びかけ
    menu:
        "こんにちは":
            pc "こんにちは..."
            stranger "いいこだね～"
        
        "...（むしする）":
            pc "..."
    
    pause 0.3
    stranger "ねえねえ、{color=#ff0000}おいしい おかしが あるんだけど、たべない？{/color}"
    stranger "こっちに おいでよ。"

    pc "いりません！"
    
    # 強制イベント化（ステージ1：腕を掴まれる）
    stranger "いいから おいでよ！"
    "ふしんしゃは うでを つかもうとしてきた！"
    
    pc "（つかまる！）"

    # Stage 1: おおごえのみ（パニック状態）
    menu:
        "おおごえを だす":
            jump .shout_stranger

# -----------------------------------------------------------------------------
# おおごえを出すルート
# -----------------------------------------------------------------------------
label .buzzer_stranger:
    # ぼうはんブザーを鳴らす
    $ play_se("buzzer")
    
    pc "えいっ！！"
    
    "{size=40}ビーーーーーーー！！！{/size}"
    
    stranger "うわっ！ なんだ！？"
    hide stranger with dissolve
    
    "ふしんしゃは おとにおどろいて にげていった！"
    
    $ update_score(20, "ぼうはんブザーで げきたい")
    
    python:
        h_tag, _unused = get_helper_data()
    
    if h_tag == "teacher":
        hide stranger
        show teacher with dissolve
        teacher "どうしたの！？ すごい おとが したけど！"
        pc "しらない ひとに こえを かけられて……"
        teacher "ブザーを ならしたのね。えらいわ！"
        hide teacher with dissolve
    else:
        hide stranger
        show officer with dissolve
        officer "どうしたの！？ すごい おとが したけど！"
        pc "しらない ひとに こえを かけられて……"
        officer "ブザーを ならしたのね。えらい！"
        hide officer with dissolve
    
    call show_feedback("buzzer_success") from _call_fb_ed_1
    return

# -----------------------------------------------------------------------------
# ついていくルート（あぶない→にげるせんたく肢）
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

# ぼうはんブザーでにげる（ついていったうしろ）
label .escape_buzzer:
    $ play_se("buzzer")
    
    "ピピピピピ！！"
    stranger "うわっ！？"
    
    hide stranger with dissolve
    
    $ update_score(15, "ぼうはんブザーで にげきった")
    
    python:
        h_tag, _unused = get_helper_data()

    if h_tag == "teacher":
        show teacher with dissolve
        teacher "どうしたの！？"
        pc "しらない ひとに つれていかれそうに..."
        teacher "よくできたね！でも さいしょから ついていかないように しようね。"
        hide teacher with dissolve
    else:
        show officer with dissolve
        officer "どうしたの！？"
        pc "しらない ひとに つれていかれそうに..."
        officer "よくできたね！でも さいしょから ついていかないように しようね。"
        hide officer with dissolve
    
    call show_feedback("buzzer_success_but_no_follow") from _call_fb_ed_2
    return

# 110番のいえににげる（フラグあり→せいこう）
label .escape_110:
    pc "（あそこに「110ばんの いえ」があった！）"
    pc "にげろーー！"
    
    python:
        escape_game = EscapeMinigame(difficulty="normal", key="K_SPACE")
    
    call screen mashing_minigame(escape_game)
    
    hide stranger
    
    if _return == "success":
        $ update_score(30, "110ばんのいえに にげこんだ")
        "「こども110ばんの いえ」に かけこんだ！"
        
        python:
            h_tag, _unused = get_helper_data()
        
        if h_tag == "teacher":
            hide stranger
            show teacher with dissolve
            teacher "どうしたの！？"
            pc "しらない ひとに つれていかれそうに……！"
            teacher "だいじょうぶ、ここは あんぜんだよ。よく にげてきたね！"
            hide teacher with dissolve
        else:
            hide stranger
            show officer with dissolve
            officer "どうしたの！？"
            pc "しらない ひとに つれていかれそうに……！"
            officer "だいじょうぶ、ここは あんぜんだよ。よく にげてきたね！"
            hide officer with dissolve
        
        call show_feedback("escape_110_success") from _call_fb_ed_3
    else:
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_2
        if _return == "success":
            jump .escape_buzzer
        
        $ update_score(10, "なんとか にげきった")
        "なんとか にげきった…でも こわかった…"
        call show_feedback("partial_escape") from _call_fb_ed_4
    return

# 110番のいえを知らない
label .escape_fail_no_110:
    pc "（110ばんの いえって どこ…？）"
    pc "にげなきゃ！"
    

    # ゲーム
    $ game = MashingMinigame(
        target_count=15,
        time_limit=8.0,
        title="全ちから疾走！", 
        text="スペースキーをれんだして\nえきまでダッシュしろ！"
    )
    call screen mashing_minigame(game)
    
    hide stranger
    
    hide stranger
    
    if _return == "success":
        $ update_score(5)
        "なんとか にげきった……"
        call show_feedback("escape_110_unknown") from _call_fb_ed_5
        return
    else:
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_3
        if _return == "success":
            jump .escape_buzzer
            
        scene black with fade
        call show_feedback("escape_110_fail") from _call_fb_ed_6
        jump game_over

# いえにはしるルート（とてもむずかしい）
label .escape_home:
    pc "いえに にげよう！"
    
    python:
        escape_game = EscapeMinigame(difficulty="hard", key="K_SPACE")
    
    call screen mashing_minigame(escape_game)
    
    hide stranger
    
    if _return == "success":
        "なんとか にげきった……"
        
        "いえの まえに ついた！"
        "（いそいで かぎを あけなきゃ！）"
        
        python:
            # 鍵を開けるゲームもれんだに変更（焦ってれんだするイメージ）
            key_game = MashingMinigame(target_count=20, time_limit=5.0, title="かぎをあけろ！", text="ボタンをれんだして\nかぎをあけろ！")
        
        call screen mashing_minigame(key_game)
        
        if _return == "miss":
            call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_4
            if _return == "success":
                jump .escape_buzzer
                
            "かぎが あかない…！"
            stranger "まてまて～"
            scene black with fade
            call show_feedback("key_failed") from _call_fb_ed_7
            jump game_over
        else:
            $ update_score(5, "いえに にげこんだ")
            "なんとか いえに にげこめた…"
            hide stranger
            show parent with dissolve
            parent "おかえり！どうしたの、そんなにあわてて？"
            pc "しらない ひとに..."
            parent "よかった、ぶじで。もうだいじょうぶよ。"
            hide parent with dissolve
            
            call show_feedback("run_success_but_dangerous") from _call_fb_ed_8
            return
    else:
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_5
        if _return == "success":
            jump .escape_buzzer

        scene black with fade
        call show_feedback("escape_failed_no_follow") from _call_fb_ed_9
        jump game_over

# おおごえを出してにげる（マイク使用）
label .escape_shout:
    pc "「たすけてーーー！！」"
    
    python:
        shout_game = ShoutMinigame(threshold=0.3, duration=5.0)
    
    call screen shout_minigame(shout_game)
    
    if _return != "miss":
        $ update_score(15, "おおごえで たすけを よんだ")
        $ play_se("buzzer")
        stranger "うわっ…！"
        hide stranger with dissolve
        
        python:
            h_tag, _unused = get_helper_data()

        if h_tag == "teacher":
            hide stranger
            show teacher with dissolve
            teacher "どうしたの！？ だいじょうぶ！？"
            pc "しらない ひとに……"
            teacher "こわかったね。よく おおごえを だせたね！"
            hide teacher with dissolve
        else:
            hide stranger
            show officer with dissolve
            officer "どうしたの！？ だいじょうぶ！？"
            pc "しらない ひとに……"
            officer "こわかったね。よく おおごえを だせたね！"
            hide officer with dissolve
            call show_feedback("shout_success_but_no_follow") from _call_fb_ed_10
    else:
        hide stranger
        call show_feedback("voice_failed") from _call_fb_ed_11
        
        "（どうしよう…！？）"
        menu:
            "ぼうはんブザーを ならす！":
                jump .buzzer_stranger
            
            "……":
                call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_6
                if _return == "success":
                    jump .escape_buzzer
                    
                scene black with fade
                jump game_over
    return

# -----------------------------------------------------------------------------
# にげるルート
# -----------------------------------------------------------------------------
label .refuse_stranger:
    $ update_score(15, "はっきりと ことわった")
    
    pc "ごめんなさい！まっすぐ かえらないといけないんです！"
    stranger "えー、ちょっとだけだよ～"
    pc "いいえ！さようなら！"
    
    "しっかり ことわって、そのばを はなれた。"
    
    hide stranger with dissolve
    
    call show_feedback("refuse_success") from _call_fb_ed_12
    return

# -----------------------------------------------------------------------------
# おおごえを出すルート（マイク使用）
# -----------------------------------------------------------------------------
label .shout_stranger:
    pc "「たすけてーー！！」"

    "（ほんとうに おおきな こえを だそう！）"

    # UI一じ非表示
    hide screen minimap
    hide screen score_hud

    python:
        # ステージ1：おおごえゲーム (ShoutMinigame)
        # 固定ダメージロジック使用 (threshold=0.35, duration=3.0)
        shout_game = ShoutMinigame(threshold=0.35, duration=8.0)

    call screen shout_minigame(shout_game)

    # UI復帰
    show screen minimap
    show screen score_hud

    if _return != "miss":
        # せいこう -> 撃退
        jump .stranger_repelled
    else:
        # しっぱい -> ステージ2へ（ここはブザーチャンスなし、つれていかれる途なか）
        jump .stage2_choice

label .stage2_choice:
    stranger "うるさいな！ こっちに こい！"
    "ふしんしゃは さらにつよく ひっぱってきた！"
    
    pc "（こわい... でも にげなきゃ！）"
    
    menu:
        "おおごえを だす":
            jump .stage2_shout
            
        "にげる":
            jump .stage2_run

label .stage2_shout:
    # ステージ2のおおごえ（難易度アップ）
    pc "「やめてーー！！」"
    
    # UI一じ非表示
    hide screen minimap
    hide screen score_hud

    python:
        shout_game = ShoutMinigame(threshold=0.45, duration=8.0)

    call screen shout_minigame(shout_game)

    # UI復帰
    show screen minimap
    show screen score_hud

    if _return != "miss":
        jump .stranger_repelled
    else:
        # しっぱい -> ステージ3へ
        jump .stage3_choice

label .stage2_run:
    # ステージ2の逃走（Mashing）
    pc "（ふりほどいて にげる！）"
    
    # UI一じ非表示
    hide screen minimap
    hide screen score_hud

    python:
        # れんだゲーム
        escape_game = MashingMinigame(target_count=15, time_limit=8.0)

    call screen mashing_minigame(escape_game)

    # UI復帰
    show screen minimap
    show screen score_hud

    if _return == "perfect" or _return == "good":
        jump .stranger_repelled_run
    else:
        jump .stage3_choice

label .stage3_choice:
    stranger "いいかげんに しろ！"
    "ふしんしゃが つよく うでを 引っ張った！"
    
    pc "（もう だめかも... でも ぼうはんブザーが ある！）"
    
    menu:
        "おおごえを だす":
            jump .stage3_shout
            
        "にげる":
            jump .stage3_run
            
        "ぼうはんブザー":
            jump .buzzer_stranger

label .stage3_shout:
    # ステージ3のおおごえ（最終）
    pc "「だれかーー！！」"
    
    hide screen minimap
    hide screen score_hud
    python:
        shout_game = ShoutMinigame(threshold=0.5, duration=8.0)
    call screen shout_minigame(shout_game)
    show screen minimap
    show screen score_hud

    if _return != "miss":
        jump .stranger_repelled
    else:
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_7
        if _return == "success":
            jump .buzzer_stranger
        jump .game_over_capture

label .stage3_run:
    # ステージ3の逃走
    pc "（にげるんだ！！）"
    
    hide screen minimap
    hide screen score_hud
    python:
        escape_game = MashingMinigame(target_count=20, time_limit=8.0)
    call screen mashing_minigame(escape_game)
    show screen minimap
    show screen score_hud

    if _return == "perfect" or _return == "good":
        jump .stranger_repelled_run
    else:
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_8
        if _return == "success":
            jump .buzzer_stranger
        jump .game_over_capture

label .stranger_repelled:
    $ update_score(25, "おおごえで げきたい")
    stranger "ちっ...！"
    "ふしんしゃは くるまに のって にげていった！"
    hide stranger with dissolve
    
    call .after_encounter_success from _call_encounter_e_stranger_after_encounter_success
    return

label .stranger_repelled_run:
    $ update_score(15)
    "なんとか にげきった！"
    hide stranger with dissolve
    
    call .after_encounter_success from _call_encounter_e_stranger_after_encounter_success_1
    return

label .game_over_capture:
    scene black with fade
    call show_feedback("captured") from _call_fb_ed_13
    jump game_over

label .after_encounter_success:
    python:
        h_tag, _unused = get_helper_data()
    
    if h_tag == "teacher":
        hide stranger
        show teacher with dissolve
        teacher "だいじょうぶ！？"
        pc "しらない ひとに..."
        teacher "こわかったね。よく がんばったね！"
        hide teacher with dissolve
    else:
        hide stranger
        show officer with dissolve
        officer "だいじょうぶ！？"
        pc "しらない ひとに..."
        officer "こわかったね。よく がんばったね！"
        hide officer with dissolve
    call show_feedback("danger_repelled") from _call_fb_ed_14
    return

# -----------------------------------------------------------------------------
# 共通結末
# -----------------------------------------------------------------------------
label .flee_stranger:
    if flag_know_110:
        jump .flee_success
    else:
        jump .flee_fail

# 110番のいえを覚えている → せいこう
label .flee_success:
    pc "（あそこに「110ばんの いえ」があった！）"
    pc "にげろーー！"
    
    python:
        flee_game = EscapeMinigame(difficulty="normal", key="K_SPACE")
    
    call screen mashing_minigame(flee_game)
    
    hide stranger
    
    if _return == "success":
        $ update_score(35, "110ばんのいえに にげこんだ")
        "PERFECT!! 「こども110ばんの いえ」に かけこんだ！"
    else:
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_9
        if _return == "success":
             jump .escape_buzzer
             
        $ update_score(20)
        "なんとか にげられた！"
    
    python:
        h_tag, _unused = get_helper_data()
    
    if h_tag == "teacher":
        show teacher with dissolve
        teacher "どうしたの！？"
        pc "しらない ひとに おいかけられて……！"
        teacher "だいじょうぶ、ここは あんぜんだよ。よく にげてきたね！"
        hide teacher with dissolve
    else:
        show officer with dissolve
        officer "どうしたの！？"
        pc "しらない ひとに おいかけられて……！"
        officer "だいじょうぶ、ここは あんぜんだよ。よく にげてきたね！"
        hide officer with dissolve
    
    call show_feedback("no_follow") from _call_fb_ed_15
    return

# 110番のいえを覚えていない → しっぱい
label .flee_fail:
    pc "にげなきゃ！"
    "はしりだしたけど……"
    pc "（どこに にげればいいの……！？）"
    
    stranger "まてまて～"
    
    call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_10
    if _return == "success":
        jump .escape_buzzer
    
    hide stranger
    scene black with fade
    call show_feedback("captured") from _call_fb_ed_16
    jump game_over
