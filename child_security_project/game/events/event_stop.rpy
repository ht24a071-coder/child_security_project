
label Event_Force_Stop:

    call screen full_image_show("images/Night.png")

    window show dissolve

    "{i}{rb}暗{/rb}{rt}くら{/rt}くなってしまった。{rb}寄{/rb}{rt}よ{/rt}り{rb}道{/rb}{rt}みち{/rt}せず、{rb}明{/rb}{rt}あか{/rt}るいうちに{rb}帰{/rb}{rt}かえ{/rt}ろう。{/i}"

    window hide dissolve

    jump game_over
    return


label Event_Warning_Stop:

    call screen full_image_show("images/Sunset.png")
    
    window show dissolve

    "{i}{rb}暗{/rb}{rt}くら{/rt}くなってきた。{rb}早{/rb}{rt}はや{/rt}く{rb}帰{/rb}{rt}かえ{/rt}ろう。{/i}"

    window hide dissolve

    return

screen full_image_show(img_path):
    # 他のUIを触らせない
    modal True

    # 画面全体に画像を表示
    add img_path:
        xsize 1.0  # 横幅いっぱい
        ysize 1.0  # 縦幅いっぱい
        fit "contain" # 画像比率を維持して最大表示（隙間なくなら "cover"）
        xalign 0.5 yalign 0.5

    # 画面全体を覆う「何もしないボタン」に Return() を持たせる
    # これにより、画面のどこをクリックしても画像が消えてシナリオに戻る
    button:
        action Return()
        xfill True
        yfill True
        background None # ボタンを透明にする

