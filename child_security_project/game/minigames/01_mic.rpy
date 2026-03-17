# =============================================================================
# Windows ネイティブ マイクおと量検出
# そと部ライブラリ不要 - Windows API (winmm.dll) を直接使用
# =============================================================================

init -1 python:
    import sys
    import struct
    import threading
    import time
    
    # Windows専用マイク機能
    _win_mic_available = False
    _win_mic_error = ""
    
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            
            # Windows Multimedia API
            winmm = ctypes.windll.winmm
            
            # 定数
            WAVE_FORMAT_PCM = 1
            WAVE_MAPPER = -1
            CALLBACK_NULL = 0
            WHDR_DONE = 0x00000001
            WHDR_PREPARED = 0x00000002
            
            # WAVEFORMATEX構造からだ
            class WAVEFORMATEX(ctypes.Structure):
                _fields_ = [
                    ("wFormatTag", wintypes.WORD),
                    ("nChannels", wintypes.WORD),
                    ("nSamplesPerSec", wintypes.DWORD),
                    ("nAvgBytesPerSec", wintypes.DWORD),
                    ("nBlockAlign", wintypes.WORD),
                    ("wBitsPerSample", wintypes.WORD),
                    ("cbSize", wintypes.WORD),
                ]
            
            # WAVEHDR構造からだ
            class WAVEHDR(ctypes.Structure):
                _fields_ = [
                    ("lpData", ctypes.POINTER(ctypes.c_char)),
                    ("dwBufferLength", wintypes.DWORD),
                    ("dwBytesRecorded", wintypes.DWORD),
                    ("dwUser", ctypes.POINTER(wintypes.DWORD)),
                    ("dwFlags", wintypes.DWORD),
                    ("dwLoops", wintypes.DWORD),
                    ("lpNext", ctypes.c_void_p),
                    ("reserved", ctypes.POINTER(wintypes.DWORD)),
                ]
            
            _win_mic_available = True
            
        except Exception as e:
            _win_mic_error = str(e)
    else:
        _win_mic_error = "WindowsいがいのOSです"


    class WinMicRecorder:
        """Windows APIを使ったマイク録おとクラス（ダブルバッファリング）"""
        
        NUM_BUFFERS = 4
        
        def __init__(self, sample_rate=22050, buffer_size=2048):
            self.sample_rate = sample_rate
            self.buffer_size = buffer_size
            self.hwi = ctypes.c_void_p()
            self.is_recording = False
            self.current_volume = 0.0
            self.buffers = []
            self.headers = None  # ctypes配列として保持
            self._lock = threading.Lock()
            self.debug_info = ""
            self._buffer_count = 0  # デバッグ用カウンタ
        
        def start(self):
            """録おとかいし"""
            if not _win_mic_available:
                self.debug_info = "not available"
                return False
            
            try:
                # フォーマットせってい
                fmt = WAVEFORMATEX()
                fmt.wFormatTag = WAVE_FORMAT_PCM
                fmt.nChannels = 1
                fmt.nSamplesPerSec = self.sample_rate
                fmt.wBitsPerSample = 16
                fmt.nBlockAlign = fmt.nChannels * fmt.wBitsPerSample // 8
                fmt.nAvgBytesPerSec = fmt.nSamplesPerSec * fmt.nBlockAlign
                fmt.cbSize = 0
                
                # デバイスオープン
                result = winmm.waveInOpen(
                    ctypes.byref(self.hwi),
                    WAVE_MAPPER,
                    ctypes.byref(fmt),
                    0,
                    0,
                    CALLBACK_NULL
                )
                
                if result != 0:
                    self.debug_info = f"open error: {result}"
                    return False
                
                # 複数バッファじゅんび - ctypes配列として確保
                buf_size = self.buffer_size * 2  # 16bit = 2bytes per sample
                self.headers = (WAVEHDR * self.NUM_BUFFERS)()
                
                for i in range(self.NUM_BUFFERS):
                    buf = ctypes.create_string_buffer(buf_size)
                    self.buffers.append(buf)
                    
                    self.headers[i].lpData = ctypes.cast(buf, ctypes.POINTER(ctypes.c_char))
                    self.headers[i].dwBufferLength = buf_size
                    self.headers[i].dwFlags = 0
                    self.headers[i].dwBytesRecorded = 0
                    
                    result = winmm.waveInPrepareHeader(self.hwi, ctypes.byref(self.headers[i]), ctypes.sizeof(WAVEHDR))
                    if result != 0:
                        self.debug_info = f"prepare error: {result}"
                        return False
                    
                    result = winmm.waveInAddBuffer(self.hwi, ctypes.byref(self.headers[i]), ctypes.sizeof(WAVEHDR))
                    if result != 0:
                        self.debug_info = f"addbuf error: {result}"
                        return False
                
                # 録おとかいし
                result = winmm.waveInStart(self.hwi)
                if result != 0:
                    self.debug_info = f"start error: {result}"
                    return False
                
                self.is_recording = True
                self.debug_info = "recording"
                
                # おと量取得スレッドかいし
                self._thread = threading.Thread(target=self._update_volume, daemon=True)
                self._thread.start()
                
                return True
                
            except Exception as e:
                self.debug_info = f"exception: {e}"
                return False
        
        def _update_volume(self):
            """おと量を継続的に更新"""
            while self.is_recording:
                try:
                    found_done = False
                    for i in range(self.NUM_BUFFERS):
                        flags = self.headers[i].dwFlags
                        if flags & WHDR_DONE:
                            found_done = True
                            self._buffer_count += 1
                            # バッファからデータ取得
                            recorded = self.headers[i].dwBytesRecorded
                            if recorded >= 2:
                                data = self.buffers[i].raw[:recorded]
                                # 16bit PCMデータからおと量計算
                                num_samples = len(data) // 2
                                samples = struct.unpack(f"<{num_samples}h", data)
                                if samples:
                                    # RMS計算
                                    sum_sq = sum(s*s for s in samples)
                                    rms = (sum_sq / num_samples) ** 0.5
                                    # 0-1に正規化（感度をしたげる）
                                    # 元は2000だったが、小こえで100%にならないように10000へ変更
                                    with self._lock:
                                        self.current_volume = min(1.0, rms / 10000)
                                        self.debug_info = f"vol:{int(rms)}/{10000} buf:{self._buffer_count}"
                            
                            # バッファを再度キューに追加（PREPAREDフラグは維持）
                            self.headers[i].dwFlags = WHDR_PREPARED
                            self.headers[i].dwBytesRecorded = 0
                            winmm.waveInAddBuffer(self.hwi, ctypes.byref(self.headers[i]), ctypes.sizeof(WAVEHDR))
                    
                    if not found_done:
                        with self._lock:
                            self.debug_info = f"waiting buf:{self._buffer_count}"
                    
                    time.sleep(0.01)
                    
                except Exception as e:
                    with self._lock:
                        self.debug_info = f"update error: {e}"
        
        def get_volume(self):
            """いまのおと量を取得 (0.0-1.0)"""
            with self._lock:
                return self.current_volume
        
        def stop(self):
            """録おと停止"""
            self.is_recording = False
            time.sleep(0.05)  # スレッドしゅうりょうを待つ
            try:
                if self.hwi:
                    winmm.waveInStop(self.hwi)
                    winmm.waveInReset(self.hwi)
                    if self.headers:
                        for i in range(self.NUM_BUFFERS):
                            winmm.waveInUnprepareHeader(self.hwi, ctypes.byref(self.headers[i]), ctypes.sizeof(WAVEHDR))
                    winmm.waveInClose(self.hwi)
                    self.hwi = ctypes.c_void_p()
                    self.buffers = []
                    self.headers = None
            except:
                pass

        def __getstate__(self):
            # ctypesオブジェクト、スレッド、ロックは保存できないため除外
            state = self.__dict__.copy()
            state['hwi'] = None
            state['headers'] = None
            state['buffers'] = []
            state['_thread'] = None
            state['_lock'] = None
            state['is_recording'] = False
            return state

        def __setstate__(self, state):
            self.__dict__.update(state)
            import threading
            self.hwi = ctypes.c_void_p()
            self.headers = None
            self.buffers = []
            self._lock = threading.Lock()
            self._thread = None


    class ShoutMinigame:
        """
        おおごえミニゲーム（ふしんしゃ撃退・HP制）
        Windows: マイク使用
        その他: ボタンれんだフォールバック
        """
        def __init__(self, 
            threshold=0.6, # 90dB相当
            duration=8.0,  # 制限じかんを長めに（削り切る必要があるため）
            hp=100,        # ふしんしゃのHP
            title=None,    # イントロ画面タイトル
            text=None):    # イントロ画面説明文
            self.threshold = threshold
            self.duration = duration
            self.max_hp = hp
            self.current_hp = hp
            
            # イントロオーバーレイ用（BaseMinigame互換）
            self.started = False
            self.key = "dismiss"  # イントロ用（実際のゲーム入ちからとは別）
            
            # マイク機能チェック（タイトル・テキストけっていまえに必要）
            self.mic_available = _win_mic_available
            
            # タイトル・テキスト（マイク有無で自動切り替え）
            if title is not None:
                self.title = title
            elif self.mic_available:
                self.title = "おおごえミニゲーム"
            else:
                self.title = "れんだミニゲーム"
            
            if text is not None:
                self.text = text
            elif self.mic_available:
                self.text = "おおきなこえで\nふしんしゃを げきたいしろ！"
            else:
                self.text = "ボタンを れんだして\nふしんしゃを げきたいしろ！"
            
            self.result = None
            self.show_result = False
            self.finished = False
            self.start_time = None
            self.elapsed = 0.0
            
            # おと量関連
            self.current_volume = 0.0
            self.max_volume = 0.0
            
            self.recorder = None
            
            # フォールバック用
            self.mash_count = 0
            
            # 演出用
            self.shout_texts = [] 
            self.next_text_time = 0.0
            self.shake_offset = (0, 0)
            self.stranger_shake = (0, 0) # ふしんしゃの揺れ
            self.damage_flash = 0.0      # ダメージじの赤フラッシュ
            
            self.debug_info = ""
            self.mic_started = False
            self.start_real_time = None
            
            self.shout_phrases = [
                "たすけて！", "やめて！", "こないで！", "だれかー！", "うわあああん！", "あっちいけ！"
            ]

        def get_remaining(self):
            """のこりじかんをリアルタイムで取得"""
            if self.start_real_time is None:
                return self.duration
            import time
            elapsed = time.time() - self.start_real_time
            return max(0.0, self.duration - elapsed)

        def start_mic(self):
            if not self.mic_available:
                return False
            try:
                self.recorder = WinMicRecorder()
                return self.recorder.start()
            except:
                self.mic_available = False
                return False

        def stop_mic(self):
            if self.recorder:
                self.recorder.stop()
                self.recorder = None

        def update(self, st, at):
            import time
            if self.start_time is None:
                self.start_time = st
                self.start_real_time = time.time()
                if self.mic_available:
                    self.start_mic()
            
            self.elapsed = time.time() - self.start_real_time
            dt = 0.02 # 近似deltaTime
            
            # マイクおと量取得
            if self.mic_available and self.recorder:
                self.current_volume = self.recorder.get_volume()
                self.max_volume = max(self.max_volume, self.current_volume)
            
            # じかん切れ判定
            if not self.show_result and self.elapsed >= self.duration:
                self.stop_mic()
                if self.current_hp <= 0:
                    self.result = "perfect" # ギリギリ倒せた
                else:
                    self.result = "miss"    # 倒せなかった
                self.show_result = True
                self.finished = True
            
            # ゲームプレイなか（HP判定とダメージ処理）
            if not self.show_result:
                # 攻撃ちから計算（閾値を超えたふんだけダメージ）
                damage = 0
                is_attacking = False
                
                if self.mic_available:
                    # 判定基準を厳しくする (閾値の80%以うえから有効)
                    damage_threshold = self.threshold * 0.8
                    
                    if self.current_volume >= damage_threshold:
                        # 以まえはおと量に応じてダメージが変わっていたが、
                        # 「ちかくで叫べばすぐ終わる」という問題を解消するため固定値に変更
                        # 3.0ダメージ/frame -> 60FPSで180DPS -> HP500を3びょう弱
                        # 調整: HP=100ならもっと低く。
                        # いまのHP=100 (init参照)。duration=5.0s。
                        # 5びょうで削り切るには 20DPS 必要 = 20/60 = 0.33/frame?
                        # updateは dt=0.02 (50FPS相当) で呼ばれているまえ提なら
                        # 100 / (5.0 * 50) = 0.4 damage/frame
                        # 余裕を持たせて 0.6 くらいにする
                        
                        # 修正: updateはRen'PyのDisplayable updateなのでFPS依存だが、dt=0.02固定で計算している
                        # 実際には st - start_time で経過じかんはただしいが、1フレームの重みはフレームレートによる
                        # とはいえ、dt=0.02 固定加算ではないので、
                        # 確実に削れるようにすこし大きめにせってい
                        
                        damage = 0.8  # 固定ダメージ (約2びょう～3びょうで満タンから削りきれるくらい)
                        is_attacking = True
                else:
                    # れんだモードはうしろ述のon_mashで処理
                    pass

                # ダメージ適用
                if damage > 0:
                    self.current_hp = max(0, self.current_hp - damage)
                    self.damage_flash = min(1.0, self.damage_flash + 0.2) # 赤くひかりらせる
                    
                    # ふしんしゃ揺らし
                    import random
                    shake_amp = int(5 * damage) 
                    self.stranger_shake = (random.randint(-shake_amp, shake_amp), random.randint(-shake_amp, shake_amp))
                    
                    # 画面揺らし (閾値超えなら激しく)
                    if self.current_volume >= self.threshold:
                        self.shake_offset = (random.randint(-5, 5), random.randint(-5, 5))
                    
                    # テキスト演出 (閾値超えのみ)
                    if st > self.next_text_time and self.current_volume >= self.threshold:
                        txt = random.choice(self.shout_phrases)
                        x = 0.5 + random.uniform(-0.4, 0.4)
                        y = 0.5 + random.uniform(-0.4, 0.4)
                        size = 40 + int(80 * self.current_volume)
                        self.shout_texts.append([txt, x, y, st, size])
                        self.next_text_time = st + 0.15
                else:
                    self.shake_offset = (0, 0)
                    self.stranger_shake = (0, 0)
                    self.damage_flash = max(0.0, self.damage_flash - 0.1)

                # 撃退完了チェック
                if self.current_hp <= 0:
                    self.stop_mic()
                    self.result = "perfect"
                    self.show_result = True
                    self.finished = True

            # HPバー表示用（割合）
            hp_ratio = self.current_hp / self.max_hp
            
            # バーのいろ（HPに応じて変化）
            if hp_ratio > 0.5:
                bar_color = "#00ff00"
            elif hp_ratio > 0.2:
                bar_color = "#ffff00"
            else:
                bar_color = "#ff0000"
            
            return Solid(bar_color, xsize=int(400 * hp_ratio), ysize=30), dt

        def on_mash(self):
            """れんだ攻撃"""
            if self.show_result or self.finished:
                return
            
            # れんだダメージ
            damage = 4.0
            self.current_hp = max(0, self.current_hp - damage)
            self.damage_flash = 1.0
            
            import random
            self.stranger_shake = (random.randint(-5, 5), random.randint(-5, 5))
            
            if self.current_hp <= 0:
                self.result = "perfect"
                self.show_result = True
                self.finished = True

        def __getstate__(self):
            # recorderは保存できないWinMicRecorderを含むため除外
            state = self.__dict__.copy()
            state['recorder'] = None
            return state

        def __setstate__(self, state):
            self.__dict__.update(state)
            # 再開じに必要ならupdate内で再生成されるロジックにするか、Noneのままにする
            # ここではrecorderをNoneにして、update時のstart_micに任せる
            self.recorder = None


    def mic_get_status():
        return {
            "available": _win_mic_available,
            "error": _win_mic_error,
            "platform": sys.platform
        }


