# 変数（セーブデータに含まれる）
default current_step = 0 
default has_encountered_suspicious = False 
default flag_know_110 = False 
default total_score = 0
default score_history = []
default trust_point = 0
default current_score = 0
default is_window_hovered = False # テキストウィンドウのホバー状態

# プレイヤーせってい
default player_name = "ナナシ"
default player_icon = "bear"
default player_destination = "" # 行き先の動的テキスト（例：「かえる」「いく」）

# やま札変数
default deck_suspicious = []
default deck_safe = []
 
# 全キャラクター・ナレーション共通でCTCをせってい
define narrator = Character(ctc="ctc_icon", ctc_position="nestled")

# キャラクター定義（CTC追加）
define officer = Character("おまわりさん", color="#c8ffc8", ctc="ctc_icon", ctc_position="nestled")
define woman = Character("おねえさん", color="#c8ffc8", ctc="ctc_icon", ctc_position="nestled")
define teacher = Character("せんせい", color="#c8ffc8", ctc="ctc_icon", ctc_position="nestled")
define stranger = Character("???", color="#ff8888", ctc="ctc_icon", ctc_position="nestled")
define pc = Character("[player_name]", image="player", ctc="ctc_icon", ctc_position="nestled")
define parent = Character("おかあさん", color="#c8ffc8", ctc="ctc_icon", ctc_position="nestled")
define t = Character("いとう まんしょ", color="#c8ffc8", ctc="ctc_icon", ctc_position="nestled")

# ふしんしゃのランダム画像用
default stranger_type = "stranger"

# 遭遇したイベントのきろく（振り返りミニゲーム用）
default encountered_events = [] 

# ふしんしゃの見ためごとのボイスマッピング
define stranger_voice_map = {
    "stranger": {
        "kaeri": "audio/stranger1_kaeri.wav",
        "okuru": "audio/stranger1_okuru.wav",
        "hello": "audio/stranger1_hello.wav",
    },
    "stranger2": {
        "kaeri": "audio/stranger2_kaeri.wav",
        "okuru": "audio/stranger2_okuru.wav",
        "hello": "audio/stranger2_hello.wav",
    },
}

# 定数
define PROB_SUSPICIOUS = 20 
define MAX_STEPS = 10 

# 画像定義
image side player = "images/icons/[player_icon].png"
image side officer = "images/actor/officer.png"
image side woman = "images/actor/woman.png"
image side teacher = "images/actor/teacher.png"
image side parent = "images/actor/woman3.png" # おかあさん（仮）
image side stranger = ConditionSwitch(
    "stranger_type == 'stranger2'", "images/actor/stranger2.png",
    "True", "images/actor/stranger.png"
)
image stranger = ConditionSwitch(
    "stranger_type == 'stranger2'", Transform("images/actor/stranger2.png", fit="contain", ysize=900),
    "True", Transform("images/actor/stranger.png", fit="contain", ysize=900)
)
image teacher = Transform("images/actor/teacher.png", fit="contain", ysize=900)
image parent = Transform("images/actor/woman3.png", fit="contain", ysize=900)
image woman = Transform("images/actor/woman.png", fit="contain", ysize=900)
image officer = Transform("images/actor/officer.png", fit="contain", ysize=900)

init python:
    def get_helper_data():
        """いまここに基づいて助けに来るひと（キャラ画像名、なまえ）を返す"""
        # いまのノードを取得（global current_node を想定、なければ safe デフォルト）
        # ただし current_node は script.rpy 等で管理されているはず
        # ここでは renpy.store.current_node を参照する
        c_node = getattr(renpy.store, "current_node", "")
        
        if c_node in NEAR_SCHOOL_NODES:
            return "teacher", "せんせい"
        else:
            return "officer", "おまわりさん"

# 1. 常じ表示するスコアボード
screen score_hud():
    zorder 100
    style_prefix "score_hud"

    frame:
        xalign 0.02 yalign 0.02 # 画面の配置（ひだりうえ）
        padding (20, 10)        # 枠の内側の余白
        background "#00000080"  # 半透明の黒背景

        hbox:
            spacing 20
            
            # スコア表示
            text "てんすう: [total_score]":
                color "#ffff00"  # 黄いろ
                size 32          # 文字サイズ
                bold True        # 太字
                yalign 0.5       # うえしたの真んなか寄せ

            # もくてきち表示（げこうモードのみ）
            $ _target_home = globals().get("target_home", None)
            if game_mode == "going_home" and _target_home:
                hbox:
                    spacing 5
                    yalign 0.5
                    add "images/gui/icon_home.png" yalign 0.5 zoom 0.8
                    
                    $ home_name = ""
                    if _target_home == "home_nw":
                        $ home_name = "ひだりうえのいえ"
                    elif _target_home == "home_sw":
                        $ home_name = "ひだりしたのいえ"
                    elif _target_home == "home_se":
                        $ home_name = "みぎしたのいえ"
                    elif _target_home == "home_w":
                        $ home_name = "ひだりのいえ"
                    
                    text "めざす ばしょ: [home_name]":
                        color "#00ffff"
                        size 24
                        bold True
                        outlines [(3, "#000000", 0, 0)] # ルビが見やすいように太めのアウトライン
                        yalign 0.5

