# =============================================================================
# メインスクリプト
# とうこう・げこう両かたに対応した設計
# =============================================================================

default game_mode = "going_home"
default _nav_color_map = {}
default show_quick_menu = False  # クイックめにゅーの初期表示状態（非表示）
default minimap_hover_node = None  # せんたく肢ホバーじの仮の行き先ノードID
default StepCount = 0 # 内部ほすう
default MaxStep = 25 # さいだいのほすう
default active_home = None # せんたくされたいえ

# =============================================================================
# 共通初期化処理
# =============================================================================
label initialize_game:
    # 変数初期化
    if game_mode == "going_home":
        # げこうモードの初期いまここはがっこう
        $ current_node = "start_point"
    else:
        # とうこうモードはせんたくしたいえが初期いまここになる（うしろでせってい）
        $ current_node = "home_se" 
        
    $ target_home = None # げこうじのゴール地点（とうこうじはNone）
    $ active_home = None # せんたくされたいえ（両モード共通）
    
    $ visited_nodes = []
    $ total_score = 0  # スコア初期化
    
    # 立ちえなどリセット
    $ previous_node = None
        
    # だいじ: used_eventsは文字列のセットとして管理
    $ used_events = set()

    $ flag_know_110 = False
    $ has_encountered_suspicious = False
    $ encountered_events = [] # 遭遇イベントりれきリセット
    $ total_score = 0
    $ score_history = []
    hide screen score_hud

    scene black

    "なまえを きめよう！"
    call screen profile_setup

    show screen score_hud
    show screen minimap
    return

# =============================================================================
# とうこうモードかいし
# =============================================================================
label going_school_start:
    $ game_mode = "going_school"
    call initialize_game from _call_initialize_game

    $ play_commute_bgm()

    # どのいえからしゅっぱつするか選ぶ
    # "どこの いえから はじめますか？"
    call screen home_select_map()
    $ current_node = _return
    $ active_home = _return
    
    # ミニマップのいまここをリセットして表示し直す（フォーカス更新）
    hide screen minimap
    show screen minimap
    
    # さいしょのいえを「とおったみち」にきろく
    python:
        if current_node not in visited_nodes:
            visited_nodes.append(current_node)

    show screen image_overlay("images/Tutorial.png", "ちゅーとりある")

    scene start with fade
    # おかあさんの見送りボイス（プレースホルダー）
    # voice "audio/voice_mother_itterasshai.mp3"
    pc "さあ、がっこうに いこう！"
    
    "みちで あった ひとの {color=#ff0000}『とくちょう』{/color}や、{color=#ff0000}『なにを されたか』{/color}を よく おぼえておこう！"
    
    jump travel_loop

