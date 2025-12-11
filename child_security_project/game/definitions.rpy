init -1 python:
    # イベントリスト
    suspicious_events = []  # 危険イベントリスト
    safe_events = []        # 安全イベントリスト

# その他の定義（define, default）
define PROB_SUSPICIOUS = 20  # 危険イベント発生確率（％）
define MAX_STEPS = 10  # マップ移動の最大ステップ数

# キャラ管理
define i = Character("常に右にいる人", color="#c8ffc8")
define t = Character("伊東マンショ", color="#c8ffc8")

default current_step = 0 # 現在のステップ数
default has_encountered_suspicious = False # 危険イベント遭遇フラグ
default flag_know_110 = False # 110番通報を知っているかどうか