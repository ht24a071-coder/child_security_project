# =============================================================================
# メインスクリプト
# 登校・下校両方に対応した設計
# =============================================================================

default game_mode = "going_home"

# =============================================================================
# 共通初期化処理
# =============================================================================
label initialize_game:
    $ current_node = "start_point"
    $ previous_node = None
    
    show screen inactivity_guard
    $ current_step = 0
    $ used_events = set()

    $ flag_know_110 = False
    $ has_encountered_suspicious = False
    $ total_score = 0
    hide screen score_hud

    scene black

    "なまえを きめよう！"
    call screen profile_setup

    show screen score_hud
    return

# =============================================================================
# 登校モード開始
# =============================================================================
label going_school_start:
    $ game_mode = "going_school"
    call initialize_game
    
    scene back_town with fade
    pc "さあ、がっこうに いこう！"
    
    jump travel_loop

# =============================================================================
# 下校モード開始
# =============================================================================
label going_home_start:
    $ game_mode = "going_home"
    call initialize_game
    
    scene back_town with fade
    pc "さあ、いえに かえろう！"
    
    jump travel_loop

# =============================================================================
# マップベース移動ループ
# =============================================================================
label travel_loop:
    $ node_data = world_map.get(current_node)
    $ current_bg = node_data["bg"]
    
    scene expression current_bg with fade
    
    if current_node == "home_front":
        jump arrival_home

    $ current_step += 1
    call trigger_node_event(node_data)

    python:
        menu_items = []
        for label_text, target_id in node_data["links"].items():
            menu_items.append((label_text, target_id))
        if previous_node:
            menu_items.append(("ひとつ{rb}前{/rb}{rt}まえ{/rt}に もどる", previous_node))
        next_location = renpy.display_menu(menu_items)

    $ previous_node = current_node
    $ current_node = next_location
    jump travel_loop

# =============================================================================
# イベント抽選
# =============================================================================
label trigger_node_event(data):
    python:
        group_name = data["group"]
        chance = data["chance"]
        target_event = None

        if renpy.random.randint(1, 100) <= chance and group_name in event_pools:
            available = [e for e in event_pools[group_name] if e not in used_events]
            if available:
                target_event = renpy.random.choice(available)
                used_events.add(target_event)

    if target_event:
        call expression target_event
    return

# =============================================================================
# 到着処理
# =============================================================================
label arrival_home:
    "ようやく いえの まえに ついた……。"
    
    python:
        lock_game = TimingMinigame(speed=4.0, perfect_range=25, good_range=60, key="K_SPACE")

    "（タイミングよく スペースキーを おせ！）"
    call screen timing_minigame(lock_game)

    if (_return == "miss"):
        jump game_over
    else:
        jump game_clear

# =============================================================================
# ゲームクリア
# =============================================================================
label game_clear:
    $ feedback_is_clear = True
    $ feedback_title = "GAME CLEAR!!"
    $ feedback_score = total_score
    
    if total_score >= 50:
        $ feedback_message = "すばらしい！あんぜん いしきが とても たかいね！"
        $ feedback_tips = [
            "「いかのおすし」を かんぺきに おぼえているね！",
            "これからも あんぜんに きをつけて すごそう！"
        ]
    elif total_score >= 30:
        $ feedback_message = "よくできました！"
        $ feedback_tips = [
            "あいさつを しっかりできていたね。",
            "110ばんの いえも おぼえておこう！"
        ]
    else:
        $ feedback_message = "もう すこし きを つけよう！"
        $ feedback_tips = [
            "しらない ひとには きを つけてね。",
            "「いかのおすし」を おもいだそう！"
        ]
    
    call screen game_feedback
    call game_end_processing
    return

# =============================================================================
# ゲームオーバー
# =============================================================================
label game_over:
    $ feedback_is_clear = False
    $ feedback_title = "GAME OVER..."
    $ feedback_score = total_score
    $ feedback_message = "つれさられてしまった..."
    $ feedback_tips = [
        "「いかのおすし」を おぼえよう！",
        "・いか（いかない）",
        "・の（のらない）",
        "・お（おおごえを だす）",
        "・す（すぐ にげる）",
        "・し（しらせる）"
    ]
    
    call screen game_feedback
    return

# =============================================================================
# おおごえテスト用ラベル
# =============================================================================
label test_mic_minigame:
    scene black with fade
    
    "おおごえの テストを はじめます！"
    
    # 設定画面を表示
    call screen mic_settings
    
    menu:
        "テストを開始する":
            pass
        "タイトルに戻る":
            return
    
    python:
        shout_game = ShoutMinigame(
            threshold=0.25,    # 音量閾値（少し下げて反応しやすく）
            duration=5.0,
            hold_time=0.3      # 必要な維持時間（短めに）
        )
    
    call screen shout_minigame(shout_game)
    
    if _return == "perfect":
        "PERFECT!! すごい おおごえだね！"
    elif _return == "good":
        "GOOD! いい こえが でていたよ！"
    else:
        "もう すこし がんばろう！"
    
    "テストを おわります。"
    return