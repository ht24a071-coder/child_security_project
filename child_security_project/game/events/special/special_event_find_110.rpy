# スペシャルイベント：110番を知る・使う知識を学ぶ
# イベント登録は def_mapdat.rpy の event_pools で管理

label special_e_find_110:
    show woman with dissolve
    woman "あら、こんにちは。{rb}一人{/rb}{rt}ひとり{/rt}でお{rb}帰{/rb}{rt}かえ{/rt}り？"
    woman "ねえ、もし{rb}何{/rb}{rt}なに{/rt}か{rb}怖{/rb}{rt}こわ{/rt}いことがあったら、どこに{rb}電話{/rb}{rt}でんわ{/rt}すればいいか{rb}知{/rb}{rt}し{/rt}ってる？"

    menu:
        "110{rb}番{/rb}{rt}ばん{/rt}！":
            $ update_score(15)
            woman "{rb}正解{/rb}{rt}せいかい{/rt}！すごいね、ちゃんと{rb}知{/rb}{rt}し{/rt}ってるんだ。"
            woman "{rb}何{/rb}{rt}なに{/rt}か{rb}怖{/rb}{rt}こわ{/rt}いことがあったら、すぐに110{rb}番{/rb}{rt}ばん{/rt}に{rb}電話{/rb}{rt}でんわ{/rt}してね。"
            woman "{rb}警察{/rb}{rt}けいさつ{/rt}のお{rb}兄{/rb}{rt}にい{/rt}さんお{rb}姉{/rb}{rt}ねえ{/rt}さんが{rb}助{/rb}{rt}たす{/rt}けてくれるからね。"
            call show_feedback("quiz_110_correct") from _call_fb_110_1

        "119{rb}番{/rb}{rt}ばん{/rt}？":
            $ update_score(5)
            woman "{rb}惜{/rb}{rt}お{/rt}しい！119{rb}番{/rb}{rt}ばん{/rt}は{rb}救急車{/rb}{rt}きゅうきゅうしゃ{/rt}や{rb}消防車{/rb}{rt}しょうぼうしゃ{/rt}だよ。"
            woman "{rb}怖{/rb}{rt}こわ{/rt}い{rb}人{/rb}{rt}ひと{/rt}に{rb}会{/rb}{rt}あ{/rt}ったときは110{rb}番{/rb}{rt}ばん{/rt}に{rb}電話{/rb}{rt}でんわ{/rt}してね。"
            woman "110は「ひゃくとおばん」って{rb}覚{/rb}{rt}おぼ{/rt}えるといいよ！"
            call show_feedback("quiz_110_close") from _call_fb_110_2

        "わからない...":
            woman "{rb}大丈夫{/rb}{rt}だいじょうぶ{/rt}、{rb}今{/rb}{rt}いま{/rt}{rb}覚{/rb}{rt}おぼ{/rt}えようね！"
            woman "{rb}怖{/rb}{rt}こわ{/rt}いことがあったら110{rb}番{/rb}{rt}ばん{/rt}に{rb}電話{/rb}{rt}でんわ{/rt}するの。"
            woman "「ひゃくとおばん」、お{rb}巡{/rb}{rt}まわ{/rt}りさんが{rb}来{/rb}{rt}き{/rt}てくれるよ！"
            call show_feedback("quiz_110_unknown") from _call_fb_110_3

    woman "{rb}気{/rb}{rt}き{/rt}をつけて{rb}帰{/rb}{rt}かえ{/rt}ってね！"
    hide woman with dissolve

    return
