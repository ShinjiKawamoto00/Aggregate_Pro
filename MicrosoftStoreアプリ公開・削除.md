## 集計くんPro の Cython による秘匿化、pyinstaller でビルド、MSIX へのパッケージ化、MSIX の署名 PowerShell スクリプト
cd C:\KCC\Aggregate\Script_10
./build_and_msix.ps1

## 自己署名証明書作成ツール Signtool.exe のインストール

```shell
$cert = New-SelfSignedCertificate -Type CodeSigningCert `
    -Subject "CN=MySelfSignedCert" `
    -KeyAlgorithm RSA `
    -KeyLength 2048 `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -NotAfter (Get-Date).AddYears(2)

# 作成した証明書を「信頼されたルート証明機関」にコピー（自分のPCで信頼させるため）
$rootStore = New-Object System.Security.Cryptography.X509Certificates.X509Store -ArgumentList "Root", "CurrentUser"
$rootStore.Open("ReadWrite")
$rootStore.Add($cert)
$rootStore.Close()
```

## ファイルとフォルダの準備

"C:\Aggregate_Pro\Aggregate_Pro_10_Package" 配下に以下のファイルとフォルダを準備
- AppxManifest.xml
- Assets フォルダ: アプリのロゴを入れる
- VFS フォルダ
    - "C:\Aggregate_Pro\Aggregate_Pro_10_Package\VFS\ProgramFilesX64\Aggregate_Pro_10" フォルダに exe や exe が使用するデータを入れる: フォルダや exe 名には日本語を使用しない

## AppxManifest.xml の作成

```xml
<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10" 
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10" 
         IgnorableNamespaces="uap">
  <Identity Name="ShinjiKawamoto.Pro10" 
            Publisher="CN=BC7C3891-AA1E-4542-A08E-36A58C1E1F84" 
            Version="1.0.0" 
            ProcessorArchitecture="x64" />
  <Properties>
    <DisplayName>集計くんPro_10</DisplayName>
    <PublisherDisplayName>Shinji Kawamoto</PublisherDisplayName>
    <Logo>Assets\Logo50.png</Logo>
  </Properties>
  <Resources>
  <Resource Language="ja-jp" />
  </Resources>
  <Applications>
    <Application Id="App" Executable="VFS\ProgramFilesX64\Aggregate_Pro_10\Aggregate_Pro_10.exe" EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements DisplayName="集計くんPro" 
                          Description="エクセルシートの集計や転記をする便利な効率化ツールです" 
                          BackgroundColor="#FFFFFF" 
                          Square150x150Logo="Assets\Logo150.png" 
                          Square44x44Logo="Assets\Logo44.png">
      </uap:VisualElements>
    </Application>
  </Applications>
</Package>
```

## MakeAppx.exe で MSIX へのパッケージ化 
```shell
& "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\makeappx.exe" pack /d "C:\Aggregate_Pro\Aggregate_Pro_10_Package" /p "C:\Aggregate_Pro\Aggregate_Pro_10.msix" /o
```
/o で上書き（更新する場合は必要）

## Microsoft_Store の証明書の生成：有効期限があるので注意
```shell
$publisher = "CN=BC7C3891-AA1E-4542-A08E-36A58C1E1F84" 
New-SelfSignedCertificate -Type Custom -Subject $publisher -KeyUsage DigitalSignature -FriendlyName "Microsoft_Store_Cert" -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3")

このコマンドで以下にように成功

   PSParentPath: Microsoft.PowerShell.Security\Certificate::CurrentUser\My

Thumbprint                                Subject              EnhancedKeyUsageList
----------                                -------              --------------------
3B98766204B58FD2863F2857516A1DBA4ADCCEBC  CN=BC7C3891-AA1E-45… コード署名
```

この Thumbprint は以下のコマンドで確認できる
```shell
Get-ChildItem Cert:\CurrentUser\My | Select-Object FriendlyName, Thumbprint, Subject

Microsoft Your Phone                            FD3D11C94F3B2812A2313CD61A198CFDF61A3D6F CN=5beb12f1-59bd-4db3-8c19-e7…
                                                F46E1621648F57E9068DE3A5E95CF6A93F11640C CN=MySelfSignedCert
                                                F209662A20C133B4D32CF628EF34E329D5E7BBB4 CN=0402010000001, O=MOJ No.04…
                                                C05D0D624B206DC7A1D1C790466E6F182750C625 CN=Registrar of Tokyo Legal A…
CrossDevice                                     B1B364034C992B9B3D9AB104A5F36CE81D1F4CAC CN=85351b69-35e4-45a7-9228-0c…
                                                87BBA87EC5B551B3753B0A021F5B19EEDEAAD68D CN=0869663581 smbc customer, …
                                                80927AD9EA74A5C4D6FF45B4E94C2E76C5DA4B08 CN=57006345a57727c6
                                                1FDAA75E5E0F11D84FB0C5CAC636F387DED89ADA CN=0869664584 smbc customer, …
                                                1A2788811623355B31BB409CD76D474FC9A4E038 CN=0869664584 smbc customer, …
APNS certificate(AppleInc.iCloud_nzyj5cx40ttqa) 115E198840FB031F9739C10359B0715E1731D56F CN=A7922FC7-317F-4E23-B970-B3…
Microsoft_Store_Cert                            3B98766204B58FD2863F2857516A1DBA4ADCCEBC CN=BC7C3891-AA1E-4542-A08E-36…
```

