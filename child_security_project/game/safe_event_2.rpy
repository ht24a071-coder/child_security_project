
init 2 python:
    safe_events.append("safe_e_test_2")

label safe_e_test_2:
    python:
        import random
        
    show rightman
    officer "やあ、こんにちは！"

    menu:
        "こんにちは！":
            $ a = renpy.random.choice(OfficerGreeting)
            officer "[a]"

        "...":
            $ a = renpy.random.choice(OfficerMissGreeting)
            #スコアが減る選択肢
            officer "[a]"

    return