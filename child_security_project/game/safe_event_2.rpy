default  boyu_flag = False

init 2 python:
    safe_events.append("safe_e_test_2")

label safe_e_test_2:

    if boyu_flag:
        "やつはきえた"
    else:
        show boy
        "あ、同じクラスの伊藤博文くんだ。"
        t "やぁ"
        $ boyu_flag = True
    
    return