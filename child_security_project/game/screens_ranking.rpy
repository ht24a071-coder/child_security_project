screen ranking_menu():
    tag menu

    # 背景
    add "images/title.png":
        xysize (config.screen_width, config.screen_height)
    
    # 画面全体を暗くする
    add Solid("#00000080")

    # メインウィンドウ
    frame:
        align (0.5, 0.5)
        xysize (1000, 600)
        padding (40, 40)
        background Solid("#ffffffcc")

        # --- コンテンツエリア（上部） ---
        vbox:
            spacing 20
            xfill True

            # 見出し
            text "🏆 ランキング 🏆":
                size 50
                color "#ff8c00"
                xalign 0.5
                bold True
                outlines [(3, "#fff", 0, 0)]

            # リスト表示エリア
            # ★高さを350にして、下のボタンと被らないようにしています
            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 350

                vbox:
                    spacing 10
                    xfill True

                    # データがない場合
                    if not persistent.ranking_list:
                        text "まだデータがありません\n遊んでスコアを登録しよう！":
                            xalign 0.5
                            yalign 0.5
                            text_align 0.5
                            color "#555"
                            size 30
                    
                    # データがある場合
                    else:
                        for i, record in enumerate(persistent.ranking_list):
                            $ rank = i + 1
                            
                            # 順位ごとの色分け
                            if rank == 1:
                                $ rank_color = "#FFD700"
                            elif rank == 2:
                                $ rank_color = "#C0C0C0"
                            elif rank == 3:
                                $ rank_color = "#CD7F32"
                            else:
                                $ rank_color = "#555555"

                            # 1行ごとの枠
                            frame:
                                xfill True
                                background Solid("#f0f8ff")
                                padding (10, 5)

                                hbox:
                                    spacing 20
                                    yalign 0.5

                                    # 順位
                                    text "[rank]位":
                                        color rank_color
                                        size 40
                                        bold True
                                        min_width 80
                                        yalign 0.5

                                    # アイコン
                                    if "icon" in record:
                                        add "images/icons/" + record['icon'] + ".png":
                                            yalign 0.5
                                            zoom 0.5

                                    # 名前と二つ名
                                    vbox:
                                        yalign 0.5
                                        text record['name']:
                                            size 32
                                            color "#333"
                                            bold True

                                    # 右寄せスペース
                                    null width 1.0

                                    # スコア
                                    text "[record['score']] 点":
                                        size 40
                                        color "#ff4500"
                                        bold True
                                        yalign 0.5
                                        text_align 1.0

        # --- ボタンエリア（vboxの外に出して固定配置） ---
        
        # 戻るボタン（中央下）
        # align (0.5, 1.0) で、フレームの一番下に固定されます
        textbutton "戻る":
            action Return()
            align (0.5, 1.0)
            text_size 40
            text_color "#333"
            text_hover_color "#ff8c00"