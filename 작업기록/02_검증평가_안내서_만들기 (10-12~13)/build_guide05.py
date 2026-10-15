"""docs/guide_v2/05_처음부터_다시_보기.md → 같은 폴더의 .html (guide.css · guide.js 스타일)"""
import re
import sys
from pathlib import Path

import markdown

G = Path(sys.argv[1])
md = (G / "05_처음부터_다시_보기.md").read_text(encoding="utf-8")
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
<title>처음부터 다시 보기</title>
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
  <p class="eyebrow">LANGCHAIN 마이그레이션 도우미 · 프로젝트와 4번 역할을 처음부터 (역할 번호로 정리)</p>
  <h1>{title}</h1>
  <span class="badge">최신 버전 · {DATE}</span>
  <p class="lead">프로젝트를 아예 처음부터 시작한다고 생각하고 다시 썼습니다. 이 프로젝트가 무엇인지, 챗봇과 팀이 어떤 순서로 일하는지, 4번이 무엇을 언제 하는지, 팀에게 어떻게 말하면 되는지를 주방 이야기로 설명합니다.</p>
  <p class="meta">이 문서가 <a href="04_팀_보고_준비.html">04 팀 보고 준비</a>(이전 버전)를 대신합니다. 함께 읽을 문서: <a href="03_팀_진행상황.html">03 팀 진행 상황</a></p>
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
  storeKey: "guide-v2-05",
  quiz: [
    {{ q: "이 프로젝트의 챗봇이 일반 AI와 다른 두 가지는?",
      opts: ["더 빠르고 더 싸다", "최신 안내서를 보고 고치고, 직접 실행해서 확인한다", "코드를 더 짧게 쓴다"],
      a: 1, why: "문서 근거와 실행 근거, 두 가지로 확인하는 것이 이중 검증입니다." }},
    {{ q: "4번의 본격적인 일이 뒤쪽인 이유는?",
      opts: ["4번이 제일 쉬워서", "화면은 보여 줄 결과, 평가는 채점할 챗봇이 있어야 해서", "발표가 마지막이라서"],
      a: 1, why: "1·2번이 뼈대와 재료를, 3번이 결과를 넘겨야 4번이 연결하고 채점할 수 있습니다." }},
    {{ q: "챗봇이 없어도 4번이 지금 할 수 있는 일이 아닌 것은?",
      opts: ["시험지 30개 모으기", "일반 AI 실험", "우리 챗봇 실험"],
      a: 2, why: "우리 챗봇 실험은 1~3번 결과가 나온 뒤에 할 수 있습니다." }},
    {{ q: "회의에서 가장 좋은 말은?",
      opts: ["평가 도구랑 화면 다 만들어 뒀어요", "1·2번 작업 끝나면 이어서 하고, 그동안 챗봇 없이 되는 것부터 할게요", "제가 정한 모양대로 해 주세요"],
      a: 1, why: "팀 순서를 존중하고, 기다리는 동안의 계획을 말하는 것이 신뢰를 줍니다." }},
    {{ q: "report는 무엇인가요?",
      opts: ["프로젝트 결과 보고서", "챗봇이 매번 내놓는 결과 정리 (영수증)", "발표 자료"],
      a: 1, why: "이름만 같습니다. 프로젝트 보고서는 4번이 마지막에 쓰는 문서입니다." }}
  ],
  checks: [
    ["1장 다시 읽고 프로젝트를 한 문장으로 말해 보기", "옛 코드를 고치고 진짜 되는지 확인하는 챗봇"],
    ["3장 그림 보고 팀 순서 말해 보기", "1·2 → 3 → 4"],
    ["1분 대본 소리 내어 읽기", "5장"],
    ["회의에서 비교 모델 · 다시 시도 횟수 같이 정하기", "평가 규칙"],
    ["1~3번에게 질문 하나씩 하기", "5장 표"],
    ["평가 규칙 정리 시작", "1단계"],
    ["시험용 옛날 코드 모으기 시작", "1단계"],
    ["매일 13:40 짧은 보고 (어제 · 오늘 · 필요한 것)", "5장 틀"]
  ]
}};
</script>
<script src="guide.js"></script>
</body>
</html>
"""
(G / "05_처음부터_다시_보기.html").write_text(html, encoding="utf-8")
print("ok", n, "chapters")