# =============================================================================
# げこうモードかいし
# =============================================================================
label going_home_start:
    $ game_mode = "going_home"
    call initialize_game from _call_initialize_game_1
    
    $ play_commute_bgm()

    scene start with fade

    # "どの いえに かえりますか？"
    call screen home_select_map()
    $ target_home = _return
    $ active_home = _return

    # ミニマップのいまここをリセットして表示し直す（フォーカス更新）
    hide screen minimap
    show screen minimap
    
    # さいしょのばしょを「とおったみち」にきろく
    python:
        if current_node not in visited_nodes:
            visited_nodes.append(current_node)

    show screen image_overlay("images/Tutorial.png", "ちゅーとりある")

    pc "さあ、いえに かえろう！"
    
    "みちで あった ひとの {color=#ff0000}『とくちょう』{/color}や、{color=#ff0000}『なにを されたか』{/color}を よく おぼえておこう！"
    
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

    # ほすうでの強制しゅうりょう
    if game_mode == "going_home":
        if StepCount == (MaxStep/2):
            call Event_Warning_Stop from _call_Event_Warning_Stop
        elif StepCount >= MaxStep:
            call Event_Force_Stop from _call_Event_Force_Stop
    else:
        if StepCount == (MaxStep/2):
            call Event_Warning_School_Stop from _call_Event_Warning_School_Stop
        elif StepCount >= MaxStep:
            call Event_Force_School_Stop from _call_Event_Force_School_Stop
        
    call trigger_node_event(node_data) from _call_trigger_node_event
    $ play_commute_bgm()

    window hide

    python:
        # 行き先ノードにいろ＋マーカー画像を割り当て（ミニマップとせんたく肢で共有）
        _nav_color_map = {}
        _nav_markers = [
            ("#FF0000", "images/gui/nav_marker_red.png"),
            ("#00CC00", "images/gui/nav_marker_green.png"),
            ("#0066FF", "images/gui/nav_marker_blue.png"),
            ("#FFDD00", "images/gui/nav_marker_yellow.png"),
        ]
        menu_items = []
        for idx, (label_text, target_id) in enumerate(node_data["links"].items()):
            # 【げこうモード】ターゲットいがいのいえへのリンクは表示しない
            if game_mode == "going_home" and target_home:
                # リンク先がhome_nodesに含まれるかチェック
                is_home = (target_id in home_nodes)
                # target_homeいがいならスキップ
                if is_home and target_id != target_home:
                    continue

            color, marker_img = _nav_markers[idx % len(_nav_markers)]
            _nav_color_map[target_id] = (color, marker_img)
            # いろ丸＋テキスト全からだを行き先のいろに変更（マップのいろと対応）
            colored_text = "{color=" + color + "}\u25cf " + label_text + "{/color}"
            menu_items.append((colored_text, target_id))
        next_location = renpy.display_menu(menu_items)
        _nav_color_map = {}

    # 寄りみち判定（いちばんちかいきょりが縮まったかチェック）
    python:
        # ゴールノードリスト作成
        if game_mode == "going_home":
            target_list = [target_home]
        else:
            target_list = ["start_point"]
        
        d_before = get_shortest_dist(current_node, target_list)
        d_after = get_shortest_dist(next_location, target_list)
        
        if d_after >= d_before:
            update_score(-2, "よりみちをした")
            if game_mode == "going_school":
                renpy.notify("みちを まちがえちゃったみたい。がっこうへ いそごう！")
            else:
                renpy.notify("みちを まちがえちゃったみたい。まっすぐ かえろう！")

    $ previous_node = current_node
    $ current_node = next_location
    play audio "audio/ローファー_2.mp3"

    python:
        if current_node not in visited_nodes:
            visited_nodes.append(current_node)
    
    $ StepCount += 1
    
    # ミニマップのいまここをリセットして表示し直す
    hide screen minimap
    show screen minimap

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

        # event_poolsをstoreから明示的に取得
        pools = event_pools
        
        # カスタム設定（出現率・最大遭遇数）を適用
        # 不審者または危険な人物(danger)のみ対象
        if group_name in ["suspicious", "danger"]:
            max_enc = getattr(persistent, "max_stranger_encounters", 2)
            # 現在の遭遇数をカウント
            # is_strangerフラグがTrueのもの、または「顔見知りの誘い(acquaintance)」をカウント
            stranger_count = sum(1 for e in encountered_events if isinstance(e, dict) and (e.get("is_stranger") or e.get("event_name") == "acquaintance"))
            
            if stranger_count >= max_enc:
                chance = 0 # 上限に達したら出現しない
            else:
                rate_mult = getattr(persistent, "stranger_encounter_rate", 1.0)
                chance = int(chance * rate_mult)

        # 確率判定とプール存在かくにん
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

                # --- 修正箇所: 型チェックを「なまえ判定」に変更して強制突破する ---
                # type(selected) が <class 'list'> とでるなら、なまえは 'list' になるはずです
                obj_type_name = type(selected).__name__
                
                # リストまたはタプルの「なまえ」を持っている、あるいは従来の判定がTrueなら通す
                if (obj_type_name in ('list', 'tuple', 'RevertableList', 'RevertableTuple') 
                    or isinstance(selected, (list, tuple))) and len(selected) >= 2:
                    
                    target_event = selected[0]
                    raw_args = selected[1]

                    # 引数部ふんも同様になまえ判定でリスト化チェック
                    args_type_name = type(raw_args).__name__
                    if args_type_name not in ('list', 'tuple', 'RevertableList', 'RevertableTuple') and not isinstance(raw_args, (list, tuple)):
                        event_args = [raw_args]
                    else:
                        event_args = raw_args

                # 文字列の場合（単純なイベント名）
                elif isinstance(selected, str) or obj_type_name == 'str':
                    target_event = selected
                    event_args = None
                
                # それいがい（単一要素のリストなど）
                else:
                    # リストっぽいが長さがあしりない場合など
                    if obj_type_name in ('list', 'tuple', 'RevertableList'):
                        if len(selected) >= 1:
                            target_event = selected[0]
                            event_args = None
                        else:
                            target_event = None
                    else:
                        target_event = selected
                        event_args = None
        
        # 文字列チェック（あんぜん策）
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
# とうちゃく処理
# =============================================================================
label arrival_home:
    hide screen minimap
    stop music fadeout 1.0
    "ようやく いえの まえに ついた……。"
    
    # おかあさんの出迎えボイス（プレースホルダー）
    # voice "audio/voice_mother_okaeri.mp3"
    
    # ミニゲームを入れるばしょ
    call recall_minigame from _call_recall_minigame

    jump game_clear

