
init 2 python:
    suspicious_events.append("suspi_e_test_1")

label suspi_e_test_1:
    python:
        import random
        
    show woman
    woman "君学校帰り？おいしいケーキがあるんだけど来ない？"

    menu:
        "いくー！":
            $ a = renpy.random.choice(WomanGreeting)
            woman "[a]"

        "ごめんなさい。まっすぐ帰らないといけないんです":
            $ a = renpy.random.choice(WomanMissGreeting)
            #スコアが減る選択肢
            woman "[a]"

    return