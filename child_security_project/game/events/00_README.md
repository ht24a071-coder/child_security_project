# イベントフレームワーク利用ガイド

## 概要
イベント演出の統一と保守性を高めるため、共通フレームワーク `00_event_framework.rpy` を導入しました。
キャラクターの立ち絵表示（表示・非表示）はこのフレームワークを通して行います。

## 主な変更点

以下のラッパーラベル（関数のようなもの）を使用してください。

### 不審者 (Stranger)
- **表示**: `call show_stranger_wrapper`
- **非表示**: `call hide_stranger_wrapper`

例：
```renpy
label encounter_e_stranger:
    "だれかが 近づいてきた。"
    
    # 以前: show stranger with dissolve
    call show_stranger_wrapper
    
    stranger "こんにちは..."
```

### 警察官 (Officer)
- **表示**: `call show_officer_wrapper`
- **非表示**: `call hide_officer_wrapper`

### お姉さん・先生 (Woman)
- **表示**: `call show_woman_wrapper`
- **非表示**: `call hide_woman_wrapper`

## ディレクトリ構成
イベントファイルは以下のフォルダに整理されています。

- `game/events/stranger/`: 不審者との遭遇イベント
- `game/events/safe/`: 安全な人（警察官など）とのイベント
- `game/events/special/`: 特殊イベント（110番の家など）
- `game/events/framework/`: フレームワーク定義（※現在は `game/events/00_event_framework.rpy` に配置）

## 新しいイベントを追加する場合
1. 適切なフォルダ（`stranger` など）に `.rpy` ファイルを作成します。
2. ラベル名を `game/definitions.rpy` や `game/mapdata.json` のイベントプールに登録します。
3. 立ち絵の表示には必ず上記のラッパーを使用してください。
