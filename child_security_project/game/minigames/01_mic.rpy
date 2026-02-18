# =============================================================================
# Windows ネイティブ マイク音量検出
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
            self.headers = None
            self._lock = threading.Lock()
            self._buffer_count = 0 
        
        def start(self):
            if not _win_mic_available: return False
            
            try:
                fmt = WAVEFORMATEX()
                fmt.wFormatTag = WAVE_FORMAT_PCM
                fmt.nChannels = 1
                fmt.nSamplesPerSec = self.sample_rate
                fmt.wBitsPerSample = 16
                fmt.nBlockAlign = fmt.nChannels * fmt.wBitsPerSample // 8
                fmt.nAvgBytesPerSec = fmt.nSamplesPerSec * fmt.nBlockAlign
                fmt.cbSize = 0
                
                result = winmm.waveInOpen(ctypes.byref(self.hwi), WAVE_MAPPER, ctypes.byref(fmt), 0, 0, CALLBACK_NULL)
                if result != 0: return False
                
                buf_size = self.buffer_size * 2
                self.headers = (WAVEHDR * self.NUM_BUFFERS)()
                
                for i in range(self.NUM_BUFFERS):
                    buf = ctypes.create_string_buffer(buf_size)
                    self.buffers.append(buf)
                    self.headers[i].lpData = ctypes.cast(buf, ctypes.POINTER(ctypes.c_char))
                    self.headers[i].dwBufferLength = buf_size
                    self.headers[i].dwFlags = 0
                    self.headers[i].dwBytesRecorded = 0
                    winmm.waveInPrepareHeader(self.hwi, ctypes.byref(self.headers[i]), ctypes.sizeof(WAVEHDR))
                    winmm.waveInAddBuffer(self.hwi, ctypes.byref(self.headers[i]), ctypes.sizeof(WAVEHDR))
                
                winmm.waveInStart(self.hwi)
                self.is_recording = True
                
                self._thread = threading.Thread(target=self._update_volume, daemon=True)
                self._thread.start()
                return True
            except Exception:
                return False
        
        def _update_volume(self):
            while self.is_recording:
                try:
                    for i in range(self.NUM_BUFFERS):
                        if self.headers[i].dwFlags & WHDR_DONE:
                            recorded = self.headers[i].dwBytesRecorded
                            if recorded >= 2:
                                data = self.buffers[i].raw[:recorded]
                                num = len(data) // 2
                                samples = struct.unpack(f"<{num}h", data)
                                if samples:
                                    rms = (sum(s*s for s in samples) / num) ** 0.5
                                    with self._lock:
                                        self.current_volume = min(1.0, rms / 10000)
                            
                            self.headers[i].dwFlags = WHDR_PREPARED
                            self.headers[i].dwBytesRecorded = 0
                            winmm.waveInAddBuffer(self.hwi, ctypes.byref(self.headers[i]), ctypes.sizeof(WAVEHDR))
                    time.sleep(0.01)
                except Exception:
                    pass
        
        def get_volume(self):
            with self._lock: return self.current_volume
        
        def stop(self):
            self.is_recording = False
            time.sleep(0.05)
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
            except: pass

    # =========================================================================
    # おおごえミニゲーム (統合版)
    # =========================================================================
    class ShoutMinigame(BaseMinigame):
        def __init__(self, threshold=0.6, duration=8.0, hp=100, **kwargs):
            if "title" not in kwargs: kwargs["title"] = "おおごえミニゲーム"
            if "text" not in kwargs: kwargs["text"] = "マイクにむかって さけべ！\n（ボタンれんだでも OK）"

            super(ShoutMinigame, self).__init__(**kwargs)
            
            self.threshold = threshold
            self.duration = duration
            self.max_hp = hp
            self.current_hp = hp
            
            self.elapsed = 0.0
            self.current_volume = 0.0
            self.max_volume = 0.0
            
            self.mic_available = _win_mic_available
            self.recorder = None
            
            # 演出用
            self.shout_texts = [] 
            self.next_text_time = 0.0
            self.shake_offset = (0, 0)
            self.stranger_shake = (0, 0)
            self.damage_flash = 0.0
            
            self.bg_displayable = Solid("#00000000") # placeholder
            self.shout_phrases = ["たすけて！", "やめて！", "こないで！", "だれかー！", "うわあああん！", "あっちいけ！"]

        def get_remaining(self):
            if not self.started or self.start_timestamp is None:
                return self.duration
            elapsed = renpy.get_game_runtime() - self.start_timestamp
            return max(0, self.duration - elapsed)

        def start_mic(self):
            if not self.mic_available: return False
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
            if not self.started:
                 return Solid("#00000000", xsize=1, ysize=1), 0.1

            if self.start_timestamp is None:
                self.start_timestamp = renpy.get_game_runtime()
                if self.mic_available: self.start_mic()
            
            elapsed = renpy.get_game_runtime() - self.start_timestamp
            dt = 0.02
            
            # マイク音量取得
            if self.mic_available and self.recorder:
                self.current_volume = self.recorder.get_volume()
                self.max_volume = max(self.max_volume, self.current_volume)
            
            # 時間切れ判定
            if not self.show_result and elapsed >= self.duration:
                self.stop_mic()
                self.result = "perfect" if self.current_hp <= 0 else "miss"
                self.show_result = self.finished = True
            
            # ゲームプレイ中
            if not self.show_result:
                damage = 0
                if self.mic_available:
                     damage_threshold = self.threshold * 0.8
                     if self.current_volume >= damage_threshold:
                         excess = self.current_volume - damage_threshold
                         damage = excess * 6.0
                
                if damage > 0:
                    self.current_hp = max(0, self.current_hp - damage)
                    self.damage_flash = min(1.0, self.damage_flash + 0.2)
                    
                    import random
                    shake_amp = int(5 * damage) 
                    self.stranger_shake = (random.randint(-shake_amp, shake_amp), random.randint(-shake_amp, shake_amp))
                    
                    if self.current_volume >= self.threshold:
                         self.shake_offset = (random.randint(-5, 5), random.randint(-5, 5))
                    
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

                if self.current_hp <= 0:
                    self.stop_mic()
                    self.result = "perfect"
                    self.show_result = self.finished = True

            hp_ratio = self.current_hp / self.max_hp
            bar_color = "#00ff00" if hp_ratio > 0.5 else "#ffff00" if hp_ratio > 0.2 else "#ff0000"
            return Solid(bar_color, xsize=int(400 * hp_ratio), ysize=30), dt

        def on_mash(self):
            if not self.started or self.show_result or self.finished: return
            damage = 4.0
            self.current_hp = max(0, self.current_hp - damage)
            self.damage_flash = 1.0
            import random
            self.stranger_shake = (random.randint(-5, 5), random.randint(-5, 5))
            if self.current_hp <= 0:
                self.result = "perfect"
                self.show_result = self.finished = True

    def mic_get_status():
        return {"available": _win_mic_available, "error": _win_mic_error, "platform": sys.platform}

