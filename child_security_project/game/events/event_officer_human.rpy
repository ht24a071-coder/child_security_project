
label Greet_officer:
    officer "こんにちは！"
    return

label Is_greet_officer:
    $ update_score(10)
    $ a = renpy.random.choice(OfficerGreeting)
    officer "[a]"
    "{i}おまわりさんにも{rb}元気{/rb}{rt}げんき{/rt}に{rb}挨拶{/rb}{rt}あいさつ{/rt}できたね！{/i}"
    return

label Bad_greet_officer:
    $ update_score(-5)
    $ a = renpy.random.choice(OfficerMissGreeting)
    officer "[a]"
    "{i}{rb}挨拶{/rb}{rt}あいさつ{/rt}は{rb}大切{/rb}{rt}たいせつ{/rt}だよ。{rb}次{/rb}{rt}つぎ{/rt}はがんばろう！{/i}"
    return

label Buzzer_officer:
    $ update_score(-5)
    $ a = renpy.random.choice(OfficerBuzzer)
    officer "[a]"
    "{i}{rb}意味{/rb}{rt}いみ{/rt}もなく、{rb}防犯{/rb}{rt}ぼうはん{/rt}ブザーを{rb}鳴{/rb}{rt}な{/rt}らしてはいけないよ！{/i}"
    return