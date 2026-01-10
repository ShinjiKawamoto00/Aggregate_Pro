# Proxy 問題の解決方法

## エラーの根本原因

- PACSession や NO_PROXY において
    - resp = session.get('https://payment.neoluxinc.com/') は成功
    - resp = session.post('https://payment.neoluxinc.com/certificate/', json=license_data) は失敗

エラー原因は、ProxyError である場合もあれば SSL エラーの場合もあるが、サブディレクトリ /certificate/ が 独立した url として扱われているが、根本原因は、

- **PACファイルの記述ミス（ポート番号欠落）の可能性が高い。**
    - ブラウザでは、このようなミスを自動補完してくれる
    - しかし、pythonは RFC準拠なので、厳密に指定する必要があり、補完の方法はない。
    - 直してもらうのは不可能に近い

## 認証ページを サブディレクトリ /certificate/ からサブドメイン certificate.neoluxinc.com への変更

- サーバー変更し、サブディレクトリ https://payment.neoluxinc.com/certificate/ からサブドメイン https://certificate.neoluxinc.com へ変更
    - これにより、上記問題が一気に解決するはず

## エラーの解決に向けたテスト１： certificate.neoluxinc.com へのアクセステスト

- ブラウザで  https://certificate.neoluxinc.com へアクセスし、下記のJSONが帰って来ることを確認
{"error_message": "POST \u3067\u9001\u4fe1\u3055\u308c\u3066\u3044\u306a\u3044\u306e\u3067\u7d42\u4e86\u3057\u307e\u3059\u3002"}

サーバーは セキュリティ上の安全性から "POST しか受け付けません。
このため "POST で送信されていないので終了します。" というUTF8が帰ってきます。

以前のテストから"neoluxinc.com"はホワイトリストに載っているはずなので、アクセスできるはず。
もし、アクセスできなければ、テスト３の NO_PROXY までのテストで完了。

## エラーの解決に向けたテスト２： NO_PROXY、certifi 証明書テスト

dist フォルダにて実行
.\test_no_proxy_certifi_cert\test_no_proxy_certifi_cert.exe

下記のメッセージが出れば成功です。
response.status_code: 200
response.text: {"serial_number": "9a13b0bf-9f86-43e6-b198-958995da79be", "mac_address": "68:e1:dc:13:52:67", "pc_uuid": "4C4C4544-004B-3310-8037-B5C04F485732", "expiration_date": "2026-01-31"}

以下同様に、テスト７までお願いします。

## エラーの解決に向けたテスト３： NO_PROXY、Windowsストア証明書テスト

.\test_no_proxy_win_cert\test_no_proxy_win_cert.exe

## エラーの解決に向けたテスト４： OS の PROXY、certifi 証明書テスト

.\test_os_proxy_certifi_cert\test_os_proxy_certifi_cert.exe


## エラーの解決に向けたテスト５： OS の PROXY、Windowsストア証明書テスト

.\test_os_proxy_win_cert\test_os_proxy_win_cert.exe

## エラーの解決に向けたテスト６： PAC の PROXY、certifi 証明書テスト

.\test_pac_proxy_certifi_cert\test_pac_proxy_certifi_cert.exe

## エラーの解決に向けたテスト７： OS の PROXY、Windowsストア証明書テスト

.\test_pac_proxy_win_cert\test_pac_proxy_win_cert.exe
