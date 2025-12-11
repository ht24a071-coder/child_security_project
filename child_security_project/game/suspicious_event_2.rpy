
init 2 python:
    suspicious_events.append("suspi_e_test_2")

label suspi_e_test_2:
    scene back_dark with fade
    show rightman
    "そこのキミ"
    i "右へ行かないか？"
    "え？"
    i "右へ行くんだ。"

    menu:
        "右へ行く":
            i "いい子だ.."

        "右へ行かない":
            i "終わったな。"

    return