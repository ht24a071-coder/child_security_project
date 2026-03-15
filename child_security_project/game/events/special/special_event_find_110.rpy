# スペシャルイベント：110番を知る・使う知識を学ぶ
# イベント登録は def_mapdat.rpy の event_pools で管理

label special_e_find_110:
    show woman with dissolve
    woman "あら、こんにちは。ひとりでおかえり？"
    woman "ねえ、もしなにかこわいことがあったら、どこにでんわすればいいかしってる？"

    menu:
        "110ばん！":
            $ update_score(15, "110ばんのクイズ")
            woman "せいかい！すごいね、ちゃんとしってるんだ。"
            woman "なにかこわいことがあったら、すぐに110ばんにでんわしてね。"
            woman "けいさつのおにいさんおねえさんがたすけてくれるからね。"
            call show_feedback("quiz_110_correct") from _call_fb_110_1

        "119ばん？":
            $ update_score(5, "110ばんのクイズ")
            woman "おしい！119ばんはきゅうきゅうしゃやしょうぼうしゃだよ。"
            woman "こわいひとにあったときは110ばんにでんわしてね。"
            woman "110は「ひゃくとおばん」っておぼえるといいよ！"
            call show_feedback("quiz_110_close") from _call_fb_110_2

        "わからない...":
            woman "だいじょうぶ、いまおぼえようね！"
            woman "こわいことがあったら110ばんにでんわするの。"
            woman "「ひゃくとおばん」、おまわりさんがきてくれるよ！"
            call show_feedback("quiz_110_unknown") from _call_fb_110_3

    woman "きをつけてかえってね！"
    hide woman with dissolve

    return
