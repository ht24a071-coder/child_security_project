# ========= 変数の初期化 =========
default mg_bar_pos = 0.0
default mg_bar_dir = 1.0
default mg_bar_running = False
default mg_bar_success = False

# ========= Python側の処理 =========
init python:
    def mg_bar_update_simple():
        global mg_bar_pos, mg_bar_dir, mg_bar_running
        
        if not mg_bar_running:
            return
            
        mg_bar_pos += 0.01 * mg_bar_dir
        
        if mg_bar_pos > 1.0:
            mg_bar_pos = 1.0
            mg_bar_dir = -1.0
        elif mg_bar_pos < 0.0:
            mg_bar_pos = 0.0
            mg_bar_dir = 1.0
            
        renpy.restart_interaction()

    def mg_bar_hit_simple():
        global mg_bar_pos, mg_bar_running, mg_bar_success
        
        if 0.375 <= mg_bar_pos <= 0.625:
            mg_bar_success = True
        else:
            mg_bar_success = False
            
        mg_bar_running = False
        renpy.hide_screen("mg_bar_simple_screen")
        return  # ← これで画面が閉じる！

# ========= ミニゲーム本体ラベル =========
label mg_bar_simple:
    "タイミングを合わせて攻撃だ！"
    
    $ mg_bar_pos = 0.0
    $ mg_bar_dir = 1.0
    $ mg_bar_running = True
    $ mg_bar_success = False
    
    call screen mg_bar_simple_screen
    
    if mg_bar_success:
        "クリティカルヒット！！"
    else:
        "空振りしてしまった……。"
    
    return

# ========= ミニゲーム用スクリーン（修正済み）=========
screen mg_bar_simple_screen():
    modal True
    
    timer 0.02 repeat True action Function(mg_bar_update_simple)
    
    # Return() を追加して、入力後に必ず画面終了
    key "K_SPACE" action [Function(mg_bar_hit_simple), Return()]
    key "K_RETURN" action [Function(mg_bar_hit_simple), Return()]
    key "mousedown_1" action [Function(mg_bar_hit_simple), Return()]
    
    frame:
        align (0.5, 0.5)
        has vbox
        
        text "スペース / Enter / クリックで攻撃！"
        
        bar:
            value mg_bar_pos
            range 1.0
            xmaximum 400
            
        hbox:
            spacing 10
            text "狙え！" color "#ffffff"
            text "← 安全 / 真ん中がベスト / 危険 →" color "#ffaaaa"
    
    text "緑ゾーン: 中央25％" align (0.5, 0.7) color "#00ff00"
