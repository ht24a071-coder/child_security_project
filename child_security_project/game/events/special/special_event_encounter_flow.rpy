# スペシャルイベント：不審者遭遇時の対処フローを学ぶ（いかのおすし）
# イベント登録は def_mapdat.rpy の event_pools で管理

label special_e_encounter_flow:
    $ setup_stranger()
    show stranger with dissolve
    stranger "ちょっとちょっと、{rb}君{/rb}{rt}きみ{/rt}～"
    stranger "ちょっとこっちに{rb}来{/rb}{rt}き{/rt}てくれない？"

    menu:
        "はい、{rb}何{/rb}{rt}なん{/rt}ですか？（{rb}近{/rb}{rt}ちか{/rt}づく）":
            stranger "（にやり）いい{rb}子{/rb}{rt}こ{/rt}だね…"
            
            call show_feedback("encounter_approach_fail") from _call_fb_flow_1

        "（{rb}無視{/rb}{rt}むし{/rt}して{rb}歩{/rb}{rt}ある{/rt}き{rb}続{/rb}{rt}つづ{/rt}ける）":
            $ update_score(15, "むしして げきたい")
            stranger "あら、{rb}行{/rb}{rt}い{/rt}っちゃうの…"
            hide stranger with dissolve
            call show_feedback("encounter_avoid_success") from _call_fb_flow_2
            return

        "（{rb}大{/rb}{rt}おお{/rt}きな{rb}声{/rb}{rt}こえ{/rt}で）{rb}助{/rb}{rt}たす{/rt}けてー！":
            $ update_score(20, "おおごえで げきたい")
            stranger "うわっ…！（{rb}逃{/rb}{rt}に{/rt}げていく）"
            hide stranger with dissolve
            call show_feedback("encounter_shout_success") from _call_fb_flow_3
            return

    hide stranger with dissolve
    
    call show_feedback("encounter_remind_ikanosushi") from _call_fb_flow_4

    return
