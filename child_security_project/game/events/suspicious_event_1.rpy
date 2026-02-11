# 不審者イベント1：お菓子で誘う不審者
# イベント登録は def_mapdat.rpy の event_pools で管理

label suspi_e_test_1:
    show stranger with dissolve
    stranger "{rb}君{/rb}{rt}きみ{/rt}{rb}学校{/rb}{rt}がっこう{/rt}{rb}帰{/rb}{rt}かえ{/rt}り？おいしいケーキがあるんだけど{rb}来{/rb}{rt}こ{/rt}ない？"

    menu:
        "いくー！":
            stranger "いい{rb}子{/rb}{rt}こ{/rt}だね～こっちこっち..."
            hide stranger
            scene black with fade
            
            "{i}{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}についていってはいけないよ！{/i}"
            "{i}「いかのおすし」を{rb}思{/rb}{rt}おも{/rt}い{rb}出{/rb}{rt}だ{/rt}そう！{/i}"
            
            jump game_over

        "ごめんなさい。まっすぐ{rb}帰{/rb}{rt}かえ{/rt}らないといけないんです":
            $ update_score(15)
            stranger "えー、つまんないな～"
            hide stranger with dissolve
            
            "{i}よくできた！{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}の{rb}誘{/rb}{rt}さそ{/rt}いはきっぱり{rb}断{/rb}{rt}ことわ{/rt}ろう！{/i}"

    return