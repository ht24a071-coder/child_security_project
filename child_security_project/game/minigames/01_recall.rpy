init -1 python:
    # 振り返りミニゲーム（不審者当てクイズ）
    class RecallMinigame(BaseMinigame):
        def __init__(self, **kwargs):
            if "title" not in kwargs: kwargs["title"] = "ふりかえり"
            if "text" not in kwargs: kwargs["text"] = "きょう あった\nあやしいひとは だれ？"
            
            super(RecallMinigame, self).__init__(**kwargs)
            self.choices = []
            self.correct_index = -1
        
        def setup(self):
            # 遭遇した不審者を取得
            if not encountered_events: return False
            
            target_type, _ = encountered_events[-1]
            dummies = []
            all_types = ["stranger", "stranger2", "officer", "woman"] 
            
            for t in all_types:
                if t != target_type:
                    dummies.append(t)
            
            import random
            options = [target_type]
            while len(options) < 3:
                d = random.choice(dummies)
                options.append(d)
                
            random.shuffle(options)
            self.choices = options
            
            for i, opt in enumerate(self.choices):
                if opt == target_type:
                    self.correct_index = i
                    break
            
            return True

# -----------------------------------------------------------------------------
# ミニゲーム画面
# -----------------------------------------------------------------------------
screen recall_minigame_screen(game):
    modal True
    
    if not game.started:
        use minigame_intro_overlay(game)
    else:
        add Solid("#000000CC")
        
        vbox:
            align (0.5, 0.1)
            spacing 20
            text "きょう あった あやしいひとは？" size 50 xalign 0.5 color "#fff" outlines [(3, "#000", 0, 0)]
        
        hbox:
            align (0.5, 0.5)
            spacing 50
            
            for i, choice_type in enumerate(game.choices):
                button:
                    xysize (300, 500)
                    background "#ffffff22"
                    hover_background "#ffffff44"
                    
                    action Return(i) # 選択したインデックスを返す
                    
                    # 画像を表示
                    if choice_type == "stranger":
                        add "images/actor/stranger.png" zoom 0.5 align (0.5, 1.0)
                    elif choice_type == "stranger2":
                        add "images/actor/stranger2.png" zoom 0.5 align (0.5, 1.0)
                    elif choice_type == "officer":
                        add "images/actor/officer.png" zoom 0.5 align (0.5, 1.0)
                    elif choice_type == "woman":
                        add "images/actor/woman.png" zoom 0.5 align (0.5, 1.0)
                    else:
                        text "?" size 100 align (0.5, 0.5)

# -----------------------------------------------------------------------------
# 呼び出しラベル (unchanged logic)
# -----------------------------------------------------------------------------
label recall_minigame:
    if len(encountered_events) == 0:
        return 
        
    python:
        recall_game = RecallMinigame()
        is_ready = recall_game.setup()
        
    if not is_ready:
        return
        
    call screen recall_minigame_screen(recall_game)
    $ result_index = _return
    
    if result_index == recall_game.correct_index:
        play audio "audio/se_good.ogg"
        $ update_score(30)
        "{i}せいかい！よく おぼえていたね！{/i}"
    else:
        play audio "audio/se_bad.ogg"
        "{i}ざんねん...とくちょうを よく おぼえておこう。{/i}"
        
    return
