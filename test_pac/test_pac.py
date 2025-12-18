from pypac import PACSession

try:
    session = PACSession(verify=False)  # SSL証明書検証無効
    resp = session.get('https://astrology.neoluxuk.com/WorkCheck/')
    print(f"resp.status_code:{resp.status_code}")
    print(f"resp.text[:100]:{resp.text[:100]}")
except Exception as e:
    print("失敗:", e)
