Ren'Py クイックリファレンスガイドこのドキュメントは、Ren'Py 8.x以降（Python 3ベース）に対応した主要な構文と機能のまとめです。1. 基本構造 (Structure)Ren'Pyのスクリプトは.rpyファイルに記述します。ゲームの開始地点# script.rpy

label start:
    # ここからゲームが始まります
    "物語が始まります。"
    
    return # ゲーム終了（メインメニューへ戻る）
コメントアウト# これは一行コメントです
2. キャラクターと台詞 (Characters & Dialogue)キャラクター定義通常はinitブロックやファイルの冒頭で定義します。# defineは定数（変化しないもの）に使用
define e = Character("エイリーン", color="#c8ffc8")
define s = Character("シルヴィ", image="sylvie") # サイドイメージ用設定
台詞の表示label start:
    # ナレーター（名前なし）
    "静かな朝だ。"

    # 定義したキャラクター
    e "こんにちは、Ren'Pyへようこそ！"

    # キャラクター名と台詞を直接記述（非推奨だが可能）
    "謎の男" "誰だお前は？"
3. 変数とフラグ管理 (Variables)Ren'Py 7/8以降では、変数の初期化にはdefaultを使用することを強く推奨します（セーブデータに含まれるため）。変数の宣言# ゲーム内で変化する値（フラグ、好感度など）
default love_points = 0
default has_key = False

# ゲーム全体で変化しない定数
define MAX_POINTS = 100
Pythonステートメント（変数の操作）    # $ マークで1行のPythonコードを実行
    $ love_points += 1
    $ has_key = True

    # 複数行のPythonブロック
    python:
        point_diff = MAX_POINTS - love_points
        if point_diff < 10:
            print("もうすぐMAXです")
変数の埋め込み    e "現在の好感度は [love_points] です。"
4. 画像と演出 (Images & Visuals)画像ファイルは images/ フォルダに入れます。画像の定義 (自動定義も有効)# image <タグ> <属性> = "ファイルパス"
image bg classroom = "bg/classroom.jpg"
image eileen happy = "eileen/happy.png"
背景と立ち絵    # 背景の表示（前の背景は消える）
    scene bg classroom

    # 立ち絵の表示
    show eileen happy

    # 立ち絵の表情変更（タグが同じなら置き換わる）
    show eileen surprised

    # 立ち絵を消す
    hide eileen
位置指定 (Transforms)Ren'Pyには標準でいくつかの位置が定義されています。    show eileen happy at right
    show eileen happy at left
    show eileen happy at center
    show eileen happy at truecenter # 画面中央
トランジション (Transitions)    scene bg gym with fade # フェード暗転
    show eileen happy with dissolve # ディゾルブ（じわっと表示）
    
    # 特殊なトランジション
    with vpunch # 縦揺れ
    with hpunch # 横揺れ
    with flash # フラッシュ
5. 音声と音楽 (Audio)オーディオファイルは game/audio/ に配置すると自動検出されます。再生と停止    # BGM（ループする）
    play music "audio/bgm01.ogg"
    
    # 音楽をフェードアウトして停止
    stop music fadeout 1.0

    # 効果音（一度だけ再生）
    play sound "audio/click.ogg"

    # ボイス（自動で音量が調整されるチャンネル）
    play voice "audio/voice001.ogg"
6. フロー制御 (Flow Control)選択肢 (Menus)menu:
    "どちらへ行きますか？"

    "教室へ行く":
        jump classroom_scene

    "屋上へ行く" if has_key: # 条件付き選択肢
        $ love_points += 5
        jump rooftop_scene
    
    "何もしない":
        pass # 何もしないで次へ進む
ジャンプとコール    # 指定ラベルへ移動（戻ってこない）
    jump label_name

    # サブルーチン呼び出し（returnで戻ってくる）
    call label_name
条件分岐 (If/Else)    if love_points >= 10:
        e "大好き！"
    elif love_points >= 5:
        e "まあまあ好き。"
    else:
        e "......"
7. ATL (Animation Transformation Language)画像を動かしたり変形させたりする強力な機能です。簡易的な動き    show eileen happy:
        xalign 0.5 yalign 1.0 # 初期位置
        linear 1.0 xalign 0.0 # 1秒かけて左へ移動
        pause 0.5             # 0.5秒待機
        ease 1.0 zoom 1.5     # 1.0秒かけてイージングしながら拡大
カスタムTransformの定義transform hop:
    yoffset 0
    easeout 0.1 yoffset -20
    easein 0.1 yoffset 0
    repeat 2 # 2回繰り返す

label start:
    show eileen happy at hop
8. スクリーン言語 (Screen Language)GUIやカスタム画面を作成するために使用します。スクリーンの定義screen my_button_screen():
    # 画像ボタンの例
    imagebutton:
        xalign 0.95 yalign 0.05
        idle "gui/icon_idle.png"
        hover "gui/icon_hover.png"
        action ShowMenu("save") # セーブ画面を開く

    # テキスト配置
    text "現在のポイント: [love_points]":
        xalign 0.05 yalign 0.05
        size 30
        color "#ffffff"
スクリーンの表示label start:
    show screen my_button_screen
    "画面にボタンが表示されています。"
    call screen my_button_screen # プレイヤーの操作を待つ場合
9. 永続データ (Persistent Data)セーブデータに関係なく、ゲーム全体で共有されるデータ（CGギャラリー解放状況やクリアフラグなど）。    # データの書き込み
    $ persistent.game_cleared = True

    # データの読み込み（条件分岐）
    if persistent.game_cleared:
        "クリアおめでとう！おまけシナリオです。"
10. テキストタグ (Text Tags)台詞の中で使用できる特殊なフォーマットです。{b}太字{/b}: 太字{i}イタリック{/i}: イタリック{s}取り消し線{/s}: ~~取り消し線~~{color=#ff0000}赤色{/color}: 色変更{size=+10}大きく{/size}: 文字サイズ変更{w}: クリック待ち{w=1.0}: 1秒待機してから自動で進む{nw}: 待機せずに次の台詞へ（早送り演出など）{p}: 改段落（クリック待ちして画面クリア）11. 特殊ファイル名options.rpy: ゲーム設定（タイトル、解像度など）screens.rpy: GUI定義gui.rpy: UIの配色やフォント設定script.rpy: メインスクリプト（通常ここから書き始める）12. 便利なショートカットキー (開発中)Shift + R: リロード（コード変更を即時反映）Shift + I: スタイルインスペクタ（UIの構成要素を調査）Shift + O: コンソール（変数の確認や書き換え）Tab: スキップ