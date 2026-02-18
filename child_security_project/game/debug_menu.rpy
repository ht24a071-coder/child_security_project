# =============================================================================
# デバッグメニュー
# =============================================================================
screen debug_event_menu():
    tag menu
    modal True
    
    add Solid("#000000CC")
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        padding (40, 40)
        
        vbox:
            spacing 20
            
            text "イベントデバッグメニュー" size 40 xalign 0.5 color "#fff"
            
            vpgrid:
                cols 2
                spacing 20
                scrollbars "vertical"
                mousewheel True
                draggable True
                side_yfill True
                
                # 不審者イベント
                textbutton "不審者遭遇 (挨拶)" action Start("encounter_e_stranger")
                textbutton "不審者 (ケーキ誘拐)" action Start("suspi_e_test_1")
                textbutton "不審者 (車連れ去り)" action Start("suspi_e_test_2")
                
                # 強制連れ去り系
                textbutton "車での連れ去り (即)" action Start("suspi_e_car")
                textbutton "母親の怪我詐欺" action Start("suspi_e_mom_injury")
                
                # 安全教室・警察
                textbutton "安全教室 (先生)" action Start("safe_e_lesson_teacher")
                textbutton "安全教室 (警察)" action Start("safe_e_lesson_officer")
                
                # その他
                textbutton "顔見知りの誘い" action Start("suspi_e_acquaintance")
                textbutton "大声テスト" action Start("test_mic_minigame")

            textbutton "戻る" action Return() xalign 0.5
