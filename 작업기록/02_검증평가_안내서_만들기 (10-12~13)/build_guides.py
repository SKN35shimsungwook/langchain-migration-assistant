"""통합 안내서(검증평가_첫걸음)를 01 전체 / 02 파트 상세로 나눠 MD·HTML(완전한 문서)로 만든다."""
import re, sys
from pathlib import Path

SRC_HTML = Path(sys.argv[1])          # 아티팩트 원본 (doctype 없음)
G = Path(sys.argv[2])                 # docs/guide
SRC_MD = G / "검증평가_첫걸음.md"
DATE = "2026-10-12"
PAGES = "https://skn35shimsungwook.github.io/langchain-migration-helper/docs/guide/"

src = SRC_HTML.read_text(encoding="utf-8")
lines = src.split("\n")
head = src[: src.index('<nav class="chapters"')]           # <title>, fonts, <style>
script = src[src.index("<script>"):]
sections = {int(n): s for n, s in re.findall(r'<!-- (\d+) -->\n(<section class="ch" id="c\d+">.*?</section>)', src, re.S)}

DOCS = {
    "01_프로젝트_전체_쉽게_보기": dict(
        title="프로젝트 전체 쉽게 보기",
        eyebrow="LANGCHAIN 마이그레이션 도우미 · 팀 모두를 위한 안내서",
        lead="우리 팀이 무엇을, 왜, 어떤 순서로 만드는지 <b>주방 이야기</b>로 설명합니다. 1~3번 팀원도, 처음 보는 사람도 읽을 수 있습니다.",
        next='다음 문서: <a href="02_검증평가_파트_상세.html">02 평가·화면 파트 상세</a> (4번 담당의 할 일)',
        chapters=[1, 2, 3, 8], quiz=[0, 1, 2], checks=False,
        nav=["주방으로 이해하기", "기본 설계", "역설계", "용어 사전", "퀴즈"]),
    "02_검증평가_파트_상세": dict(
        title="평가·화면 파트 상세",
        eyebrow="LANGCHAIN 마이그레이션 도우미 · 4번(화면·평가) 담당 안내서",
        lead="4번 담당이 맡은 <b>요리 대회 심사위원</b>과 <b>손님 테이블(화면)</b> 임무를 설명합니다. 도구, 명령어, 결과 읽는 법, 발표 질문까지 담았습니다.",
        next='먼저 읽을 문서: <a href="01_프로젝트_전체_쉽게_보기.html">01 프로젝트 전체 쉽게 보기</a>',
        chapters=[4, 5, 6, 7], quiz=[3, 4, 5, 6, 7], checks=True,
        nav=["내 임무", "따라 하기", "결과 읽기", "발표 질문", "퀴즈", "체크리스트"]),
}
REMEMBER = src[src.index('<div class="box remember">'): src.index("</header>")].rstrip()


def html_doc(name, d):
    order = d["chapters"] + [9] + ([10] if d["checks"] else [])
    renum = {old: i + 1 for i, old in enumerate(order)}
    body_secs = []
    for old in order:
        s = sections[old]
        s = re.sub(r'<p class="chno">\d+장</p>', f'<p class="chno">{renum[old]}장</p>', s)
        s = s.replace(f'id="c{old}"', f'id="s{renum[old]}"')
        if old == 9:
            s = s.replace("0 / 8", f"0 / {len(d['quiz'])}")
        body_secs.append(s)
    nav = "\n".join(f'    <li><a href="#s{i + 1}">{i + 1} {t}</a></li>' for i, t in enumerate(d["nav"]))
    js = script.replace("const QUIZ = [", "let QUIZ = [", 1)
    js = js.replace("function store(", f"QUIZ = QUIZ.filter((_, i) => {d['quiz']}.includes(i));\nfunction store(", 1)
    if d["checks"]:
        # 체크리스트의 장 번호를 이 문서 기준으로
        js = js.replace('"5장 ', f'"{renum[5]}장 ').replace("7장 예상 질문", f"{renum[7]}장 예상 질문")
    else:
        js = js[: js.index("const checksEl")] + "</script>\n"
    footer = (f'<footer>최신 버전 · {DATE} · 같은 내용의 MD와 PDF는 저장소 <code>docs/guide</code> 폴더에 있습니다. '
              f'이전 버전: <code>docs/역순설계_쉽게_이해하기.md</code></footer>')
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head.replace('<title>검증·평가 첫걸음</title>', f'<title>{d["title"]}</title>')}
<style>[hidden]{{display:none!important}} body{{margin:0}} .badge{{display:inline-block;align-self:flex-start;font-size:13px;font-weight:700;color:var(--pass);background:var(--pass-soft);border-radius:999px;padding:2px 10px}}</style>
</head>
<body>
<nav class="chapters" aria-label="장 목록">
  <ol>
{nav}
  </ol>
