"""docs/guide_v2/04_팀_보고_준비.md → 같은 폴더의 .html (guide.css · guide.js 스타일)"""
import re
import sys
from pathlib import Path

import markdown

G = Path(sys.argv[1])
md = (G / "04_팀_보고_준비.md").read_text(encoding="utf-8")
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
<title>팀 보고 준비</title>
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
  <p class="eyebrow">LANGCHAIN 마이그레이션 도우미 · 4번 팀 보고 준비 (역할 번호로 정리)</p>
  <h1>{title}</h1>
  <span class="badge">최신 버전 · {DATE}</span>
  <p class="lead">"평가 도구랑 화면 뼈대는 거의 만들어 뒀어요." 이 한 문장을 풀어서, 4번이 무엇을 만들었고, 팀 저장소에서 무엇부터 하고, 팀원에게 어떻게 말하면 되는지 정리했습니다. 회의 대본과 복사해서 쓰는 메시지도 들어 있습니다.</p>
  <p class="meta">함께 읽을 문서: <a href="03_팀_진행상황.html">03 팀 진행 상황</a> · <a href="02_화면평가_파트.html">02 화면·평가 파트</a></p>
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
  <h2>체크리스트</h2>
  <p>체크한 내용은 이 브라우저에만 저장됩니다. <span class="progress" id="progress"></span></p>
  <div class="checks" id="checks"></div>
</section>

<footer>최신 버전 · {DATE} · 같은 내용의 MD와 PDF가 같은 폴더에 있습니다. 팀원은 역할 번호로만 적었습니다.</footer>
</div>
<script>
window.GUIDE = {{
  storeKey: "guide-v2-04",
  quiz: [
    {{ q: "회의 첫 마디에서 가장 먼저 말할 것은?",
      opts: ["내가 만든 파일 개수", "팀원이 바로 가져다 쓸 수 있는 것", "남은 일정"],
      a: 1, why: "상대에게 무엇이 편해지는지부터 말해야 부담 없이 받아들입니다." }},
    {{ q: "'거의 만들어 뒀다'에서 '거의'가 뜻하는 것은?",
      opts: ["코드가 반쯤 됨", "도구는 완성, 실제 결과 숫자는 팀 챗봇이 있어야 채움", "화면이 없음"],
      a: 1, why: "과장하지 않고 범위를 정확히 말하면 신뢰가 생깁니다." }},
    {{ q: "팀 챗봇이 없어도 지금 바로 할 수 있는 실험은?",
      opts: ["일반 AI(A) 실험", "우리 프로그램(B) 실험", "그래프 3장"],
      a: 0, why: "run_baseline.py는 API 키와 비교 모델만 정하면 혼자 돌아갑니다." }},
    {{ q: "3번에게 건넬 가장 큰 도움은?",
      opts: ["발표 자료", "채점 로봇 verify.py", "목차 페이지"],
      a: 1, why: "verifier (b)의 핵심이 이미 완성되어 있고, 평가와 채점 기준도 같아집니다." }}
  ],
  checks: [
    ["1분 대본 소리 내어 한 번 읽기", "5장"],
    ["회의에서 정할 것 3개 받기", "report 노드 담당, 함수 방식, 비교 모델"],
    ["디스코드 전체 공지 올리기", "5장 복사해서 사용"],
    ["1번에게 1:1 메시지", "함수 모양, 파일 넣을 자리"],
    ["3번에게 1:1 메시지", "verify.py, report 노드"],
    ["2번에게 1:1 메시지", "symbol_map 검사기, 벡터 DB 공유"],
    ["1번 확인 후 for_team_repo 복사하고 PR", "5장 PR 설명 사용"],
    ["비교 모델 정해지면 일반 AI 실험 3문제", "run_baseline.py --limit 3"]
  ]
}};
</script>
<script src="guide.js"></script>
</body>
</html>
"""
(G / "04_팀_보고_준비.html").write_text(html, encoding="utf-8")
print("ok", n, "chapters")
