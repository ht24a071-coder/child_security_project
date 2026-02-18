# =============================================================================
# 安全教室イベント：先生や警察官から防犯の話を聞く（スコアアップ枠）
# =============================================================================

label safe_e_lesson_teacher:
    call show_woman_wrapper from _call_show_woman_wrapper_1
    # 先生役として woman を使用（あるいは専用画像があればそちら）
    
    woman "あ、[player_name]さん。こんにちは。"
    
    pc "先生、こんにちは！"
    
    woman "元気に挨拶できてえらいわね。"
    woman "そういえば、最近不審者が増えているのを知ってる？"
    
    pc "えっ、そうなの？"
    
    woman "ええ。「お母さんが怪我した」とか「子犬を見に行こう」とか言って、"
    woman "子供を連れ去ろうとする悪い人がいるみたいなの。"
    
    woman "もしそんなことを言われても、絶対についていっちゃだめよ。"
    woman "知っている人でも、お家の人に確認してからにしてね。"
    
    pc "うん、わかった！"
    
    woman "よし、気をつけて帰ってね。"
    
    $ update_score(15)
    
    "{i}先生の話をよく聞けました！{/i}"
    "{i}「いかのおすし」を思い出して、自分の身を守ろう！{/i}"
    
    call hide_woman_wrapper from _call_hide_woman_wrapper_3
    return

label safe_e_lesson_officer:
    call show_officer_wrapper from _call_show_officer_wrapper_1
    
    officer "やあ、気をつけて帰っているかな？"
    
    pc "うん、大丈夫！"
    
    officer "えらいぞ。実はな、最近「道案内をしてほしい」と言ってくる不審者がいるんだ。"
    officer "大人が子供に道を尋ねるなんて、ちょっと変だろ？"
    officer "今の時代、スマホもあるしね。"
    
    officer "もし道を聞かれても、「わかりません」と言って、すぐに離れるんだぞ。"
    officer "近すぎて捕まらないように、距離を取るのが大事だ。"
    
    pc "わかった！距離をとる！"
    
    officer "よし、気をつけてな。"
    
    $ update_score(15)
    
    "{i}お巡りさんのアドバイスを聞けました！{/i}"
    "{i}大人に話しかけられても、距離を保つことが大事だよ。{/i}"
    
    call hide_officer_wrapper from _call_hide_officer_wrapper_1
    return
