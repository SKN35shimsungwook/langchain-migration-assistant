import re, sys
from pathlib import Path

MD = Path(sys.argv[1]); HTML = Path(sys.argv[2])

def sub1(pat, rep, text, label):
    new, n = re.subn(pat, lambda m: rep, text, count=1, flags=re.S)
    assert n == 1, f"not found: {label}"
    return new

def fig(name, alt, cap=""):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="pic"><img src="../images/{name}.svg" alt="{alt}" loading="lazy">{c}</figure>'

# ---------- MD ----------
m = MD.read_text(encoding="utf-8")
m = sub1(r"\| 도구 \| 옛날 위치 \| 지금 위치 \|.*?create_agent` \|\n", "![LangChain 1.0에서 도구가 새 서랍으로 이사 간 모습](../images/01_kitchen_move.svg)\n", m, "md tools")
m = sub1(r"- \*\*문제\*\*: AI는.*?\*\*\"이중 검증\"\*\*입니다\.\n",
         "![같은 옛날 레시피, 두 요리사](../images/02_two_cooks.svg)\n\n**이중 검증** = ① 안내서 보기(문서 근거) + ② 서랍 직접 열기(실행 근거)\n", m, "md cooks")
m = sub1(r"\| 순서 \| 직원 \|.*?일반 AI에는 이 길이 없습니다\.\n",
         "![다섯 단계 파이프라인과 되돌아가는 길](../images/03_pipeline_loop.svg)\n\n레시피 카드가 ④ 서랍 열기에서 막히면 ②로 돌아가 다시 찾습니다. 이 되돌아가는 길이 **검증 루프**입니다.\n", m, "md pipeline")
m = sub1(r"```text\n🏆 발표:.*?```\n", "![역설계 계단](../images/04_reverse_stairs.svg)\n", m, "md stairs")
m = sub1(r"(도구가 다 있으면 합격을 줍니다\.\n)", r"\1" + "\n![요리 대회 심사위원](../images/05_judge_contest.svg)\n", m, "md judge")
m = m.replace(r"\1", "도구가 다 있으면 합격을 줍니다.\n")
m = sub1(r"\| 공정한 시합 규칙 \| 달리기로 말하면 \|.*?코스 가로지르면 실격 \|\n\n", "", m, "md fair")
m = sub1(r"\| 숫자 \| 뜻 \| 예시 \|.*?\*\*%p\*\*는 퍼센트끼리 뺀 값입니다\.\n", "![검증 루프 효과 읽는 법](../images/06_loop_effect.svg)\n", m, "md loop")
m = sub1(r"\| 성공의 종류 \| 주방 비유 \|.*?\| 실패 \| 서랍에 도구가 없음 \|\n", "![성공의 질 네 가지](../images/07_success_quality.svg)\n", m, "md quality")
MD.write_text(m, encoding="utf-8")

# ---------- HTML (아티팩트 원본) ----------
h = HTML.read_text(encoding="utf-8")
if "figure.pic" not in h:
    h = h.replace("footer { padding-block",
                  "figure.pic { margin: 0; display: flex; flex-direction: column; gap: 6px; }\n"
                  "figure.pic img { width: 100%; height: auto; display: block; border-radius: 12px; border: 1px solid var(--line); background: #F7F8FA; }\n"
                  "figure.pic figcaption { font-size: 14px; color: var(--ink-2); }\n"
                  "footer { padding-block", 1)
h = sub1(r'<div class="table-wrap"><table>\s*<tr><th>도구</th>.*?</table></div>', fig("01_kitchen_move", "LangChain 1.0에서 도구가 새 서랍으로 이사 간 모습"), h, "html tools")
h = sub1(r'<h3>문제: 옛날 주방만 기억하는 요리사</h3>.*?(?=<p>①을)', fig("02_two_cooks", "같은 옛날 레시피, 두 요리사") + "\n  ", h, "html cooks")
h = sub1(r'<div class="flow" role="list">.*?\(최대 3번\)</p>', fig("03_pipeline_loop", "다섯 단계 파이프라인과 되돌아가는 길", "레시피 카드가 ④에서 막히면 ②로 돌아가 다시 찾습니다."), h, "html pipeline")
h = sub1(r'<div class="stairs">.*?(?=<h3>두 설계는)', fig("04_reverse_stairs", "역설계 계단") + "\n  ", h, "html stairs")
h = sub1(r'(도구가 다 있으면 합격을 줍니다\.</p>)', "도구가 다 있으면 합격을 줍니다.</p>\n  " + fig("05_judge_contest", "요리 대회 심사위원"), h, "html judge")
h = sub1(r'<h3>공정한 시합 규칙 \(달리기와 같습니다\)</h3>\s*<div class="table-wrap"><table>.*?</table></div>\s*', "", h, "html fair")
h = sub1(r'<div class="box">\s*<p class="label">예시: 난이도별 성공률</p>.*?<p><b>%p\(퍼센트 포인트\)</b>.*?</p>', fig("06_loop_effect", "검증 루프 효과 읽는 법"), h, "html loop")
h = sub1(r'(<h3>성공에도 품질이 있습니다</h3>)\s*<div class="table-wrap"><table>.*?</table></div>', "<h3>성공에도 품질이 있습니다</h3>\n  " + fig("07_success_quality", "성공의 질 네 가지"), h, "html quality")
HTML.write_text(h, encoding="utf-8")
print("ok", h.count('class="pic"'), "figures in html,", m.count("../images/"), "in md")
