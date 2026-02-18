# =============================================================================
# 共通：防犯ブザー反撃（ミニゲーム失敗時の救済措置）
# =============================================================================

label fallback_buzzer_sequence:
    # ミニゲーム失敗後に呼ばれる
    # scene black  <-- Removed to keep context visible
    # with None
    
    # 緊迫した演出
    "つかまりそうになった！！"
    "でも まだ ぼうはんブザーが ある！！"
    
    # ブザーチャンス画面呼び出し
    # UI一時非表示
    hide screen minimap
    hide screen score_hud
    
    call screen buzzer_chance_screen
    
    # UI復帰
    show screen minimap
    show screen score_hud
    
    if _return == "success":
        jump .buzzer_success
    else:
        jump .buzzer_fail

label .buzzer_success:
    play audio "audio/buzzer.mp3"
    # フラッシュ演出（背景を消さないように show を使用）
    show expression Solid("#ffffff") as flash zorder 1000
    with None
    pause 0.1
    hide flash with dissolve
    
    "ピピピピピ！！"
    
    "おおきな おとが なった！"
    "ふしんしゃは ひるんで にげていった！"
    
    return "success"

label .buzzer_fail:
    "ブザーを ならせなかった..."
    return "fail"


# -----------------------------------------------------------------------------
# ブザーチャンス画面
# -----------------------------------------------------------------------------
screen buzzer_chance_screen():
    modal True
    zorder 300
    
    default time_limit = 5.0
    default start_time = None
    
    # 画面更新用タイマー
    timer 0.05 repeat True action Function(renpy.restart_interaction)
    
    if start_time is None:
        $ start_time = renpy.get_game_runtime()
        
    $ elapsed = renpy.get_game_runtime() - start_time
    $ remaining = max(0.0, time_limit - elapsed)
    
    # タイムアウト
    if remaining <= 0:
        timer 0.1 action Return("fail")
        
    add Solid("#550000") alpha 0.5
    
    vbox:
        align (0.5, 0.5)
        spacing 30
        
        text "ブザーをならせ！！" size 80 color "#ffff00" bold True outlines [(4, "#f00", 0, 0)] xalign 0.5 at truecenter
        
        text "のこり [remaining:.1f]" size 40 color "#fff" xalign 0.5
        
        # ボタン
        imagebutton:
            idle Transform("images/00000436.png", fit="contain", xysize=(300, 300)) # 画像サイズを調整
            hover Transform("images/00000436.png", fit="contain", xysize=(300, 300), matrixcolor=BrightnessMatrix(0.2)) # ホバー時は明るく
            action Return("success")
            xalign 0.5
            
        # 代替テキストボタン（画像がない場合用）
        textbutton "おす！":
            text_size 60
            text_color "#fff"
            background "#ff0000"
            padding (40, 20)
            action Return("success")
            xalign 0.5
            
    # キー入力対応
    key "K_SPACE" action Return("success")
    key "dismiss" action Return("success")