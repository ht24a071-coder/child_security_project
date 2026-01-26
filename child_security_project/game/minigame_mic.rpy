# =============================================================================
# マイク音量検出ミニゲーム
# 「おおごえを出す」を実際にマイクで検出
# =============================================================================

init -1 python:
    import threading
    import time
    
    # マイク機能が使えるかチェック
    _mic_available = False
    try:
        import sounddevice as sd
        import numpy as np
        _mic_available = True
    except ImportError:
        pass

    class ShoutMinigame(object):
        """
        マイクから音量を取得し、一定以上の声が出たらクリア
        マイクが使えない場合は自動的にフォールバック
        """
        def __init__(self, 
                     threshold=0.3,      # 音量閾値 (0.0〜1.0)
                     duration=3.0,       # 制限時間
                     hold_time=0.5):     # この時間以上大声を維持したらクリア
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
            self.mic_available = _mic_available
            self.stream = None
            self.running = False
            
            # フォールバック用（連打カウント）
            self.mash_count = 0
            self.mash_target = 12

        def start_mic(self):
            """マイク入力を開始"""
            if not self.mic_available:
                return False
            
            try:
                import sounddevice as sd
                import numpy as np
                
                def audio_callback(indata, frames, time_info, status):
                    if self.running:
                        # 音量計算（RMS）
                        volume = np.sqrt(np.mean(indata**2))
                        self.current_volume = min(1.0, volume * 3)  # スケール調整
                        self.max_volume = max(self.max_volume, self.current_volume)
                
                self.stream = sd.InputStream(
                    channels=1,
                    samplerate=44100,
                    callback=audio_callback
                )
                self.stream.start()
                self.running = True
                return True
            except Exception as e:
                print(f"Mic error: {e}")
                self.mic_available = False
                return False

        def stop_mic(self):
            """マイク入力を停止"""
            self.running = False
            if self.stream:
                try:
                    self.stream.stop()
                    self.stream.close()
                except:
                    pass
                self.stream = None

        def update(self, st, at):
            """画面更新"""
            if self.start_time is None:
                self.start_time = st
                if self.mic_available:
                    self.start_mic()
            
            self.elapsed = st - self.start_time
            
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


# =============================================================================
# マイク音量ミニゲーム画面
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
                
                text "（マイクが つかえません）":
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
