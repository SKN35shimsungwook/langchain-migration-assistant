"""발표 대본 HTML: python build_script.py <script.json> <out.html>"""
import html
import json
import sys

S = json.load(open(sys.argv[1], encoding="utf-8"))
e = html.escape
main = [x for x in S if x["time"] != "질문용"]
appx = [x for x in S if x["time"] == "질문용"]

CSS = """
@page { size: A4; margin: 16mm 16mm; }
body { font-family: 'Malgun Gothic', sans-serif; color: #1D1D1F; background: #fff; font-size: 11pt; line-height: 1.75; }
h1 { font-size: 26pt; margin: 0; letter-spacing: -0.5px; } .sub { color: #6E6E73; margin: 4px 0 18px; }
.rules { display: flex; gap: 10px; margin: 0 0 22px; }
.rules div { flex: 1; background: #F5F5F7; border-radius: 12px; padding: 10px 14px; font-size: 10pt; color: #3A3A3C; }
.rules b { display: block; color: #0071E3; font-size: 10.5pt; }
.slide { background: #F5F5F7; border-radius: 16px; padding: 16px 20px; margin: 0 0 14px; page-break-inside: avoid; }
.top { display: flex; align-items: baseline; gap: 12px; }
.no { font-size: 20pt; font-weight: bold; color: #0071E3; min-width: 44px; }
.screen { font-weight: bold; font-size: 12.5pt; } .time { margin-left: auto; color: #6E6E73; font-size: 10pt; }
.hook { background: #fff; border-radius: 10px; padding: 8px 12px; margin: 10px 0 8px; font-weight: bold; font-size: 12.5pt; }
.hook:before { content: "훅  "; color: #FF9F0A; }
.body p { margin: 2px 0; } .bridge { color: #0071E3; font-size: 10.5pt; margin-top: 8px; }
.bridge:before { content: "→ 넘기며  "; font-weight: bold; }
h2 { font-size: 15pt; margin: 26px 0 10px; color: #6E6E73; } .pb { page-break-before: always; }
"""


def block(x, label):
    body = "".join(f"<p>{e(line)}</p>" for line in x["body"].split("\n"))
    bridge = f'<div class="bridge">{e(x["bridge"])}</div>' if x["bridge"] else ""
    return (f'<div class="slide"><div class="top"><span class="no">{label}</span><span class="screen">{e(x["screen"])}</span>'
            f'<span class="time">{e(x["time"])}</span></div><div class="hook">{e(x["hook"])}</div>'
            f'<div class="body">{body}</div>{bridge}</div>')


out = [f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>발표 대본</title><style>{CSS}</style></head><body>",
       "<h1>발표 대본</h1><p class='sub'>LangChain 버전 마이그레이션 코드 어시스턴트 · 15분 (본편 약 13분 + 질문) · 발표 [이름]</p>",
       "<div class='rules'><div><b>화면은 훅만</b>큰 숫자 · 한 문장 · 에러 한 줄. 설명은 말로 합니다.</div>"
       "<div><b>장마다 세 박자</b>훅 한 마디 → 설명 → 넘기는 말로 다음 장 예고</div>"
       "<div><b>멈추기</b>숫자를 말한 뒤, 질문을 던진 뒤 1초 쉬기</div></div>"]
out += [block(x, f"{x['no']:02d}") for x in main]
out.append("<h2 class='pb'>질문이 나오면 (부록)</h2>")
out += [block(x, f"부록{i + 1}") for i, x in enumerate(appx)]
out.append("""<h2>예상 질문 답변</h2><div class="slide"><div class="body">
<p><b>통과하면 정답인가요?</b> 아닙니다. 코드 검사까지이고, 실행 결과 비교는 다음 단계입니다. (13장)</p>
<p><b>왜 검사를 LLM에게 맡기지 않았나요?</b> 검사하는 LLM도 같은 옛 지식을 갖고 있어서, 코드로 확인했습니다. (부록 2)</p>
<p><b>근거를 지어낼 수 있지 않나요?</b> 이번에 실제로 보여 준 근거 ID만 인정하고, 기록 없이 바뀐 줄은 걸러 냅니다.</p>
<p><b>30개로 충분한가요?</b> 열 가지 유형 · 난이도별 경향을 보는 게 목적입니다. 다음엔 실사용 코드로 늘립니다. (부록 3)</p>
<p><b>왜 1분이나 걸리나요?</b> 검사에 실패하면 최대 세 번 다시 고치기 때문입니다. 속도 개선이 다음 단계입니다.</p>
<p><b>대화는 어디에 저장되나요?</b> TiDB에 사용자 · 대화 두 테이블로 저장합니다. (부록 1)</p>
</div></div></body></html>""")
open(sys.argv[2], "w", encoding="utf-8").write("".join(out))
print("ok")
