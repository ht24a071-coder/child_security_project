label Event_Force_Stop:

    scene Night with pixellate
    window show dissolve

    "{i}くらくなってしまった。よりみちせず、あかるいうちにかえろう。{/i}"

    window hide dissolve

    call game_over(set_message="よるになってしまった。") from _call_game_over
    return

label Event_Force_School_Stop:

    window show dissolve

    "{i}ちこくしてしまった！{/i}"

    window hide dissolve

    call game_over(set_message="ちこくしてしまった...") from _call_game_over_school
    return


label Event_Warning_Stop:

    scene Sunset with pixellate
    window show dissolve

    "{i}くらくなってきた。はやくかえろう。{/i}"

    window hide dissolve

    return

label Event_Warning_School_Stop:

    window show dissolve

    "{i}ちこくしちゃうかも。いそいで がっこうにむかおう！{/i}"

    window hide dissolve

    return

screen full_image_show(img_path):
    # 他のUIを触らせない
    modal True

    # 画面全からだに画像を表示
    add img_path:
        xsize 1.0  # よこ幅いっぱい
        ysize 1.0  # 縦幅いっぱい
        fit "contain" # 画像比率を維持してさいだい表示（隙間なくなら "cover"）
        xalign 0.5 yalign 0.5

    # 画面全からだを覆う「なにもしないボタン」に Return() を持たせる
    # これにより、画面のどこをクリックしても画像が消えてシナリオにもどる
    button:
        action Return()
        xfill True
        yfill True
        background None # ボタンを透明にする

