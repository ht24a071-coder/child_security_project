# =============================================================================
# メインスクリプト
# 登校・下校両方に対応した設計
# =============================================================================

default game_mode = "going_home"
default _nav_color_map = {}
default show_quick_menu = False  # クイックメニューの初期表示状態（非表示）
default minimap_hover_node = None  # 選択肢ホバー時の仮の行き先ノードID
default StepCount = 0 # 内部歩数
default MaxStep = 25 # 最大歩数

# 全ホームノードのリスト
define home_nodes = ["home_nw", "home_se", "home_sw", "home_w"]

# =============================================================================
# 共通初期化処理
# =============================================================================
label initialize_game:
    # 変数初期化
    if game_mode == "going_home":
        # 下校モードの初期現在地は学校
        $ current_node = "start_point"
    else:
        # 登校モードは選択した家が初期現在地になる（後で設定）
        $ current_node = "home_se" 
        
    $ target_home = None # 下校時の目標地点（登校時はNone）
    
    $ visited_nodes = []
    $ total_score = 0  # スコア初期化
    
    # 立ち絵などリセット
    $ previous_node = None
        
    # 重要: used_eventsは文字列のセットとして管理
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
    # "どこの いえから はじめますか？"
    call screen home_select_map()
    $ current_node = _return

    scene back_town with fade
    pc "さあ、がっこうに いこう！"
    
    jump travel_loop

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

    # "どの いえに かえりますか？"
    call screen home_select_map()
    $ target_home = _return

    pc "さあ、いえに かえろう！"
    
    jump travel_loop

# =============================================================================
# マップベース移動ループ
# =============================================================================
label travel_loop:
    $ node_data = world_map.get(current_node)
    $ current_bg = node_data["bg"]
    
    scene expression current_bg with pixellate
    
    # ゴール判定（モードによって変わる）
    if game_mode == "going_home" and current_node in home_nodes:
        jump arrival_home
    elif game_mode == "going_school" and current_node == "start_point":
        jump arrival_school

    # 歩数での強制終了
    if StepCount == (MaxStep/2):
        call Event_Warning_Stop
    elif StepCount >= MaxStep:
        call Event_Force_Stop
        
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
            # 【下校モード】ターゲット以外の家へのリンクは表示しない
            if game_mode == "going_home" and target_home:
                # リンク先がhome_nodesに含まれるかチェック
                is_home = (target_id in home_nodes)
                # target_home以外ならスキップ
                if is_home and target_id != target_home:
                    continue

            color, marker_img = _nav_markers[idx % len(_nav_markers)]
            _nav_color_map[target_id] = (color, marker_img)
            # 色丸＋テキスト全体を行き先の色に変更（マップの色と対応）
            colored_text = "{color=" + color + "}\u25cf " + label_text + "{/color}"
            menu_items.append((colored_text, target_id))
        next_location = renpy.display_menu(menu_items)
        _nav_color_map = {}

    $ previous_node = current_node
    $ current_node = next_location

    $ StepCount += 1

    jump travel_loop

# =============================================================================
# イベント抽選
# =============================================================================
# =============================================================================
# イベント抽選
# =============================================================================
# =============================================================================
# イベント抽選
# =============================================================================
label trigger_node_event(data):
    python:
        group_name = data["group"]
        chance = data["chance"]
        target_event = None
        event_args = None

        # event_poolsをstoreから明示的に取得
        pools = event_pools
        
        # 確率判定とプール存在確認
        if renpy.random.randint(1, 100) <= chance and group_name in pools:
            available = []
            for e in pools[group_name]:
                # イベントを文字列化して既出チェック
                event_key = str(e)
                if event_key not in used_events:
                    available.append(e)

            if available:
                selected = renpy.random.choice(available)
                used_events.add(str(selected))

                # --- 修正箇所: 型チェックを「名前判定」に変更して強制突破する ---
                # type(selected) が <class 'list'> と出るなら、名前は 'list' になるはずです
                obj_type_name = type(selected).__name__
                
                # リストまたはタプルの「名前」を持っている、あるいは従来の判定がTrueなら通す
                if (obj_type_name in ('list', 'tuple', 'RevertableList', 'RevertableTuple') 
                    or isinstance(selected, (list, tuple))) and len(selected) >= 2:
                    
                    target_event = selected[0]
                    raw_args = selected[1]

                    # 引数部分も同様に名前判定でリスト化チェック
                    args_type_name = type(raw_args).__name__
                    if args_type_name not in ('list', 'tuple', 'RevertableList', 'RevertableTuple') and not isinstance(raw_args, (list, tuple)):
                        event_args = [raw_args]
                    else:
                        event_args = raw_args

                # 文字列の場合（単純なイベント名）
                elif isinstance(selected, str) or obj_type_name == 'str':
                    target_event = selected
                    event_args = None
                
                # それ以外（単一要素のリストなど）
                else:
                    # リストっぽいが長さが足りない場合など
                    if obj_type_name in ('list', 'tuple', 'RevertableList'):
                        if len(selected) >= 1:
                            target_event = selected[0]
                            event_args = None
                        else:
                            target_event = None
                    else:
                        target_event = selected
                        event_args = None
        
        # 文字列チェック（安全策）
        if target_event and not isinstance(target_event, str):
            target_event = None

        # --- 修正箇所: ここでイベント呼び出しを行います ---
        if target_event:
            target_event = str(target_event)

            if event_args:
                renpy.call(target_event, *event_args)
            else:
                renpy.call(target_event)

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
label game_over(set_message="つれさられてしまった..."):
    $ feedback_is_clear = False
    $ feedback_title = "GAME OVER..."
    $ feedback_score = total_score
    $ feedback_message = set_message
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