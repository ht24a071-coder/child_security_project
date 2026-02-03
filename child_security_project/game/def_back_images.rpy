init python:
    # --------------------------------------------------------------------------------
    # images/back/ フォルダ内の画像を自動リサイズする処理
    # --------------------------------------------------------------------------------
    
    # 目標サイズ
    target_width = 1920
    target_height = 1080
    
    # ゲーム内の全ファイルをチェック
    for fn in renpy.list_files():
        
        # "images/back/" で始まり、画像ファイルであるものを対象にする
        if fn.startswith("images/back/") and fn.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            
            # 画像のサイズを取得 (width, height)
            size = renpy.image_size(fn)
            
            if size:
                w, h = size
                
                # サイズが 1920x1080 と違う場合のみ再定義する
                if (w, h) != (target_width, target_height):
                    
                    # 画像名を作成 (例: "images/back/bg01.png" -> "back bg01")
                    # 1. 拡張子を削除
                    name_no_ext = fn.rsplit(".", 1)[0]
                    
                    # 3. 画像名を決定
                    # ゲーム内では "back_tunnel" のようにファイル名だけで呼ばれているため、
                    # パスを含めず、ファイル名部分だけを画像名として登録する
                    image_name = name_no_ext.split("/")[-1]

                    
                    # Transformを使ってリサイズして再定義
                    # fitを指定せず size だけ指定すると、アスペクト比を無視してそのサイズに引き伸ばします
                    renpy.image(image_name, Transform(fn, size=(target_width, target_height)))

                    
                    # 確認用ログ（デバッグ時に有効化してください）
                    # print(f"[Auto-Resize] {image_name}: {w}x{h} -> {target_width}x{target_height}")
