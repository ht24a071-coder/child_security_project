# 不審者イベント1：お菓子で誘う不審者
# イベント登録は def_mapdat.rpy の event_pools で管理

label suspi_e_test_1:
    $ setup_stranger()
    show stranger with dissolve
    stranger "{rb}君{/rb}{rt}きみ{/rt}{rb}学校{/rb}{rt}がっこう{/rt}{rb}帰{/rb}{rt}かえ{/rt}り？おいしいケーキがあるんだけど{rb}来{/rb}{rt}こ{/rt}ない？"

    menu:
        "いくー！":
            stranger "いい{rb}子{/rb}{rt}こ{/rt}だね～こっちこっち..."
            hide stranger
            scene black with fade
            
            "{i}{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}についていってはいけないよ！{/i}"
            "{i}「いかのおすし」を{rb}思{/rb}{rt}おも{/rt}い{rb}出{/rb}{rt}だ{/rt}そう！{/i}"
            
            jump game_over

        "ごめんなさい。まっすぐ{rb}帰{/rb}{rt}かえ{/rt}らないといけないんです":
            $ update_score(15)
            
            pc "いりません！"
            
            # 強制連れ去りイベント
            stranger "いいから こいよ！"
            "ふしんしゃは うでを つかもうとしてきた！"
            
            menu:
                "おおごえを だす":
                    jump .shout_cake
                
                "にげる":
                    jump .run_cake

label .shout_cake:
    # 大声ミニゲーム
    window hide
    # UI一時非表示
    hide screen minimap
    hide screen score_hud
    
    $ shout_game = ShoutMinigame(threshold=0.5, duration=8.0)
    call screen shout_minigame(shout_game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    window show
    
    if _return != "miss":
        jump .cake_success
    else:
        call fallback_buzzer_sequence
        if _return == "success":
            jump .cake_success_buzzer
        else:
            jump .cake_fail

label .run_cake:
    # 逃走ミニゲーム（連打）
    window hide
    # UI一時非表示
    hide screen minimap
    hide screen score_hud
    
    $ game = MashingMinigame(target_count=15, time_limit=8.0, title="にげろ", text="ボタンを連打して\nダッシュしろ！")
    call screen mashing_minigame(game)
    
    # UI復帰
    show screen minimap
    show screen score_hud
    window show
    
    if _return == "perfect" or _return == "good":
        jump .cake_success
    else:
        call fallback_buzzer_sequence
        if _return == "success":
            jump .cake_success_buzzer
        else:
            jump .cake_fail

label .cake_success:
    $ update_score(20)
    play audio "audio/buzzer.mp3"
    stranger "ちっ...！"
    "ふしんしゃは おおごえに おどろいて にげていった！"
    hide stranger with dissolve
    jump .cake_rescued

label .cake_success_buzzer:
    $ update_score(15)
    "ピピピピピ！！"
    stranger "うわっ、なんだ！！"
    "ふしんしゃは あわてて にげだした！"
    hide stranger with dissolve
    jump .cake_rescued

label .cake_rescued:
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
    
    "{i}よくできた！しらない ひとには ぜったいに ついていかないように しよう。{/i}"
    return

label .cake_fail:
    pc "はなしてよー！"
    stranger "うるさい！"
    scene black with fade
    "{i}ふしんしゃに つれさられてしまった...{/i}"
    jump game_over