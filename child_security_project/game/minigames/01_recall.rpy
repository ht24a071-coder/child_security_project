# =============================================================================
# 振り返りミニゲーム（ふしんしゃ当てクイズ）
# =============================================================================

init python:
    class RecallMinigame:
        def __init__(self):
            self.questions = []
            self.current_q_index = 0
            self.score = 0

        def setup(self):
            if not encountered_events:
                return False
            
            import random
            
            # 遭遇した全てのひとに対してクイズを生成
            for encounter in encountered_events:
                # 1. 見ためクイズ（画像せんたく）
                target_type = encounter["char_type"]
                options = [target_type]
                dummies = ["stranger", "stranger2", "officer", "woman", "teacher", "parent"]
                dummies = [d for d in dummies if d != target_type]
                options.extend(random.sample(dummies, 2))
                random.shuffle(options)
                
                self.questions.append({
                    "type": "image",
                    "text": "このなかの だれに あったかな？",
                    "choices": options,
                    "correct_index": options.index(target_type),
                    "sprite_map": {
                        "stranger": "images/actor/stranger.png",
                        "stranger2": "images/actor/stranger2.png",
                        "officer": "images/actor/officer.png",
                        "woman": "images/actor/woman.png",
                        "teacher": "images/actor/teacher.png",
                        "parent": "images/actor/woman3.png"
                    }
                })

                # ふしんしゃの場合のみ追加の質問
                if encounter.get("is_stranger"):
                    # 2. 特徴クイズ（テキストせんたく）
                    target_trait = encounter["trait"]
                    t_options = [target_trait]
                    t_dummies = [t for t in stranger_traits if t != target_trait]
                    t_options.extend(random.sample(t_dummies, 2))
                    random.shuffle(t_options)
                    
                    self.questions.append({
                        "type": "text",
                        "text": "どんな とくちょうが あったかな？",
                        "choices": t_options,
                        "correct_index": t_options.index(target_trait)
                    })

                    # 3. 行動クイズ（テキストせんたく）
                    event_name = encounter["event_name"]
                    target_action = event_action_map.get(event_name, "なにかをされた")
                    a_options = [target_action]
                    a_dummies = [v for k, v in event_action_map.items() if v != target_action]
                    a_options.extend(random.sample(a_dummies, min(2, len(a_dummies))))
                    random.shuffle(a_options)

                    self.questions.append({
                        "type": "text",
                        "text": "なにを されたかな？",
                        "choices": a_options,
                        "correct_index": a_options.index(target_action)
                    })

            return True

        def get_current_question(self):
            if self.current_q_index < len(self.questions):
                return self.questions[self.current_q_index]
            return None

        def next_question(self, selected_index):
            q = self.get_current_question()
            if q is not None and selected_index == q["correct_index"]:
                is_correct = True
            else:
                is_correct = False
            
            self.current_q_index += 1
            return is_correct

# -----------------------------------------------------------------------------
# ミニゲーム画面
# -----------------------------------------------------------------------------
screen recall_minigame_screen(game):
    modal True
    add Solid("#000000CC")

    # ---------------------------------------------------------------
    # 背景アニメーション
    # ---------------------------------------------------------------
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

    # 帯
    add Solid("#224466", xsize=1280, ysize=2) alpha 0.3:
        align (0.5, 0.35)
        at mg_bg_drift(delay=0.0, dist=40, period=5.0)
    add Solid("#335577", xsize=1280, ysize=2) alpha 0.3:
        align (0.5, 0.65)
        at mg_bg_drift(delay=2.0, dist=-40, period=4.5)

    $ current_q = game.get_current_question()
    
    if current_q:
        $ q_text = current_q.get("text", "")
        vbox:
            align (0.5, 0.1)
            spacing 20
            text "[q_text]" size 50 xalign 0.5 color "#fff" outlines [(3, "#000", 0, 0)]
            text "第 [game.current_q_index + 1] 問 / 全 [len(game.questions)] 問" size 24 xalign 0.5 color "#aaa"

        if current_q["type"] == "image":
            hbox:
                align (0.5, 0.5)
                spacing 50
                for i, choice_type in enumerate(current_q["choices"]):
                    button:
                        xysize (300, 600)
                        background "#ffffff22"
                        hover_background "#ffffff44"
                        action Return(i)
                        
                        $ img_path = current_q["sprite_map"].get(choice_type, "")
                        if img_path:
                            add Transform(img_path, fit="cover", xysize=(280, 580), align=(0.5, 0.0))
                        else:
                            text "?" size 100 align (0.5, 0.5)
        else:
            # テキストかたち式のせんたく肢（特徴や行動）
            vbox:
                align (0.5, 0.5)
                spacing 20
                for i, choice_text in enumerate(current_q["choices"]):
                    textbutton "[choice_text]":
                        xsize 800
                        padding (20, 20)
                        background Solid("#ffffff22")
                        hover_background Solid("#ffffff44")
                        text_size 32
                        text_xalign 0.5
                        action Return(i)

# -----------------------------------------------------------------------------
# 呼び出しラベル
# -----------------------------------------------------------------------------
label recall_minigame:
    
    # とうちゃくじの会はなしイベント
    if game_mode == "going_school":
        show teacher at center with dissolve
        teacher "おはよう！　ぶじに　ついて　よかったわ。"
    else:
        show parent at center with dissolve
        parent "おかえり！　ぶじで　よかったわ。"

    # 遭遇チェック
    if not encountered_events:
        if game_mode == "going_school":
            teacher "きょうは　だれにも　あわなかったみたいね。あんぜんに　これて　えらかったわ！"
        else:
            parent "きょうは　だれにも　あわなかったのね。あんぜんに　かえれて　えらかったわ！"
        hide teacher
        hide parent
        return

    # ミニゲームセットアップ
    python:
        recall_minigame_obj = RecallMinigame()
        is_ready = recall_minigame_obj.setup()
        
    if not is_ready:
        hide teacher
        hide parent
        return

    # 会はなしを挟む
    if game_mode == "going_school":
        teacher "きょうは　だれかに　あったかな？　どんな　ひとだったか　おもいだしてみましょう。"
    else:
        parent "きょうは　だれかに　あった？　どんな　ひとだったか　おしえてくれる？"

    # UI一じ非表示
    hide screen minimap
    hide screen score_hud
    hide teacher
    hide parent

    # クイズループ
    while recall_minigame_obj.get_current_question() is not None:
        call screen recall_minigame_screen(recall_minigame_obj)
        $ is_correct = recall_minigame_obj.next_question(_return)
        
        if is_correct:
            play audio "audio/se_good.ogg"
            "{b}せいかい！{/b}"
            $ update_score(10, "クイズにせいかいした")
        else:
            play audio "audio/se_bad.ogg"
            "{b}ざんねん...{/b}"

    # UI復帰
    show screen minimap
    show screen score_hud
    
    # 最終的なフィードバック
    if game_mode == "going_school":
        show teacher at center with dissolve
        teacher "よく　おしえてくれたわね。ありがとう！"
        hide teacher
    else:
        show parent at center with dissolve
        parent "よく　おしえてくれたわね。ありがとう！"
        hide parent
    
    return
