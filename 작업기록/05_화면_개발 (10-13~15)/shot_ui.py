"""발표용 화면 캡처: 로그인 → 사이드바 예시 질문 보내기 → 1920x1080 캡처."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
QID = sys.argv[2] if len(sys.argv) > 2 else "q10"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg.goto("http://localhost:8601", wait_until="networkidle")
    pg.get_by_role("tab", name="이어서 하기").click()
    box = pg.get_by_label("내 username")
    box.fill("발표데모")
    box.press("Enter")
    pg.wait_for_timeout(3000)
    if pg.get_by_label("내 username").count():          # 처음이면 가입
        pg.get_by_role("tab", name="처음이에요").click()
        box = pg.get_by_label("사용할 username")
        box.fill("발표데모")
        box.press("Enter")
        pg.wait_for_timeout(3000)
    sb = pg.locator('[data-testid="stSidebar"]')
    sb.get_by_text("예시 질문", exact=False).first.click()
    pg.wait_for_timeout(800)
    sel = sb.locator('[data-testid="stSelectbox"]').first
    sel.click()
    pg.wait_for_timeout(500)
    pg.get_by_role("option").filter(has_text=sys.argv[3]).first.click()
    pg.wait_for_timeout(800)
    sb.get_by_role("button", name="이 질문 보내기").click()
    pg.wait_for_timeout(5000)
    pg.screenshot(path=str(OUT / f"ui_{QID}.png"))
    # 변경표 탭도 한 장
    pg.get_by_role("tab", name="변경표 · 근거").click()
    pg.wait_for_timeout(1500)
    pg.screenshot(path=str(OUT / f"ui_{QID}_table.png"))
    b.close()
print("ok")
