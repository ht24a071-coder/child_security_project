init -1 python:
    # イベントIDと、表示したい背景画像の対応表
    # 書かれていないイベントは「今歩いている場所の背景」のままになります
    event_bg_map = {
        # "イベントラベル名" : "画像名（またはimage定義名）",
        "safe_e_test_1"      : "back_town",      # 例のイベント
        "suspicious_event_1" : "back_danger",  # 路地裏
        "suspicious_event_2" : "back_dark"
    }

label update_walking_background:
    if current_step <= 3:
        scene back_town with dissolve
    elif current_step <= 7:
        scene back_town with dissolve
    else:
        scene back_tunnel with dissolve
    return

# 画像定義
image back_town = "images/back/back_town.png"
image back_dark = "images/back/back_dark.png"
image back_danger = "images/back/back_danger.png"