# UI操作SE フレームワーク

`gui_system/ui_se.rpy` で定義されている、UI操作音（SE）の一元管理フレームワーク。

---

## ファイル構成

```
game/
└── gui_system/
    └── ui_se.rpy   ← フレームワーク本体
```

---

## SEの定義テーブル `UI_SE`

`ui_se.rpy` 内の `UI_SE` 辞書がすべてのSEを管理している。

```python
UI_SE = {
    # キー名          : (ファイルパス,                    ボリューム)
    "hover"           : ("audio/se_ui_hover.ogg",         0.5),
    "decide"          : ("audio/se_ui_decide.ogg",        0.8),
    "cancel"          : ("audio/se_ui_cancel.ogg",        0.7),
    "good"            : ("audio/se_good.ogg",             1.0),
    "bad"             : ("audio/se_bad.ogg",              1.0),
    "buzzer"          : ("audio/buzzer.mp3",              1.0),
    "minigame_start"  : ("audio/se_ui_decide.ogg",        0.9),
    "minigame_hit"    : ("audio/se_ui_decide.ogg",        0.6),
    "minigame_result" : ("audio/se_good.ogg",             1.0),
}
```

**SEを変更・追加するときはここだけ編集すればよい。**  
ファイルが存在しない場合は自動でスキップ（エラーにならない）。

---

## API

### `play_se(key, channel="sound")`

ラベル内やPythonコードからSEを再生する。

```renpy
label some_label:
    $ play_se("good")
    "せいかい！"
```

```python
# Python内から
play_se("buzzer")
```

---

### `SoundAction(key)`

`screen` の `action` や `hovered` に渡せるActionクラス。  
既存のアクションとリストで組み合わせて使う。

```renpy
# 決定SE + 画面遷移
textbutton "セーブ":
    action [SoundAction("decide"), ShowMenu("save")]
    hovered SoundAction("hover")

# キャンセルSE + 戻る
textbutton "戻る":
    action [SoundAction("cancel"), Return()]
    hovered SoundAction("hover")
```

---

## 現在SEが組み込まれている箇所

| 画面 | ボタン | SEキー |
|---|---|---|
| メインメニュー | 全ボタン | `decide` / `hover` |
| ゲームメニュー ナビゲーション | 全ボタン | `decide` / `cancel` / `hover` |
| ゲームメニュー | 「戻る」ボタン | `cancel` / `hover` |
| クイックメニュー | 全ボタン | `decide` / `cancel` / `hover` |
| 選択肢（`choice`） | 全選択肢 | `decide` / `hover` |
| ミニゲームイントロ | 「START」ボタン | `minigame_start` / `hover` |

---

## 新しいSEを追加する手順

1. `UI_SE` テーブルに1行追加する

```python
"my_se": ("audio/my_sound.ogg", 0.8),
```

2. 使いたい場所で呼ぶ

```renpy
$ play_se("my_se")
# または
action [SoundAction("my_se"), SomeAction()]
```

以上。音源ファイルを後から追加しても自動で反映される。
