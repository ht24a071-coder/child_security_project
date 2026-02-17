label Greet_woman:
    woman "{rb}学校{/rb}{rt}がっこう{/rt}{rb}終{/rb}{rt}お{/rt}わり？おかえり！"
    return

label Is_greet_woman:
    $ update_score(-5)
    woman "{rb}元気{/rb}{rt}げんき{/rt}なご{rb}挨拶{/rb}{rt}あいさつ{/rt}だね。"
    "{i}{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}には、あまり{rb}近{/rb}{rt}ちか{/rt}づいたり{rb}話{/rb}{rt}はな{/rt}しかけたりしないほうがいいよ。{/i}"
    "{i}もしものことがあるから、{rb}距離{/rb}{rt}きょり{/rt}を{rb}取{/rb}{rt}と{/rt}ろうね。{/i}"
    return

label Bad_greet_woman:
    $ update_score(10)
    woman "..."
    "{i}よくできた！{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}とは{rb}距離{/rb}{rt}きょり{/rt}を{rb}取{/rb}{rt}と{/rt}るのが{rb}正解{/rb}{rt}せいかい{/rt}だよ。{/i}"
    return

label Buzzer_woman:
    # ブザーは過剰反応かもしれないが、警戒心としてはOK
    $ update_score(5) 
    woman "えっ！？"
    woman "びっくりした..."
    "{i}{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}が{rb}怖{/rb}{rt}こわ{/rt}かったら、ブザーを{rb}準備{/rb}{rt}じゅんび{/rt}するのはいいことだよ。{/i}"
    return

# 110番の家イベントは、別の安全なイベント（先生や警察官）に移すべきか、
# あるいは「無視」した後に教えてくれる？
# 無視した後に教えるのは不自然。
# 今回は「挨拶で110番を教わる」ルートは削除し、別途「安全教室イベント」などで教えることにする。
# したがって greet_110 以下のロジックは削除（または無効化）。