# =============================================================================
# おおごえミニゲーム画面（ふしんしゃバトル版）
# =============================================================================
screen shout_minigame(game):
    modal True
    zorder 200 # ミニマップ(98)よりてまえに表示
    
    # イントロオーバーレイ（STARTボタン押したまえ）
    if not game.started:
        use minigame_intro_overlay(game)
    else:
        # ゲームほん編
        if not game.finished:
            timer 0.05 repeat True action Function(renpy.restart_interaction)
        
        add Solid("#000000DD")
        
        # ---------------------------------------------------------------
        # 背景アニメーション（激しさ・爆発感 / 赤・黄いろ系）
        # ---------------------------------------------------------------
        # おと波を模した同こころ円（パルス）
        add Solid("#330000", xsize=600, ysize=600):
            align (0.5, 0.5)
            at mg_bg_pulse(delay=0.0, lo=0.8, hi=1.2, period=1.2)
        add Solid("#220000", xsize=900, ysize=900):
            align (0.5, 0.5)
            at mg_bg_pulse(delay=0.4, lo=0.85, hi=1.1, period=1.6)
        add Solid("#110000", xsize=1200, ysize=1200):
            align (0.5, 0.5)
            at mg_bg_pulse(delay=0.8, lo=0.9, hi=1.05, period=2.0)

        # ひだりみぎに浮遊する炎のような図かたち
        add Solid("#ff2200", xsize=80, ysize=80) rotate 45 alpha 0.15:
            align (0.05, 0.4)
            at mg_bg_float(delay=0.0, amp=30)
        add Solid("#ff6600", xsize=60, ysize=60) rotate 30 alpha 0.15:
            align (0.95, 0.3)
            at mg_bg_float(delay=0.7, amp=25)
        add Solid("#ffaa00", xsize=50, ysize=50) rotate 60 alpha 0.15:
            align (0.08, 0.7)
            at mg_bg_float(delay=1.4, amp=20)
        add Solid("#ff4400", xsize=70, ysize=70) rotate 15 alpha 0.15:
            align (0.92, 0.65)
            at mg_bg_float(delay=0.3, amp=35)

        # ダメージフラッシュ（damage_flash > 0 のとき赤くひかりる）
        if game.damage_flash > 0.0:
            add Solid("#ff0000", xsize=1920, ysize=1080) alpha game.damage_flash:
                at mg_flash_in

        # ---------------------------------------------------------------
        
        # 叫び文字演出（背景側）
        # スレッドあんぜんのためコピーして回す
        $ display_shout_texts = list(game.shout_texts)
        for txt_data in display_shout_texts:
            $ txt = txt_data[0]
            $ tx = txt_data[1]
            $ ty = txt_data[2]
            $ t_size = txt_data[4]
            if renpy.get_game_runtime() - txt_data[3] < 0.6:
                text "[txt]":
                    size t_size
                    xalign tx
                    yalign ty
                    color "#ff3333"
                    bold True
                    outlines [(3, "#ffffff", 0, 0)]
        
        # メインフレーム
        frame:
            xalign 0.5
            yalign 0.5
            padding (40, 40)
            background None # 背景なしでオーバーレイかぜに
            xoffset game.shake_offset[0]
            yoffset game.shake_offset[1]
            
            vbox:
                spacing 20
                xalign 0.5
                
                # タイトル
                if game.mic_available:
                    text "こえで げきたいしろ！":
                        size 50
                        xalign 0.5
                        color "#ff0000"
                        bold True
                        outlines [(2, "#ffffff", 0, 0)]
                else:
                    text "れんだで げきたいしろ！":
                        size 50
                        xalign 0.5
                        color "#ff0000"
                        bold True
                        outlines [(2, "#ffffff", 0, 0)]

                null height 180

                # ふしんしゃエリア（HPバー + 画像）
                frame:
                    background None
                    xalign 0.5
                    ysize 400
                    xsize 400
                    
                    # ふしんしゃの画像（いま遭遇しているふしんしゃを表示）
                    $ st_img_path = "images/actor/stranger2.png" if getattr(store, "stranger_type", "stranger") == "stranger2" else "images/actor/stranger.png"
                    add st_img_path:
                        xalign 0.5
                        yalign 1.0
                        zoom 0.6
                        xoffset game.stranger_shake[0]
                        yoffset game.stranger_shake[1]
                    
                    # HPバー（あたまうえ）
                    vbox:
                        xalign 0.5
                        yalign 0.0
                        spacing 5
                        
                        text "ふしんしゃの HP":
                            size 24
                            color "#ffffff"
                            xalign 0.5
                            outlines [(1, "#000000", 0, 0)]
                            
                        frame:
                            background "#333333"
                            xsize 400
                            ysize 30
                            xalign 0.5
                            
                            add DynamicDisplayable(game.update):
                                xalign 0.0
                                ycenter 0.5
                
                null height 20
                
                # のこりじかん
                $ remaining = game.get_remaining()
                text "のこり: [remaining:.1f] びょう":
                    size 40
                    xalign 0.5
                    color "#ffff00"
                    bold True
                    outlines [(2, "#000000", 0, 0)]
                
                # 自ふんのおと量メーター（した部）
                if game.mic_available:
                    vbox:
                        xalign 0.5
                        spacing 5
                        text "あなたの こえの おおきさ":
                            size 20
                            color "#aaaaaa"
                            xalign 0.5
                        
                        frame:
                            xsize 300
                            ysize 20
                            background "#333333"
                            xalign 0.5
                            
                            # いまのおと量バー
                            $ v_width = int(300 * min(1.0, game.current_volume / game.threshold))
                            frame:
                                background "#00ffff"
                                xsize v_width
                                ysize 20
                                xalign 0.0

                # フォールバックあんない
                elif not game.mic_available:
                    text "ボタンを れんだ！！":
                        size 30
                        color "#ff8800"
                        bold True

        # 入ちから処理（例そと防止のため全てのキーをキャッチしてなにもしない）
        if not game.show_result:
            if not game.mic_available:
                key "K_SPACE" action Function(game.on_mash)
                key "dismiss" action Function(game.on_mash)
            else:
                # マイク使用じはキーで抜けないようダミーを置く
                key "dismiss" action []
            
            # システムキー等の誤爆防止
            key "K_ESCAPE" action []
            key "K_RETURN" action []
            key "K_KP_ENTER" action []
            key "joy_dismiss" action []
        
        # 結果表示
        if game.show_result:
            frame:
                xalign 0.5
                yalign 0.5
                background Solid("#000000aa")
                padding (50, 30)
                
                if game.result == "perfect":
                    text "げきたい せいこう！！":
                        size 80
                        color "#ffff00"
                        bold True
                        outlines [(4, "#ff0000", 0, 0)]
                else:
                    text "げきたい しっぱい……":
                        size 60
                        color "#aaaaaa"
                        bold True
            
            timer 2.5 action Return(game.result)


# =============================================================================
# マイクせってい・デバッグ画面
# =============================================================================
screen mic_settings():
    modal True
    add Solid("#000000DD")
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        padding (40, 40)
        background "#222244"
        
        vbox:
            spacing 20
            xalign 0.5
            
            text "マイクせってい":
                size 40
                color "#ffffff"
                bold True
                xalign 0.5
            
            null height 20
            
            # 状態表示
            $ status = mic_get_status()
            $ mic_ok = status["available"]
            $ mic_err = status["error"]
            $ mic_platform = status["platform"]
            
            text "OS: [mic_platform]":
                size 20
                color "#aaaaaa"
            
            if mic_ok:
                text "✓ マイク: 使用可能":
                    size 28
                    color "#00ff00"
            else:
                text "✗ マイク: 使用不可":
                    size 28
                    color "#ff0000"
                if mic_err:
                    $ err_msg = mic_err
                    text "[err_msg]":
                        size 16
                        color "#ff6666"
                text "（ボタンれんだモードで動作します）":
                    size 18
                    color "#888888"
            
            null height 30
            
            # とじるボタン
            textbutton "とじる":
                xalign 0.5
                action Return()
                text_size 28
                text_color "#ffffff"