# =============================================================================
# あんぜん教室イベント：せんせいやけいさつかんからぼうはんのはなしを聞く（スコアアップ枠）
# =============================================================================

label safe_e_lesson_dispatch:
    # 状況に応じて、せんせいかけいさつかんかを振りふんけるラッパーイベント
    
    if game_mode == "going_school":
        # とうこうときはけいさつかん（見守り）
        call safe_e_lesson_officer from _call_safe_e_lesson_officer
    else:
        # げこうとき
        # がっこう付近ならせんせい
        if current_node in ["start_point", "school_park"]:
            call safe_e_lesson_teacher from _call_safe_e_lesson_teacher
        else:
            # それいがいはけいさつかん
            call safe_e_lesson_officer from _call_safe_e_lesson_officer_1
    return

label safe_e_lesson_teacher:
    show teacher with dissolve
    # せんせい役として teacher を使用
    
    $ record_encounter("teacher", "teacher")
    
    teacher "あ、[player_name]さん。こんにちは。"
    
    pc "せんせい、こんにちは！"
    
    teacher "げんきにあいさつできてえらいわね。"
    teacher "そういえば、さいきんふしんしゃがふえているのをしってる？"
    
    pc "えっ、そうなの？"
    
    teacher "ええ。「おかあさんがけがした」とか「こいぬをみにいこう」とかいって、"
    teacher "こどもをつれさろうとするわるいひとがいるみたいなの。"
    
    teacher "もしそんなことをいわれても、ぜったいについていっちゃだめよ。"
    teacher "しっているひとでも、おうちのひとにかくにんしてからにしてね。"
    
    pc "うん、わかった！"
    
    teacher "よし、きをつけてかえってね。"
    
    $ update_score(15, "あんぜんきょうしつ")
    
    call show_feedback("lesson_teacher") from _call_fb_lesson_1
    
    hide teacher with dissolve
    return

label safe_e_lesson_officer:
    call show_officer_wrapper from _call_show_officer_wrapper_1
    
    $ record_encounter("officer", "officer")
    
    officer "やあ、きをつけてかえっているかな？"
    
    pc "うん、だいじょうぶ！"
    
    officer "えらいぞ。じつはな、さいきん「みちあんないをしてほしい」といってくるふしんしゃがいるんだ。"
    officer "おとながこどもにみちをたずねるなんて、ちょっとへんだろ？"
    officer "いまのじだい、スマホもあるしね。"
    
    officer "もしみちをきかれても、「わかりません」といって、すぐにはなれるんだぞ。"
    officer "ちかすぎてつかまらないように、きょりをとるのがだいじだ。"
    
    pc "わかった！きょりをとる！"
    
    officer "よし、きをつけてな。"
    
    $ update_score(15, "あんぜんきょうしつ")
    
    call show_feedback("lesson_officer") from _call_fb_lesson_2
    
    call hide_officer_wrapper from _call_hide_officer_wrapper_1
    return
