# =============================================================================
# 安全教室イベント：先生や警察官から防犯の話を聞く（スコアアップ枠）
# =============================================================================

label safe_e_lesson_dispatch:
    # 状況に応じて、先生か警察官かを振り分けるラッパーイベント
    
    if game_mode == "going_school":
        # 登校時は警察官（見守り）
        call safe_e_lesson_officer from _call_safe_e_lesson_officer
    else:
        # 下校時
        # 学校付近なら先生
        if current_node in ["start_point", "school_park"]:
            call safe_e_lesson_teacher from _call_safe_e_lesson_teacher
        else:
            # それ以外は警察官
            call safe_e_lesson_officer from _call_safe_e_lesson_officer_1
    return

label safe_e_lesson_teacher:
    show teacher with dissolve
    # 先生役として teacher を使用
    
    $ record_encounter("teacher", "teacher")
    
    teacher "あ、[player_name]さん。こんにちは。"
    
    pc "{rb}先生{/rb}{rt}せんせい{/rt}、こんにちは！"
    
    teacher "{rb}元気{/rb}{rt}げんき{/rt}に{rb}挨拶{/rb}{rt}あいさつ{/rt}できてえらいわね。"
    teacher "そういえば、{rb}最近{/rb}{rt}さいきん{/rt}{rb}不審者{/rb}{rt}ふしんしゃ{/rt}が{rb}増{/rb}{rt}ふ{/rt}えているのを{rb}知{/rb}{rt}し{/rt}ってる？"
    
    pc "えっ、そうなの？"
    
    teacher "ええ。「お{rb}母{/rb}{rt}かあ{/rt}さんが{rb}怪我{/rb}{rt}けが{/rt}した」とか「{rb}子犬{/rb}{rt}こいぬ{/rt}を{rb}見{/rb}{rt}み{/rt}に{rb}行{/rb}{rt}い{/rt}こう」とか{rb}言{/rb}{rt}い{/rt}って、"
    teacher "{rb}子供{/rb}{rt}こども{/rt}を{rb}連{/rb}{rt}つ{/rt}れ{rb}去{/rb}{rt}さ{/rt}ろうとする{rb}悪{/rb}{rt}わる{/rt}い{rb}人{/rb}{rt}ひと{/rt}がいるみたいなの。"
    
    teacher "もしそんなことを{rb}言{/rb}{rt}い{/rt}われても、{rb}絶対{/rb}{rt}ぜったい{/rt}についていっちゃだめよ。"
    teacher "{rb}知{/rb}{rt}し{/rt}っている{rb}人{/rb}{rt}ひと{/rt}でも、お{rb}家{/rb}{rt}うち{/rt}の{rb}人{/rb}{rt}ひと{/rt}に{rb}確認{/rb}{rt}かくにん{/rt}してからにしてね。"
    
    pc "うん、わかった！"
    
    teacher "よし、{rb}気{/rb}{rt}き{/rt}をつけて{rb}帰{/rb}{rt}かえ{/rt}ってね。"
    
    $ update_score(15, "あんぜんきょうしつ")
    
    call show_feedback("lesson_teacher") from _call_fb_lesson_1
    
    hide teacher with dissolve
    return

label safe_e_lesson_officer:
    call show_officer_wrapper from _call_show_officer_wrapper_1
    
    $ record_encounter("officer", "officer")
    
    officer "やあ、{rb}気{/rb}{rt}き{/rt}をつけて{rb}帰{/rb}{rt}かえ{/rt}っているかな？"
    
    pc "うん、{rb}大丈夫{/rb}{rt}だいじょうぶ{/rt}！"
    
    officer "えらいぞ。{rb}実{/rb}{rt}じつ{/rt}はな、{rb}最近{/rb}{rt}さいきん{/rt}「{rb}道案内{/rb}{rt}みちあんない{/rt}をしてほしい」と{rb}言{/rb}{rt}い{/rt}ってくる{rb}不審者{/rb}{rt}ふしんしゃ{/rt}がいるんだ。"
    officer "{rb}大人{/rb}{rt}おとな{/rt}が{rb}子供{/rb}{rt}こども{/rt}に{rb}道{/rb}{rt}みち{/rt}を{rb}尋{/rb}{rt}たず{/rt}ねるなんて、ちょっと{rb}変{/rb}{rt}へん{/rt}だろ？"
    officer "{rb}今{/rb}{rt}いま{/rt}の{rb}時代{/rb}{rt}じだい{/rt}、スマホもあるしね。"
    
    officer "もし{rb}道{/rb}{rt}みち{/rt}を{rb}聞{/rb}{rt}き{/rt}かれても、「わかりません」と{rb}言{/rb}{rt}い{/rt}って、すぐに{rb}離{/rb}{rt}はな{/rt}れるんだぞ。"
    officer "{rb}近{/rb}{rt}ちか{/rt}すぎて{rb}捕{/rb}{rt}つか{/rt}まらないように、{rb}距離{/rb}{rt}きょり{/rt}を{rb}取{/rb}{rt}と{/rt}るのが{rb}大事{/rb}{rt}だいじ{/rt}だ。"
    
    pc "わかった！{rb}距離{/rb}{rt}きょり{/rt}をとる！"
    
    officer "よし、{rb}気{/rb}{rt}き{/rt}をつけてな。"
    
    $ update_score(15, "あんぜんきょうしつ")
    
    call show_feedback("lesson_officer") from _call_fb_lesson_2
    
    call hide_officer_wrapper from _call_hide_officer_wrapper_1
    return
