"""테스트 계획 및 결과 보고서 HTML 만들기: python build_report.py <questions.json> <botcheck.txt> <out.html>"""
import collections
import html
import json
import sys

QS = json.load(open(sys.argv[1], encoding="utf-8"))
BOT = [l.strip() for l in open(sys.argv[2], encoding="utf-8") if l.startswith("[")]
OUT = sys.argv[3]
e = html.escape
UP = [q for q in QS if q["type"] != "버전 오가기"]
HOP = [q for q in QS if q["type"] == "버전 오가기"]


def table(head, rows, cls=""):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


types = list(dict.fromkeys(q["type"] for q in UP))
grid = []
for t in types:
    c = collections.Counter(q["difficulty"] for q in UP if q["type"] == t)
    grid.append([t, c["쉬움"], c["중간"], c["어려움"], sum(c.values())])
dc = collections.Counter(q["difficulty"] for q in UP)
grid.append(["<b>합계</b>", f"<b>{dc['쉬움']}</b>", f"<b>{dc['중간']}</b>", f"<b>{dc['어려움']}</b>", f"<b>{len(UP)}</b>"])
vers = collections.Counter(q["source_version"] for q in UP)

groups = [("로그인 · 아이디", BOT[0:4]), ("세션 저장", BOT[4:6]), ("버전 (질문에서 읽음)", BOT[6:12]),
          ("질문 실행 · 예제 · 코드 없는 질문", BOT[12:16]), ("대화 기록 · 사용자 분리", BOT[16:19])]
bot_rows = []
for g, items in groups:
    for i, it in enumerate(items):
        ok = it.startswith("[OK")
        body = it[5:].strip()
        cut = next((i for i in range(len(body)) if body.startswith(" · ", i)
                    and body[:i].count("(") == body[:i].count(")")), None)   # 괄호 밖 첫 ' · '
        name, detail = (body[:cut], body[cut + 3:]) if cut is not None else (body, "")
        bot_rows.append([g if i == 0 else "", e(name), e(detail), "통과" if ok else "실패"])

changes = [
    ("from langchain.chat_models import ChatOpenAI", "from langchain_openai import ChatOpenAI", "imap-02229b7d73", "ChatOpenAI import 경로 변경"),
    ("from langchain.prompts import PromptTemplate", "from langchain_core.prompts import PromptTemplate", "imap-8ed4309a81", "PromptTemplate import 경로 변경"),
    ("from langchain.chains import LLMChain", "(삭제)", "imap-41c19d624a", "LCEL로 바꿔 쓰지 않게 된 import 삭제"),
    ("(새 줄)", "from langchain_core.output_parsers import StrOutputParser", "doc-1f037eaf7dfb", "StrOutputParser 사용을 위해 추가"),
    ("chain = LLMChain(llm=llm, prompt=…)", "chain = PromptTemplate.from_template(…) | llm | StrOutputParser()", "mmap-246a7c2258, doc-1f037eaf7dfb", "LLMChain → LCEL"),
    ("print(chain.run(word='크다'))", "print(chain.invoke({'word': '크다'}))", "mmap-246a7c2258, doc-1f037eaf7dfb", ".run → .invoke, 문자열 반환 유지"),
]

