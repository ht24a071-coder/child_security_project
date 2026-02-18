# =============================================================================
# イベント共通フレームワーク
# =============================================================================

# 立ち絵表示などの共通処理をここに定義します。
# 各イベントファイルから `call show_stranger_wrapper` のように呼び出して使います。

# -----------------------------------------------------------------------------
# 不審者（Stranger）用ラッパー
# -----------------------------------------------------------------------------
label show_stranger_wrapper(transition=dissolve):
    # 不審者の見た目をランダム設定など（既存のsetup_strangerを呼ぶ）
    # 引数なしで呼ぶとランダム、引数ありなら固定など、setup_strangerの実装に依存
    $ setup_stranger()
    
    # 立ち絵表示
    show stranger with transition
    return

label hide_stranger_wrapper(transition=dissolve):
    hide stranger with transition
    return

# -----------------------------------------------------------------------------
# 警察官（Officer）用ラッパー
# -----------------------------------------------------------------------------
label show_officer_wrapper(transition=dissolve):
    show officer with transition
    return

label hide_officer_wrapper(transition=dissolve):
    hide officer with transition
    return

# -----------------------------------------------------------------------------
# お姉さん・先生（Woman）用ラッパー
# -----------------------------------------------------------------------------
label show_woman_wrapper(transition=dissolve):
    show woman with transition
    return

label hide_woman_wrapper(transition=dissolve):
    hide woman with transition
    return

# -----------------------------------------------------------------------------
# ユーティリティ
# -----------------------------------------------------------------------------
# スコア加算ラッパー（演出付き） - 既存のupdate_scoreを使うが、将来的な拡張のためにここを経由してもよい
# 現状は関数呼び出し $ update_score() が主流なので、ラベル版も用意しておく

label add_score(amount):
    if amount > 0:
        $ play_se("good")
    else:
        $ play_se("bad")
    $ update_score(amount)
    return
