# =============================================================================
# ふしんしゃイベント：知り合い（かお見知り）の誘い
# =============================================================================

label suspi_e_acquaintance:


    call show_stranger_wrapper("suspi_e_acquaintance") from _call_show_stranger_wrapper_acquaintance

    # 特徴を表示
    $ current_trait = next((e['trait'] for e in encountered_events if e['event_name'] == 'suspi_e_acquaintance'), "")
    if current_trait:
        "（{color=#ff0000}[current_trait]{/color} ひとのようだ。）"

    
    $ play_voice("auto")
    stranger "おーい、[player_name]ちゃん！"
    $ s_text = get_commute_text("がっこうおわりかい？", "がっこうに いくのかい？")
    stranger "[s_text] えらいねえ。"

    $ pc_greeting = get_commute_text("こんばんは。", "おはよう。")
    pc "あ、[pc_greeting]"
    $ pc_inner = get_commute_text("こんばんは", "おはよう")
    pc "（やさしそうなおじさんだ。しってるひとだしあんしんかな？）"

    stranger "おかあさんは げんきにしてるかい？"
    pc "うん、げんきだよ。"
    
    stranger "そうかそうか。じつはね、{color=#ff0000}あっちに かわいいこいぬがいるんだ。{/color}"
    stranger "[player_name]ちゃん、いぬすきだよね？ ちょっとみていかない？"

    pc "えっ、こいぬ..."
    pc "（みたいな... しってるひとだし...）"
    
    # ここでせんたく肢
    menu:
        "ついていく":
            jump .follow_acquaintance
        
        "ことわる":
            jump .refuse_acquaintance
        
        "ぼうはんブザーを ならす":
            jump .buzzer_acquaintance

# -----------------------------------------------------------------------------
# ついていく（GAME OVER）
# -----------------------------------------------------------------------------
label .follow_acquaintance:
    pc "はーい！なになに？"
    
    stranger "こっちだよ...もっと おくのほう..."
    
    "おじさんは ひとけのない ほうへ あるいていく。"
    
    call hide_stranger_wrapper from _call_hide_stranger_wrapper
    scene black with fade
    
    call show_feedback("acquaintance_follow") from _call_fb_acq_1
    
    jump game_over

# -----------------------------------------------------------------------------
# 断る（正解）
# -----------------------------------------------------------------------------
label .refuse_acquaintance:
    $ update_score(10, "ことわった")
    
    pc "ごめんなさい！いま いそいでるんです！"
    
    play music "audio/Pinch!!.mp3" fadein 1.0 volume 0.3
    stranger "えー、いいじゃないか。ちょっとだけだよ？"
    
    pc "（しつこいな...）"
    pc "ママに おこられるから！"
    
    "あわてて そのばを はなれた。"
    
    hide stranger with dissolve
    
    # 助けに来るひとをばしょでけってい
    python:
        h_tag, _unused = get_helper_data()
    
    if h_tag == "officer":
        show officer with dissolve
        officer "どうしたの！？"
    else:
        show teacher with dissolve
        teacher "どうしたの！？"
    
    call show_feedback("acquaintance_refuse") from _call_fb_acq_2
    
    if h_tag == "officer":
        hide officer with dissolve
    else:
        hide teacher with dissolve
    
    return

# -----------------------------------------------------------------------------
# ぼうはんブザー（大正解）
# -----------------------------------------------------------------------------
label .buzzer_acquaintance:
    $ play_se("buzzer")
    
    $ update_score(15, "ぼうはんブザーで げきたい")
    
    "ピピピピピ！！"
    stranger "おいおい！なにをするんだ！"
    
    "おじさんは びっくりして いなくなった。"
    hide stranger with dissolve
    
    # 助けに来るひとをばしょでけってい
    python:
        h_tag, _unused = get_helper_data()
    
    if h_tag == "officer":
        show officer with dissolve
        officer "どうしたの？ ブザーをならしたのね！"
        hide officer with dissolve
    else:
        show teacher with dissolve
        teacher "どうしたの？ ブザーをならしたのね！"
        hide teacher with dissolve
    
    pc "（ちょっと こわかった...）"
    
    call show_feedback("acquaintance_buzzer") from _call_fb_acq_3
    
    return
