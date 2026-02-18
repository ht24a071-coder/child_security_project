# =============================================================================
# UI操作SE フレームワーク
# game/gui_system/ui_se.rpy
#
# 使い方:
#   ラベル内:  $ play_se("decide")
#   screen内:  action [SoundAction("decide"), ShowMenu("save")]
#              hovered SoundAction("hover")
# =============================================================================

init -2 python:

    # =========================================================================
    # SE定義テーブル
    # ここを編集するだけで全UIのSEを一括変更できる
    # =========================================================================
    UI_SE = {
        # キー名          : (ファイルパス,                    ボリューム)
        "hover"           : ("audio/se_ui_hover.mp3",         0.5),
        "decide"          : ("audio/se_ui_decide.mp3",        0.8),
        "cancel"          : ("audio/se_ui_cancel.mp3",        0.7),
        "good"            : ("audio/se_good.mp3",             1.0),
        "bad"             : ("audio/se_bad.mp3",              1.0),
        "buzzer"          : ("audio/buzzer.mp3",              1.0),
        "minigame_start"  : ("audio/se_ui_decide.mp3",        0.9),
        "minigame_hit"    : ("audio/se_ui_decide.mp3",        0.6),
        "minigame_result" : ("audio/se_good.mp3",             1.0),
    }

# =========================================================================
    # play_se() 関数 (修正版)
    # =========================================================================
    def play_se(key, channel="sound"):
        entry = UI_SE.get(key)
        if entry is None:
            print(f"SE Error: Key '{key}' not found.") # デバッグ用に表示
            return
            
        path, volume = entry

        # -----------------------------------------------------------
        # 【重要】 volume引数を削除し、relative_volume を使用するか、単純に再生する
        # Ren'Py 7.5 / 8.0 以降であれば relative_volume が使えます
        # それ以前のバージョンの場合は、volume指定を無視して再生するしかありません
        # -----------------------------------------------------------
        try:
            # 最新版Ren'Pyなら relative_volume が効く可能性があります
            renpy.sound.play(path, channel=channel, relative_volume=volume)
            
            # ※ 古いRen'Pyでエラーが出る場合は上記をコメントアウトし、下記を使ってください
            # renpy.sound.play(path, channel=channel)
            
        except Exception as e:
            # エラーを握りつぶさず、コンソールに出す
            print(f"SE Play Error: {e}")
            pass

    # =========================================================================
    # SoundAction クラス
    # screen の action / hovered / unhovered に渡して使う
    # =========================================================================
    class SoundAction(Action):
        """
        SE再生アクション。他のアクションとリストで組み合わせ可能。

        例:
            action [SoundAction("decide"), ShowMenu("save")]
            hovered SoundAction("hover")
        """
        def __init__(self, key, channel="sound"):
            self.key = key
            self.channel = channel

        def __call__(self):
            play_se(self.key)

        def __eq__(self, other):
            return isinstance(other, SoundAction) and self.key == other.key

        def __hash__(self):
            return hash(("SoundAction", self.key))
