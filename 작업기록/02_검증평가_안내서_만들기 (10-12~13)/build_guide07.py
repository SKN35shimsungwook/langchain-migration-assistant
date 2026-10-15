"""docs/guide_v2/07_프로젝트_설명서.md → 같은 폴더의 .html (guide.css · guide.js 스타일)"""
import re
import sys
from pathlib import Path

import markdown

G = Path(sys.argv[1])
md = (G / "07_프로젝트_설명서.md").read_text(encoding="utf-8")
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
    h = h.replace(chr(92) + "|", "|")
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
<title>프로젝트 설명서</title>
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
  <p class="eyebrow">LANGCHAIN 마이그레이션 도우미 · 팀 저장소 기준 프로젝트 설명서 (역할 번호로 정리)</p>
  <h1>{title}</h1>
  <span class="badge">최신 버전 · {DATE}</span>
  <p class="lead">1번이 만든 폴더 구조와 2번이 모은 데이터 · 검색기만 기준으로 다시 썼습니다. 큰 그림, 예시 하나로 따라가는 전체 흐름, 팀 저장소 실물 지도, 지금 평가, 3번과 4번의 역할, 4번에게 필요한 역량, 당장 할 일, 용어를 담았습니다.</p>
  <p class="meta">함께 읽을 문서: <a href="06_데이터_분석.html">06 2번 데이터 분석</a> · <a href="05_처음부터_다시_보기.html">05 처음부터 다시 보기</a></p>
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
  storeKey: "guide-v2-07",
  quiz: [
    {{ q: "옛 코드가 들어오면 가장 먼저 2번 검색기가 하는 일은?",
      opts: ["AI에게 코드를 고치게 함", "이사 목록(대응표)에서 새 위치를 정확히 찾음", "코드를 실행함"],
      a: 1, why: "① 정확 매칭이 먼저이고, 그다음 문서를 하이브리드로 검색합니다." }},
    {{ q: "대응표에서 LLMChain의 종류(kind)는?",
      opts: ["native", "classic_fallback", "unresolved"],
      a: 1, why: "1.x에서 없어져 langchain_classic에만 남았습니다. 대신 대안 prompt | llm이 적혀 있습니다." }},
    {{ q: "1번의 MigrateState는 지금 무엇의 모양인가요?",
      opts: ["그래프 전체 정보", "이사 한 건 (old, new, evidence_id, kind)", "화면 설정"],
      a: 1, why: "그래프 전체가 주고받을 칸은 1번이 앞으로 채울 것으로 보입니다. 회의 질문거리입니다." }},
    {{ q: "3번과 4번이 꼭 맞춰야 하는 것은?",
      opts: ["발표 순서", "검증 기준과 결과(report) 모양", "브랜치 이름"],
      a: 1, why: "같은 기준으로 채점해야 비교가 공정하고, 결과 모양을 알아야 화면을 만듭니다." }},
    {{ q: "4번이 챗봇 없이도 지금 할 수 있는 일은?",
      opts: ["우리 챗봇 실험", "평가 규칙과 시험용 옛 코드 준비, 일반 AI 실험", "화면을 챗봇에 연결"],
      a: 1, why: "나머지는 1 · 3번 결과가 나와야 할 수 있습니다." }},
    {{ q: "2번 검색기의 근거 중 url(문서 링크)이 있는 것은?",
      opts: ["대응표 근거", "문서 근거 (최신 문서 · 옛 가이드)", "둘 다"],
      a: 1, why: "대응표 근거는 옛 위치 → 새 위치로 보여 주면 됩니다." }}
  ],
  checks: [
    ["3장 예시를 보지 않고 ①~⑤로 설명해 보기", "발표 연습 겸"],
    ["4장 폴더 지도에서 2번 폴더 6개가 각각 무엇인지 말해 보기", "import_map, docs_collect, chunking, embedding, retrieval"],
    ["2번 검색기 직접 돌려 보기", "8장 명령, .env 에 내 키"],
    ["2번에게 반응 + 깃 관리방 찬성", "9장"],
    ["회의 질문 4개 준비", "8장 표"],
    ["평가 규칙 초안 쓰기", "같은 모델 · 같은 문제 · 같은 채점"],
    ["시험용 옛 코드 모으기 시작", "2번 옛 가이드 24개 활용"],
    ["Streamlit 튜토리얼 30분", "7장 역량"]
  ]
}};
</script>
<script src="guide.js"></script>
</body>
</html>
"""
(G / "07_프로젝트_설명서.html").write_text(html, encoding="utf-8")
print("ok", n, "chapters")