# 2. 点数変動じのポップアップ演出
screen score_popup(amount):
    zorder 101 # スコアボードよりさらにてまえ

    # プラスかマイナスかでいろと記号を変える
    if amount >= 0:
        $ display_text = "+" + str(amount)
        $ text_color = "#00ff00" # 緑いろ
    else:
        $ display_text = str(amount) # マイナスは最初からついてる
        $ text_color = "#ff0000" # 赤いろ

    # ふわっと消えるアニメーションを適用
    text "[display_text]" at score_float_up:
        color text_color
        size 40
        outlines [(2, "#000000", 0, 0)] # くろいフチドリで見やすく
        # ★修正済み：bold True
        bold True
        xalign 0.05 yalign 0.08 # スコアボードのちょっとしたに表示

    # 1.5びょううしろに自動で消す
    timer 1.5 action Hide("score_popup")

# 3. アニメーションの動き定義（トランスフォーム）
transform score_float_up:
    alpha 0.0 yoffset 20 # 最初は透明でちょっとした
    easein 0.3 alpha 1.0 yoffset 0 # 0.3びょうで現れる
    time 1.0 # 1びょう間そのまま
    easeout 0.5 alpha 0.0 yoffset -30 # 0.5びょうかけてうえに浮きながら消える

# 4. 便利な関数（update_score）
init python:
    def update_score(amount, reason=None):
        # グローバル変数のスコアを更新
        # グローバル変数のスコアを更新（0をしょげんとする）
        global total_score
        total_score = max(0, total_score + amount)
        
        # りれきに追加
        # reasonがない場合は自動的に補完するか、Noneのままにして表示側で処理
        if reason:
            score_history.append((amount, reason))
        else:
            # 理由がない場合のデフォルト表記（必要なら）
            pass

        # ポップアップ演出を表示（引数で増減値を渡す）
        renpy.show_screen("score_popup", amount=amount)
        
        # おとを鳴らす（ファイルがない場合はコメントアウトしてください）
        # if amount > 0:
        #    renpy.play("audio/se_good.ogg", channel="sound")
        # elif amount < 0:
        #    renpy.play("audio/se_bad.ogg", channel="sound")

    def setup_stranger(event_name="unknown"):
        """ランダムでふしんしゃの見ためを選ぶ & 遭遇イベントをきろく"""
        global stranger_type
        stranger_type = renpy.random.choice(["stranger", "stranger2"])
        
        # 特徴をランダムにけってい
        trait = renpy.random.choice(stranger_traits)
        
        # 遭遇リストに追加
        record_detailed_encounter(stranger_type, event_name, trait=trait, is_stranger=True)

    def record_detailed_encounter(char_type, event_name, trait=None, is_stranger=False):
        """遭遇イベントを詳細にきろくする"""
        # 重複チェック（同じイベント名は一度だけきろく）
        for e in encountered_events:
            if isinstance(e, dict) and e.get("event_name") == event_name:
                return
            elif isinstance(e, tuple) and e[1] == event_name: # 互換性
                return

        # スプライト(画像パス)のけってい
        sprite_map = {
            "stranger": "images/actor/stranger.png",
            "stranger2": "images/actor/stranger2.png",
            "officer": "images/actor/officer.png",
            "woman": "images/actor/woman.png",
            "teacher": "images/actor/teacher.png",
            "parent": "images/actor/woman3.png"
        }
        sprite = sprite_map.get(char_type, "")

        # きろく
        data = {
            "char_type": char_type,
            "event_name": event_name,
            "sprite": sprite,
            "trait": trait,
            "is_stranger": is_stranger
        }
        encountered_events.append(data)

    def record_encounter(char_type, event_name):
        """遭遇イベントをきろく（うしろかた互換性用）"""
        record_detailed_encounter(char_type, event_name)

    def get_stranger_voice(line_id=None):
        """
        いまのstranger_typeに対応するボイスファイルパスを返す
        line_idがNone、または 'auto' の場合は、game_modeに合わせて kaeri(げこう) か okuru(とうこう) を選ぶ
        """
        if line_id is None or line_id == "auto":
            # game_mode が going_home なら kaeri、それいがいなら okuru
            line_id = "kaeri" if getattr(renpy.store, "game_mode", "going_home") == "going_home" else "okuru"
            
        return stranger_voice_map.get(stranger_type, {}).get(line_id, None)

    def play_voice(line_id="auto"):
        """ふしんしゃのボイスを自動判別して再生する"""
        v = get_stranger_voice(line_id)
        if v:
            try:
                # voiceチャンネルで再生
                renpy.music.play(v, channel="voice")
            except:
                pass

    def play_commute_bgm(fadein=1.0):
        """モードに合わせてBGMを再生する"""
        import store
        # game_modeがうまく取れない場合を考慮
        mode = getattr(store, "game_mode", "going_home")
        
        # ユーザーゆび定のBGMを再生
        renpy.music.play("audio/あにまるさんぽ.mp3", fadein=fadein, loop=True, if_changed=True)

    def get_npc_dialogue(npc_tag, dialogue_type="Greeting"):
        """
        NPCのセリフリストをモードに合わせて取得する
        npc_tag: 'Officer', 'Woman' など
        dialogue_type: 'Greeting', 'MissGreeting' など
        例: get_npc_dialogue('Officer', 'Greeting') -> OfficerGreeting_Home or School のリスト
        """
        mode_suffix = "_Home" if getattr(renpy.store, "game_mode", "going_home") == "going_home" else "_School"
        list_name = npc_tag + dialogue_type + mode_suffix
        
        # globals() からリストを取得
        dialogue_list = globals().get(list_name, [])
        if not dialogue_list:
            # フォールバック: モードゆび定なしのなまえを試す
            dialogue_list = globals().get(npc_tag + dialogue_type, ["..."])
            
        return renpy.random.choice(dialogue_list)

    def get_commute_text(home_text, school_text):
        """
        game_mode に基づいてテキストを返す
        home_text: げこうじのテキスト
        school_text: とうこうじのテキスト
        """
        if getattr(renpy.store, "game_mode", "going_home") == "going_home":
            return home_text
        return school_text

    # -----------------------------------------------------------
