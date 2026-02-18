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
            target_type, _unused = encountered_events[-1]
            
            # ダミーの不審者リスト（定義されてる画像から適当に）
            # ここでは簡易的に stranger, stranger2 を使いまわすが、理想はもっと種類があるべき
            # ダミー用に color matrix で色を変えたバージョンなどを用意するのも手
            
            dummies = []
            all_types = ["stranger", "stranger2", "officer", "woman", "teacher", "parent"]
            
            for t in all_types:
                if t != target_type:
                    dummies.append(t)
            
            # 3択を作る
            import random
            options = [target_type]
            
            # ダミーから重複なしで選ぶ
            if len(dummies) >= 2:
                selected_dummies = random.sample(dummies, 2)
                options.extend(selected_dummies)
            elif len(dummies) == 1:
                options.append(dummies[0])
                # 足りない場合は仕方ないので重複させるか、空白にするか
                # ここでは重複もやむなし（仕様上起きないはず）
                options.append(dummies[0])

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

    # ---------------------------------------------------------------
    # 背景アニメーション（謎解き・思い出し感 / 暗い青・グレー系）
    # ---------------------------------------------------------------
    # 霧のようにゆっくり浮遊する半透明の大きな図形
    add Solid("#001133", xsize=400, ysize=400):
        align (0.15, 0.3)
        at mg_bg_float(delay=0.0, amp=20)
    add Solid("#002244", xsize=300, ysize=300):
        align (0.85, 0.6)
        at mg_bg_float(delay=1.2, amp=15)
    add Solid("#001122", xsize=500, ysize=500):
        align (0.5, 0.8)
        at mg_bg_float(delay=0.6, amp=25)
    add Solid("#003355", xsize=250, ysize=250):
        align (0.2, 0.75)
        at mg_bg_float(delay=1.8, amp=18)

    # 上から降ってくる疑問符パーティクル（上昇の逆：yoffset正方向）
    # mg_particle_rise を反転させて「降下」に使う
    add Solid("#334466", xsize=6, ysize=6):
        align (0.1, 0.0)
        at mg_particle_rise(delay=0.0, rise=-500, period=4.0)
    add Solid("#445577", xsize=8, ysize=8):
        align (0.3, 0.0)
        at mg_particle_rise(delay=1.5, rise=-500, period=3.5)
    add Solid("#334466", xsize=5, ysize=5):
        align (0.6, 0.0)
        at mg_particle_rise(delay=0.8, rise=-500, period=4.5)
    add Solid("#556688", xsize=7, ysize=7):
        align (0.8, 0.0)
        at mg_particle_rise(delay=2.2, rise=-500, period=3.8)
    add Solid("#445577", xsize=6, ysize=6):
        align (0.45, 0.0)
        at mg_particle_rise(delay=1.0, rise=-500, period=4.2)

    # 横に流れる細い光の帯
    add Solid("#224466", xsize=1280, ysize=2) alpha 0.3:
        align (0.5, 0.35)
        at mg_bg_drift(delay=0.0, dist=40, period=5.0)
    add Solid("#335577", xsize=1280, ysize=2) alpha 0.3:
        align (0.5, 0.65)
        at mg_bg_drift(delay=2.0, dist=-40, period=4.5)

    # ---------------------------------------------------------------
    
    vbox:
        align (0.5, 0.1)
        spacing 20
        text "きょう あった あやしいひとは？" size 50 xalign 0.5 color "#fff" outlines [(3, "#000", 0, 0)]
    
    hbox:
        align (0.5, 0.5)
        spacing 50
        
        for i, choice_type in enumerate(game.choices):
            button:
                xysize (300, 600)
                background "#ffffff22"
                hover_background "#ffffff44"
                
                action Return(i) # 選択したインデックスを返す
                
                # 画像を表示
                # fit="contain" で枠内に収める
                $ img_path = ""
                if choice_type == "stranger":
                     $ img_path = "images/actor/stranger.png"
                elif choice_type == "stranger2":
                     $ img_path = "images/actor/stranger2.png"
                elif choice_type == "officer":
                     $ img_path = "images/actor/officer.png"
                elif choice_type == "woman":
                     $ img_path = "images/actor/woman.png"
                elif choice_type == "teacher":
                     $ img_path = "images/actor/teacher.png"
                elif choice_type == "parent":
                     $ img_path = "images/actor/woman3.png"
                
                if img_path:
                    # fit="cover" & align(0.5, 0.0) で顔付近を中心にトリミング表示
                    add Transform(img_path, fit="cover", xysize=(280, 580), align=(0.5, 0.0))
                else:
                    text "?" size 100 align (0.5, 0.5)

