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
                                    # 0-1に正規化（感度を上げる）
                                    with self._lock:
                                        self.current_volume = min(1.0, rms / 2000)
                                        self.debug_info = f"vol:{int(rms)} buf:{self._buffer_count}"
                            
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
        おおごえミニゲーム
        Windows: マイク使用
        その他: ボタン連打フォールバック
        """
        def __init__(self, 
                     threshold=0.3,
                     duration=3.0,
                     hold_time=0.5):
            self.threshold = threshold
            self.duration = duration
            self.hold_time = hold_time
            
            self.result = None
            self.show_result = False
            self.start_time = None
            self.elapsed = 0.0
            
            # 音量関連
            self.current_volume = 0.0
            self.max_volume = 0.0
            self.loud_start_time = None
            self.loud_duration = 0.0
            
            # マイク機能チェック
            self.mic_available = _win_mic_available
            self.recorder = None
            
            # フォールバック用（連打カウント）
            self.mash_count = 0
            self.mash_target = 12
            
            # デバッグ情報
            self.debug_info = ""
            self.mic_started = False

        def start_mic(self):
            """マイク入力を開始"""
            if not self.mic_available:
                self.debug_info = "mic not available"
                return False
            
            try:
                self.recorder = WinMicRecorder()
                result = self.recorder.start()
                if result:
                    self.debug_info = "recording started"
                    self.mic_started = True
                else:
                    self.debug_info = f"start failed: {self.recorder.debug_info}"
                return result
            except Exception as e:
                self.debug_info = f"exception: {e}"
                self.mic_available = False
                return False

        def stop_mic(self):
            """マイク入力を停止"""
            if self.recorder:
                self.recorder.stop()
                self.recorder = None

        def update(self, st, at):
            """画面更新"""
            if self.start_time is None:
                self.start_time = st
                if self.mic_available:
                    self.start_mic()
            
            self.elapsed = st - self.start_time
            
            # マイクから音量取得
            if self.mic_available and self.recorder:
                self.current_volume = self.recorder.get_volume()
                self.max_volume = max(self.max_volume, self.current_volume)
            
            # 時間切れチェック
            if not self.show_result and self.elapsed >= self.duration:
                self.stop_mic()
                self.result = "miss"
                self.show_result = True
            
            # 大声継続チェック（マイクモード）
            if self.mic_available and not self.show_result:
                if self.current_volume >= self.threshold:
                    if self.loud_start_time is None:
                        self.loud_start_time = st
                    self.loud_duration = st - self.loud_start_time
                    
                    if self.loud_duration >= self.hold_time:
                        self.stop_mic()
                        if self.max_volume >= self.threshold * 1.5:
                            self.result = "perfect"
                        else:
                            self.result = "good"
                        self.show_result = True
                else:
                    self.loud_start_time = None
                    self.loud_duration = 0.0
            
            # 音量バー表示
            bar_width = int(300 * self.current_volume)
            if self.current_volume >= self.threshold:
                bar_color = "#00ff00"
            else:
                bar_color = "#ff6600"
            
            bar = Solid(bar_color, xsize=max(1, bar_width), ysize=50)
            return bar, 0.02

        def on_mash(self):
            """フォールバック用：連打入力"""
            if self.show_result:
                return
            self.mash_count += 1
            if self.mash_count >= self.mash_target:
                if self.elapsed < self.duration * 0.5:
                    self.result = "perfect"
                else:
                    self.result = "good"
                self.show_result = True


    def mic_get_status():
        """マイクの状態を取得"""
        return {
            "available": _win_mic_available,
            "error": _win_mic_error,
            "platform": sys.platform
        }


# =============================================================================
# おおごえミニゲーム画面
# =============================================================================
screen shout_minigame(game):
    modal True
    add Solid("#000000DD")
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (60, 60)
        background "#222244"
        
        vbox:
            spacing 25
            xalign 0.5
            
            # タイトル
            if game.mic_available:
                text "おおごえを だそう！":
                    size 42
                    xalign 0.5
                    color "#ffffff"
                    bold True
                
                text "「たすけて！」と さけぼう！":
                    size 28
                    xalign 0.5
                    color "#ffff00"
            else:
                text "れんだ！おおごえを だそう！":
                    size 36
                    xalign 0.5
                    color "#ffffff"
                    bold True
                
                text "（スペースキーを れんだ！）":
                    size 20
                    xalign 0.5
                    color "#888888"
            
            null height 10
            
            # 残り時間
            $ remaining = max(0, game.duration - game.elapsed)
            text "のこり: [remaining:.1f] びょう":
                size 28
                xalign 0.5
                color "#ffff00"
            
            # 音量メーター
            frame:
                xsize 320
                ysize 60
                xalign 0.5
                background "#333333"
                
                # 閾値ライン
                frame:
                    xpos int(300 * game.threshold)
                    yalign 0.5
                    xsize 3
                    ysize 50
                    background "#ffffff"
                
                # 音量バー
                add DynamicDisplayable(game.update):
                    xalign 0.0
                    yalign 0.5
            
            # 音量表示（マイクモード）
            if game.mic_available:
                $ vol_percent = int(game.current_volume * 100)
                text "おんりょう: [vol_percent]%":
                    size 24
                    xalign 0.5
                    color "#aaaaaa"
                
                # デバッグ情報
                $ dbg = game.debug_info
                text "[dbg]":
                    size 14
                    xalign 0.5
                    color "#666666"
            else:
                # フォールバック：連打カウント
                text "[game.mash_count] / [game.mash_target]":
                    size 40
                    xalign 0.5
                    color "#ff6600"
                    bold True
            
            null height 10
            
            # 結果表示
            if game.show_result:
                if game.result == "perfect":
                    text "PERFECT!!":
                        size 50
                        color "#ffff00"
                        bold True
                        xalign 0.5
                elif game.result == "good":
                    text "GOOD!":
                        size 40
                        color "#00ff00"
                        bold True
                        xalign 0.5
                else:
                    text "こえが ちいさい...":
                        size 36
                        color "#ff0000"
                        bold True
                        xalign 0.5

    # 入力処理（フォールバックモード用）
    if not game.show_result and not game.mic_available:
        key "K_SPACE" action Function(game.on_mash)
    
    if game.show_result:
        timer 1.5 action Return(game.result)


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