</nav>
<div class="wrap">
<header class="hero">
  <p class="eyebrow">{d["eyebrow"]}</p>
  <h1>{d["title"]}</h1>
  <span class="badge">최신 버전 · {DATE}</span>
  <p class="lead">{d["lead"]}</p>
  <p class="meta">{d["next"]}</p>
  {REMEMBER}
</header>
{chr(10).join(body_secs)}
{footer}
</div>
{js}
</body>
</html>
"""


def md_split():
    md = SRC_MD.read_text(encoding="utf-8")
    parts = re.split(r"\n(?=## )", md)
    remember = next(p for p in parts if p.startswith("## 이것 세 줄"))
    chap = {int(re.match(r"## (\d+)장", p).group(1)): p for p in parts if re.match(r"## \d+장", p)}
    quiz = re.findall(r"<details>.*?</details>", chap[9], re.S)
    out = {}
    for name, d in DOCS.items():
        order = d["chapters"]
        text = [f"# {d['title']}\n",
                f"> **최신 버전 · {DATE}**  ",
                f"> 웹에서 보기(퀴즈 포함): [HTML]({PAGES}{name}.html) · 인쇄용: [PDF]({name}.pdf)  ",
                "> " + re.sub(r'<a href="([^"]+)\.html">([^<]+)</a>', r"[\2](\1.md)", d["next"]) + "  ",
                "> 이전 버전: [역순설계_쉽게_이해하기.md](../역순설계_쉽게_이해하기.md)\n",
                remember.rstrip() + "\n\n---\n"]
        n = 0
        for old in order:
            n += 1
            text.append(re.sub(r"^## \d+장", f"## {n}장", chap[old].rstrip()) + "\n")
        n += 1
        picked = [q for i, q in enumerate(quiz) if i in d["quiz"][: len(quiz)] or (i == 6 and 7 in d["quiz"])]
        # MD 퀴즈는 7문항(Q1~Q7). HTML의 Q7(공정성)은 MD에 없으므로 인덱스를 맞춰 고른다.
        md_pick = [0, 1, 2] if not d["checks"] else [3, 4, 5, 6]
        qs = [quiz[i] for i in md_pick]
        qs = [re.sub(r"<summary>Q\d+\.", f"<summary>Q{k + 1}.", q, 1) for k, q in enumerate(qs)]
        text.append(f"## {n}장. 확인 퀴즈\n\n" + "\n\n".join(qs) + "\n")
        if d["checks"]:
            n += 1
            ck = re.sub(r"^## \d+장", f"## {n}장", chap[10].rstrip())
            text.append(ck.replace("(EVAL_RULES 9장)", "(EVAL_RULES 9장)") + "\n")
        out[name] = "\n".join(text)
    return out


for name, d in DOCS.items():
    (G / f"{name}.html").write_text(html_doc(name, d), encoding="utf-8")
for name, text in md_split().items():
    (G / f"{name}.md").write_text(text, encoding="utf-8")
print("ok")
