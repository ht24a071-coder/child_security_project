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
    
    # 到着時の会話イベント
    # モードによって相手を変える
    if game_mode == "going_school":
        # 先生 (woman2)
        show woman2 at center with dissolve
        "せんせい" "おはよう！　ぶじに　ついて　よかったわ。"
    else:
        # 親 (woman)
        show woman at center with dissolve
        "お母さん" "おかえり！　ぶじで　よかったわ。"

    # 不審者遭遇チェック
    if len(encountered_events) == 0:
        # 遭遇なし：平和な会話で終了
        if game_mode == "going_school":
            "せんせい" "きょうは　あやしいひとは　いなかったみたいね。\nきょうも　げんきに　すごしましょう！"
        else:
            "お母さん" "きょうは　あやしいひとは　いなかったのね。\nてあらい　うがいを　しっかりしてね！"
        
        hide woman2
        hide woman
        return

    # 遭遇あり：タイプを確認
    # 直近の遭遇を取得
    python:
        last_event = encountered_events[-1]
        # タプル (char_type, event_name)
        # char_type: "stranger", "stranger2", "woman", "officer"
        # event_name: "acquaintance", "safe_person", "mom_injury", etc.
        
        encounter_char = last_event[0]
        encounter_event = last_event[1]
            
        # 安全な人（警察官など）かどうか
        is_safe_person = encounter_event in ["officer", "safe_person"]
        # 知り合いかどうか
        is_acquaintance = encounter_event == "acquaintance"

    if is_safe_person:
        # 安全な人の場合は報告だけして終了（ミニゲームなし）
        if game_mode == "going_school":
            "せんせい" "きょうは　だれかに　あった？"
            pc "うん、ちいきの　ひとに　あったよ！"
            "せんせい" "そう、あいさつできたかな？\nちいきの　ひとは　みんなを　まもってくれているのよ。"
        else:
            "お母さん" "きょうは　だれかに　あった？"
            pc "うん、ちいきの　ひとに　あったよ！"
            "お母さん" "そう、あいさつできた？\nこまっていることがあったら　そうだんしようね。"
            
        hide woman2
        hide woman
        return

    # ここから下は不審者（または怪しい知り合い）の場合
    if game_mode == "going_school":
        "せんせい" "……あら？　なにか　あったの？"
        "せんせい" "えっ、あやしいひとに　あったの！？\nどんな　ひとだったか　おしえてくれる？"
    else:
        "お母さん" "……えっ？　なにか　あったの？"
        "お母さん" "あやしいひとに　あったの！？\nどんな　ひとだったか　おしえて？"

    # ミニゲームセットアップ
    python:
        recall_game = RecallMinigame()
        is_ready = recall_game.setup()
        
    if not is_ready:
        "（おもいだせない……）"
        hide woman2
        hide woman
        return
        
    # ミニゲーム開始
    call screen recall_minigame_screen(recall_game)
    $ result_index = _return
    
    if result_index == recall_game.correct_index:
        play audio "audio/se_good.ogg"
        $ update_score(30)
        
        if game_mode == "going_school":
            "せんせい" "そう……よく　おぼえていたわね。"
            if is_acquaintance:
                "せんせい" "しらない ひとじゃなくても、いやなことを されたら すぐに おしえてね。\n先生から 親御さんに 連絡しておくわ。"
            else:
                "せんせい" "すぐに　けいさつに　れんらくするわ！\nおしえてくれて　ありがとう。"
        else:
            "お母さん" "そう……よく　おぼえていたわね。"
            if is_acquaintance:
                "お母さん" "しっている ひとでも、いやなことを されたら すぐに おしえてね。\nなにか あったら すぐに ママに いうのよ。"
            else:
                "お母さん" "すぐに　けいさつに　れんらくするわ！\nぶじに　かえってこれて　ほんとうに　よかった！"
            
        "{i}せいかい！よく おぼえていたね！{/i}"
    else:
        play audio "audio/se_bad.ogg"
        
        if game_mode == "going_school":
            "せんせい" "うーん、ちょっと　ちがうみたい……？\nでも、ぶじで　よかったわ。"
        else:
            "お母さん" "うーん、ひょっとして　みまちがいかな……？\nでも、ぶじで　よかったわ。"

        "{i}ざんねん...とくちょうを よく おぼえておこう。{/i}"
        
    hide woman2
    hide woman
    return

