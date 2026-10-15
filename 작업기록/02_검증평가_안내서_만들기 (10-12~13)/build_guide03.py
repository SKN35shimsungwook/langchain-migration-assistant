"""docs/guide_v2/03_팀_진행상황.md → 같은 폴더의 .html (guide.css · guide.js 스타일)"""
import re
import sys
from pathlib import Path

import markdown

G = Path(sys.argv[1])
md = (G / "03_팀_진행상황.md").read_text(encoding="utf-8")
DATE = "2026-10-13"

title = re.match(r"# (.+)", md).group(1)
remember = re.search(r"## 이것 세 줄만 기억해도 됩니다\n\n(.*?)\n\n---", md, re.S).group(1)
body = md.split("\n---\n", 1)[1]
chapters = re.split(r"\n(?=## \d+장\. )", "\n" + body.strip())
chapters = [c.strip() for c in chapters if c.strip()]


def to_html(text):
    h = markdown.markdown(text, extensions=["tables", "fenced_code"])
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
<title>팀 진행 상황</title>
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
  <p class="eyebrow">LANGCHAIN 마이그레이션 도우미 · 팀 진행 상황 (역할 번호로 정리)</p>
  <h1>{title}</h1>
  <span class="badge">최신 버전 · {DATE}</span>
  <p class="lead">팀 저장소가 지금 어디까지 왔는지, 팀 대화에서 무엇을 정했는지, 4번(나)이 무엇을 했고 다음에 무엇을 하는지, 오늘 물어본 것을 한곳에 모았습니다.</p>
  <p class="meta">함께 읽을 문서: <a href="01_프로젝트_한눈에.html">01 프로젝트 한눈에</a> · <a href="02_화면평가_파트.html">02 화면·평가 파트</a></p>
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
  storeKey: "guide-v2-03",
  quiz: [
    {{ q: "report 노드와 결과 보고서의 차이는?",
      opts: ["같은 것이다", "report 노드는 요청마다 나오는 영수증, 보고서는 프로젝트 끝에 쓰는 문서", "보고서가 프로그램의 단계다"],
      a: 1, why: "이름만 같습니다. 보고서는 4번 확정, report 노드 담당은 회의에서 확인합니다." }},
    {{ q: "PowerShell에서 'cd 폴더 && uv sync'가 안 될 때는?",
      opts: ["한 줄씩 따로 실행한다", "관리자 권한으로 다시 연다", "uv를 다시 설치한다"],
      a: 0, why: "Windows PowerShell 5.1은 &&를 지원하지 않습니다. 한 줄씩 또는 ;로 실행합니다." }},
    {{ q: "화면이 팀 그래프를 부르는 기본안은?",
      opts: ["HTTP 서버를 꼭 띄운다", "run_migration(code, target_version) 함수를 바로 부른다", "파일로 주고받는다"],
      a: 1, why: "팀 저장소에 FastAPI가 없고 화면이 같은 저장소에 있어서, 함수 하나로 부르는 것이 1번 부담이 가장 적습니다." }},
    {{ q: "MigrateState의 kind가 classic_fallback이면?",
      opts: ["최신 방식으로 고쳤다", "langchain_classic으로 우회했다", "검증에 실패했다"],
      a: 1, why: "평가의 classic 의존 비율과 같은 구분입니다. 통과는 하지만 최신 방식은 아닙니다." }}
  ],
  checks: [
    ["팀 저장소 폴더를 바탕화면으로 옮기기", "Move-Item .\\\\eq-test\\\\SKN35-3rd-4Team ."],
    ["uv sync 실행하고 git branch로 내 브랜치 확인", "한 줄씩 실행"],
    ["13:40 회의에서 05 문서 대본으로 말하기", "6장"],
    ["report 노드 담당 정하기", "3번 또는 4번"],
    ["화면이 챗봇을 부르는 방식 물어보기", "1번에게 질문으로"],
    ["3번과 검증 범위 맞추기", "질문으로"],
    ["2번과 근거 ID 규칙 · 벡터 DB 공유 방법 정하기", "symbol_map 합의안"],
    ["비교 모델, 최대 시도 횟수 정하기", "EVAL_RULES 9장"],
    ["1·2번 결과가 나오면 팀 저장소에서 화면·평가 새로 만들기", "개인 초안은 참고만"]
  ]
}};
</script>
<script src="guide.js"></script>
</body>
</html>
"""
(G / "03_팀_진행상황.html").write_text(html, encoding="utf-8")
print("ok", n, "chapters")
