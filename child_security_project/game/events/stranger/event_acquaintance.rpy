# =============================================================================
# 不審者イベント：知り合い（顔見知り）の誘い
# =============================================================================

label suspi_e_acquaintance:


    call show_stranger_wrapper from _call_show_stranger_wrapper_acquaintance

    # 特徴を表示
    $ current_trait = next((e['trait'] for e in encountered_events if e['event_name'] == 'acquaintance'), "")
    if current_trait:
        "（[current_trait] ひとのようだ。）"

    
    $ play_voice("003")
    stranger "おーい、[player_name]ちゃん！"
    $ s_text = get_commute_text("{rb}学校{/rb}{rt}がっこう{/rt}おわりかい？", "{rb}学校{/rb}{rt}がっこう{/rt}に いくのかい？")
    stranger "[s_text] えらいねえ。"

    $ pc_greeting = get_commute_text("こんばんは。", "おはよう。")
    pc "あ、[pc_greeting]"
    $ pc_inner = get_commute_text("こんばんは", "おはよう")
    pc "（優しそうなおじさんだ。知ってる人だし安心かな？）"

    stranger "お{rb}母{/rb}{rt}かあ{/rt}さんは {rb}元気{/rb}{rt}げんき{/rt}にしてるかい？"
    pc "うん、{rb}元気{/rb}{rt}げんき{/rt}だよ。"
    
    stranger "そうかそうか。{rb}実{/rb}{rt}じつ{/rt}はね、あっちに {rb}可愛{/rb}{rt}かわい{/rt}い{rb}子犬{/rb}{rt}こいぬ{/rt}がいるんだ。"
    stranger "[player_name]ちゃん、{rb}犬{/rb}{rt}いぬ{/rt}{rb}好{/rb}{rt}す{/rt}きだよね？ ちょっと{rb}見{/rb}{rt}み{/rt}ていかない？"

    pc "えっ、{rb}子犬{/rb}{rt}こいぬ{/rt}..."
    pc "（{rb}見{/rb}{rt}み{/rt}たいな... {rb}知{/rb}{rt}し{/rt}ってる{rb}人{/rb}{rt}ひと{/rt}だし...）"
    
    # ここで選択肢
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
    
    "おじさんは ひと{rb}気{/rb}{rt}け{/rt}のない ほうへ あるいていく。"
    
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
    
    stranger "えー、いいじゃないか。ちょっとだけだよ？"
    
    pc "（しつこいな...）"
    pc "ママに おこられるから！"
    
    "あわてて そのばを はなれた。"
    
    call hide_stranger_wrapper(dissolve) from _call_hide_stranger_wrapper_1
    
    call show_feedback("acquaintance_refuse") from _call_fb_acq_2
    
    return

# -----------------------------------------------------------------------------
# 防犯ブザー（大正解）
# -----------------------------------------------------------------------------
label .buzzer_acquaintance:
    play audio "audio/buzzer.mp3"
    
    $ update_score(15, "ぼうはんブザーで げきたい")
    
    "ピピピピピ！！"
    stranger "おいおい！なにをするんだ！"
    
    "おじさんは びっくりして いなくなった。"
    call hide_stranger_wrapper(dissolve) from _call_hide_stranger_wrapper_2
    
    pc "（ちょっと こわかった...）"
    
    call show_feedback("acquaintance_buzzer") from _call_fb_acq_3
    
    return