# -----------------------------------------------------------------------------
# 呼び出しラベル
# -----------------------------------------------------------------------------
label recall_minigame:
    
    # 到着時の会話イベント
    # モードによって相手を変える
    if game_mode == "going_school":
        # 先生 (teacher)
        show teacher at center with dissolve
        teacher "おはよう！　ぶじに　ついて　よかったわ。"
    else:
        # 親 (parent)
        show parent at center with dissolve
        parent "おかえり！　ぶじで　よかったわ。"

    # 不審者遭遇チェック
    if len(encountered_events) == 0:
        # 遭遇なし：平和な会話で終了
        if game_mode == "going_school":
            teacher "きょうは　あやしいひとは　いなかったみたいね。\nきょうも　げんきに　すごしましょう！"
        else:
            
            parent "きょうは　あやしいひとは　いなかったのね。\nてあらい　うがいを　しっかりしてね！"
        
        hide teacher
        hide parent
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
            teacher "きょうは　だれかに　あった？"
            pc "うん、ちいきの　ひとに　あったよ！"
            teacher "そう、あいさつできたかな？\nちいきの　ひとは　みんなを　まもってくれているのよ。"
        else:
            parent "きょうは　だれかに　あった？"
            pc "うん、ちいきの　ひとに　あったよ！"
            parent "そう、あいさつできた？\nこまっていることがあったら　そうだんしようね。"
            
        hide teacher
        hide parent
        return

    # ここから下は不審者（または怪しい知り合い）の場合
    if game_mode == "going_school":
        teacher "……あら？　なにか　あったの？"
        teacher "えっ、あやしいひとに　あったの！？\nどんな　ひとだったか　おしえてくれる？"
    else:
        parent "……えっ？　なにか　あったの？"
        parent "あやしいひとに　あったの！？\nどんな　ひとだったか　おしえて？"

    # ミニゲームセットアップ
    python:
        recall_game = RecallMinigame()
        is_ready = recall_game.setup()
        
    if not is_ready:
        "（おもいだせない……）"
        hide teacher
        hide parent
        return
        
    # ミニゲーム開始
    # 全キャラを一旦非表示（クイズ画面と被らないように）
    hide teacher
    hide parent
    hide woman
    hide officer
    hide stranger
    # UI一時非表示
    hide screen minimap
    hide screen score_hud
    
    call screen recall_minigame_screen(recall_game)
    $ result_index = _return
    
    # UI復帰
    show screen minimap
    show screen score_hud
    
    # クイズ後のキャラ再表示
    if game_mode == "going_school":
        show teacher at center with dissolve
    else:
        show parent at center with dissolve
    
    if result_index == recall_game.correct_index:
        play audio "audio/se_good.ogg"
        $ update_score(30, "ふしんしゃの とくちょうを おぼえていた")
        
        if game_mode == "going_school":
            teacher "そう……よく　おぼえていたわね。"
            if is_acquaintance:
                teacher "しらない ひとじゃなくても、いやなことを されたら すぐに おしえてね。\n先生から 親御さんに 連絡しておくわ。"
            else:
                teacher "すぐに　けいさつに　れんらくするわ！\nおしえてくれて　ありがとう。"
        else:
            parent "そう……よく　おぼえていたわね。"
            if is_acquaintance:
                parent "しっている ひとでも、いやなことを されたら すぐに おしえてね。\nなにか あったら すぐに ママに いうのよ。"
            else:
                parent "すぐに　けいさつに　れんらくするわ！\nぶじに　かえってこれて　ほんとうに　よかった！"
            
        "{i}せいかい！よく おぼえていたね！{/i}"
    else:
        play audio "audio/se_bad.ogg"
        
        if game_mode == "going_school":
            teacher "うーん、ちょっと　ちがうみたい……？\nでも、ぶじで　よかったわ。"
        else:
            parent "うーん、ひょっとして　みまちがいかな……？\nでも、ぶじで　よかったわ。"

        "{i}ざんねん...とくちょうを よく おぼえておこう。{/i}"
        
    hide teacher
    hide parent
    return