# =============================================================================
# おおごえミニゲーム画面
# =============================================================================
screen shout_minigame(game):
    modal True
    zorder 200 
    
    if not game.started:
        use minigame_intro_overlay(game)
    else:
        # ゲーム本編
        if not game.finished:
            timer 0.05 repeat True action Function(renpy.restart_interaction)
        
        add Solid("#000000DD")
        
        # 叫び文字演出
        for txt_data in game.shout_texts:
            $ txt, tx, ty, t_st, t_size = txt_data
            if renpy.get_game_runtime() - t_st < 0.6:
                 text "[txt]":
                    size t_size xalign tx yalign ty color "#ff3333" bold True outlines [(3, "#ffffff", 0, 0)]
        
        # メインフレーム
        frame:
            xalign 0.5 yalign 0.5 padding (40, 40) background None
            xoffset game.shake_offset[0] yoffset game.shake_offset[1]
            
            vbox:
                spacing 20 xalign 0.5
                
                # タイトル等はIntroで出したので省略、または小さく表示
                if game.mic_available:
                    text "こえで げきたいしろ！" size 40 color "#ff0000" bold True xalign 0.5 outlines [(2, "#ffffff", 0, 0)]
                else:
                    text "れんだで げきたいしろ！" size 40 color "#ff0000" bold True xalign 0.5 outlines [(2, "#ffffff", 0, 0)]

                null height 20

                # 不審者エリア
                frame:
                    background None xalign 0.5 ysize 400 xsize 400
                    add "images/actor/stranger.png":
                        xalign 0.5 yalign 1.0 zoom 0.6
                        xoffset game.stranger_shake[0] yoffset game.stranger_shake[1]

                    vbox:
                        xalign 0.5 yalign 0.0 spacing 5
                        text "ふしんしゃの HP" size 24 color "#ffffff" xalign 0.5 outlines [(1, "#000000", 0, 0)]
                        frame:
                            background "#333333" xsize 400 ysize 30 xalign 0.5
                            add DynamicDisplayable(game.update):
                                xalign 0.0 ycenter 0.5
                
                null height 20
                
                # 残り時間
                text "のこり: [game.get_remaining():.1f] びょう":
                    size 40 xalign 0.5 color "#ffff00" bold True outlines [(2, "#000000", 0, 0)]
                
                # 自分音量メーター
                if game.mic_available:
                     vbox:
                        xalign 0.5 spacing 5
                        text "あなたの こえの おおきさ" size 20 color "#aaaaaa" xalign 0.5
                        frame:
                            xsize 300 ysize 20 background "#333333" xalign 0.5
                            $ v_width = int(300 * min(1.0, game.current_volume / game.threshold))
                            frame:
                                background "#00ffff" xsize v_width ysize 20 xalign 0.0

                elif not game.mic_available:
                    text "スペースキーを れんだ！！" size 30 color "#ff8800" bold True

        # 入力処理
        if not game.show_result and not game.mic_available:
            key "K_SPACE" action Function(game.on_mash)
        
        # 結果表示
        if game.show_result:
            frame:
                xalign 0.5 yalign 0.5 background Solid("#000000aa") padding (50, 30)
                if game.result == "perfect":
                    text "げきたい せいこう！！" size 80 color "#ffff00" bold True outlines [(4, "#ff0000", 0, 0)]
                else:
                    text "げきたい しっぱい……" size 60 color "#aaaaaa" bold True
            timer 2.5 action Return(game.result)
