@echo off
cd /d %~dp0

:: 現在のブランチ名を取得
for /f "delims=" %%i in ('git branch --show-current') do set CURRENT_BRANCH=%%i

cls
echo ==========================================
echo  Git 作業保存ツール (Safety Mode)
echo ==========================================
echo.
echo [現在のブランチ]: %CURRENT_BRANCH%
echo.

:: main または master の場合は警告へ
if "%CURRENT_BRANCH%"=="main" goto WARNING
if "%CURRENT_BRANCH%"=="master" goto WARNING
goto STATUS

:WARNING
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo   【 警 告 】
echo   現在、本番用ブランチ [ %CURRENT_BRANCH% ] です。
echo   このまま進むと、本番環境へ直接反映されます。
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo.

:STATUS
echo [変更ファイル一覧]
git status -s
echo.
echo ------------------------------------------

:: ■ 安全装置: 実行確認 ■
set confirm=
set /p confirm="この内容で保存とアップロードを実行しますか？ (y/n): "

:: y 以外なら終了
if /i not "%confirm%"=="y" (
    echo.
    echo キャンセルしました。何もせず終了します。
    timeout /t 3 >nul
    exit
)

:: ■ コミットメッセージ入力 ■
echo.
set msg=
set /p msg="コミットメッセージを入力 (Enterで日時自動入力): "
if "%msg%"=="" set msg=Update %date% %time%

echo.
echo ==========================================
echo 処理を開始します...
echo メッセージ: "%msg%"
echo アップロード先: origin %CURRENT_BRANCH%
echo ==========================================

:: 1. Add
echo [1/3] ファイルを追加中...
git add . >nul

:: 2. Commit
echo [2/3] コミット作成中...
git commit -m "%msg%" >nul

:: 3. Push
echo [3/3] %CURRENT_BRANCH% へプッシュ中...
git push origin %CURRENT_BRANCH%

echo.
echo ==========================================
echo 完了しました！
echo GitHub等でプルリクエストを作成してください。
echo ==========================================

pause