ただし、今回作成した自己署名証明書には有効期限（デフォルトでは1年など）があります。期限が切れると Thumbprint も新しく作り直す必要があるため、1年後くらいに「また署名エラーが出るな？」と思ったら、期限切れを疑ってください。

## Signtool.exe で Thumbprint を使って署名
```shell
$thumb = "3B98766204B58FD2863F2857516A1DBA4ADCCEBC"
& "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe" sign /fd SHA256 /sha1 $thumb "C:\Aggregate_Pro\Aggregate_Pro_10.msix"
```

Done Adding Additional Store
Successfully signed: C:\Aggregate_Pro\Aggregate_Pro_10.msix


## 古いパッケージを削除する方法
```shell
Get-AppxPackage *ShinjiKawamoto.Pro10*


Name              : ShinjiKawamoto.Pro10
Publisher         : CN=BC7C3891-AA1E-4542-A08E-36A58C1E1F84
Architecture      : X64
ResourceId        :
Version           : 1.0.5.0
PackageFullName   : ShinjiKawamoto.Pro10_1.0.5.0_x64__0e95t2hq56xt6
InstallLocation   : C:\Program Files\WindowsApps\ShinjiKawamoto.Pro10_1.0.5.0_x64__0e95t2hq56xt6
IsFramework       : False
PackageFamilyName : ShinjiKawamoto.Pro10_0e95t2hq56xt6
PublisherId       : 0e95t2hq56xt6
IsResourcePackage : False
IsBundle          : False
IsDevelopmentMode : False
NonRemovable      : False
IsPartiallyStaged : False
SignatureKind     : Developer
Status            : Ok

## これで削除される
Remove-AppxPackage -Package "ShinjiKawamoto.Pro10_1.0.5.0_x64__0e95t2hq56xt6"

```

## Aggregate_Pro_10.msix の公開

Microsoft パートナー センターのアプリとゲームから登録・公開する

https://partner.microsoft.com/ja-jp/dashboard/apps-and-games/overview



## Aggregate_Pro_10.msix のテスト

### 個人署名しかしていない Aggregate_Pro_10.msix のインストール方法

- ストアからダウンロードする場合はMicrosoftが保証してくれますが、自分で作ったMSIXをダブルクリック（サイドロード）してテストするには、**「証明書のインポート」**という儀式が必須です。

1. パッケージから証明書を抽出する
作成した .msix ファイルを右クリック > プロパティ。

**「デジタル署名」タブを開き、一覧にある署名を選択して「詳細」**をクリック。

**「証明書の表示」**をクリック。

**「証明書のインストール」**をクリックします。

2. 「信頼されたルート証明機関」に叩き込む（重要）
ここが運命の分かれ道です。デフォルト設定のまま進むと失敗します。

保存場所は**「ローカル コンピューター」**を選択して「次へ」。

「証明書をすべて次のストアに配置する」を選択し、**「参照」**をクリック。

リストから 「信頼されたルート証明機関」 (Trusted Root Certification Authorities) を選択して OK。

そのまま完了まで進めます。

3. インストールを再試行


### インストールした Aggregate_Pro_10.exe の実行

管理者モードで PowerShellを開いて

cd "C:\Program Files\WindowsApps\ShinjiKawamoto.Pro10_1.0.3.0_x64__0e95t2hq56xt6\VFS\ProgramFilesX64\Aggregate_Pro_10"
> ./Aggregate_Pro_10.exe

Traceback (most recent call last):
  File "aggregate_pro.py", line 8, in <module>
  File "aggregate_pro.pyx", line 6, in init aggregate_pro_core
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "pyimod02_importers.py", line 457, in exec_module
  File "modules\gradio_utils.py", line 32, in <module>
  File "modules\logger_utils.py", line 18, in setup_logger
  File "logging\handlers.py", line 223, in __init__
  File "logging\handlers.py", line 64, in __init__
  File "logging\__init__.py", line 1219, in __init__
  File "logging\__init__.py", line 1248, in _open
PermissionError: [Errno 13] Permission denied: 'C:\\Program Files\\WindowsApps\\ShinjiKawamoto.Pro10_1.0.1.0_x64__0e95t2hq56xt6\\VFS\\ProgramFilesX64\\Aggregate_Pro_10\\logs\\log.txt'
[PYI-388:ERROR] Failed to execute script 'aggregate_pro' due to unhandled exception!
