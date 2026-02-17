# =============================================================================
# 振り返りミニゲーム（不審者当てクイズ）
# =============================================================================

init python:
    class RecallMinigame:
        def __init__(self):
            self.choices = []
            self.correct_index = -1
            self.question_text = "きょう どの ひとは あやしかった？"

        def setup(self):
            # 遭遇した不審者を取得
            if not encountered_events:
                # 遭遇してないならスキップ用のフラグとか
                return False
            
            # 直近の遭遇、あるいはランダムに1つ選ぶ
            # ここでは「最後に遭遇した人」を正解にする
            target_type, _ = encountered_events[-1]
            
            # ダミーの不審者リスト（定義されてる画像から適当に）
            # ここでは簡易的に stranger, stranger2 を使いまわすが、理想はもっと種類があるべき
            # ダミー用に color matrix で色を変えたバージョンなどを用意するのも手
            
            dummies = []
            all_types = ["stranger", "stranger2", "officer", "woman"] # officerとか混ぜる？
            
            for t in all_types:
                if t != target_type:
                    dummies.append(t)
            
            # 3択を作る
            import random
            options = [target_type]
            # ダミーから2つ選ぶ（足りなければ重複許容）
            while len(options) < 3:
                d = random.choice(dummies)
                options.append(d)
                
            random.shuffle(options)
            self.choices = options
            
            # 正解のインデックスを探す
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
                # choice_type から画像パスを解決
                # ここでは簡易実装として if文で
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
# 呼び出しラベル
# -----------------------------------------------------------------------------
label recall_minigame:
    if len(encountered_events) == 0:
        return # 遭遇してなければスキップ
        
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
