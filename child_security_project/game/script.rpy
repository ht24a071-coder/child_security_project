# =============================================================================
# メインスクリプト
# 登校・下校両方に対応した設計
# =============================================================================

default game_mode = "going_home"
default _nav_color_map = {}
default show_quick_menu = False  # クイックメニューの初期表示状態（非表示）
default minimap_hover_node = None  # 選択肢ホバー時の仮の行き先ノードID

# 全ホームノードのリスト
define home_nodes = ["home_up", "home_down", "home_left_down", "home_right_up"]

# =============================================================================
# 共通初期化処理
# =============================================================================
label initialize_game:
    # 変数初期化
    $ current_node = "start_point" if game_mode == "going_home" else "home_down"
    $ visited_nodes = []
    $ total_score = 0  # スコア初期化
    
    # 立ち絵などリセット
    $ previous_node = None
    
    #show screen inactivity_guard
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
    show screen minimap
    return

# =============================================================================
# 登校モード開始
# =============================================================================
label going_school_start:
    $ game_mode = "going_school"
    call initialize_game

    # どの家から出発するか選ぶ
    "どこの いえから はじめますか？"
    menu:
        "{rb}左上{/rb}{rt}ひだりうえ{/rt}の{rb}家{/rb}{rt}いえ{/rt}から":
            $ current_node = "home_up"
        "{rb}右下{/rb}{rt}みぎした{/rt}の{rb}家{/rb}{rt}いえ{/rt}から":
            $ current_node = "home_down"
        "{rb}左下{/rb}{rt}ひだりした{/rt}の{rb}家{/rb}{rt}いえ{/rt}から":
            $ current_node = "home_left_down"
        "{rb}右上{/rb}{rt}みぎうえ{/rt}の{rb}家{/rb}{rt}いえ{/rt}から":
            $ current_node = "home_right_up"

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
    
    # ゴール判定（モードによって変わる）
    if game_mode == "going_home" and current_node in home_nodes:
        jump arrival_home
    elif game_mode == "going_school" and current_node == "start_point":
        jump arrival_school

    $ current_step += 1
    call trigger_node_event(node_data)

    window hide

    python:
        # 行き先ノードに色＋マーカー画像を割り当て（ミニマップと選択肢で共有）
        _nav_color_map = {}
        _nav_markers = [
            ("#FF0000", "images/gui/nav_marker_red.png"),
            ("#00CC00", "images/gui/nav_marker_green.png"),
            ("#0066FF", "images/gui/nav_marker_blue.png"),
            ("#FFDD00", "images/gui/nav_marker_yellow.png"),
        ]
        menu_items = []
        for idx, (label_text, target_id) in enumerate(node_data["links"].items()):
            color, marker_img = _nav_markers[idx % len(_nav_markers)]
            _nav_color_map[target_id] = (color, marker_img)
            # 色丸＋テキスト全体を行き先の色に変更（マップの色と対応）
            colored_text = "{color=" + color + "}\u25cf " + label_text + "{/color}"
            menu_items.append((colored_text, target_id))
        next_location = renpy.display_menu(menu_items)
        _nav_color_map = {}

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
        event_args = None

        if renpy.random.randint(1, 100) <= chance and group_name in event_pools:
            available = []
            for e in event_pools[group_name]:
                # リストならタプルに変換、そうでないならそのまま
                check_item = tuple(e) if isinstance(e, list) else e
                if check_item not in used_events:
                    available.append(e)

            if available:
                selected = renpy.random.choice(available)
                
                # used_eventsに追加するときもタプル形式にする
                used_item = tuple(selected) if isinstance(selected, list) else selected
                used_events.add(used_item)

                # --- 判定ロジック ---
                if isinstance(selected, list) and len(selected) == 2:
                    target_event = selected[0]
                    event_args = selected[1]
                else:
                    target_event = selected
                    event_args = None

    if target_event:
        if event_args is not None:
            call expression target_event(*event_args)
        else:
            call expression target_event
    return

# =============================================================================
# 到着処理
# =============================================================================
label arrival_home:
    hide screen minimap
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
# 登校時の到着処理
# =============================================================================
label arrival_school:
    hide screen minimap
    "がっこうに ついた！"
    
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
    $ renpy.full_restart()

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