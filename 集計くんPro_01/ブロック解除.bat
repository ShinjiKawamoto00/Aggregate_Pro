@echo off
echo 全ファイルのブロック解除を開始します！
powershell -ExecutionPolicy Bypass -Command "Get-ChildItem . -Recurse | Unblock-File"
echo 全ファイルのブロック解除完了！
pause
