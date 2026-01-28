# =============================================================================
# ゲーム終了フィードバック画面
# =============================================================================

default feedback_title = ""
default feedback_score = 0
default feedback_message = ""
default feedback_tips = []
default feedback_is_clear = True

# =============================================================================
# フィードバック表示スクリーン（フルスクリーン・中央配置）
# =============================================================================
screen game_feedback():
    modal True
    
    # 背景
    if feedback_is_clear:
        add Solid("#2E7D32")
    else:
        add Solid("#C62828")
    
    # メインコンテンツ（中央配置）
    frame:
        align (0.5, 0.5)
        xsize 800
        padding (40, 40)
        background None
        
        vbox:
            xalign 0.5
            spacing 25
            
            # タイトル
            text feedback_title:
                size 60
                color "#FFFFFF"
                bold True
                xalign 0.5
                text_align 0.5
                outlines [(3, "#000000", 0, 0)]
            
            # スコア表示
            frame:
                background "#00000080"
                padding (50, 20)
                xalign 0.5
                
                vbox:
                    spacing 10
                    xalign 0.5
                    
                    text "スコア":
                        size 28
                        color "#FFEB3B"
                        xalign 0.5
                    
                    text "[feedback_score] てん":
                        size 60
                        color "#FFFFFF"
                        bold True
                        xalign 0.5
                        outlines [(2, "#000000", 0, 0)]
            
            # メッセージ
            text feedback_message:
                size 26
                color "#FFFFFF"
                xalign 0.5
                text_align 0.5
                outlines [(2, "#000000", 0, 0)]
            
            # アドバイス
            if len(feedback_tips) > 0:
                frame:
                    background "#FFFFFF30"
                    padding (30, 15)
                    xalign 0.5
                    
                    vbox:
                        spacing 8
                        xalign 0.5
                        
                        for tip in feedback_tips:
                            text tip:
                                size 22
                                color "#FFFFFF"
                                xalign 0.5
                                text_align 0.5
            
            # 続けるボタン
            null height 10
            
            textbutton "つづける":
                action Return()
                xalign 0.5
                text_size 32
                text_color "#FFFFFF"
                text_hover_color "#FFEB3B"
                text_outlines [(2, "#000000", 0, 0)]
