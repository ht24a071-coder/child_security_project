# =============================================================================
# Windows ネイティブ マイク音量検出
# 外部ライブラリ不要 - Windows API (winmm.dll) を直接使用
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
            
            # WAVEFORMATEX構造体
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
            
            # WAVEHDR構造体
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
        _win_mic_error = "Windows以外のOSです"


    class WinMicRecorder:
        """Windows APIを使ったマイク録音クラス（ダブルバッファリング）"""
        
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
            """録音開始"""
            if not _win_mic_available:
                self.debug_info = "not available"
                return False
            
            try:
                # フォーマット設定
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
                
                # 複数バッファ準備 - ctypes配列として確保
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
                
                # 録音開始
                result = winmm.waveInStart(self.hwi)
                if result != 0:
                    self.debug_info = f"start error: {result}"
                    return False
                
                self.is_recording = True
                self.debug_info = "recording"
                
                # 音量取得スレッド開始
                self._thread = threading.Thread(target=self._update_volume, daemon=True)
                self._thread.start()
                
                return True
                
            except Exception as e:
                self.debug_info = f"exception: {e}"
                return False
        
        def _update_volume(self):
            """音量を継続的に更新"""
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
                                # 16bit PCMデータから音量計算
                                num_samples = len(data) // 2
                                samples = struct.unpack(f"<{num_samples}h", data)
                                if samples:
                                    # RMS計算
                                    sum_sq = sum(s*s for s in samples)
                                    rms = (sum_sq / num_samples) ** 0.5
                                    # 0-1に正規化（感度を下げる）
                                    # 元は2000だったが、小声で100%にならないように10000へ変更
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
            """現在の音量を取得 (0.0-1.0)"""
            with self._lock:
                return self.current_volume
        
        def stop(self):
            """録音停止"""
            self.is_recording = False
            time.sleep(0.05)  # スレッド終了を待つ
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


    class ShoutMinigame:
        """
        おおごえミニゲーム（不審者撃退・HP制）
        Windows: マイク使用
        その他: ボタン連打フォールバック
        """
        def __init__(self, 
                     threshold=0.6, # 90dB相当
                     duration=8.0,  # 制限時間を長めに（削り切る必要があるため）
                     hp=100):       # 不審者のHP
            self.threshold = threshold
            self.duration = duration
            self.max_hp = hp
            self.current_hp = hp
            
            self.result = None
            self.show_result = False
            self.finished = False
            self.start_time = None
            self.elapsed = 0.0
            
            # 音量関連
            self.current_volume = 0.0
            self.max_volume = 0.0
            
            # マイク機能チェック
            self.mic_available = _win_mic_available
            self.recorder = None
            
            # フォールバック用
            self.mash_count = 0
            
            # 演出用
            self.shout_texts = [] 
            self.next_text_time = 0.0
            self.shake_offset = (0, 0)
            self.stranger_shake = (0, 0) # 不審者の揺れ
            self.damage_flash = 0.0      # ダメージ時の赤フラッシュ
            
            self.debug_info = ""
            self.mic_started = False
            self._real_start_time = None
            
            self.shout_phrases = [
                "たすけて！", "やめて！", "こないで！", "だれかー！", "うわあああん！", "あっちいけ！"
            ]

        def get_remaining(self):
            """残り時間をリアルタイムで取得"""
            if self._real_start_time is None:
                return self.duration
            elapsed = renpy.get_game_runtime() - self._real_start_time
            return max(0, self.duration - elapsed)

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
            if self.start_time is None:
                self.start_time = st
                self._real_start_time = renpy.get_game_runtime()
                if self.mic_available:
                    self.start_mic()
            
            self.elapsed = st - self.start_time
            dt = 0.02 # 近似deltaTime
            
            # マイク音量取得
            if self.mic_available and self.recorder:
                self.current_volume = self.recorder.get_volume()
                self.max_volume = max(self.max_volume, self.current_volume)
            
            # 時間切れ判定
            if not self.show_result and self.elapsed >= self.duration:
                self.stop_mic()
                if self.current_hp <= 0:
                    self.result = "perfect" # ギリギリ倒せた
                else:
                    self.result = "miss"    # 倒せなかった
                self.show_result = True
                self.finished = True
            
            # ゲームプレイ中（HP判定とダメージ処理）
            if not self.show_result:
                # 攻撃力計算（閾値を超えた分だけダメージ）
                damage = 0
                is_attacking = False
                
                if self.mic_available:
                    # 判定基準を厳しくする (閾値の80%以上から有効)
                    damage_threshold = self.threshold * 0.8
                    
                    if self.current_volume >= damage_threshold:
                        # 以前は音量に応じてダメージが変わっていたが、
                        # 「近くで叫べばすぐ終わる」という問題を解消するため固定値に変更
                        # 3.0ダメージ/frame -> 60FPSで180DPS -> HP500を3秒弱
                        # 調整: HP=100ならもっと低く。
                        # 現在のHP=100 (init参照)。duration=5.0s。
                        # 5秒で削り切るには 20DPS 必要 = 20/60 = 0.33/frame?
                        # updateは dt=0.02 (50FPS相当) で呼ばれている前提なら
                        # 100 / (5.0 * 50) = 0.4 damage/frame
                        # 余裕を持たせて 0.6 くらいにする
                        
                        # 修正: updateはRen'PyのDisplayable updateなのでFPS依存だが、dt=0.02固定で計算している
                        # 実際には st - start_time で経過時間は正しいが、1フレームの重みはフレームレートによる
                        # とはいえ、dt=0.02 固定加算ではないので、
                        # 確実に削れるように少し大きめに設定
                        
                        damage = 0.8  # 固定ダメージ (約2秒～3秒で満タンから削りきれるくらい)
                        is_attacking = True
                else:
                    # 連打モードは後述のon_mashで処理
                    pass

                # ダメージ適用
                if damage > 0:
                    self.current_hp = max(0, self.current_hp - damage)
                    self.damage_flash = min(1.0, self.damage_flash + 0.2) # 赤く光らせる
                    
                    # 不審者揺らし
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
            
            # バーの色（HPに応じて変化）
            if hp_ratio > 0.5:
                bar_color = "#00ff00"
            elif hp_ratio > 0.2:
                bar_color = "#ffff00"
            else:
                bar_color = "#ff0000"
            
            return Solid(bar_color, xsize=int(400 * hp_ratio), ysize=30), dt

        def on_mash(self):
            """連打攻撃"""
            if self.show_result or self.finished:
                return
            
            # 連打ダメージ
            damage = 4.0
            self.current_hp = max(0, self.current_hp - damage)
            self.damage_flash = 1.0
            
            import random
            self.stranger_shake = (random.randint(-5, 5), random.randint(-5, 5))
            
            if self.current_hp <= 0:
                self.result = "perfect"
                self.show_result = True
                self.finished = True


    def mic_get_status():
        return {
            "available": _win_mic_available,
            "error": _win_mic_error,
            "platform": sys.platform
        }