issues = [
    ("대화가 질문마다 다른 세션으로 저장됨", "예시 질문 버튼이 빈 대화 화면에만 있어 질문마다 '새 대화'를 눌러야 했음",
     "새 대화를 누를 때만 세션 생성, 화면 위에 세션 정보 표시, 자동 점검 항목 추가"),
    ("세션 시작 시각이 9시간 이르게 보임", "DB 시각은 UTC로 저장", "화면 표시만 한국 시간(+9)으로"),
    ("평가 질문 1개가 1번 그래프 시험 질문과 똑같음", "같은 예제를 각자 사용", "겹치지 않는 새 LLMChain 질문으로 교체 (유형별 3개 유지)"),
    ("팀 저장소 app.py를 화면과 1번 시험 코드가 같이 씀", "같은 파일 이름", "화면 입구를 streamlit_app.py로 분리, app.py는 1번 것 그대로"),
    ("팀 ERD 확정 (users, chat_history)", "3테이블 설계와 다름", "ERD 그대로 저장 구조 변경, 아이디 중복 검사 추가 (이전 설계는 문서에 보관)"),
    ("TiDB 값이 비었거나 틀리면 화면이 멈춤", "연결 실패를 처리하지 않음", "로컬 저장으로 넘어가고 사이드바에 이유 표시"),
    ("배포 화면에서 그래프 · TiDB 연결 안 됨", "Secrets 값을 읽기 전에 그래프를 불러오고, 실패를 기억함",
     "Secrets를 먼저 읽고 키부터 확인, 실패는 기억하지 않고 다시 시도 (배포와 같은 조건에서 연결 확인)"),
    ("새 입구 supervisor()가 아직 연결 중", "분류 결과 이름 · 노드 연결 · 입력 형식이 맞지 않음 (1번 작업 중)",
     "1번이 수정 (10-15 dev), 화면 입구를 supervisor()로 변경"),
    ("버전 선택 상자가 그래프와 중복", "그래프가 질문에서 목표 버전을 읽게 됨 (2번 target_version)", "선택 상자 제거, 배지는 '원래 버전 → 바꾼 버전'"),
    ("변환에 약 1분, 그동안 화면이 멈춘 것처럼 보임", "검사 · 재시도 때문에 단계가 많음", "그래프 진행 소식(stream)으로 단계별 진행 실시간 표시"),
    ("'다시 시도해줘'라고 쳐도 엉뚱한 답", "화면이 마지막 메시지만 보내서 그래프가 이전 코드를 모름", "검사 실패 결과에 '같은 요청으로 다시 시도' 버튼"),
    ("요청 코드에 없던 줄(ChatCerebras 등)이 생겨 3회 모두 실패", "검색이 상관없는 채팅 모델 연결 문서를 근거로 넘기고, 다시 쓰기가 그 예시를 베낌. 재시도 때 틀린 근거가 빠지지 않음",
     "검사기가 '기록 없는 변경(환각)'으로 정확히 잡음. 2 · 3번에 검색 필터 · 다시 쓰기 규칙 · 재시도 제외 규칙 전달"),
]

appendix = [[q["id"], e(q["type"]), q["difficulty"], f"{q['source_version']} → {q['target_version']}", e(q["request"])] for q in QS]

CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: 'Malgun Gothic', sans-serif; color: #1B2433; font-size: 10.5pt; line-height: 1.6; }
h1 { font-size: 24pt; margin: 0 0 6px; } h2 { font-size: 15pt; color: #1F5FAE; border-bottom: 2px solid #1F5FAE; padding-bottom: 3px; margin-top: 26px; }
h3 { font-size: 12pt; margin: 18px 0 6px; } p { margin: 6px 0; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 9.5pt; page-break-inside: auto; }
th, td { border: 1px solid #C9CCD3; padding: 4px 7px; text-align: left; vertical-align: top; word-break: keep-all; } th { background: #ECEBE5; white-space: nowrap; }
td code { word-break: break-all; }
tr { page-break-inside: avoid; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always; }
.cover .k { color: #1F5FAE; font-weight: bold; letter-spacing: 1px; } .cover .t { font-size: 30pt; font-weight: bold; line-height: 1.25; }
.box { background: #F3F6FB; border-left: 4px solid #1F5FAE; padding: 8px 12px; margin: 10px 0; }
.warn { background: #FFF6EF; border-left: 4px solid #B4471B; }
code, pre { font-family: Consolas, monospace; font-size: 9pt; } pre { background: #14202E; color: #E8ECF1; padding: 10px; border-radius: 6px; white-space: pre-wrap; }
.blank { color: #B4471B; font-weight: bold; } .small { font-size: 8.8pt; } .pb { page-break-before: always; }
.two { display: flex; gap: 10px; } .two pre { flex: 1; }
"""

body = f"""
<div class="cover">
  <div class="k">SKN35 · LLM 연동 내외부 문서 기반 질의응답 시스템</div>
  <div>
    <div class="t">테스트 계획 및 결과 보고서</div>
    <p style="font-size:15pt;color:#4A5363">LangChain 버전 마이그레이션 코드 어시스턴트</p>
  </div>
  <div>
    {table(["항목", "내용"], [["팀", "SKN35 3rd 4Team"], ["작성", "4번 (화면 · DB · 평가) [이름]"], ["작성일", "2026-10-15"],
                           ["기준 코드", "팀 저장소 sungwook 브랜치 (dev 최신 반영, 2026-10-14)"],
                           ["상태", "테스트 계획 확정 · 화면 · DB · 질문 세트 검사 완료 · <span class='blank'>비교 실험 결과 미입력</span>"]])}
  </div>
</div>

<h2>요약</h2>
<div class="box">
<p><b>무엇을 만들었나</b>: 옛 버전 LangChain 코드를 넣고 바꿀 버전을 고르면, 대응표 · 공식 문서를 근거로 고치고 verifier가 LLM 없이 11가지를 검사해, 실패하면 최대 3회 다시 고치는 챗봇.</p>
<p><b>무엇을 시험했나</b>: (A) 평가 질문 36개가 올바른 시험지인지 (B) 화면 · DB가 의도대로 동작하는지 (C) 화면이 팀 그래프를 불러 실제 결과를 보여 주는지 (D) 일반 LLM과 비교해 얼마나 나은지.</p>
<p><b>지금까지 결과</b>: 질문 세트 검사 <b>36/36</b> · 화면 · DB 자동 점검 <b>19/19</b> · 최상위 그래프 세 갈래(변환 · 검색 · 일반) 연결 확인 · TiDB 저장 · 중복 검사 확인 · 그래프 연결 실행 <b>2회 모두 3회차 통과</b>(바뀐 6줄 모두 근거 ID) · 비교 실험 <span class="blank">[__]</span></p>
</div>

<h2>1. 개요</h2>
<h3>1-1. 배경</h3>
<p>LangChain은 1.0에서 패키지가 나뉘고 <code>LLMChain</code>, <code>initialize_agent</code> 같은 옛 체인 · 에이전트가 빠졌습니다. 인터넷의 코드는 대부분 옛 버전이라 LLM은 옛 방식을 답하고, 틀려도 모릅니다(버전 지체 환각). 연구에서도 문서가 부족하면 LLM 코드의 42.55%만, 문서를 줘도 66.36%만 목표 버전에서 실행됩니다(When LLMs Lag Behind, 2026).</p>
<h3>1-2. 테스트 목표</h3>
{table(["목표", "확인 방법"], [
    ["시험지가 공정한가", "옛 코드가 1.x에서 실제로 깨지는지, 기대하는 답의 import가 1.x에서 실제로 되는지 자동 확인"],
    ["화면 · DB가 의도대로 동작하는가", "자동 점검 봇이 로그인부터 대화 다시 열기까지 19가지를 화면으로 실행"],
    ["팀 그래프와 연결되는가", "같은 코드를 화면 경로로 그래프에 보내 결과 모양 · 근거 ID · 검사 결과 확인"],
    ["일반 LLM보다 나은가", "같은 질문 30개 · 같은 모델 · 같은 채점 기준으로 비교 (진행 예정)"]])}
<h3>1-3. 범위</h3>
<p>포함: LangChain 0.0.300 ~ 0.3.30 코드를 1.x로 올리기(그래프), 질문에 적은 버전으로 바꾸기, LangChain 질문 · 일반 질문 답변, 화면, 대화 기록(TiDB). 제외: 바뀐 코드의 실제 실행 결과 비교.</p>

<h2>2. 시스템 구성</h2>
{table(["단계", "하는 일", "담당"], [
    ["질문 분류", "코드 변환(migration) · LangChain 질문(search) · 일반 질문(general)으로 나눔", "1번"],
    ["① analyzer", "질문에서 코드를 뽑고 바꿀 부분 찾기 (LLM)", "1번"],
    ["② retriever", "import · 메서드 대응표 정확 매칭 + 문서 하이브리드 검색(BM25 + 벡터), 재시도 때 틀린 근거 제외", "2번"],
    ["③ rewriter", "근거를 보고 코드 다시 쓰기, 바뀐 줄마다 근거 ID · 이유", "3번"],
    ["④ verifier", "LLM 없이 11가지 검사, 실패하면 ②로 (최대 3회)", "3번"],
    ["화면 · DB · 평가", "Streamlit 화면, TiDB 대화 기록, 평가 질문 · 점검 도구", "4번"]])}
{table(["근거 데이터 (2번)", "규모"], [["import 대응표", "9,155줄 (옛 경로 → 1.x 경로)"], ["메서드 대응표", "42개 (.run → .invoke 등)"],
                                   ["공식 문서", "최신 271개 + 옛 마이그레이션 가이드 24개"], ["검색용 조각", "11,945개 (Chroma Cloud, text-embedding-3-small)"],
                                   ["버전별 도구 목록", "23개 패키지 · 버전"]])}
<p class="small">verifier 11가지: ① 문법 ② 근거 ID(이번에 보여 준 근거만) ③ 변경 기록(기록 없는 변경 = 환각) ④ 남은 옛 import ⑤ import 존재 ⑥ 남은 옛 메서드(경고) ⑦ 안 쓰는 import ⑧ 반환값 보존 ⑨ 정의 안 된 이름 ⑩ 출력 꺼내기 ⑪ 체인 입출력 키</p>
{table(["구성", "선택"], [["언어 · 패키지", "Python 3.12, uv (배포는 requirements.txt)"], ["LLM 연동", "LangChain 1.4.4, LangGraph, langchain-openai (gpt-4o-mini)"],
                       ["벡터 DB · 검색", "Chroma Cloud, BM25 + 벡터 하이브리드"], ["DB", "TiDB Cloud (users, chat_history)"], ["화면 · 배포", "Streamlit, Streamlit Community Cloud"]])}

<h2 class="pb">3. 테스트 계획</h2>
<h3>3-1. 테스트 종류</h3>
{table(["구분", "대상", "방법", "도구"], [
    ["A. 질문 세트 검사", "평가 질문 36개", "옛 코드가 1.x에서 깨지는지, 기대 import가 1.x에서 되는지 (0.x 목표는 버전별 도구 목록으로 확인)", "eval/check_questions.py"],
    ["B. 화면 · DB 자동 점검", "화면 전체 흐름", "임시 DB로 화면을 직접 실행해 19가지 확인 (유료 API 없이)", "tools/bot_check.py"],
    ["C. 그래프 연결 실행", "화면 → 팀 그래프", "같은 코드를 화면과 같은 경로로 그래프에 보내 결과 확인", "src/ui/client.py run()"],
    ["D. 비교 실험", "일반 LLM vs 우리 챗봇", "질문 30개, 같은 모델 · 같은 입력 · 같은 채점", "진행 예정"]])}
<h3>3-2. 평가 질문 36개</h3>
<p>실제 사용자가 보낼 법한 <b>자연어 요청 + 옛 코드</b>로 만들었습니다. 1.x로 올리기 30개(10유형 × 3)와 버전 오가기 6개(되돌리기 · 중간 단계)입니다. 비교 실험은 팀 그래프가 지원하는 1.x로 올리기 30개로 합니다.</p>
{table(["유형", "쉬움", "중간", "어려움", "합계"], grid)}
<p class="small">지금 코드 버전 분포(30개): {' · '.join(f'{k} {v}개' for k, v in sorted(vers.items()))} · 버전 오가기 6개: 1.x → 0.2 · 0.3 · 0.1 되돌리기, 0.3 → 0.1 · 0.0.354, 0.0.300 → 0.2</p>
<h3>3-3. 비교 실험 설계</h3>
{table(["항목", "규칙"], [["비교 대상", "일반 LLM(같은 모델에 질문만) vs 우리 챗봇(팀 그래프)"], ["모델", "양쪽 같은 <span class='blank'>[모델명]</span>, temperature 0"],
                       ["입력", "같은 요청 문장 + 같은 코드"], ["채점", "verifier와 같은 검사 기준 (11가지 중 오류 항목이 없으면 통과)"],
                       ["최대 시도", "우리 챗봇 3회, 일반 LLM 1회"], ["공정성", "같은 질문 · 같은 모델 · 같은 채점기, LangChain import를 지워서 통과하는 꼼수는 실패 처리"]])}
{table(["지표", "정의"], [["검증 통과율", "통과한 질문 수 ÷ 30"], ["근거 포함률", "근거 ID가 붙은 바뀐 줄 수 ÷ 전체 바뀐 줄 수"],
                       ["재시도 효과", "최종 통과율 − 1회차 통과율 (%p)"], ["평균 시도", "통과한 질문의 시도 횟수 평균"]])}

<h2 class="pb">4. 테스트 결과</h2>
<h3>4-1. A. 질문 세트 검사: 36/36 통과</h3>
<p>36개 모두 옛 코드가 LangChain 1.4.4에서 실제로 깨지고, 기대하는 답의 import가 1.x에서 됩니다. 패키지가 없는 import는 2번의 버전별 도구 목록으로 확인했습니다. 0.x로 되돌리는 6개는 옛 경로가 목표 버전에 없는지, 기대 경로가 목표 버전에 있는지 도구 목록으로 확인했습니다. (2026-10-14)</p>
<h3>4-2. B. 화면 · DB 자동 점검: 19/19 통과</h3>
{table(["영역", "점검 항목", "확인 내용", "결과"], bot_rows, "small")}
<p class="small">팀 저장소 구조 + 2번 데이터로 실행. 임시 SQLite를 써서 실제 TiDB에는 쓰지 않음. 2026-10-15 버전 선택 상자를 없애면서(바꿀 버전은 그래프가 질문에서 읽음) 버전 선택 관련 항목을 빼고 '버전 고르기 없음' 항목을 넣어 30 → 19가지가 됐습니다.</p>
<h3>4-3. TiDB 저장 확인 (직접 확인)</h3>
{table(["확인", "결과"], [["TiDB Cloud에 langchain_db · users · chat_history 생성", "완료"], ["화면 로그인 화면 표시 '대화 기록 저장: TiDB'", "확인"],
                       ["가입 → users 1행, 같은 대화에 질문 2개 → chat_history 같은 session_id 2행", "확인"], ["같은 아이디 다시 가입 → '이미 있는 아이디예요'", "확인"],
                       ["TiDB 값이 비었을 때 → 로컬 저장으로 넘어가고 이유 표시", "확인"]])}
<h3>4-4. C. 그래프 연결 실행</h3>
<p>0.0.300 시절 LLMChain 코드를 화면과 같은 경로(<code>run()</code>)로 팀 그래프에 보냈습니다. 같은 코드를 dev 반영 전후 두 번 실행해 <b>두 번 모두 3회차에 검사를 통과</b>했습니다(약 44초 · 61초).</p>
<div class="two">
<pre>{e('''from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(temperature=0)
chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template('{word}의 반대말은?'))
print(chain.run(word='크다'))''')}</pre>
<pre>{e('''from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(temperature=0)
chain = PromptTemplate.from_template('{word}의 반대말은?') | llm | StrOutputParser()
print(chain.invoke({'word': '크다'}))''')}</pre>
</div>
{table(["옛 줄", "새 줄", "근거 ID", "이유"], [[f"<code>{e(a)}</code>", f"<code>{e(b)}</code>", e(c), e(d)] for a, b, c, d in changes], "small")}
<p>바뀐 6줄 모두 근거 ID가 붙었고(근거 포함률 100%, 이 사례 기준), 근거 부족으로 못 바꾼 줄은 0줄, 설치 안내는 <code>langchain-core</code>, <code>langchain-openai</code>였습니다.</p>
<h3>4-5. C-2. 최상위 그래프 세 갈래 연결 (2026-10-15)</h3>
{table(["질문", "분류", "결과"], [["\"안녕하세요\"", "general", "2.5초, 일반 답변"], ["\"0.3에서 1.0으로 오면서 LLMChain은 어떻게 바뀌었어?\"", "search", "12.5초, 문서 근거로 설명"], ["옛 코드 + \"최신 버전으로 바꿔 줘\"", "migration", "16초, 목표 1.4.5 (질문에서 읽음), 1회 만에 검사 통과"], ["새 코드 + \"0.2에서 돌아가게 바꿔 줘\"", "migration", "28초, 목표 0.2.17은 맞게 읽었으나 3회 모두 검사 실패 (5장 참고)"]])}
<p>화면은 그래프 단계(질문 분류 → 바꿀 부분 → 근거 → 고치기 → 검사, 실패하면 다시)를 실시간으로 보여 주고, 검사에 실패하면 "같은 요청으로 다시 시도" 버튼을 띄웁니다.</p>
<h3>4-6. D. 비교 실험 결과 <span class="blank">[실험 후 입력]</span></h3>
{table(["시스템", "검증 통과율", "쉬움", "중간", "어려움", "근거 포함률", "평균 시도"], [
    ["우리 챗봇", "[__]%", "[__]%", "[__]%", "[__]%", "[__]%", "[__]회"],
    ["일반 LLM", "[__]%", "[__]%", "[__]%", "[__]%", "-", "1회"]])}
<p>1회차 통과율 <span class="blank">[__]%</span> → 최종 <span class="blank">[__]%</span> (재시도 효과 <span class="blank">+[__]%p</span>)</p>

<h2 class="pb">5. 테스트 중 발견한 문제와 조치</h2>
{table(["문제", "원인", "조치"], [[e(a), e(b), e(c)] for a, b, c in issues], "small")}

<h2>6. 한계와 다음 단계</h2>
{table(["한계", "다음 단계"], [
    ["11가지 코드 검사까지 하지만, 바뀐 코드의 실제 실행 결과는 확인하지 않음", "가짜 LLM을 넣어 코드 전체 실행 테스트"],
    ["옛 버전으로 되돌리기는 아직 검사 통과율이 낮고, 상관없는 문서 예시를 베끼는 경우가 있음", "다시 쓰기 규칙 강화, 틀린 근거를 다음 시도에서 빼기, 상관없는 문서 걸러내기 (2 · 3번)"],
    ["검사 · 재시도로 한 번 변환에 약 1분 (진행 단계는 화면에 실시간 표시)", "쉬운 import는 대응표만으로 바로 답하기"],
    ["다시 연 대화는 결과 패널 없이 질문 · 답만 (ERD에 결과 열 없음)", "필요하면 결과 열 추가를 팀과 협의"],
    ["질문 30개 · LangChain만 대상", "실사용 코드로 확장, 다른 라이브러리로 확장"]])}

<h2 class="pb">부록 A. 평가 질문 36개</h2>
{table(["ID", "유형", "난이도", "버전", "요청"], appendix, "small")}

<h2>부록 B. 재현 방법</h2>
<pre>{e('''# 팀 저장소 (sungwook) 에서
uv sync
uv pip install -r requirements.txt

# A. 질문 세트 검사 (LangChain 1.x 가 깔린 별도 환경 필요)
python eval/check_questions.py --py <1.x python> --map data/processed/import_map.jsonl --symbols data/raw/symbols

# B. 화면 · DB 자동 점검 (임시 SQLite, 유료 API 없음)
python tools/bot_check.py

# 화면 실행 (.env 에 OPENAI_API_KEY · CHROMA_* · TIDB_* )
streamlit run streamlit_app.py''')}</pre>
"""

open(OUT, "w", encoding="utf-8").write(
    f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>테스트 계획 및 결과 보고서</title><style>{CSS}</style></head><body>{body}</body></html>")
print("저장", OUT)
