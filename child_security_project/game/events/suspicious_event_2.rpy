# 不審者イベント2：車に乗せようとする不審者
# イベント登録は def_mapdat.rpy の event_pools で管理

label suspi_e_test_2:
    show stranger with dissolve
    stranger "ねえ、{rb}道{/rb}{rt}みち{/rt}に{rb}迷{/rb}{rt}まよ{/rt}っちゃったんだ。{rb}車{/rb}{rt}くるま{/rt}で{rb}送{/rb}{rt}おく{/rt}ってあげようか？"

    menu:
        "{rb}乗{/rb}{rt}の{/rt}ります！":
            stranger "よかった、じゃあこっちに..."
            hide stranger
            scene black with fade
            
            "{i}{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}の{rb}車{/rb}{rt}くるま{/rt}には{rb}乗{/rb}{rt}の{/rt}っちゃダメ！{/i}"
            "{i}「いかのおすし」の「の」={rb}乗{/rb}{rt}の{/rt}らない！{/i}"
            
            jump game_over

        "{rb}大丈夫{/rb}{rt}だいじょうぶ{/rt}です。{rb}自分{/rb}{rt}じぶん{/rt}で{rb}帰{/rb}{rt}かえ{/rt}れます":
            $ update_score(15)
            stranger "そう...じゃあね..."
            hide stranger with dissolve
            
            "{i}えらい！{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}の{rb}車{/rb}{rt}くるま{/rt}には{rb}絶対{/rb}{rt}ぜったい{/rt}{rb}乗{/rb}{rt}の{/rt}らないでね！{/i}"

    return