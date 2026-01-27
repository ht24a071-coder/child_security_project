# 安全イベント1：町の人との挨拶
# イベント登録は def_mapdat.rpy の event_pools で管理

label safe_e_test_1:
    show woman with dissolve
    woman "{rb}学校{/rb}{rt}がっこう{/rt}{rb}終{/rb}{rt}お{/rt}わり？おかえり！"

    menu:
        "ただいまー！":
            $ total_score += 10
            $ a = renpy.random.choice(WomanGreeting)
            woman "[a]"
            "{i}{rb}挨拶{/rb}{rt}あいさつ{/rt}できたね！えらい！{/i}"

        "...（{rb}無視{/rb}{rt}むし{/rt}する）":
            $ a = renpy.random.choice(WomanMissGreeting)
            woman "[a]"
            "{i}{rb}挨拶{/rb}{rt}あいさつ{/rt}を{rb}返{/rb}{rt}かえ{/rt}すと、{rb}地域{/rb}{rt}ちいき{/rt}の{rb}人{/rb}{rt}ひと{/rt}があなたを{rb}覚{/rb}{rt}おぼ{/rt}えてくれるよ。{/i}"

    hide woman with dissolve
    return