import os
import ssl
import urllib3
from pypac import PACSession

# 環境変数 全無効化（最上部）
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['SSL_CERT_FILE'] = ''

# グローバルSSL無効
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = PACSession(
    allow_non_idn=True,
    socket_timeout=30
)

resp = session.get('https://payment.neoluxinc.com/')
print(f"resp.status_code:{resp.status_code}")
print(f"resp.text[:100]:{resp.text[:100]}")