# =============================================================================
# とうこうじのとうちゃく処理
# =============================================================================
label arrival_school:
    hide screen minimap
    stop music fadeout 1.0
    "がっこうに ついた！"
    
    # ミニゲームを入れるばしょ
    call recall_minigame from _call_recall_minigame_1
    
    jump game_clear

# =============================================================================
# ゲームくりあ
# =============================================================================
label game_clear:
    $ feedback_is_clear = True
    $ feedback_title = "GAME CLEAR!!"
    $ feedback_score = total_score
    
    python:
        # フィードバックのヒントを動的に生成
        feedback_tips = []
        
        # 1. 遭遇したイベントに基づくアドバイス
        has_stranger = any(isinstance(e, dict) and e.get("event_name") in ["suspicious", "stranger", "car", "mom_injury", "car_abduction", "suspicious_event_1", "suspicious_event_2", "encounter_danger"] for e in encountered_events)
        has_acquaintance = any(isinstance(e, dict) and e.get("event_name") == "acquaintance" for e in encountered_events)
        has_officer = any(isinstance(e, dict) and e.get("char_type") in ["officer", "teacher"] for e in encountered_events)
        has_safe_person = any(isinstance(e, dict) and e.get("char_type") == "safe_person" for e in encountered_events)
        
        # だれも会わなかった場合
        if not encountered_events:
            if game_mode == "going_school":
                feedback_tips.append("よりみちを せずに、まっすぐ がっこうに つけたね！")
            else:
                feedback_tips.append("よりみちを せずに、まっすぐ かえれたね！")
            feedback_tips.append("だれにも あわないのが いちばん あんぜんだよ。")
        else:
            if has_stranger:
                feedback_tips.append("しらない ひとは、ぜったいに ついていかない ようにしよう。")
                feedback_tips.append("こわいと おもったら、すぐに ぼうはんブザーを つかおうね。")
            
            if has_acquaintance:
                feedback_tips.append("しっている ひとでも、いやなことを されたら おとなに いおうね。")
                feedback_tips.append("かってに ついていくのは、しっている ひとでも ダメだよ。")
                
            if has_officer:
                feedback_tips.append("おまわりさんや せんせいの はなしを よく きけたかな？")
                feedback_tips.append("こまったときは、こども110ばんの いえや こうばんに たすけを もとめよう。")
            elif has_safe_person:
                feedback_tips.append("あんぜんな ひとには げんきに あいさつ できたかな？")
                feedback_tips.append("あぶない ひとと あんぜんな ひとを みわける ちからを つけよう。")

        # 2. スコアに基づくフィードバック
        if total_score >= 50:
            feedback_message = "すばらしい！あんぜん いしきが とても たかいね！"
            feedback_tips.append("これからも そのちょうしで きをつけよう！")
        elif total_score >= 30:
            feedback_message = "よくできました！"
            if not has_stranger and not has_acquaintance:
                feedback_tips.append("つぎは あいさつも もっと げんきよく してみよう！")
        else:
            feedback_message = "もう すこし きを つけよう！"
            feedback_tips.append("「いかのおすし」を もういちど かくにんしよう！")
    
    hide screen score_hud
    hide screen minimap
    
    # くりあBGM再生
    stop music fadeout 1.5
    play audio "audio/お披露目ファンファーレ.mp3"
    
    call screen game_feedback
    call game_end_processing from _call_game_end_processing
    return

# =============================================================================
# げーむおーばー
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
    
    hide screen score_hud
    hide screen minimap
    
    # しっぱいBGM再生
    stop music fadeout 1.5
    play audio "audio/失敗、ゲームオーバー.mp3"
    
    call screen game_feedback
    $ renpy.full_restart()

# =============================================================================
# おおごえてすと用ラベル
# =============================================================================
label test_mic_minigame:
    scene black with fade
    
    "おおごえの てすとを はじめます！"
    
    # せってい画面を表示
    call screen mic_settings
    
    menu:
        "てすとをかいしする":
            pass
        "タイトルにもどる":
            return
    
    python:
        shout_game = ShoutMinigame(
            threshold=0.25,    # おと量閾値（すこししたげて反応しやすく）
            duration=5.0
        )
    
    call screen shout_minigame(shout_game)
    
    if _return == "perfect":
        "PERFECT!! すごい おおごえだね！"
    elif _return == "good":
        "GOOD! いい こえが でていたよ！"
    else:
        "もう すこし がんばろう！"
    
    "てすとを おわります。"
    return