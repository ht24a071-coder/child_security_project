# --- 粒子（マナ）の定義：個別にランダムな動きをさせる ---
transform stardust_move:
    # 初期位置をバラバラにする（ここがループの起点）
    block:
        # 画面下のランダムな位置
        xpos renpy.random.random() 
        ypos 1.1 + 10 * renpy.random.random() 
        alpha 0.0
        # 粒子の大きさをランダムに
        zoom (renpy.random.random() * 1.5 + 0.5)
        
        parallel:
            # パッと光って、ゆっくり消える
            linear 1.0 alpha 1.0
            linear 2.5 alpha 0.0
        parallel:
            # ぐんぐん昇っていく
            linear 3.5 ypos -0.2
        parallel:
            # 左右にゆらゆら揺れる
            linear 1.75 xoffset 40
            linear 1.75 xoffset -40
            
        # これで「消えたらまた下から」のループになる
        repeat

# --- 光の柱（ゴッドレイ）の定義：もっと太く、明るく！ ---
image bg_god_ray_strong:
    # 柱が見えない原因はおそらく透明度とボケすぎ。
    # Solidを少し明るい色にして、加算合成を最強にする
    Solid("#ffffff") 
    additive 1.0 # 加算合成を最大に
    xsize 300    # 幅を太く
    ysize 1200
    # ぼかし(blur)は重い場合があるので、アルファでグラデーションっぽく見せる
    alpha 0.5

transform ray_flare_strong(x_pos, d):
    xpos x_pos
    yalign 0.5
    rotate 5 # 少し斜めにするのがFFっぽい
    alpha 0.0
    pause d
    block:
        # 呼吸するように明滅させる
        linear 3.0 alpha 0.2
        linear 3.0 alpha 0.1
        repeat

# --- 背景専用スクリーン（増量版） ---
screen adventure_bg_v2():
    # 背景は深い青
    add Solid("#020830")

    # 1. 背後の巨大な光の輪（魔法陣の代わり）
    # 画像がなくても、大きな白い円を加工して「聖なる感じ」を出す
    add Solid("#4db6ac") alpha 0.1:
        align (0.5, 0.5)
        xysize (800, 800)
        at transform:
            # 巨大なオーラがゆっくり回転
            rotate 0
            linear 60 rotate 360
            repeat

    # 2. 光の柱（左右と中央に配置）

    # 3. 粒子を「80個」に増量！
    # range(80)で画面中をキラキラに埋め尽くす
    for i in range(100):
        # 1つ1つ出現タイミングをずらす(i * 0.05)
        add Solid("#fff"):
            xysize (4, 4)
            additive 1.0
            at stardust_move