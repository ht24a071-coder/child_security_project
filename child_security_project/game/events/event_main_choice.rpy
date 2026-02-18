
# 共通選択肢フレームワーク
label event_main_choice(human_type):

    # officer player woman stranger
    show expression human_type with dissolve
    window show dissolve
    
    $ greeting = "Greet_" + human_type
    
    # 遭遇記録（到着時に参照するため）
    # human_type が "officer" なら "officer", それ以外なら "safe_person" として記録
    $ rec_event = "officer" if human_type == "officer" else "safe_person"
    $ record_encounter(human_type, rec_event)

    call expression greeting

    menu:
        "あいさつをする":
            $ greeting_is = "Is_greet_" + human_type
            call expression greeting_is

        "...（むしする）":
            $ greeting_is = "Bad_greet_" + human_type
            call expression greeting_is

        "（ぼうはんブザーを にぎる）":
            "{i}{rb}防犯{/rb}{rt}ぼうはん{/rt}ブザーが{rb}激{/rb}{rt}はげ{/rt}しく{rb}鳴{/rb}{rt}な{/rt}る！{/i}"
            $ buzzer_eve = "Buzzer_" + human_type
            call expression buzzer_eve

    window hide dissolve
    hide expression human_type with dissolve

    return