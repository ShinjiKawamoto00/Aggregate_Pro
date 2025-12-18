import ssl
import urllib3
from pypac import PACSession

# グローバルSSL検証無効
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()

session = PACSession()
resp = session.get('https://payment.neoluxinc.com/')
print(f"resp.status_code:{resp.status_code}")
print(f"resp.text[:100]:{resp.text[:100]}")