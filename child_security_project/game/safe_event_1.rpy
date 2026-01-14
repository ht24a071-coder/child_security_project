
init 2 python:
    safe_events.append("safe_e_test_1")

label safe_e_test_1:
    python:
        import random
        
    show woman
    woman "学校終わり？おかえり！"

    menu:
        "ただいまー！":
            $ a = renpy.random.choice(WomanGreeting)
            woman "[a]"

        "...":
            $ a = renpy.random.choice(WomanMissGreeting)
            #スコアが減る選択肢
            woman "[a]"

    return