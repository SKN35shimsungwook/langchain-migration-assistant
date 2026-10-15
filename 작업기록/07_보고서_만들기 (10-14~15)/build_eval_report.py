"""평가 보고서 HTML: python build_eval_report.py <summary.json> <findings.json> <out.html>"""
import html
import json
import sys

S = json.load(open(sys.argv[1], encoding="utf-8"))
F = json.load(open(sys.argv[2], encoding="utf-8"))
OUT = sys.argv[3]
e = html.escape
UP, HOP = S["compare"].get("upgrade"), S["compare"].get("hop")
SE = S["self_eval"]


def pct(x):
    return "-" if x is None else f"{x * 100:.0f}%"


def table(head, rows, cls=""):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def bars(rows):
    """[(라벨, 챗봇, 일반)] → 가로 막대 두 줄씩."""
    out = []
    for label, a, b in rows:
        out.append(f"<div class='bl'>{label}</div>"
                   f"<div class='br'><span class='bar bot' style='width:{(a or 0) * 100:.0f}%'></span><span class='v'>{pct(a)}</span></div>"
                   f"<div class='br'><span class='bar llm' style='width:{(b or 0) * 100:.0f}%'></span><span class='v'>{pct(b)}</span></div>")
    return "<div class='bars'>" + "".join(out) + "</div>"


CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: 'Malgun Gothic', sans-serif; color: #1B2433; font-size: 10.5pt; line-height: 1.6; }
h1 { font-size: 24pt; margin: 0 0 6px; } h2 { font-size: 15pt; color: #1F5FAE; border-bottom: 2px solid #1F5FAE; padding-bottom: 3px; margin-top: 26px; }
h3 { font-size: 12pt; margin: 18px 0 6px; } p { margin: 6px 0; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 9.3pt; }
th, td { border: 1px solid #C9CCD3; padding: 4px 7px; text-align: left; vertical-align: top; word-break: keep-all; } th { background: #ECEBE5; white-space: nowrap; }
td code { word-break: break-all; } tr { page-break-inside: avoid; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always; }
.cover .k { color: #1F5FAE; font-weight: bold; letter-spacing: 1px; } .cover .t { font-size: 30pt; font-weight: bold; line-height: 1.25; }
.box { background: #F3F6FB; border-left: 4px solid #1F5FAE; padding: 8px 12px; margin: 10px 0; }
.warn { background: #FFF6EF; border-left: 4px solid #B4471B; }
code, pre { font-family: Consolas, monospace; font-size: 9pt; } pre { background: #14202E; color: #E8ECF1; padding: 10px; border-radius: 6px; white-space: pre-wrap; }
.small { font-size: 8.6pt; } .pb { page-break-before: always; }
.kpis { display: flex; gap: 10px; margin: 12px 0; } .kpi { flex: 1; border: 1px solid #D8DCE3; border-radius: 8px; padding: 10px 12px; }
.kpi .n { font-size: 22pt; font-weight: bold; color: #1F5FAE; line-height: 1.2; } .kpi .l { font-size: 9pt; color: #4A5363; }
.kpi.o .n { color: #B4471B; }
.bars { display: grid; grid-template-columns: 34% 1fr; gap: 2px 10px; margin: 10px 0; font-size: 9.3pt; }
.bl { grid-row: span 2; align-self: center; } .br { display: flex; align-items: center; gap: 6px; height: 15px; }
.bar { display: inline-block; height: 11px; border-radius: 3px; } .bar.bot { background: #1F5FAE; } .bar.llm { background: #B9BFC9; }
.v { font-size: 8.6pt; color: #4A5363; } .legend span { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin: 0 4px 0 10px; }
.ok { color: #2E7D32; font-weight: bold; } .ng { color: #B4471B; font-weight: bold; }
"""

up_bot, up_llm = UP["bot"], UP["llm"]
kpis = f"""<div class="kpis">
<div class="kpi"><div class="n">{pct(up_bot['pass'])}</div><div class="l">우리 챗봇 · 공통 기준 통과<br>(1.x로 올리기 {UP['n']}개)</div></div>
<div class="kpi o"><div class="n">{pct(up_llm['pass'])}</div><div class="l">일반 LLM · 공통 기준 통과<br>(같은 모델 gpt-4o-mini)</div></div>
<div class="kpi"><div class="n">{SE['total']}점</div><div class="l">자체 평가 ({SE['grade']}등급)<br>목표 달성 {SE['met']}/{SE['items']}항목</div></div>
<div class="kpi"><div class="n">{pct(up_bot['verified'])}</div><div class="l">챗봇 검증 통과 (자체 판정)<br>3회차까지 누적</div></div>
</div>"""

judge_rows = [[e(v["label"]), pct(v["rate"]), pct(up_llm["items"][k]["rate"])] for k, v in up_bot["items"].items()]
judge_rows.insert(0, ["<b>공통 기준 통과 (8개 모두)</b>", f"<b>{pct(up_bot['pass'])}</b>", f"<b>{pct(up_llm['pass'])}</b>"])
judge_rows.insert(1, ["실행 기준 통과 (정답 import 제외 7개)", pct(up_bot["run_pass"]), pct(up_llm["run_pass"])])
judge_rows += [["응답 시간 (중앙값)", f"{up_bot['median_sec']}초", f"{up_llm['median_sec']}초"],
               ["남은 옛 메서드 호출 (경고 수, 적을수록 좋음)", str(up_bot["legacy_methods"]), str(up_llm["legacy_methods"])]]

diff_rows = [[e(d), pct(up_bot["by_difficulty"][d]), pct(up_llm["by_difficulty"].get(d))] for d in ("쉬움", "중간", "어려움") if d in up_bot["by_difficulty"]]
type_rows = [[e(t), pct(up_bot["by_type"][t]), pct(up_llm["by_type"].get(t))] for t in up_bot["by_type"]]

curve = S.get("attempt_curve", {})
curve_rows = [[f"{n}회차까지", pct(curve.get(str(n), curve.get(n)))] for n in (1, 2, 3)]

se_rows = []
for r in SE["rows"]:
    mark = f"<span class='ok'>달성</span>" if r["met"] else f"<span class='ng'>미달</span>"
    fails = ", ".join(r["fails"][:8]) + (" …" if len(r["fails"]) > 8 else "")
    se_rows.append([r["id"], e(r["area"]), e(r["item"]), f"<span class='small'>{e(r['basis'])}</span>",
                    f"{pct(r['rate'])} ({r['ok']}/{r['n']})", pct(r["target"]), mark, f"{r['score']}/{r['weight']}",
                    f"<span class='small'>{e(fails)}</span>"])

areas = {}
for r in SE["rows"]:
    a = areas.setdefault(r["area"], [0, 0])
    a[0] += r["score"]
    a[1] += r["weight"]
area_rows = [[e(k), f"{v[0]:.1f} / {v[1]}", pct(v[0] / v[1])] for k, v in areas.items()]

pq_rows = []
for p in UP["per_question"] + (HOP["per_question"] if HOP else []):
    b = "<span class='ok'>통과</span>" if p["bot_pass"] else "<span class='ng'>실패</span>"
    l = "<span class='ok'>통과</span>" if p["llm_pass"] else "<span class='ng'>실패</span>"
    v = f"통과 · {p['attempts']}회" if p["bot_verified"] else (f"실패 · {p['attempts']}회" if p["attempts"] else "변환 안 함")
    why = "; ".join(p["bot_detail"])[:120]
    pq_rows.append([p["id"], e(p["type"]), e(p["difficulty"]), b, v, l, f"<span class='small'>{e(why)}</span>"])

hop_html = ""
if HOP:
    hop_html = f"""<h3>2-4. 버전 오가기 ({HOP['n']}개, 참고)</h3>
<p>목표가 0.x인 질문은 2번의 1.x 도구 목록으로 확인할 수 없는 항목(옛 import · import 존재 · 남은 import)을 빼고 5항목으로 채점했습니다.</p>
{table(["", "우리 챗봇", "일반 LLM"], [["공통 기준 통과", pct(HOP['bot']['pass']), pct(HOP['llm']['pass'])],
                                       ["챗봇 검증 통과", pct(HOP['bot']['verified']), "-"],
                                       ["응답 시간 (중앙값)", f"{HOP['bot']['median_sec']}초", f"{HOP['llm']['median_sec']}초"]])}"""

find_rows = [[str(i), e(f["what"]), e(f["evidence"]), e(f["owner"]), e(f["fix"])] for i, f in enumerate(F["findings"], 1)]

body = f"""
<div class="cover">
  <div class="k">SKN35 · LLM 연동 내외부 문서 기반 질의응답 시스템</div>
  <div>
    <div class="t">비교 평가 · 자체 평가<br>결과 보고서</div>
    <p style="font-size:15pt;color:#4A5363">LangChain 버전 마이그레이션 코드 어시스턴트</p>
  </div>
  <div>
    {table(["항목", "내용"], [["팀", "SKN35 3rd 4Team"], ["작성", "4번 (화면 · DB · 평가)"], ["실행", e(S['run_at'])],
                           ["대상", "팀 저장소 dev 최신 그래프 (최상위 supervisor) · 모델 gpt-4o-mini"],
                           ["평가 도구", "eval/run_eval.py (실행) · eval/score.py (채점, LLM 사용 안 함)"], ["관련 문서", "프로젝트 최종 보고서 (설계 · 역할별 작업 기록 · 트러블슈팅 전체) · 테스트 계획 및 결과 보고서"]])}
  </div>
</div>

<h2>요약</h2>
{kpis}
<div class="box">{"".join(f"<p>{e(x)}</p>" for x in F["summary"])}</div>

<h3>실제 화면</h3>
<figure style="margin:10px 0;text-align:center"><img src="screen_result.jpg" style="width:100%;border:1px solid #C9CCD3;border-radius:6px"><figcaption class="small" style="color:#4A5363">실제 화면 (2026-10-15) · 확인용 예제 q11(LLMChain → LCEL)을 보내 2회차에 검증 통과 · 0.0.300 ~ 0.3.30 → 1.4.5 · 바뀐 줄을 빨강 · 초록으로 비교</figcaption></figure>

<h2 class="pb">강점 (숫자로 확인된 것)</h2>
{table(["강점", "근거"], [[f"<b>{e(a)}</b>", e(b)] for a, b in F["strengths"]])}

<h2>1. 평가 설계</h2>
<h3>1-1. 두 가지 평가</h3>
{table(["", "비교 평가", "자체 평가"], [
    ["질문", "일반 LLM보다 나은가?", "우리가 정한 규칙대로 동작하는가?"],
    ["대상", "우리 챗봇 vs 일반 LLM (같은 질문, 같은 모델)", "우리 챗봇만"],
    ["기준", "공통 채점 8항목 (두 답에 같은 잣대)", "팀 프롬프트 · 코드에 적힌 규칙 21항목 (100점)"],
    ["쓰는 곳", "발표 결과 슬라이드, README 결과", "다음 개선 순서 정하기, 담당별 전달"]])}
<h3>1-2. 실험 조건</h3>
{table(["항목", "내용"], [
    ["질문", "eval/questions.json 36개 (1.x로 올리기 30 + 버전 오가기 6) · 분류 확인 질문 eval/route_probes.json 14개"],
    ["입력", "요청 문장 + 코드 블록. 두 시스템에 글자 하나 다르지 않게 같은 글"],
    ["일반 LLM", "gpt-4o-mini, temperature 0, 시스템 프롬프트 없음 (ChatGPT에 붙여 넣는 상황)"],
    ["우리 챗봇", "팀 그래프 그대로 (분류 → 분석 → 근거 검색 → 고쳐 쓰기 → 검사, 최대 3회). 화면과 같은 호출 방식"],
    ["채점", "LLM 없이 코드로만 채점 (사람 · LLM 판정의 주관 없음). 같은 결과를 몇 번 채점해도 같은 점수"],
    ["횟수", "질문마다 1회 실행 (분류 일관성만 3회)"]])}
<h3>1-3. 공통 채점 8항목</h3>
<p>일반 LLM 답에는 근거 기록이 없으므로, 근거 ID · 변경 기록처럼 우리 챗봇에만 있는 검사는 넣지 않았습니다. 8개를 모두 통과해야 '공통 기준 통과'입니다.</p>
{table(["#", "항목", "통과 조건", "확인 방법"], [
    ["1", "문법", "파이썬으로 읽힘", "ast"],
    ["2", "옛 import 없음", "2번 대응표의 옛 경로가 남지 않음", "import_map 9,155줄"],
    ["3", "import 실제 존재", "새 import 경로가 LangChain 1.x에 있음", "2번 버전별 도구 목록 (1.4.5)"],
    ["4", "정의 안 된 이름 없음", "원래 코드엔 없던 NameError가 생기지 않음", "ast"],
    ["5", "결과값 보존", "문자열 결과 유지, LCEL 결과를 ['text']로 꺼내지 않음, 체인 입출력 키가 맞음", "verifier 8 · 10 · 11번 + 더 넓은 꺼내기 검사"],
    ["6", "남은 import 없음", "바꾸고 안 쓰게 된 import가 남지 않음", "ast"],
    ["7", "정답 import 포함", "질문마다 사람이 정한 정답 import가 모두 들어 있음", "questions.json expected_imports"],
    ["8", "코드를 실제로 바꿈", "원문 그대로 돌려주지 않음", "줄 비교"]])}

<h2 class="pb">2. 비교 평가 결과</h2>
<h3>2-1. 1.x로 올리기 {UP['n']}개</h3>
<p class="legend small"><span style="background:#1F5FAE"></span>우리 챗봇<span style="background:#B9BFC9"></span>일반 LLM</p>
{bars([(v['label'], v['rate'], up_llm['items'][k]['rate']) for k, v in up_bot['items'].items()])}
{table(["항목", "우리 챗봇", "일반 LLM"], judge_rows)}
<h3>2-2. 난이도 · 유형별 공통 기준 통과</h3>
{table(["난이도", "챗봇", "일반 LLM"], diff_rows)}
{table(["유형 (각 3개)", "챗봇", "일반 LLM"], type_rows)}
<h3>2-3. 실패를 알려 주는가</h3>
{table(["", "개수", "뜻"], [
    ["실패했지만 '검증 실패'로 알림", str(up_bot['flagged_failures']), "사용자가 결과를 그대로 믿지 않게 화면에 실패 배지와 이유를 보여 줌"],
    ["검증은 통과했는데 공통 채점에서 실패", str(up_bot['silent_failures']), "검사기가 놓친 경우. 4장 개선 대상"],
    ["질문 분류가 틀려 변환을 안 함", str(len(up_bot.get('misrouted', []))), ", ".join(up_bot.get('misrouted', [])) or "-"]])}
<p class="small">일반 LLM은 틀린 코드도 맞다고 생각하고 내놓습니다. 실패 여부를 알려 주는 장치가 없습니다.</p>
{hop_html}

<h2 class="pb">3. 자체 평가 (점검표 · 점수표)</h2>
<p>팀이 프롬프트와 코드에 적어 둔 규칙을 실제 실행 기록으로 확인했습니다. 점수 = 배점 × 달성률. 목표는 실무에서 '믿고 쓸 수 있다'고 볼 최소 수준으로 4번이 정했습니다.</p>
<div style="display:flex;gap:12px;align-items:flex-start">
<div style="flex:1">{table(["영역", "점수", "달성률"], area_rows + [["<b>합계</b>", f"<b>{SE['total']} / 100</b>", f"<b>{SE['grade']}등급</b>"]])}</div>
<div style="flex:1" class="box small"><p><b>등급</b>: A 90점 이상 · B 80 · C 70 · D 70 미만</p><p><b>읽는 법</b>: '미달'인 항목이 다음에 고칠 곳입니다. 마지막 칸은 미달을 만든 질문 번호입니다.</p></div>
</div>
{table(["#", "영역", "점검 항목", "팀이 정한 근거", "결과", "목표", "판정", "점수", "미달 질문"], se_rows, "small")}
<h3>3-1. 다시 시도의 효과 (1.x로 올리기)</h3>
{table(["", "검증 통과 (누적)"], curve_rows)}

<h2 class="pb">4. 약점과 개선 방안</h2>
<p class="small">① ~ ④는 고칠 순서. 담당은 4번 제안이며 팀 확인 후 확정합니다.</p>
{table(["#", "무엇", "근거 (이번 실행)", "담당", "개선안"], find_rows)}

<h2>5. 프로젝트 의의</h2>
<ol>{"".join(f"<li>{e(x)}</li>" for x in F["significance"])}</ol>

<h2>6. 한계</h2>
<ul>{"".join(f"<li>{e(x)}</li>" for x in F["limits"])}</ul>

<h2>7. 다시 해 보기</h2>
<pre>python eval/run_eval.py          # 질문 50개 실행 (챗봇 · 일반 LLM · 분류 3회), 끊겨도 이어서
python eval/score.py             # 채점 → eval/results/summary.json, scorecard.md</pre>

<h2 class="pb">부록. 질문별 결과</h2>
{table(["id", "유형", "난이도", "챗봇", "챗봇 검증", "일반 LLM", "챗봇이 걸린 항목"], pq_rows, "small")}
"""

open(OUT, "w", encoding="utf-8").write(
    f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>비교 평가 · 자체 평가 결과 보고서</title><style>{CSS}</style></head><body>{body}</body></html>")
print("저장", OUT)
