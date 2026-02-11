# 日常イベント：こども110番の家発見
# 町の人たちの憩いの場で、挨拶を通じて110番の家の存在を知る
# イベント登録は def_mapdat.rpy の event_pools で管理

# =====================================================
# こども110番の家を発見するイベント
# =====================================================
label daily_e_find_110house:

    "{rb}歩{/rb}{rt}ある{/rt}いていると、{rb}公園{/rb}{rt}こうえん{/rt}のベンチで{rb}町{/rb}{rt}まち{/rt}の{rb}人{/rb}{rt}ひと{/rt}たちが{rb}話{/rb}{rt}はな{/rt}しているのが{rb}見{/rb}{rt}み{/rt}えた。"
    
    show woman with dissolve
    
    woman "あら、こんにちは！{rb}学校{/rb}{rt}がっこう{/rt}{rb}帰{/rb}{rt}かえ{/rt}り？"

    menu:
        "こんにちは！":
            jump .greet_110
        
        "...（{rb}通{/rb}{rt}とお{/rt}り{rb}過{/rb}{rt}す{/rt}ぎる）":
            jump .ignore_110

label .greet_110:
    $ update_score(5)
    
    woman "{rb}元気{/rb}{rt}げんき{/rt}ね！えらいえらい。"
    woman "ねえ、あそこに{rb}見{/rb}{rt}み{/rt}える「こども110{rb}番{/rb}{rt}ばん{/rt}の{rb}家{/rb}{rt}いえ{/rt}」って{rb}知{/rb}{rt}し{/rt}ってる？"
    
    menu:
        "{rb}知{/rb}{rt}し{/rt}ってる！":
            woman "すごい！ちゃんと{rb}覚{/rb}{rt}おぼ{/rt}えてるんだね。"
            $ flag_know_110 = True
            $ update_score(10)
            jump .explain_110
        
        "{rb}知{/rb}{rt}し{/rt}らない...":
            woman "じゃあ{rb}教{/rb}{rt}おし{/rt}えてあげるね！"
            jump .explain_110
        
        "なにそれ？":
            woman "いいことを{rb}教{/rb}{rt}おし{/rt}えてあげる！"
            jump .explain_110

label .explain_110:
    woman "「こども110{rb}番{/rb}{rt}ばん{/rt}の{rb}家{/rb}{rt}いえ{/rt}」はね、"
    woman "{rb}困{/rb}{rt}こま{/rt}ったときや{rb}怖{/rb}{rt}こわ{/rt}いことがあったとき、"
    woman "{rb}助{/rb}{rt}たす{/rt}けてもらえるお{rb}家{/rb}{rt}うち{/rt}やお{rb}店{/rb}{rt}みせ{/rt}のことだよ。"
    
    woman "あの{rb}旗{/rb}{rt}はた{/rt}が{rb}目印{/rb}{rt}めじるし{/rt}なの。{rb}覚{/rb}{rt}おぼ{/rt}えておいてね！"
    
    # フラグ獲得
    $ flag_know_110 = True
    
    "「こども110{rb}番{/rb}{rt}ばん{/rt}の{rb}家{/rb}{rt}いえ{/rt}」の{rb}場所{/rb}{rt}ばしょ{/rt}を{rb}覚{/rb}{rt}おぼ{/rt}えた！"
    
    woman "{rb}何{/rb}{rt}なに{/rt}かあったら、あそこに{rb}逃{/rb}{rt}に{/rt}げ{rb}込{/rb}{rt}こ{/rt}むんだよ。"
    woman "{rb}気{/rb}{rt}き{/rt}をつけて{rb}帰{/rb}{rt}かえ{/rt}ってね！"
    
    $ update_score(15)
    
    "{i}すばらしい！{rb}町{/rb}{rt}まち{/rt}の{rb}人{/rb}{rt}ひと{/rt}と{rb}挨拶{/rb}{rt}あいさつ{/rt}して、{rb}大切{/rb}{rt}たいせつ{/rt}なことを{rb}教{/rb}{rt}おし{/rt}えてもらったね。{/i}"
    
    hide woman with dissolve
    return

label .ignore_110:
    woman "あら...{rb}急{/rb}{rt}いそ{/rt}いでるのかな。"
    
    hide woman with dissolve
    
    "{i}{rb}挨拶{/rb}{rt}あいさつ{/rt}をすると、{rb}町{/rb}{rt}まち{/rt}の{rb}人{/rb}{rt}ひと{/rt}から{rb}大切{/rb}{rt}たいせつ{/rt}なことを{rb}教{/rb}{rt}おし{/rt}えてもらえることがあるよ。{/i}"
    
    return
