# =============================================================================
# マップエディタツール
# コンソールから mapdata.json を編集するための関数群
# 使い方: Shift+O でコンソールを開き、コマンドを入力
# =============================================================================

init -5 python:
    import json
    import os
    import re
    
    # =========================================================================
    # JSON読み書き関数
    # =========================================================================
    
    def _get_mapdata_path():
        """mapdata.json のフルパスを取得"""
        return os.path.join(config.gamedir, "mapdata.json")
    
    def _load_mapdata():
        """mapdata.json を読み込む"""
        path = _get_mapdata_path()
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _save_mapdata(data):
        """mapdata.json に保存"""
        path = _get_mapdata_path()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # メモリ上のデータも更新
        global world_map, event_pools
        world_map = data["world_map"]
        event_pools = data["event_pools"]
    
    # =========================================================================
    # ルビ変換ヘルパー
    # =========================================================================
    
    def ruby(text):
        """
        簡易ルビ記法を Ren'Py 形式に変換
        例: ruby("道(みち)を進(すす)む") → "{rb}道{/rb}{rt}みち{/rt}を{rb}進{/rb}{rt}すす{/rt}む"
        """
        # パターン: 漢字(ふりがな)
        pattern = r'([一-龯々]+)\(([ぁ-んァ-ン]+)\)'
        result = re.sub(pattern, r'{rb}\1{/rb}{rt}\2{/rt}', text)
        return result
    
    # =========================================================================
    # ノード管理コマンド
    # =========================================================================
    
    def add_node(name, bg, x, y, group="safe", chance=0):
        """
        ノードを追加または編集
        
        引数:
            name: ノード名 (例: "street_1")
            bg: 背景画像名 (例: "back_town")
            x, y: ミニマップ座標
            group: イベントグループ (safe/suspicious/crossing/none)
            chance: イベント発生確率 (0-100)
        
        使用例:
            add_node("new_street", "back_street_0", 300, 400)
            add_node("danger_zone", "back_tunnel", 200, 300, "suspicious", 50)
        """
        data = _load_mapdata()
        
        is_edit = name in data["world_map"]
        
        if is_edit:
            # 既存ノードを編集（linksは保持）
            existing_links = data["world_map"][name].get("links", {})
            data["world_map"][name] = {
                "bg": bg,
                "links": existing_links,
                "group": group,
                "chance": chance,
                "minimap": [x, y]
            }
            action = "編集"
        else:
            # 新規ノードを追加
            data["world_map"][name] = {
                "bg": bg,
                "links": {},
                "group": group,
                "chance": chance,
                "minimap": [x, y]
            }
            action = "追加"
        
        _save_mapdata(data)
        
        # map_coordinates も更新
        global map_coordinates
        map_coordinates[name] = (x, y)
        
        print("✓ ノード '{}' を{}しました".format(name, action))
        print("  bg: {}, 座標: ({}, {}), group: {}, chance: {}".format(bg, x, y, group, chance))
        return True
    
    def delete_node(name):
        """
        ノードを削除
        
        使用例:
            delete_node("test_node")
        """
        data = _load_mapdata()
        
        if name not in data["world_map"]:
            print("✗ ノード '{}' が見つかりません".format(name))
            return False
        
        del data["world_map"][name]
        _save_mapdata(data)
        
        # map_coordinates からも削除
        global map_coordinates
        if name in map_coordinates:
            del map_coordinates[name]
        
        print("✓ ノード '{}' を削除しました".format(name))
        return True
    
    def show_node(name):
        """
        ノードの詳細を表示
        
        使用例:
            show_node("start_point")
        """
        data = _load_mapdata()
        
        if name not in data["world_map"]:
            print("✗ ノード '{}' が見つかりません".format(name))
            return
        
        node = data["world_map"][name]
        print("=" * 50)
        print("ノード: {}".format(name))
        print("=" * 50)
        print("  bg: {}".format(node.get("bg", "未設定")))
        print("  minimap: {}".format(node.get("minimap", [0, 0])))
        print("  group: {}".format(node.get("group", "safe")))
        print("  chance: {}".format(node.get("chance", 0)))
        print("  links:")
        links = node.get("links", {})
        if links:
            for text, dest in links.items():
                print("    「{}」 → {}".format(text, dest))
        else:
            print("    (なし)")
        print("=" * 50)
    
    def list_nodes():
        """
        全ノードの一覧を表示
        
        使用例:
            list_nodes()
        """
        data = _load_mapdata()
        nodes = data["world_map"]
        
        print("=" * 60)
        print("全ノード一覧 ({} 件)".format(len(nodes)))
        print("=" * 60)
        for name, node in sorted(nodes.items()):
            coords = node.get("minimap", [0, 0])
            link_count = len(node.get("links", {}))
            print("  {} [bg:{}, pos:({},{}), links:{}]".format(
                name, node.get("bg", "?"), coords[0], coords[1], link_count))
        print("=" * 60)
    
    # =========================================================================
    # リンク管理コマンド
    # =========================================================================
    
    def add_link(from_node, text, to_node):
        """
        ノード間のリンクを追加
        
        引数:
            from_node: リンク元ノード名
            text: 選択肢テキスト (ruby()関数でルビ付けも可)
            to_node: リンク先ノード名
        
        使用例:
            add_link("street_1", "先へ進む", "street_2")
            add_link("street_1", ruby("先(さき)へ進(すす)む"), "street_2")
        """
        data = _load_mapdata()
        
        if from_node not in data["world_map"]:
            print("✗ 元ノード '{}' が見つかりません".format(from_node))
            return False
        
        if to_node not in data["world_map"]:
            print("✗ 先ノード '{}' が見つかりません".format(to_node))
            return False
        
        data["world_map"][from_node]["links"][text] = to_node
        _save_mapdata(data)
        
        print("✓ リンクを追加しました")
        print("  {} →「{}」→ {}".format(from_node, text, to_node))
        return True
    
    def remove_link(from_node, text):
        """
        リンクを削除
        
        使用例:
            remove_link("street_1", "先へ進む")
        """
        data = _load_mapdata()
        
        if from_node not in data["world_map"]:
            print("✗ ノード '{}' が見つかりません".format(from_node))
            return False
        
        links = data["world_map"][from_node].get("links", {})
        if text not in links:
            print("✗ リンク「{}」が見つかりません".format(text))
            print("  現在のリンク:")
            for t in links:
                print("    - {}".format(t))
            return False
        
        del data["world_map"][from_node]["links"][text]
        _save_mapdata(data)
        
        print("✓ リンク「{}」を削除しました".format(text))
        return True
    
    def show_links(node_name):
        """
        ノードのリンク一覧を表示
        
        使用例:
            show_links("street_1")
        """
        data = _load_mapdata()
        
        if node_name not in data["world_map"]:
            print("✗ ノード '{}' が見つかりません".format(node_name))
            return
        
        links = data["world_map"][node_name].get("links", {})
        print("=" * 50)
        print("ノード '{}' のリンク ({} 件)".format(node_name, len(links)))
        print("=" * 50)
        if links:
            for i, (text, dest) in enumerate(links.items(), 1):
                print("  {}. 「{}」 → {}".format(i, text, dest))
        else:
            print("  (リンクなし)")
        print("=" * 50)
    
    # =========================================================================
    # ヘルプ
    # =========================================================================
    
    def map_help():
        """マップエディタのヘルプを表示"""
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                    マップエディタ コマンド一覧                       ║
╠══════════════════════════════════════════════════════════════════╣
║ ■ ノード管理                                                     ║
║   add_node("name", "bg", x, y)      ノード追加/編集               ║
║   add_node("name", "bg", x, y, "group", chance)  フルオプション   ║
║   delete_node("name")               ノード削除                    ║
║   show_node("name")                 ノード詳細表示                ║
║   list_nodes()                      全ノード一覧                  ║
║                                                                  ║
║ ■ リンク管理                                                     ║
║   add_link("from", "表示テキスト", "to")  リンク追加              ║
║   remove_link("from", "表示テキスト")     リンク削除              ║
║   show_links("node")                      リンク一覧              ║
║                                                                  ║
║ ■ ルビ変換                                                       ║
║   ruby("道(みち)")  → {rb}道{/rb}{rt}みち{/rt}                    ║
║                                                                  ║
║ ■ ヘルプ                                                         ║
║   map_help()                        このヘルプを表示              ║
╚══════════════════════════════════════════════════════════════════╝
        """)
