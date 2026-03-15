# スペシャルイベント：ふしんしゃ遭遇ときの対処フローを学ぶ（いかのおすし）
# イベント登録は def_mapdat.rpy の event_pools で管理

label special_e_encounter_flow:
    $ setup_stranger()
    show stranger with dissolve
    stranger "ちょっとちょっと、きみ～"
    stranger "ちょっとこっちにきてくれない？"

    menu:
        "はい、なんですか？（ちかづく）":
            stranger "（にやり）いいこだね…"
            
            call show_feedback("encounter_approach_fail") from _call_fb_flow_1

        "（むししてあるきつづける）":
            $ update_score(15, "むしして げきたい")
            stranger "あら、いっちゃうの…"
            hide stranger with dissolve
            call show_feedback("encounter_avoid_success") from _call_fb_flow_2
            return

        "（おおきなこえで）たすけてー！":
            $ update_score(20, "おおごえで げきたい")
            stranger "うわっ…！（にげていく）"
            hide stranger with dissolve
            call show_feedback("encounter_shout_success") from _call_fb_flow_3
            return

    hide stranger with dissolve
    
    call show_feedback("encounter_remind_ikanosushi") from _call_fb_flow_4

    return
