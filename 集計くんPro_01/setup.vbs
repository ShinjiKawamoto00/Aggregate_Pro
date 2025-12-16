Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' 現在フォルダ取得
currentDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

' ブロック解除
Set objFolder = objFSO.GetFolder(currentDir)
For Each objFile In objFolder.Files
    objFile.Attributes = objFile.Attributes And Not 2 ' 読み取り専用解除
Next

' ショートカット作成
Set objLink = objShell.CreateShortcut(currentDir & "\集計くんPro.lnk")
objLink.TargetPath = currentDir & "\集計くんPro_01.exe"
objLink.Arguments = "-pf 集計処理.json"
objLink.WorkingDirectory = currentDir
objLink.IconLocation = currentDir & "\集計くんPro_01.exe, 0"
objLink.Save

WScript.Echo "? セットアップ完了！" & vbCrLf & "「集計くんPro.lnk」をダブルクリックで実行"
