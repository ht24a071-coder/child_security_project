
init 2 python:
    suspicious_events.append("suspi_e_test_2")

label suspi_e_test_2:
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