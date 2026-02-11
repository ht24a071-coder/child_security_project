# 安全イベント2：おまわりさんとの挨拶
# イベント登録は def_mapdat.rpy の event_pools で管理

label safe_e_test_2:
    show officer with dissolve
    officer "こんにちは！{rb}学校{/rb}{rt}がっこう{/rt}の{rb}帰{/rb}{rt}かえ{/rt}りかな？"

    menu:
        "こんにちは！":
            $ update_score(10)
            $ a = renpy.random.choice(OfficerGreeting)
            officer "[a]"
            "{i}おまわりさんにも{rb}元気{/rb}{rt}げんき{/rt}に{rb}挨拶{/rb}{rt}あいさつ{/rt}できたね！{/i}"

        "...（{rb}無視{/rb}{rt}むし{/rt}する）":
            $ a = renpy.random.choice(OfficerMissGreeting)
            officer "[a]"
            "{i}{rb}挨拶{/rb}{rt}あいさつ{/rt}は{rb}大切{/rb}{rt}たいせつ{/rt}だよ。{rb}次{/rb}{rt}つぎ{/rt}はがんばろう！{/i}"

    hide officer with dissolve
    return