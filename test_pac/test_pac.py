import sys
import os
from pypac import PACSession

# python-certifi-win32初期化（Windows Python用）
if sys.platform == "win32":
    try:
        import certifi_win32
        # 仮想PEMパス返却
        os.environ['REQUESTS_CA_BUNDLE'] = certifi_win32.wincerts.where()
        print("python-certifi-win32 initialize complete - Using Windows Certificate Store!")
    except ImportError:
        print("python-certifi-win32 error!")
        sys.exit()

try:
    session = PACSession()
    resp = session.get('https://payment.neoluxinc.com/')
    print(f"resp.status_code: {resp.status_code}")
    print(f"resp.text: {resp.text[:200]}")
except Exception as e:
    print("失敗:", e)