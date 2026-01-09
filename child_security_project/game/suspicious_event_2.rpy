
init 2 python:
    suspicious_events.append("suspi_e_test_2")

label suspi_e_test_2:
    show rightman
    officer "やあ、こんにちは！"

    menu:
        "こんにちは！":
            officer "元気な返事だね"

        "...":
            #スコアが減る選択肢
            officer "挨拶はちゃんとするようにね。"
            
    officer "右へ行くんだ。"

    menu:
        "右へ行く":
            officer "いい子だ.."

        "右へ行かない":
            officer "終わったな。"

    return