# =============================================================================
# おおごえミニゲーム画面（不審者バトル版）
# =============================================================================
screen shout_minigame(game):
    modal True
    zorder 200 # ミニマップ(98)より手前に表示
    
    if not game.finished:
        timer 0.05 repeat True action Function(renpy.restart_interaction)
    
    add Solid("#000000DD")
    
    # 叫び文字演出（背景側）
    for txt_data in game.shout_texts:
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
        background None # 背景なしでオーバーレイ風に
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

            # 不審者エリア（HPバー + 画像）
            frame:
                background None
                xalign 0.5
                ysize 400
                xsize 400
                
                # 不審者の画像（簡易表示、実際は立ち絵があればそれを使う）
                # ここではShake演出用に位置をずらす
                add "images/actor/stranger.png":
                    xalign 0.5
                    yalign 1.0
                    zoom 0.6
                    xoffset game.stranger_shake[0]
                    yoffset game.stranger_shake[1]
                    # ダメージ時の赤フラッシュ（MatrixColor等が使えないので簡易的にTint）
                    # tint (1.0, 1.0 - game.damage_flash, 1.0 - game.damage_flash) 
                
                # HPバー（頭上）
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
            
            # 残り時間
            $ remaining = game.get_remaining()
            text "のこり: [remaining:.1f] びょう":
                size 40
                xalign 0.5
                color "#ffff00"
                bold True
                outlines [(2, "#000000", 0, 0)]
            
            # 自分の音量メーター（下部）
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
                        
                        # 現在の音量バー
                        $ v_width = int(300 * min(1.0, game.current_volume / game.threshold))
                        frame:
                            background "#00ffff"
                            xsize v_width
                            ysize 20
                            xalign 0.0

            # フォールバック案内
            elif not game.mic_available:
                text "ボタンを れんだ！！":
                    size 30
                    color "#ff8800"
                    bold True

    # 入力処理
    if not game.show_result and not game.mic_available:
        key "K_SPACE" action Function(game.on_mash)
    
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
# マイク設定・デバッグ画面
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
            
            text "マイク設定":
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
                text "（ボタン連打モードで動作します）":
                    size 18
                    color "#888888"
            
            null height 30
            
            # 閉じるボタン
            textbutton "閉じる":
                xalign 0.5
                action Return()
                text_size 28
                text_color "#ffffff"
