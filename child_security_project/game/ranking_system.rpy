# ranking_system.rpy

label game_end_processing:
    # -----------------------------------------------------------
    # 1. 二つ名の生成（さっきと同じ）
    # -----------------------------------------------------------
    python:
        import random
        # ランダム作成（例）
        title_p1 = random.choice(list_part1)
        title_p2 = random.choice(list_part2)
        title_p3 = random.choice(list_part3)
        current_title = title_p1 + title_p2 + title_p3

    # -----------------------------------------------------------
    # 2. 重複チェック（ここが変わります！）
    # -----------------------------------------------------------
    python:
        # 重複しているデータの場所（インデックス）を探す
        duplicate_index = -1
        
        for i, record in enumerate(persistent.ranking_list):
            # 名前・アイコン・二つ名がすべて完全に一致するか？
            if (record['name'] == player_name and 
                record['icon'] == player_icon and 
                record['title'] == current_title):
                
                duplicate_index = i
                break

    # 重複が見つかった場合（duplicate_index が -1 じゃない時）
    if duplicate_index != -1:
        jump ask_overwrite_confirmation
    
    # 重複がないなら、そのまま保存へ
    else:
        jump save_new_record


# --- 重複があったときの確認画面 ---
label ask_overwrite_confirmation:
    
    # ここで博士などを表示してもOK
    "ランキングに おなじ なまえと アイコンの 人が いるよ！"
    "「[current_title] [player_name]」は、きみのこと？"

    menu:
        "ぼくだよ！（ハイスコアなら 更新）":
            python:
                old_score = persistent.ranking_list[duplicate_index]['score']
                
                # 今回の方が点数が高い場合だけ上書き
                if total_score > old_score:
                    persistent.ranking_list[duplicate_index]['score'] = total_score
                    is_updated = True
                else:
                    is_updated = False
            
            if is_updated:
                "記録（きろく）を 更新（こうしん）したよ！やったね！"
            else:
                "前の 記録のほうが 点数が高かったから、そのままにしておくね！"
            
            # 保存して終了へ
            jump save_and_sort

        "ちがう人だよ！（新しく 保存）":
            "わかった！ 別の人として 新しく 保存するね。"
            # そのまま下（save_new_record）に進む


# --- 新規保存の処理 ---
label save_new_record:
    python:
        new_record = {
            "title": current_title,
            "name": player_name,
            "score": total_score,
            "icon": player_icon  # アイコンも保存しておく
        }
        persistent.ranking_list.append(new_record)
    
    # ここへ合流
    jump save_and_sort


# --- 最後の並び替えと保存 ---
label save_and_sort:
    python:
        # スコアが高い順に並び替え
        persistent.ranking_list.sort(key=lambda x: x['score'], reverse=True)

        # データを保存
        renpy.save_persistent()

    return