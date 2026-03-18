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
            
            # イベントに登場しない「誰だか分からない人」リスト（不正解用）
            # stranger, officer, woman, teacher, parent は正解になり得るので、それ以外を使用
            stranger_actors = ["man3", "man4", "man5", "woman2", "woman4", "woman5", "officer2", "officer3", "officer4", "officer5"]
            sprite_paths = {
                "stranger": "images/actor/stranger.png",
                "stranger2": "images/actor/stranger2.png",
                "officer": "images/actor/officer.png",
                "officer2": "images/actor/officer2.png",
                "officer3": "images/actor/officer3.png",
                "officer4": "images/actor/officer4.png",
                "officer5": "images/actor/officer5.png",
                "woman": "images/actor/woman.png",
                "woman2": "images/actor/woman2.png",
                "woman3": "images/actor/woman3.png",
                "woman4": "images/actor/woman4.png",
                "woman5": "images/actor/woman5.png",
                "man3": "images/actor/man3.png",
                "man4": "images/actor/man4.png",
                "man5": "images/actor/man5.png",
                "teacher": "images/actor/teacher.png",
                "parent": "images/actor/woman3.png"
            }

            # 遭遇した全てのひとに対してクイズを生成
            temp_questions = []
            is_multi = len(encountered_events) > 1

            for idx, encounter in enumerate(encountered_events):
                encounter_num = idx + 1
                
                if is_multi:
                    q1_text = "{}にんめに あったのは だれかな？".format(encounter_num)
                    q2_text = "{}にんめの ひとは どんな とくちょうだったかな？".format(encounter_num)
                    q3_text = "{}にんめの ひとに なにを されたかな？".format(encounter_num)
                else:
                    q1_text = "このなかの だれに あったかな？"
                    q2_text = "どんな とくちょうが あったかな？"
                    q3_text = "なにを されたかな？"

                encounter_questions = []

                # 1. 見ためクイズ（画像せんたく）
                target_type = encounter["char_type"]
                options = [target_type]
                
                # 不正解の選択肢を「絶対に違う人」にする
                dummies = [d for d in stranger_actors if d != target_type]
                random.shuffle(dummies)
                options.extend(dummies[:2])
                random.shuffle(options)
                
                encounter_questions.append({
                    "type": "image",
                    "text": q1_text,
                    "choices": options,
                    "correct_index": options.index(target_type),
                    "sprite_map": sprite_paths
                })

                # ふしんしゃの場合のみ追加の質問
                if encounter.get("is_stranger"):
                    # 2. 特徴クイズ（テキストせんたく）
                    target_trait = encounter.get("trait", "おおきい")
                    t_options = [target_trait]
                    t_dummies = [t for t in stranger_traits if t != target_trait]
                    random.shuffle(t_dummies)
                    # 重複排除
                    t_unique_dummies = []
                    for d in t_dummies:
                        if d not in t_unique_dummies and d != target_trait:
                            t_unique_dummies.append(d)
                    
                    t_options.extend(t_unique_dummies[:2])
                    random.shuffle(t_options)
                    
                    encounter_questions.append({
                        "type": "text",
                        "text": q2_text,
                        "choices": t_options,
                        "correct_index": t_options.index(target_trait)
                    })

                    # 3. 行動クイズ（テキストせんたく）
                    event_name = encounter["event_name"]
                    target_action = event_action_map.get(event_name, "あやしい こえを かけられた")
                    a_options = [target_action]
                    
                    import copy
                    a_dummies = copy.copy(dummy_action_list)
                    random.shuffle(a_dummies)
                    a_options.extend(a_dummies[:2])
                    random.shuffle(a_options)

                    encounter_questions.append({
                        "type": "text",
                        "text": q3_text,
                        "choices": a_options,
                        "correct_index": a_options.index(target_action)
                    })

                # ふしんしゃの場合は3問から2問をランダムに選ぶ（順番は維持）
                if len(encounter_questions) >= 3:
                    indices = sorted(random.sample(range(len(encounter_questions)), 2))
                    encounter_questions = [encounter_questions[i] for i in indices]

                temp_questions.extend(encounter_questions)

            # クイズの問題数の制限とシャッフルをなくし、遭遇順で出題する
            self.questions = temp_questions

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
        teacher "あったひと　１にんにつき、２つの　しつもんを　するわね。"
    else:
        parent "きょうは　だれかに　あった？　どんな　ひとだったか　おしえてくれる？"
        parent "あったひと　１にんにつき、２つの　しつもんを　するね。"

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
            play audio "audio/正解、ピンポーン_2.mp3"
            "{b}せいかい！{/b}"
            $ update_score(10, "クイズにせいかいした")
        else:
            play audio "audio/ブブー、不正解.mp3"
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
