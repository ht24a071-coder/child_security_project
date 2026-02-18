# 不審者イベント2：車に乗せようとする不審者
# イベント登録は def_mapdat.rpy の event_pools で管理

label suspi_e_test_2:
    $ setup_stranger()
    show stranger with dissolve
    stranger "ねえ、{rb}道{/rb}{rt}みち{/rt}に{rb}迷{/rb}{rt}まよ{/rt}っちゃったんだ。{rb}車{/rb}{rt}くるま{/rt}で{rb}送{/rb}{rt}おく{/rt}ってあげようか？"

    menu:
        "{rb}乗{/rb}{rt}の{/rt}ります！":
            stranger "よかった、じゃあこっちに..."
            hide stranger
            scene black with fade
            
            "{i}{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}の{rb}車{/rb}{rt}くるま{/rt}には{rb}乗{/rb}{rt}の{/rt}っちゃダメ！{/i}"
            "{i}「いかのおすし」の「の」={rb}乗{/rb}{rt}の{/rt}らない！{/i}"
            
            jump game_over

        "{rb}大丈夫{/rb}{rt}だいじょうぶ{/rt}です。{rb}自分{/rb}{rt}じぶん{/rt}で{rb}帰{/rb}{rt}かえ{/rt}れます":
            $ update_score(15)
            
            stranger "いいから のりなよ！"
            "ふしんしゃは うでを つかもうとしてきた！"
            
            menu:
                "おおごえを だす":
                    jump .shout_car_2
                
                "にげる":
                    jump .run_car_2

label .shout_car_2:
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
        jump .car_2_success
    else:
        call fallback_buzzer_sequence
        if _return == "success":
            jump .car_2_success_buzzer
        else:
            jump .car_2_fail

label .run_car_2:
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
        jump .car_2_success
    else:
        call fallback_buzzer_sequence
        if _return == "success":
            jump .car_2_success_buzzer
        else:
            jump .car_2_fail

label .car_2_success:
    $ update_score(20)
    play audio "audio/buzzer.mp3"
    stranger "ちっ...！"
    "ふしんしゃは おおごえに おどろいて にげていった！"
    hide stranger with dissolve
    jump .car_2_rescued

label .car_2_success_buzzer:
    $ update_score(15)
    "ピピピピピ！！"
    stranger "うわっ、なんだ！！"
    "ふしんしゃは あわてて にげだした！"
    hide stranger with dissolve
    jump .car_2_rescued

label .car_2_rescued:
    # 助けに来る人を場所で決定
    python:
        h_tag, _ = get_helper_data()
    
    if h_tag == "officer":
         show officer with dissolve
         officer "どうしたの！？"
         pc "くるまに のせられそうに..."
         officer "こわかったね！よく がんばったね！"
         hide officer with dissolve
    else:
         show teacher with dissolve
         teacher "どうしたの！？"
         pc "くるまに のせられそうに..."
         teacher "こわかったわね！よく がんばったわね！"
         hide teacher with dissolve
    
    "{i}えらい！{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}の{rb}車{/rb}{rt}くるま{/rt}には{rb}絶対{/rb}{rt}ぜったい{/rt}{rb}乗{/rb}{rt}の{/rt}らないでね！{/i}"
    return

label .car_2_fail:
    stranger "つかまえた！"
    scene black with fade
    "{i}ふしんしゃに つれさられてしまった...{/i}"
    jump game_over