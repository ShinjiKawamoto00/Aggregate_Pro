# 集計くんPro_集計.ps1
if ($MyInvocation.MyCommand.Path) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
} else {
    $scriptDir = $PWD
}

$exePath = Join-Path $scriptDir "集計くんPro_01.exe"

if (Test-Path $exePath) {
    Write-Host "集計くんProを起動します..." -ForegroundColor Green
    Start-Process $exePath -ArgumentList "-pf", "集計処理.json" -WorkingDirectory $scriptDir -Wait
    Write-Host "処理完了。" -ForegroundColor Yellow
} else {
    Write-Host "集計くんPro_01.exeが見つかりません" -ForegroundColor Red
}

# 画面を維持（batのpause相当）
Write-Host "終了します...（ウィンドウを閉じますか？ Y/N）" -ForegroundColor Cyan
$choice = Read-Host
