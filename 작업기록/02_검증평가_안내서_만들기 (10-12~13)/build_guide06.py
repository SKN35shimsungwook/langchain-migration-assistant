"""docs/guide_v2/06_데이터_분석.md → 같은 폴더의 .html (guide.css · guide.js 스타일)"""
import re
import sys
from pathlib import Path

import markdown

G = Path(sys.argv[1])
md = (G / "06_데이터_분석.md").read_text(encoding="utf-8")
DATE = "2026-10-13"

title = re.match(r"# (.+)", md).group(1)
remember = re.search(r"## 이것 세 줄만 기억해도 됩니다\n\n(.*?)\n\n---", md, re.S).group(1)
body = md.split("\n---\n", 1)[1]
chapters = re.split(r"\n(?=## \d+장\. )", "\n" + body.strip())
chapters = [c.strip() for c in chapters if c.strip() and "체크리스트" not in c.splitlines()[0]]


def to_html(text):
    h = markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])
    h = h.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    h = re.sub(r'<p><img alt="([^"]*)" src="([^"]*)" /></p>',
               r'<figure class="pic"><img src="\2" alt="\1"></figure>', h)
    h = re.sub(r"<blockquote>\s*(.*?)\s*</blockquote>", r'<div class="box tip">\1</div>', h, flags=re.S)
    h = h.replace('href="../../for_team_repo/"', 'href="https://github.com/SKN35shimsungwook/langchain-migration-helper/tree/main/for_team_repo"')
    return h


secs, nav = [], []
for i, c in enumerate(chapters, 1):
    head, rest = c.split("\n", 1)
    name = re.sub(r"^## \d+장\. ", "", head)
    short = name.split(" (")[0]
    nav.append(f'    <li><a href="#s{i}">{i} {short}</a></li>')
    secs.append(f'<section class="ch" id="s{i}">\n  <p class="chno">{i}장</p>\n  <h2>{name}</h2>\n{to_html(rest)}\n</section>')
n = len(chapters)
nav += [f'    <li><a href="#s{n + 1}">{n + 1} 퀴즈</a></li>', f'    <li><a href="#s{n + 2}">{n + 2} 체크리스트</a></li>']
remember_html = markdown.markdown(remember)

html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>2번 데이터 분석</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Do+Hyeon&family=Noto+Sans+KR:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="guide.css">
<style>h3 {{ margin-top: 8px; }} section.ch ul {{ margin: 0; padding-left: 1.3em; }} pre code {{ background: none; padding: 0; color: inherit; font-size: inherit; }} td:first-child, th:first-child {{ white-space: nowrap; }}</style>
</head>
<body>
<nav class="chapters" aria-label="장 목록">
  <ol>
{chr(10).join(nav)}
  </ol>
</nav>
<div class="wrap">

<header class="hero">
  <p class="eyebrow">LANGCHAIN 마이그레이션 도우미 · 2번 데이터 분석 (팀 저장소 읽기 전용 · 역할 번호로 정리)</p>
  <h1>{title}</h1>
  <span class="badge">최신 버전 · {DATE}</span>
  <p class="lead">팀 저장소 2번 브랜치에 올라온 문서 · import 대응표 · 검색 조각 · 벡터 DB를 숫자로 살펴보고, 4번의 시험지 30문제와 맞춰 봤습니다. 2번을 평가하려는 것이 아니라 프로젝트를 이해하려는 분석입니다.</p>
  <p class="meta">함께 읽을 문서: <a href="05_처음부터_다시_보기.html">05 처음부터 다시 보기</a> · <a href="03_팀_진행상황.html">03 팀 진행 상황</a></p>
  <div class="box remember">
    <p class="label">이것 세 줄만 기억해도 됩니다</p>
    {remember_html}
  </div>
</header>

{chr(10).join(secs)}

<section class="ch" id="s{n + 1}">
  <p class="chno">{n + 1}장</p>
  <h2>확인 퀴즈</h2>
  <p>답을 누르면 바로 알려 줍니다. <span class="score" id="score"></span></p>
  <div class="quiz" id="quiz"></div>
</section>

<section class="ch" id="s{n + 2}">
  <p class="chno">{n + 2}장</p>
  <h2>오늘 체크리스트</h2>
  <p>체크한 내용은 이 브라우저에만 저장됩니다. <span class="progress" id="progress"></span></p>
  <div class="checks" id="checks"></div>
</section>

<footer>최신 버전 · {DATE} · 같은 내용의 MD와 PDF가 같은 폴더에 있습니다. 팀원은 역할 번호로만 적었습니다.</footer>
</div>
<script>
window.GUIDE = {{
  storeKey: "guide-v2-06",
  quiz: [
    {{ q: "검색 창고 조각 11,903개 중 가장 많은 것은?",
      opts: ["최신 공식 문서", "import 대응표 한 줄짜리", "옛 마이그레이션 가이드"],
      a: 1, why: "9,155개(77%)가 대응표 조각입니다. 검색기는 대응표와 문서를 따로 찾아서 섞이지 않게 합니다." }},
    {{ q: "시험지 옛 import 57종 중 대응표에 있는 것은?",
      opts: ["30종", "55종", "57종 전부"],
      a: 1, why: "55종이 있고, 없는 2종은 위치가 그대로인 tool과 빠진 hub입니다." }},
    {{ q: "LLMChain을 대응표는 어디로 안내하나요?",
      opts: ["langchain_core", "langchain_classic (우회)", "langchain_openai"],
      a: 1, why: "1.x에서 없어져 classic에만 남았습니다. 최신 방식(LCEL)은 가이드 문서에 있습니다." }},
    {{ q: "4번이 근거 ID 형식을 어떻게 하면 좋을까요?",
      opts: ["내 연습 초안 형식을 2번에게 요청", "2번의 chunk_id 형식을 그대로 따름", "새로 만듦"],
      a: 1, why: "데이터는 2번 영역입니다. 4번은 평가와 화면을 그 형식에 맞춥니다." }}
  ],
  checks: [
    ["2장 그래프 4개를 한 줄씩 말로 설명해 보기", "조각 구성, 대응표 종류, 시험지 대조"],
    ["3장 표 보고 '55/57종, 53/55 import'의 뜻 말해 보기", "4번 평가와 연결"],
    ["4장 질문 중 1~2개만 골라 회의에서 묻기", "질문으로, 짧게"],
    ["6장 메시지로 2번에게 공유", "좋은 점 먼저"],
    ["근거 ID는 2번 형식(chunk_id)으로 맞추기", "내 연습 초안은 참고만"],
    ["팀 검증 환경 패키지 목록을 1번 · 3번과 맞추기", "langchain_chroma 등"]
  ]
}};
</script>
<script src="guide.js"></script>
</body>
</html>
"""
(G / "06_데이터_분석.html").write_text(html, encoding="utf-8")
print("ok", n, "chapters")
