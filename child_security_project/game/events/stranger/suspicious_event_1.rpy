# ふしんしゃイベント1：お菓こで誘うふしんしゃ
# イベント登録は def_mapdat.rpy の event_pools で管理

label suspi_e_test_1:
    $ setup_stranger("suspi_e_test_1")
    # play music "audio/Pinch!!.mp3" fadein 1.0 volume 1.0  # 削除：ここではまだ流さない
    show stranger with dissolve
    
    # 特徴を表示
    $ current_trait = next((e['trait'] for e in encountered_events if e['event_name'] == 'suspicious_event_1'), "")
    if current_trait:
        "（[current_trait] ひとのようだ。）"
    $ s_text = get_commute_text("がっこうかえり？", "がっこうに いくの？")
    $ player_destination = get_commute_text("かえら", "か")
    
    play music "audio/Pinch!!.mp3" fadein 1.0 volume 0.2  # ここで流す

    # mode に合わせてボイスを流す（かえり or hello）
    $ play_voice("auto")

    stranger "きみ [s_text] {color=#ff0000}おいしいケーキがあるんだけどこない？{/color}"

    menu:
        "いくー！":
            stranger "いいこだね～こっちこっち..."
            hide stranger
            scene black with fade
            
            call show_feedback("followed_stranger") from _call_fb_s1_1
            
            jump game_over

        "ごめんなさい。まっすぐ [player_destination]ないといけないんです":
            $ play_se("decide")
            $ player_destination = get_commute_text("かえら", "か")
            $ update_score(15, "はっきりと ことわった")
            
            pc "いりません！"
            
            # 強制連れ去りイベント
            stranger "いいから こいよ！"
            "ふしんしゃは うでを つかもうとしてきた！"
            
            menu:
                "おおごえを だす":
                    $ play_se("decide")
                    jump .shout_cake
                
                "にげる":
                    $ play_se("decide")
                    jump .run_cake

label .shout_cake:
    # おおごえミニゲーム
    window hide
    # UI一じ非表示
    hide screen minimap
    hide screen score_hud
    
    $ shout_game = ShoutMinigame(threshold=0.5, duration=8.0)
    call screen shout_minigame(shout_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    window show
    
    if _return != "miss":
        jump .cake_success_shout
    else:
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_13
        if _return == "success":
            jump .cake_success_buzzer
        else:
            jump .cake_fail

label .run_cake:
    # 逃走ミニゲーム（れんだ）
    window hide
    # UI一じ非表示
    hide screen minimap
    hide screen score_hud
    
    $ game = MashingMinigame(target_count=15, time_limit=8.0, title="にげろ", text="ボタンをれんだして\nダッシュしろ！")
    call screen mashing_minigame(game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    window show
    
    if _return == "perfect" or _return == "good":
        jump .cake_success_run
    else:
        call fallback_buzzer_sequence from _call_fallback_buzzer_sequence_14
        if _return == "success":
            jump .cake_success_buzzer
        else:
            jump .cake_fail

label .cake_success_shout:
    $ update_score(25, "おおごえで げきたい")
    $ play_se("buzzer")
    stranger "ちっ...！"
    "ふしんしゃは おおごえに おどろいて にげていった！"
    hide stranger with dissolve
    jump .cake_rescued

label .cake_success_run:
    $ update_score(15, "なんとか にげきった")
    "なんとか にげきった！"
    hide stranger with dissolve
    jump .cake_rescued

label .cake_success_buzzer:
    $ update_score(15, "ぼうはんブザーで げきたい")
    $ play_se("buzzer")
    "ピピピピピ！！"
    stranger "うわっ、なんだ！！"
    "ふしんしゃは あわてて にげだした！"
    hide stranger with dissolve
    jump .cake_rescued

label .cake_rescued:
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
    
    call show_feedback("no_follow") from _call_fb_s1_2
    return

label .cake_fail:
    pc "はなしてよー！"
    stranger "うるさい！"
    scene black with fade
    call show_feedback("captured") from _call_fb_s1_3
    jump game_over