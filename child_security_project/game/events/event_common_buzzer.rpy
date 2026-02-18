# =============================================================================
# 共通：防犯ブザー反撃（ミニゲーム失敗時の救済措置）
# =============================================================================

label fallback_buzzer_sequence:
    # ミニゲーム失敗後に呼ばれる
    scene black
    with None
    
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
    scene flash_white
    "ピピピピピ！！"
    
    "おおきな おとが なった！"
    "ふしんしゃは ひるんで にげていった！"
    
    return # 呼び出し元に戻る（成功扱い）

label .buzzer_fail:
    "ブザーを ならせなかった..."
    return # 呼び出し元に戻る（失敗扱い -> Game Overへ）


# -----------------------------------------------------------------------------
# ブザーチャンス画面
# -----------------------------------------------------------------------------
screen buzzer_chance_screen():
    modal True
    zorder 300
    
    default time_limit = 3.0
    default start_time = None
    
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
            idle "gui/button/buzzer_idle.png" # 仮の画像、なければテキストボタン
            hover "gui/button/buzzer_hover.png"
            action Return("success")
            xalign 0.5
            
        # 代替テキストボタン（画像がない場合用）
        textbutton "PUSH!!":
            text_size 60
            text_color "#fff"
            background "#ff0000"
            padding (40, 20)
            action Return("success")
            xalign 0.5
            
    # キー入力対応
    key "K_SPACE" action Return("success")
    key "dismiss" action Return("success")
