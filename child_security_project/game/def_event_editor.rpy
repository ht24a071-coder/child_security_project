# =============================================================================
# イベントセリフ ルビエディタ
# リンクエディタから遷移して、イベント .rpy ファイルのセリフのルビを編集する
# =============================================================================

init -3 python:
    import os
    import re

    _event_editor_state = {
        "mode": "file_list",       # file_list, line_list, ruby_edit
        "files": [],               # [(filename, filepath), ...]
        "selected_file": None,     # filepath
        "selected_filename": None, # filename
        "lines": [],               # [(line_no, speaker, text, full_line), ...]
        "editing_line": None,      # (line_no, full_line)
    }

    def event_editor_scan_files():
        """events/ ディレクトリの .rpy ファイルを一覧"""
        events_dir = os.path.join(config.gamedir, "events")
        files = []
        if os.path.isdir(events_dir):
            for f in sorted(os.listdir(events_dir)):
                if f.endswith(".rpy"):
                    files.append((f, os.path.join(events_dir, f)))
        _event_editor_state["files"] = files
        return files

    def event_editor_extract_lines(filepath):
        """指定ファイルからセリフ行を抽出"""
        lines = []
        # セリフパターン:
        #   キャラ名 "テキスト"    → say文
        #   "テキスト"             → ナレーター
        #   "テキスト":            → メニュー選択肢
        say_pattern = re.compile(r'^(\s+)(?:(\w+)\s+)?"(.*)"(\s*:)?\s*$')

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                file_lines = f.readlines()
        except Exception:
            return lines

        for i, line in enumerate(file_lines):
            m = say_pattern.match(line)
            if m:
                indent = m.group(1)
                speaker = m.group(2) or ""
                text = m.group(3)
                is_menu = bool(m.group(4))  # ":" で終わる = メニュー選択肢
                # ルビタグが含まれる行、またはすべてのセリフ行を表示
                line_type = "menu" if is_menu else ("say" if speaker else "narr")
                lines.append({
                    "line_no": i + 1,
                    "speaker": speaker,
                    "text": text,
                    "type": line_type,
                    "full_line": line,
                    "indent": indent,
                })
        return lines

    def event_editor_open():
        """イベントエディタを開く"""
        event_editor_scan_files()
        _event_editor_state["mode"] = "file_list"
        _event_editor_state["selected_file"] = None
        _event_editor_state["selected_filename"] = None
        _event_editor_state["lines"] = []
        _event_editor_state["editing_line"] = None
        _link_editor_state["mode"] = "event_editor"
        renpy.restart_interaction()

    def event_editor_select_file(filename, filepath):
        """ファイルを選択してセリフ一覧を表示"""
        lines = event_editor_extract_lines(filepath)
        _event_editor_state["selected_file"] = filepath
        _event_editor_state["selected_filename"] = filename
        _event_editor_state["lines"] = lines
        _event_editor_state["mode"] = "line_list"
        renpy.restart_interaction()

    def event_editor_edit_line(line_info):
        """セリフのルビを編集"""
        text = line_info["text"]
        base_text, ruby_ranges = parse_ruby_text(text)
        _ruby_editor_state["text"] = base_text
        _ruby_editor_state["ruby_ranges"] = ruby_ranges
        _ruby_editor_state["selecting"] = False
        _ruby_editor_state["select_start"] = -1
        _event_editor_state["editing_line"] = line_info
        _event_editor_state["mode"] = "ruby_edit"
        _link_editor_state["mode"] = "event_ruby_edit"
        renpy.restart_interaction()

    def event_editor_save_ruby():
        """ルビ編集結果を .rpy ファイルに書き戻す"""
        new_text = ruby_editor_get_result()
        line_info = _event_editor_state["editing_line"]
        if not line_info:
            return

        filepath = _event_editor_state["selected_file"]
        line_no = line_info["line_no"]  # 1-indexed
        speaker = line_info["speaker"]
        indent = line_info["indent"]
        line_type = line_info["type"]

        # 新しい行を構築
        if line_type == "menu":
            new_line = '{}"{}":'.format(indent, new_text)
        elif speaker:
            new_line = '{}{} "{}"'.format(indent, speaker, new_text)
        else:
            new_line = '{}"{}"'.format(indent, new_text)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                file_lines = f.readlines()

            # 改行を保持
            original_newline = "\r\n" if file_lines[line_no - 1].endswith("\r\n") else "\n"
            file_lines[line_no - 1] = new_line + original_newline

            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(file_lines)

            renpy.notify("保存しました: L{}".format(line_no))
        except Exception as e:
            renpy.notify("保存失敗: " + str(e))

        # セリフ一覧に戻る（再読み込み）
        event_editor_select_file(
            _event_editor_state["selected_filename"],
            _event_editor_state["selected_file"]
        )
        _link_editor_state["mode"] = "event_editor"
        renpy.restart_interaction()

    def event_editor_cancel_ruby():
        """ルビ編集をキャンセル"""
        _ruby_editor_state["text"] = ""
        _ruby_editor_state["ruby_ranges"] = []
        _event_editor_state["editing_line"] = None
        _event_editor_state["mode"] = "line_list"
        _link_editor_state["mode"] = "event_editor"
        renpy.restart_interaction()

    def event_editor_back():
        """ファイル一覧に戻る"""
        _event_editor_state["mode"] = "file_list"
        _event_editor_state["selected_file"] = None
        _event_editor_state["lines"] = []
        renpy.restart_interaction()

    def event_editor_close():
        """イベントエディタを閉じてリンクエディタに戻る"""
        _event_editor_state["mode"] = "file_list"
        _link_editor_state["mode"] = "edit_links" if _link_editor_state.get("selected_node") else "select_node"
        renpy.restart_interaction()
