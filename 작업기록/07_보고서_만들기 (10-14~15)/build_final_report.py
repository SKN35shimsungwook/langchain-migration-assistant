"""프로젝트 최종 보고서: Markdown → (mermaid 그림 PNG) → HTML.
python build_final_report.py <보고서.md> <이미지 폴더> <출력 폴더>
"""
import html
import re
import shutil
import sys
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

MD, IMG_DIR, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
text = MD.read_text(encoding="utf-8")

# 1. mermaid 블록 → PNG
MERMAID = re.compile(r"```mermaid\n(.*?)```", re.S)
blocks = MERMAID.findall(text)
PAGE = """<!doctype html><html><head><meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<style>body{margin:0;background:#fff;font-family:'Malgun Gothic',sans-serif}#d{display:inline-block;padding:12px}</style></head>
<body><div id="d" class="mermaid">%s</div>
<script>mermaid.initialize({startOnLoad:true,theme:'base',themeVariables:{fontFamily:'Malgun Gothic',fontSize:'15px',
primaryColor:'#EEF3FB',primaryBorderColor:'#1F5FAE',primaryTextColor:'#1B2433',lineColor:'#7A8494',secondaryColor:'#FFF6EF',tertiaryColor:'#F7F7F4'}});</script>
</body></html>"""
with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge")
    page = browser.new_page(device_scale_factor=2, viewport={"width": 1400, "height": 900})
    for i, b in enumerate(blocks, 1):
        page.set_content(PAGE % html.escape(b))
        page.wait_for_selector("#d svg", timeout=30000)
        page.wait_for_timeout(500)
        page.locator("#d").screenshot(path=str(OUT / f"diagram_{i}.png"))
    browser.close()
counter = iter(range(1, len(blocks) + 1))
text = MERMAID.sub(lambda m: (lambda n: f"![그림 {n}](diagram_{n}.png)")(next(counter)), text)

# 2. 이미지 경로
for img in IMG_DIR.glob("*"):
    shutil.copy(img, OUT / img.name)
text = text.replace("](images/", "](")

# 3. 목차 링크는 PDF에서 쓸모없으니 글자만
text = re.sub(r"\[([^\]]+)\]\(#[^)]+\)", r"\1", text)
text = text.replace("](평가_결과와_개선방안.md)", "](#)")

body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
body = body.replace('<a href="#">', "<span>").replace("</a>", "</a>")

CSS = """
@page { size: A4; margin: 16mm 15mm 16mm 15mm; }
body { font-family: 'Malgun Gothic', sans-serif; color: #1B2433; font-size: 10pt; line-height: 1.6; }
h1 { font-size: 21pt; margin: 0 0 8px; color: #1B2433; }
h2 { font-size: 15pt; color: #1F5FAE; border-bottom: 2px solid #1F5FAE; padding-bottom: 3px; margin-top: 26px; page-break-after: avoid; }
h2:not(:first-of-type) { page-break-before: always; }
h3 { font-size: 12pt; margin: 18px 0 6px; page-break-after: avoid; }
p { margin: 6px 0; } blockquote { margin: 8px 0; padding: 6px 12px; background: #F3F6FB; border-left: 4px solid #1F5FAE; color: #4A5363; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 8.8pt; }
th, td { border: 1px solid #C9CCD3; padding: 4px 6px; text-align: left; vertical-align: top; word-break: keep-all; overflow-wrap: anywhere; }
th { background: #ECEBE5; } tr { page-break-inside: avoid; }
code { font-family: Consolas, monospace; font-size: 8.6pt; background: #F1F2F4; padding: 0 3px; border-radius: 3px; }
pre { background: #14202E; color: #E8ECF1; padding: 10px; border-radius: 6px; white-space: pre-wrap; font-size: 8.4pt; line-height: 1.45; page-break-inside: avoid; }
pre code { background: none; color: inherit; padding: 0; }
img { max-width: 100%; max-height: 165mm; display: block; margin: 8px auto; page-break-inside: avoid; }
img[src='diagram_3.png'] { max-width: 50%; }
hr { display: none; }
.cover { height: 255mm; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always; }
.cover .k { color: #1F5FAE; font-weight: bold; letter-spacing: 1px; } .cover .t { font-size: 30pt; font-weight: bold; line-height: 1.25; }
.cover table { font-size: 10pt; }
"""
cover = """<div class="cover"><div class="k">SKN35 · LLM 연동 내외부 문서 기반 질의응답 시스템</div>
<div><div class="t">LangChain 버전 마이그레이션<br>코드 어시스턴트</div>
<p style="font-size:17pt;color:#4A5363;margin-top:10px">프로젝트 최종 보고서</p></div>
<div><img src="langchain-migration-assistant-screen.jpg" style="width:100%;border:1px solid #C9CCD3;border-radius:6px">
<table><tr><th>팀</th><td>SKN35 3rd 4Team (1번 그래프 · 백엔드 / 2번 데이터 · 검색 / 3번 변환 · 검증 / 4번 화면 · DB · 평가 · 발표)</td></tr>
<tr><th>기간</th><td>2026-10-12 ~ 2026-10-15</td></tr>
<tr><th>저장소</th><td>github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-3rd-4Team · 배포 github.com/SKN35shimsungwook/langchain-migration-assistant</td></tr>
<tr><th>배포 화면</th><td>langchain-migration-assistant-btn5chcr8ragnwts68rmhf.streamlit.app</td></tr></table></div></div>"""
# 첫 h1(보고서 제목)은 표지로 대신한다
body = re.sub(r"^<h1>.*?</h1>", "", body, count=1, flags=re.S)
(OUT / "final_report.html").write_text(
    f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>프로젝트 최종 보고서</title><style>{CSS}</style></head>"
    f"<body>{cover}{body}</body></html>", encoding="utf-8")
print("저장", OUT / "final_report.html", "그림", len(blocks))
