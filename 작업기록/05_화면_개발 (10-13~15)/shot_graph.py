"""발표용 캡처: 그래프 연결된 화면에서 확인용 예제 하나 보내고 결과 캡처."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
PICK = sys.argv[2]          # 예제 목록에서 고를 글자 (예: "q10 ·")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto("http://localhost:8544", wait_until="networkidle")
    pg.get_by_role("tab", name="이어서 하기").click()
    box = pg.get_by_label("내 아이디")
    box.fill("발표데모")
    box.press("Enter")
    pg.wait_for_timeout(4000)
    if pg.get_by_label("내 아이디").count():            # 처음이면 가입
        pg.get_by_role("tab", name="처음이에요").click()
        box = pg.get_by_label("사용할 아이디")
        box.fill("발표데모")
        box.press("Enter")
        pg.wait_for_timeout(4000)
    sb = pg.locator('[data-testid="stSidebar"]')
    sb.get_by_text("확인용 예제", exact=False).first.click()
    pg.wait_for_timeout(800)
    sb.locator('[data-testid="stSelectbox"]').first.click()
    pg.wait_for_timeout(500)
    pg.get_by_role("option").filter(has_text=PICK).first.click()
    pg.wait_for_timeout(800)
    sb.get_by_role("button", name="이 예제 보내기").click()
    pg.get_by_text("팀 그래프", exact=True).first.wait_for(timeout=240000)   # 결과 배지
    pg.wait_for_timeout(2000)
    pg.screenshot(path=str(OUT / "graph_before_after.png"))
    pg.get_by_role("tab", name="변경표 · 근거").click()
    pg.wait_for_timeout(1500)
    pg.screenshot(path=str(OUT / "graph_table.png"))
    b.close()
print("ok")
