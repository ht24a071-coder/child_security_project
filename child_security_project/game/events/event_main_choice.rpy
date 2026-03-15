
# 共通せんたく肢フレームワーク
label event_main_choice(human_type):

    # officer player woman stranger
    show expression human_type with dissolve
    window show dissolve
    
    $ greeting = "Greet_" + human_type
    call expression greeting from _call_expression

    menu:
        "あいさつをする":
            $ greeting_is = "Is_greet_" + human_type
            call expression greeting_is from _call_expression_1

        "...（むしする）":
            $ greeting_is = "Bad_greet_" + human_type
            call expression greeting_is from _call_expression_2

        "（ぼうはんブザーを にぎる）":
            "{i}ぼうはんブザーがはげしくなる！{/i}"
            $ buzzer_eve = "Buzzer_" + human_type
            call expression buzzer_eve from _call_expression_3

    window hide dissolve
    hide expression human_type with dissolve

    return