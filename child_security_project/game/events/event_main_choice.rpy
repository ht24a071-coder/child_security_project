
# 共通選択肢フレームワーク
label event_main_choice(human_type):

    # officer player woman stranger
    show expression human_type with dissolve
    
    $ greeting = "Greet_" + human_type
    call expression greeting

    menu:
        "あいさつをする":
            $ greeting_is = "Is_greet_" + human_type
            call expression greeting_is
            return
        "...（むしする）":
            $ greeting_is = "Bad_greet_" + human_type
            call expression greeting_is
            return
        "（ぼうはんブザーを にぎる）":
            "{i}{rb}防犯{/rb}{rt}ぼうはん{/rt}ブザーが{rb}激{/rb}{rt}はげ{/rt}しく{rb}鳴{/rb}{rt}な{/rt}る！{/i}"
            $ buzzer_eve = "Buzzer_" + human_type
            call expression buzzer_eve
            return

    hide expression human_type with dissolve

    return