# コントローラーせってい
# -----------------------------------------------------------
default persistent.controller_layout = "standard"

init python:
    # Switch Proコントローラーがデフォルトでブロックされている場合があるため解除
    if "Nintendo Switch" in config.controller_blocklist:
        config.controller_blocklist.remove("Nintendo Switch")
    
    # 一般的なSwitch ProコントローラーのSDL2マッピングを追加（認識精度向うえ）
    # 030000007e0500000920000000000000,Nintendo Switch Pro Controller,a:b0,b:b1,back:b8,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b4,leftstick:b10,lefttrigger:b6,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b11,righttrigger:b7,rightx:a2,righty:a3,start:b9,x:b2,y:b3,
    try:
        import os
        # 環境変数SDL_GAMECONTROLLERCONFIGに追記することで認識させる
        sdl_mapping = "030000007e0500000920000000000000,Nintendo Switch Pro Controller,platform:Windows,a:b0,b:b1,back:b8,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b4,leftstick:b10,lefttrigger:b6,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b11,righttrigger:b7,rightx:a2,righty:a3,start:b9,x:b2,y:b3,"
        current_mappings = os.environ.get("SDL_GAMECONTROLLERCONFIG", "")
        if sdl_mapping not in current_mappings:
            os.environ["SDL_GAMECONTROLLERCONFIG"] = current_mappings + sdl_mapping
    except:
        pass

    def update_controller_bindings():
        """コントローラーのボタン割り当てを更新"""
        
        # Nintendoレイアウト（Aけってい=みぎ、Bもどる=した）
        if persistent.controller_layout == "nintendo":
            # Aボタン（XboxのB位置）でけってい
            config.pad_bindings["pad_b_press"] = [ "dismiss", "button_select", "bar_activate", "bar_deactivate", "chosen" ]
            # Bボタン（XboxのA位置）でめにゅーを開く
            config.pad_bindings["pad_a_press"] = [ "game_menu" ]
            
        # Standardレイアウト（Aけってい=した、Bもどる=みぎ）
        else:
            # Aボタン（XboxのA位置）でけってい
            config.pad_bindings["pad_a_press"] = [ "dismiss", "button_select", "bar_activate", "bar_deactivate", "chosen" ]
            # Bボタン（XboxのB位置）できゃんせる・めにゅー
            config.pad_bindings["pad_b_press"] = [ "game_menu" ]

    # 初期化じに適用
    update_controller_bindings()

# -----------------------------------------------------------
# クリック待ちアイコン（CTC）
# -----------------------------------------------------------
image ctc_icon:
    # ホバーじは黄いろ、通常は白
    ConditionSwitch(
        "is_window_hovered", Text("▼", size=24, color="#ffff00", outlines=[(2, "#000000", 0, 0)]),
        "True", Text("▼", size=24, color="#ffffff", outlines=[(2, "#000000", 0, 0)])
    )
    alpha 1.0
    linear 0.5 alpha 0.0
    linear 0.5 alpha 1.0
    repeat

