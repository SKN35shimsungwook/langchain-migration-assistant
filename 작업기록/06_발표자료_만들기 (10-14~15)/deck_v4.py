"""발표 PPT v2 (17장, 15분): python deck_slides.py <출력.pptx> -"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "deck_helpers.py"), encoding="utf-8").read())


def capture(s, x, y, w, h, what, dark=False):
    """직접 찍어 넣을 화면 캡처 자리."""
    box(s, x, y, w, h, fill=NAVY2 if dark else WHITE, line="5A6B80" if dark else "C3C2B7", dash=True)
    text(s, x + 0.3, y + h / 2 - 0.45, w - 0.6, 0.9, "[화면 캡처]\n" + what, size=14, bold=True,
         color="8A9AAD" if dark else MUTED, align=PP_ALIGN.CENTER)


def code_box(s, x, y, w, h, title, code, accent):
    box(s, x, y, w, h, fill=NAVY, line=None)
    text(s, x + 0.25, y + 0.15, w - 0.5, 0.3, title, size=12, bold=True, color=accent)
    text(s, x + 0.25, y + 0.5, w - 0.5, h - 0.6, code, size=11, color="E8ECF1", font=MONO, spacing=1.3)


def _chart(s, kind, x, y, w, h, cats, series, colors):
    """PowerPoint 기본 차트 (PPT에서 값 · 색을 바로 고칠 수 있음)."""
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_LEGEND_POSITION, XL_LABEL_POSITION
    data = CategoryChartData()
    data.categories = cats
    for name, vals in series:
        data.add_series(name, vals)
    box(s, x, y, w, h)
    ch = s.shapes.add_chart(kind, Inches(x + 0.15), Inches(y + 0.1), Inches(w - 0.3), Inches(h - 0.2), data).chart
    ch.font.size = Pt(12)
    ch.font.name = FONT
    ch.has_legend = len(series) > 1
    if ch.has_legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
    va = ch.value_axis
    va.maximum_scale, va.minimum_scale = 1.0, 0.0
    va.has_major_gridlines = False
    va.visible = False
    ch.category_axis.tick_labels.font.size = Pt(12)
    ch.category_axis.format.line.color.rgb = rgb(LINE)
    plot = ch.plots[0]
    plot.gap_width = 60
    plot.overlap = -10
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format, dl.number_format_is_linked = "0%", False
    dl.font.size, dl.font.bold = Pt(12), True
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    for ser, c in zip(plot.series, colors):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = rgb(c)
    return ch


def bar_chart(s, x, y, w, h, cats, series):
    from pptx.enum.chart import XL_CHART_TYPE
    ch = _chart(s, XL_CHART_TYPE.BAR_CLUSTERED, x, y, w, h, cats, series, [BLUE, "B9BFC9"])
    ch.category_axis.reverse_order = True   # 위에서부터 순서대로
    return ch


def column_chart(s, x, y, w, h, cats, series):
    from pptx.enum.chart import XL_CHART_TYPE
    return _chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, w, h, cats, series, [BLUE])


# 1. 표지 ----------------------------------------------------------------------
s = new(NAVY)
text(s, 0.75, 0.75, 11.8, 0.4, "SKN35 · LLM 연동 내외부 문서 기반 질의응답 시스템", size=15, bold=True, color=SKY)
text(s, 0.75, 2.25, 11.8, 2.0, "LangChain 버전\n마이그레이션 코드 어시스턴트", size=50, bold=True, color="F2F1EC", spacing=1.1)
text(s, 0.75, 4.35, 11.8, 0.6, "Langration · 옛 버전 코드를 원하는 버전에서 돌아가는 코드로, 근거와 검증까지 함께", size=21, color="B9C3CF")
text(s, 0.75, 6.55, 11.8, 0.4, "SKN35 3rd 4Team · 발표 [이름] · 2026-10-15", size=14, color="B9C3CF")
notes(s, "[0:00~0:30] 안녕하세요, SKN35 3기 4팀 발표를 맡은 [이름]입니다. 저희는 옛 버전 LangChain 코드를 넣고 바꿀 버전을 고르면, "
         "그 버전에서 돌아가는 코드로 고쳐 주고, 정말 돌아가는지 검사까지 해 주는 챗봇을 만들었습니다. "
         "오늘 핵심 단어는 두 개, '근거'와 '검증'입니다.")

# 1-1. 목차 --------------------------------------------------------------------
SECTIONS = [("1", "문제와 해결", "LLM은 옛 코드를 주고 틀려도 모른다 → 근거 + 검사"),
            ("2", "만든 것", "데이터 · 그래프 · 검증 11가지 · 화면 · 대화 기록"),
            ("3", "평가와 결과", "질문 30개 비교 설계 · 실제 실행 사례 · 결과"),
            ("4", "배운 것", "발견 · 한계 · 가치")]
s = new(LIGHT)
head(s, "목차", "15분 동안 이 순서로 말씀드리겠습니다")
for i, (n, t, d) in enumerate(SECTIONS):
    y = 2.05 + i * 1.12
    box(s, 0.75, y, 11.83, 0.95)
    text(s, 1.05, y + 0.18, 0.8, 0.6, n, size=28, bold=True, color=BLUE)
    text(s, 1.85, y + 0.14, 3.6, 0.5, t, size=20, bold=True)
    text(s, 5.2, y + 0.24, 7.2, 0.5, d, size=15, color=GRAY)
foot(s)
notes(s, "[0:30~0:50] 오늘은 네 부분으로 말씀드리겠습니다. 먼저 어떤 문제를 풀었는지, 다음으로 팀이 무엇을 만들었는지, "
         "그다음 어떻게 평가했고 결과가 어땠는지, 마지막으로 만들면서 배운 것을 말씀드리겠습니다.")

# 2. 문제 ----------------------------------------------------------------------
s = new(LIGHT)
head(s, "문제", "ChatGPT가 준 LangChain 코드, 실행하면 깨집니다")
box(s, 0.75, 2.0, 6.6, 3.1, fill=NAVY, line=None)
text(s, 1.05, 2.25, 6.0, 0.3, "# LLM이 흔히 주는 코드", size=13, color="8FA0B3", font=MONO)
text(s, 1.05, 2.65, 6.0, 0.8, "from langchain.chat_models import ChatOpenAI\nfrom langchain.chains import LLMChain",
     size=15, color="E8ECF1", font=MONO, spacing=1.4)
line(s, 1.05, 3.55, 7.05, 3.55, color="34445A", width=0.75)
text(s, 1.05, 3.75, 6.0, 0.3, "# LangChain 1.4.5에서 실행 결과", size=13, color="8FA0B3", font=MONO)
text(s, 1.05, 4.15, 6.0, 0.8, "ImportError: cannot import name 'ChatOpenAI'\nModuleNotFoundError: No module named 'langchain.chains'",
     size=13, color=PEACH, font=MONO, spacing=1.4)
text(s, 7.85, 2.0, 4.8, 0.5, "첫 줄부터 에러", size=22, bold=True)
text(s, 7.85, 2.5, 4.8, 1.0, "LangChain 1.0에서 패키지가 나뉘고, 옛 체인과 에이전트가 빠졌습니다.", size=17, color=GRAY, spacing=1.35)
text(s, 7.85, 3.7, 4.8, 0.5, "더 큰 문제", size=22, bold=True)
text(s, 7.85, 4.2, 4.8, 0.8, [[("LLM은 자기 답이 틀렸다는 것을 ", {}), ("모릅니다.", {"bold": True, "color": INK})]],
     size=17, color=GRAY, spacing=1.35)
foot(s)
notes(s, "[0:30~1:20] LangChain을 LLM에게 물어보면 복잡한 질문일수록 옛 버전 코드를 줍니다. 왼쪽은 그 코드를 최신 LangChain 1.4.4에서 "
         "실제로 실행한 결과입니다. 첫 줄 import부터 에러가 납니다. 1.0에서 패키지가 나뉘고 LLMChain 같은 옛 체인이 빠졌기 때문입니다. "
         "더 큰 문제는 LLM이 이 답이 틀렸다는 것을 모른다는 점입니다. 사용자가 직접 에러를 검색하며 고쳐야 합니다.")

# 3. 원인 ----------------------------------------------------------------------
s = new(LIGHT)
head(s, "원인: 버전 지체 환각", "인터넷에는 옛 버전 코드가 더 많습니다",
     sub="LLM은 데이터가 많은 쪽을 따라갑니다. 라이브러리는 빨리 바뀌어도, 학습 데이터 속 코드는 대부분 과거 버전입니다.")
for i, (n, lab, src) in enumerate([
        ("42.55%", "문서가 부족할 때, LLM 코드 중 목표 버전에서 실행되는 비율", "When LLMs Lag Behind, 2026"),
        ("66.36%", "구조화된 문서를 줘도 실행되는 비율", "When LLMs Lag Behind, 2026"),
        ("48~51%", "최신 상용 모델의 버전 지정 코드 생성 성공률", "GitChameleon 2.0, 2025")]):
    big_card(s, 0.75 + i * 4.0, 2.55, 3.75, 2.4, n, lab, src)
text(s, 0.75, 5.35, 11.8, 0.5, "→ 문서를 주는 것만으로는 부족하고, 고친 코드를 확인하는 단계가 필요합니다.", size=17, bold=True, color=BLUE)
foot(s)
notes(s, "[1:20~2:10] 이 현상을 '버전 지체 환각'이라고 부릅니다. 연구에서도 문서가 부족하면 LLM 코드의 약 43%만 목표 버전에서 실행되고, "
         "구조화된 문서를 줘도 66% 정도에 머뭅니다. 최신 상용 모델도 버전을 지정한 코드 생성은 절반 정도만 성공합니다. "
         "그래서 저희는 문서를 주는 것에서 멈추지 않고, 고친 코드를 검사하고 틀리면 다시 고치는 단계를 넣었습니다. "
         "(출처: arXiv 2604.09515, arXiv 2507.12367)")

# 4. 해결 ----------------------------------------------------------------------
s = new(LIGHT)
head(s, "해결", "근거로 고치고, 검사로 한 번 더 확인합니다")
table(s, 0.75, 2.0, 11.83, [
    ["구분", "일반 LLM", "우리 챗봇"],
    ["근거", "학습 데이터 (옛 버전이 다수)", "import · 메서드 대응표 + 최신 공식 문서 검색 (RAG)"],
    ["확인", "없음", "verifier가 LLM 없이 11가지 검사 (문법, import 존재, 남은 옛 import …)"],
    ["틀렸을 때", "모름", "실패 이유로 근거를 다시 찾고, 틀린 근거는 빼고 다시 고침 (최대 3회)"],
    ["답변", "코드만", "고친 코드 + 바뀐 줄마다 근거 출처 · 설명 + 시도 횟수 + 설치할 패키지"],
    ["버전", "대부분 최신으로만", "질문에 적은 버전으로 (적지 않으면 최신 1.4.5), 되돌리기 포함"],
], [1.9, 3.4, 6.53], size=15, row_h=0.62, first_bold=True, colors={1: GRAY})
foot(s)
notes(s, "[2:10~3:00] 해결 방법을 일반 LLM과 비교하면 이렇습니다. 첫째, 기억이 아니라 대응표와 최신 공식 문서를 근거로 고칩니다. "
         "둘째, 고친 코드를 verifier가 LLM 없이 11가지로 검사합니다. 셋째, 틀리면 실패 이유를 들고 근거를 다시 찾는데, 이미 틀린 근거는 빼고 찾습니다. "
         "최대 3번입니다. 그래서 답변에는 코드뿐 아니라 바뀐 줄마다 근거 ID와 이유, 몇 번 만에 통과했는지가 함께 나옵니다.")

# 5. 데이터 --------------------------------------------------------------------
s = new(LIGHT)
head(s, "근거 데이터 · 2번", "고칠 때 볼 근거를 미리 만들어 두었습니다")
for i, (n, lab) in enumerate([("9,155줄", "import 대응표\n옛 경로 → 1.x 경로"),
                              ("42개", "메서드 대응표\n.run() → .invoke() 등"),
                              ("295개", "공식 문서\n최신 271 · 가이드 24"),
                              ("11,945개", "검색용 조각 (청크)\nChroma Cloud + BM25")]):
    big_card(s, 0.75 + i * 3.0, 2.0, 2.8, 2.15, n, lab, num_size=32)
text(s, 0.75, 4.5, 11.8, 0.4, "출처 4가지", size=17, bold=True)
table(s, 0.75, 4.95, 11.83, [
    ["PyPI 패키지 코드", "langchain-cli 변환 규칙", "최신 공식 문서", "0.3.30 옛 마이그레이션 가이드"],
    ["버전별 도구 목록 42개", "공식 자동 변환 규칙", "임베딩: text-embedding-3-small", "옛 방식 → 새 방식 설명"],
], [2.95, 2.95, 2.95, 2.98], size=13, row_h=0.5)
foot(s, extra=" · 2026-10-15 팀 저장소 기준")
notes(s, "[3:00~3:50] 2번이 만든 근거 데이터입니다. 옛 import 경로를 1.x 경로로 잇는 대응표가 9,155줄, .run 같은 옛 메서드를 잇는 메서드 대응표가 42개 있습니다. "
         "최신 공식 문서 271개와 옛 마이그레이션 가이드 24개를 11,945개 조각으로 나눠 Chroma Cloud에 넣었고, 단어 검색 BM25와 벡터 검색을 합친 "
         "하이브리드 검색으로 찾습니다. 근거마다 imap, mmap, doc으로 시작하는 ID가 붙어서, 나중에 어떤 근거로 고쳤는지 추적할 수 있습니다.")

# 6. 시스템 구조 -----------------------------------------------------------------
s = new(LIGHT)
head(s, "시스템 구조 · 1번", "네 단계를 거치고, 실패하면 되돌아갑니다")
text(s, 0.75, 1.7, 11.8, 0.4, "질문 분류 → 코드 변환이면 아래 파이프라인 · LangChain 질문은 문서 검색으로 답 · 일반 질문은 바로 답",
     size=14, color=GRAY)
steps = [("① analyzer", "1번", "바꿀 부분 찾기"), ("② retriever", "2번", "대응표 정확 매칭\n+ 하이브리드 검색"),
         ("③ rewriter", "3번", "근거 ID를 붙여\n코드 다시 쓰기"), ("④ verifier", "3번", "LLM 없이\n11가지 검사"),
         ("결과 → 화면", "4번", "결과 패널 표시\nTiDB에 대화 저장")]
bw, gap, y0 = 2.05, 0.39, 2.35
for i, (name, who, desc) in enumerate(steps):
    x = 0.75 + i * (bw + gap)
    hl = i == 3
    box(s, x, y0, bw, 1.75, fill=BLUE if hl else WHITE, line=None if hl else LINE)
    text(s, x + 0.2, y0 + 0.18, bw - 0.4, 0.3, f"담당 {who}", size=12, color="D6E5F8" if hl else MUTED)
    text(s, x + 0.2, y0 + 0.48, bw - 0.4, 0.4, name, size=17, bold=True, color=WHITE if hl else INK)
    text(s, x + 0.2, y0 + 0.92, bw - 0.4, 0.8, desc, size=13, color="E4EEFB" if hl else GRAY, spacing=1.25)
    if i < 4:
        arrow(s, x + bw + 0.04, y0 + 0.87, x + bw + gap - 0.04, y0 + 0.87)
vx = 0.75 + 3 * (bw + gap) + bw / 2
rx = 0.75 + 1 * (bw + gap) + bw / 2
line(s, vx, y0 + 1.75, vx, 4.75, color=ORANGE, dash=True)
line(s, vx, 4.75, rx, 4.75, color=ORANGE, dash=True)
arrow(s, rx, 4.75, rx, y0 + 1.8, color=ORANGE, dash=True)
text(s, rx - 1.0, 4.85, vx - rx + 2.0, 0.4, "검증 실패 → 실패 이유 + 틀린 근거 제외로 다시 검색 (최대 3회)", size=14, bold=True,
     color=ORANGE, align=PP_ALIGN.CENTER)
text(s, 0.75, 5.75, 11.8, 0.4, "연결 · 재시도 · 질문 분류: 1번 (LangGraph)   ·   목표 버전: 질문에서 읽음 (기본 최신 1.4.5)   ·   모델: gpt-4o-mini",
     size=14, color=GRAY)
foot(s)
notes(s, "[3:50~5:00] 질문이 들어오면 먼저 질문을 분류합니다. 코드를 바꿔 달라는 요청이면 네 단계 파이프라인으로 갑니다. "
         "1번이 만든 analyzer가 코드에서 바꿀 부분을 찾고, 2번의 retriever가 대응표와 문서에서 근거를 찾습니다. "
         "3번의 rewriter가 바뀐 줄마다 근거 ID를 붙여 코드를 다시 쓰고, 핵심인 verifier가 LLM 없이 검사합니다. "
         "실패하면 실패 이유를 들고 retriever로 돌아가는데, 틀린 근거는 빼고 다시 찾습니다. 최대 3번입니다. "
         "단계 연결과 재시도 판단, 질문 분류는 1번이 LangGraph로 맡았고, 결과는 제가 만든 화면에 보여 주고 대화는 TiDB에 저장합니다. "
         "(질문 분류 연결은 마무리 중: 발표 시점 상태에 맞게 수정)")

# 7. verifier 11가지 -------------------------------------------------------------
s = new(LIGHT)
head(s, "검증 · 3번", "verifier는 LLM 없이 11가지를 검사합니다")
checks = [("1", "문법", "파이썬 문법 통과"), ("2", "근거 ID", "보여 준 근거만 썼는지"),
          ("3", "변경 기록", "기록 없는 변경 = 환각"), ("4", "남은 옛 import", "옛 경로가 남았는지"),
          ("5", "import 존재", "1.x에 그 경로가 있는지"), ("6", "남은 옛 메서드", ".run() 같은 옛 호출 (경고)"),
          ("7", "안 쓰는 import", "필요 없는 import가 남았나"), ("8", "반환값 보존", "문자열 결과를 잃지 않았나"),
          ("9", "정의 안 된 이름", "실행하면 NameError"), ("10", "출력 꺼내기", "['text'] 잘못 꺼내기"),
          ("11", "체인 입출력 키", "실제 키와 같은지")]
for i, (n, t, d) in enumerate(checks):
    col, row = i % 4, i // 4
    x, y = 0.75 + col * 3.0, 1.95 + row * 1.5
    box(s, x, y, 2.8, 1.32)
    text(s, x + 0.22, y + 0.12, 0.6, 0.4, n, size=18, bold=True, color=BLUE)
    text(s, x + 0.75, y + 0.15, 1.95, 0.4, t, size=15, bold=True)
    text(s, x + 0.22, y + 0.68, 2.4, 0.55, d, size=12, color=GRAY)
x, y = 0.75 + 3 * 3.0, 1.95 + 2 * 1.5
box(s, x, y, 2.8, 1.32, fill=NAVY, line=None)
text(s, x + 0.22, y + 0.18, 2.4, 1.0, "오류 → 다시 시도\n경고 → 결과에 표시", size=14, bold=True, color="F2F1EC", spacing=1.4)
foot(s)
notes(s, "[5:00~6:00] verifier가 이 프로젝트의 핵심입니다. 맞았는지 LLM에게 묻지 않고, 코드로 11가지를 검사합니다. "
         "문법, 근거 ID가 이번에 실제로 보여 준 근거인지, 기록 없이 바뀐 줄이 있는지(이건 환각입니다), 옛 import가 남았는지, 새 경로가 1.x에 진짜 있는지, "
         "그리고 반환값을 잃지 않았는지, 정의 안 된 이름을 쓰지 않았는지 같은 실행 오류까지 봅니다. 오류는 재시도 이유가 되고, 경고는 결과에 표시합니다. "
         "LLM에게 검증을 맡기지 않은 이유는, 검증하는 LLM도 같은 옛 지식을 갖고 있기 때문입니다.")

# 8. 화면 -----------------------------------------------------------------------
s = new(LIGHT)
head(s, "화면 · 4번", "결과와 근거를 한 화면에서 봅니다")
_shot = os.path.join(HERE, "screen_result.jpg")   # 2026-10-15 실제 화면 (확인용 예제 q11, 2회차 검증 통과)
if os.path.exists(_shot):
    _h = 4.2
    _w = _h * 800 / 500
    s.shapes.add_picture(_shot, Inches(0.75 + (7.9 - _w) / 2), Inches(2.0), Inches(_w), Inches(_h))
else:
    capture(s, 0.75, 2.0, 7.9, 4.2, "확인용 예제를 보낸 뒤 결과 패널\n(검증 통과 배지 · 원래 → 바꾼 버전 · 전후 비교 빨강 · 초록)")
feats = [("말로 부탁", "\"0.2로 되돌려 줘\" · 버전 선택 상자 없음"),
         ("진행 과정 상세", "근거 · 바뀐 줄 · 검사 이유, 답 위에 남김"),
         ("결과 패널", "전후 비교 · 변경 사항 · 근거 · 검사 결과"),
         ("코드 받기 · 다시 시도", ".py · 변경 리포트 .md · 실패 시 버튼 하나로"),
         ("대화 맥락 · 저장", "앞 대화 기억 · TiDB 저장 · 예제 30개")]
for i, (t, d) in enumerate(feats):
    y = 2.0 + i * 0.84
    line(s, 8.95, y, 12.58, y, color="D4D3CC", width=1)
    text(s, 8.95, y + 0.1, 3.63, 0.4, t, size=15, bold=True, color=BLUE if i in (1, 2) else INK)
    text(s, 8.95, y + 0.44, 3.63, 0.4, d, size=12, color=GRAY)
foot(s)
notes(s, "[6:00~7:00] 제가 맡은 화면입니다. 아이디로 들어오면 ChatGPT처럼 왼쪽에 대화 목록이 있고, '새 대화'를 누를 때마다 세션이 하나 생깁니다. "
         "위에서 지금 코드 버전과 바꿀 버전을 고르고 코드를 보내면, 오른쪽 결과 패널에 검증 배지, 고치기 전과 후, 바뀐 줄마다 근거 ID와 바꾼 이유가 나옵니다. "
         "근거가 부족해서 못 바꾼 줄과 새로 설치해야 할 패키지도 알려 줍니다. 사이드바의 확인용 예제 30개로 바로 시험해 볼 수 있습니다.")

# 9. DB -------------------------------------------------------------------------
s = new(LIGHT)
head(s, "대화 기록 · 4번", "TiDB에 사용자와 대화를 저장합니다")
def entity(x, y, name, rows):
    box(s, x, y, 4.2, 0.55 + 0.42 * len(rows), fill=WHITE, line=BLUE)
    box(s, x, y, 4.2, 0.55, fill=BLUE, line=None)
    text(s, x + 0.25, y + 0.12, 3.7, 0.35, name, size=16, bold=True, color=WHITE)
    for i, (col, typ, mark) in enumerate(rows):
        yy = y + 0.65 + i * 0.42
        text(s, x + 0.25, yy, 1.6, 0.35, col, size=13, bold=bool(mark), font=MONO)
        text(s, x + 1.85, yy, 1.4, 0.35, typ, size=11, color=GRAY, font=MONO)
        text(s, x + 3.25, yy, 0.8, 0.35, mark, size=11, bold=True, color=ORANGE)
entity(0.75, 2.0, "users", [("uuid", "VARCHAR(36)", "PK"), ("user_id", "VARCHAR(100)", "UNIQUE"),
                             ("created_at", "DATETIME", "")])
entity(5.6, 2.0, "chat_history", [("uuid", "VARCHAR(36)", "PK"), ("user_id", "VARCHAR(100)", "FK"),
                                   ("session_id", "VARCHAR(100)", "IDX"), ("question", "TEXT", ""),
                                   ("answer", "TEXT", ""), ("created_at", "DATETIME", "IDX")])
arrow(s, 4.95, 3.27, 5.6, 3.27, color=BLUE, width=2)
text(s, 4.9, 2.85, 0.8, 0.35, "1 : N", size=12, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
pts = [("아이디 중복 검사", "가입 전 확인 + UNIQUE"),
       ("질문 + 답 = 한 행", "새 대화 = 새 session_id"),
       ("목록 · 다시 열기", "session_id로 묶고 시간순으로"),
       ("키가 없을 때", "로컬 저장으로 넘어가고 이유 표시")]
for i, (t, d) in enumerate(pts):
    y = 2.0 + i * 1.0
    text(s, 10.15, y, 2.5, 0.4, t, size=14, bold=True)
    text(s, 10.15, y + 0.37, 2.5, 0.55, d, size=11, color=GRAY)
foot(s)
notes(s, "[7:00~7:50] 대화 기록은 TiDB에 저장합니다. 팀에서 정한 ERD대로 테이블은 두 개입니다. users에는 아이디가 중복 없이 들어가고, "
         "chat_history에는 질문 하나와 그 답이 한 행으로 들어갑니다. '새 대화'를 누르면 새 session_id가 생기고, 대화 목록은 session_id로 묶어 보여 줍니다. "
         "아이디는 가입 전에 중복을 검사하고, 동시에 가입하는 경우도 DB의 UNIQUE가 한 번 더 막습니다. TiDB에 연결할 수 없으면 화면이 멈추지 않고 "
         "로컬 저장으로 넘어가면서 이유를 보여 줍니다.")

# 10. 실험 설계 -----------------------------------------------------------------
s = new(LIGHT)
head(s, "실험 설계 · 4번", "같은 질문 30개, 같은 조건으로 비교합니다")
cards = [("1.x로 올리기 30개", "10가지 유형 × 3: import 경로 · 로더 · 임베딩 · LLMChain → LCEL ·\n체인 조합 · RAG · 메모리 · 에이전트 · 출력 파서 · 실무 상황"),
         ("난이도", "쉬움 7 · 중간 15 · 어려움 8\n실제 사용자처럼 '요청 문장 + 옛 코드'로 구성"),
         ("미리 확인 (36/36)", "옛 코드가 1.x에서 깨지는지, 기대 import가 되는지\n+ 버전 오가기 6개 (되돌리기 · 중간 단계)")]
for i, (t, d) in enumerate(cards):
    y = 2.0 + i * 1.45
    box(s, 0.75, y, 5.6, 1.3)
    text(s, 1.0, y + 0.15, 5.1, 0.4, t, size=17, bold=True)
    text(s, 1.0, y + 0.55, 5.1, 0.75, d, size=12, color=GRAY, spacing=1.25)
table(s, 6.7, 2.0, 5.88, [
    ["항목", "규칙"],
    ["비교 대상", "일반 LLM vs 우리 챗봇"],
    ["모델", "양쪽 같은 gpt-4o-mini, temperature 0"],
    ["입력", "같은 요청 문장 + 같은 코드"],
    ["채점", "LLM 없이 코드로, 공통 기준 8가지"],
    ["최대 시도", "3회 (우리 챗봇)"],
    ["지표", "공통 기준 통과율 · 재시도 효과 · 자체 평가"],
], [1.7, 4.18], size=14, row_h=0.56, first_bold=True)
foot(s)
notes(s, "[7:50~8:50] 평가는 공정하게 비교하려고 규칙을 먼저 정했습니다. 실제 사용자가 보낼 법한 요청 문장과 옛 코드로 1.x로 올리는 질문 30개를 만들었습니다. "
         "10가지 유형마다 3개씩이고, 쉬움 7, 중간 15, 어려움 8입니다. 30개 모두 옛 코드가 1.x에서 실제로 깨지는지, 기대하는 답의 import가 실제로 되는지 미리 확인했습니다. "
         "일반 LLM과 우리 챗봇은 같은 모델, 같은 입력을 쓰고, 채점은 verifier와 같은 기준으로 합니다. 지표는 검증 통과율, 바뀐 줄에 근거가 붙은 비율, "
         "재시도로 오른 통과율 세 가지입니다.")

# 11. 실제 실행 사례 --------------------------------------------------------------
s = new(NAVY)
head(s, "실제 실행 · 2026-10-14", "LLMChain 코드가 3회차에 통과했습니다", dark=True)
code_box(s, 0.75, 2.0, 5.7, 2.6, "변경 전 (옛 코드)",
         "from langchain.chat_models import ChatOpenAI\nfrom langchain.prompts import PromptTemplate\n"
         "from langchain.chains import LLMChain\n\nllm = ChatOpenAI(temperature=0)\n"
         "chain = LLMChain(llm=llm, prompt=PromptTemplate\n    .from_template('{word}의 반대말은?'))\nprint(chain.run(word='크다'))", PEACH)
code_box(s, 6.88, 2.0, 5.7, 2.6, "변경 후 (팀 그래프 결과)",
         "from langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import PromptTemplate\n"
         "from langchain_core.output_parsers import StrOutputParser\n\nllm = ChatOpenAI(temperature=0)\n"
         "chain = PromptTemplate.from_template(\n    '{word}의 반대말은?') | llm | StrOutputParser()\nprint(chain.invoke({'word': '크다'}))", SKY)
for i, (n, t) in enumerate([("3회", "검사 통과까지 시도"), ("6줄", "바뀐 줄 모두 근거 ID\n(imap · mmap · doc)"),
                             ("0줄", "근거 부족으로 못 바꾼 줄"), ("약 1분", "한 번 변환에 걸린 시간")]):
    x = 0.75 + i * 2.98
    box(s, x, 4.85, 2.78, 1.45, fill=NAVY2, line=None)
    text(s, x + 0.25, 4.95, 2.3, 0.6, n, size=26, bold=True, color=SKY if i != 3 else PEACH)
    text(s, x + 0.25, 5.55, 2.3, 0.7, t, size=12, color="B9C3CF", spacing=1.25)
foot(s, dark=True, extra=" · 화면 캡처는 9장 · 같은 코드를 두 번 실행해 두 번 모두 3회차 통과")
notes(s, "[8:50~10:00] 실제로 돌린 결과입니다. 왼쪽은 0.0.300 시절의 LLMChain 코드입니다. 오른쪽이 팀 그래프가 고친 코드인데, "
         "LLMChain이 prompt | llm | StrOutputParser() 형태의 최신 방식으로 바뀌었고 .run은 .invoke로 바뀌었습니다. "
         "1회차와 2회차는 verifier 검사에 걸렸고, 실패 이유를 들고 근거를 다시 찾아 3회차에 통과했습니다. 바뀐 6줄 모두에 근거 ID가 붙었습니다. "
         "다만 검사와 재시도 때문에 한 번 변환에 1분 정도 걸립니다. [데모 캡처를 넣는다면 9장 결과 패널 캡처를 다시 보여 주기]")

# 11-1. 최상위 그래프 세 갈래 (10-15) ------------------------------------------------
s = new(LIGHT)
head(s, "실제 실행 · 2026-10-15", "질문 하나로, 알아서 세 갈래로 답합니다")
rows3 = [("일반 질문", "\"안녕하세요\"", "2.5초", "일반 답변", "2E7D32"),
         ("LangChain 질문", "\"0.3 → 1.0, LLMChain은 어떻게 바뀌었어?\"", "12.5초", "문서를 찾아 설명", "2E7D32"),
         ("코드 변환 · 최신", "옛 코드 + \"최신으로 바꿔 줘\"", "16초", "목표 1.4.5 · 1회 만에 통과", "2E7D32"),
         ("코드 변환 · 되돌리기", "새 코드 + \"0.2에서 돌아가게\"", "28초", "목표 0.2.17 · 3회 모두 실패", ORANGE)]
for i, (k, q, t, r, c) in enumerate(rows3):
    y = 2.0 + i * 0.98
    box(s, 0.75, y, 7.7, 0.82)
    text(s, 1.0, y + 0.13, 2.4, 0.3, k, size=15, bold=True)
    text(s, 1.0, y + 0.45, 4.6, 0.3, q, size=11, color=GRAY)
    text(s, 5.0, y + 0.13, 0.9, 0.3, t, size=14, bold=True, color=BLUE)
    text(s, 5.9, y + 0.13, 2.4, 0.6, r, size=12, color=c, spacing=1.2)
box(s, 8.75, 2.0, 3.83, 3.76, fill=NAVY, line=None)
text(s, 9.0, 2.15, 3.4, 0.3, "화면 진행 표시 (실제 기록)", size=12, bold=True, color=SKY)
text(s, 9.0, 2.55, 3.4, 3.1,
     "✓ 질문 종류: 코드 변환\n✓ ① 바꿀 부분 3곳 · 목표 1.4.5\n✓ ② 근거 9개\n✓ ③ 5곳 고침\n✓ ④ 1회차 실패 → 다시\n✓ ② 근거 14개\n✓ ③ 6곳 고침\n✓ ④ 검사 통과 (2회차)",
     size=12, color="E8ECF1", font=MONO, spacing=1.45)
foot(s, extra=" · 화면 → 최상위 그래프(supervisor) 연결 후 시험")
notes(s, "")

# 12. 결과 ----------------------------------------------------------------------
s = new(LIGHT)
head(s, "결과 · 1.x로 올리기 30개", "같은 모델인데, 57% 대 0%입니다")
text(s, 0.75, 2.05, 4.2, 0.4, "우리 챗봇 · 공통 기준 통과", size=15, bold=True, color=BLUE)
text(s, 0.75, 2.45, 4.2, 1.0, "57%", size=60, bold=True, color=BLUE)
text(s, 0.75, 3.5, 4.2, 0.4, "정답 import 빼고 '실행 기준'이면 87%", size=12.5, color=GRAY)
text(s, 0.75, 4.05, 4.2, 0.4, "일반 LLM · 공통 기준 통과", size=15, bold=True, color=ORANGE)
text(s, 0.75, 4.45, 4.2, 1.0, "0%", size=60, bold=True, color=ORANGE)
text(s, 0.75, 5.5, 4.2, 0.7, "30개 중 29개가 옛 import 그대로인데\n\"1.x에 맞게 수정했다\"고 답함", size=12.5, color=GRAY, spacing=1.3)
bar_chart(s, 5.3, 1.95, 7.28, 4.55,
          ["옛 import 없음", "import 실제 존재", "정답 import 포함", "실행 기준 통과", "공통 기준 통과"],
          [("우리 챗봇", [0.93, 0.90, 0.60, 0.87, 0.57]), ("일반 LLM", [0.03, 0.03, 0.0, 0.0, 0.0])])
foot(s, extra=" · gpt-4o-mini · temperature 0 · LLM 없이 코드로 채점 · 2026-10-15")
notes(s, "[10:00~11:00] 결과입니다. 검증 통과율은 일반 LLM이 [__]%, 우리 챗봇이 [__]%였습니다. 특히 [__] 유형에서 차이가 가장 컸습니다. "
         "우리 챗봇이 바꾼 줄 중 [__]%에 근거 ID가 붙었습니다. [실험 결과를 보고 제목과 설명 수정]")

# 13. 재시도 효과 ----------------------------------------------------------------
s = new(LIGHT)
head(s, "검증 루프 효과", "다시 고쳐서 +10%p, 실패는 숨기지 않습니다")
column_chart(s, 0.75, 1.95, 7.4, 4.5, ["1회차까지", "2회차까지", "3회차까지"],
             [("검증 통과 (누적)", [0.43, 0.53, 0.53])])
for i, (lab, val, c) in enumerate([("1회차 → 최종 검증 통과", "43 → 53%", BLUE), ("통과한 답의 평균 시도", "1.2회", INK),
                                   ("바뀐 줄에 근거가 붙은 비율", "93%", INK)]):
    y = 2.0 + i * 1.5
    line(s, 8.6, y, 12.58, y, color="D4D3CC", width=1)
    text(s, 8.6, y + 0.15, 4.0, 0.4, lab, size=15, color=GRAY)
    text(s, 8.6, y + 0.55, 4.0, 0.8, val, size=40, bold=True, color=c)
foot(s)
notes(s, "[11:00~11:50] 첫 시도만 보면 통과율이 [__]%인데, 실패 이유로 근거를 다시 찾아 고치면 최종 [__]%까지 올라갑니다. "
         "확인하고 다시 고치는 루프가 [__]%p를 만들었습니다. 앞에서 본 LLMChain 사례도 1회차에는 실패했다가 3회차에 통과한 경우입니다.")

# 14. 발견 ----------------------------------------------------------------------
s = new(LIGHT)
head(s, "실험이 알려 준 약점", "약점도 숫자로 찾았고, 고칠 곳도 정했습니다")
finds = [("질문 분류", "고쳐 달라면서 에러 이유도 물으면 설명만 하고 끝남 (30개 중 6개).\n→ 분류 규칙 보강 · 온도 0",
          "1번 · 분류 확인 3회 모두 같음"),
         ("환각 · 근거 누락", "실패 원인 1위 '기록 없는 변경'. 그래도 검사기가 막아 통과는 못 함.\n→ 프롬프트 강화 · 틀린 근거 제외",
          "3번 · 1번"),
         ("검사기 빈틈", "['text'] 꺼내기는 평가 직후 3번이 고침 ✅. 0.x 되돌리기를 1.x 기준으로 검사하는 건 남음.\n→ 목표 버전별 도구 목록으로",
          "3번 · 2번 (데이터는 이미 있음)"),
         ("옛 창고 우회", "최신 방식 대신 langchain_classic으로 우회 3개. 실행은 되지만 지원 종료 예정.\n→ 대안 문서 함께 검색 · 안내",
          "2번 · 3번")]
for i, (t, d, src) in enumerate(finds):
    x = 0.75 + i * 2.99
    box(s, x, 2.0, 2.84, 3.6, fill="EAF2FC" if i == 1 else WHITE, line=BLUE if i == 1 else LINE)
    text(s, x + 0.25, 2.2, 2.4, 0.8, t, size=17, bold=True, color=BLUE if i == 1 else INK, spacing=1.15)
    text(s, x + 0.25, 3.0, 2.4, 2.0, d, size=12.5, color=GRAY, spacing=1.4)
    text(s, x + 0.25, 5.1, 2.4, 0.4, src, size=10, color=MUTED)
foot(s)
notes(s, "[11:50~12:40] 만들면서 예상하지 못한 것을 세 가지 발견했습니다. 첫째, langchain-community는 import만 해도 지원 종료 경고가 나옵니다. "
         "둘째, 옛 체인을 langchain_classic에서 가져오면 import는 되지만 최신 방식은 아닙니다. 그래서 대응표와 화면에서 '옛 창고'로 따로 표시했습니다. "
         "셋째, 버전 되돌리기를 만들며 버전별 도구 목록을 비교해 보니 0.0.300부터 0.3.30까지는 자주 쓰는 경로가 거의 같았습니다. "
         "크게 바뀌는 것은 1.x와의 사이입니다.")

# 15. 한계 ----------------------------------------------------------------------
s = new(LIGHT)
head(s, "자체 평가 · 다음 단계", "자체 평가 83점, 약한 곳부터 고칩니다")
table(s, 0.75, 2.0, 11.83, [
    ["영역 (팀이 정한 규칙 21가지)", "점수", "다음 단계 (우선순위 순)"],
    ["분석 · 근거 검색 · 답변 규칙 · 안정성", "98~100%", "유지 (목표 달성)"],
    ["질문 분류", "14.0 / 15", "① 고쳐 달라는 말이 있으면 코드 변환으로 분류"],
    ["고쳐 쓰기 (환각 · 근거 누락)", "22.3 / 25", "② 없던 줄 금지 명시 · 틀린 근거는 다음 시도에서 빼기"],
    ["검증 · 재시도", "17.3 / 30", "③ 목표 버전별 검사 · 실행 테스트 (['text'] 검사 ✅)"],
], [4.3, 1.5, 6.03], size=14.5, row_h=0.66)
text(s, 0.75, 5.55, 11.83, 0.7, "한계: 질문마다 1회 실행 · 코드는 실행하지 않고 정적으로 확인 · 질문 30개는 팀이 직접 구축 (실사용 코드로 확장 예정)",
     size=12.5, color=GRAY)
foot(s)
notes(s, "[12:40~13:30] 한계도 말씀드리겠습니다. 가장 큰 한계는 통과가 곧 정답은 아니라는 점입니다. 코드를 11가지로 검사하지만, 실행 결과까지 맞는지는 "
         "확인하지 못합니다. 또 다시 쓰기는 1.x로 올리는 쪽이 중심이라, 옛 버전으로 되돌리기는 지금 화면 쪽에서 임시로 처리합니다. "
         "검사와 재시도 때문에 한 번에 1분 정도 걸리는 것도 개선할 점입니다. 다음 단계로 가짜 LLM을 넣은 실행 테스트, 목표 버전 전달, "
         "테스트셋과 대상 라이브러리 확장을 생각하고 있습니다.")

# 16. 가치 ----------------------------------------------------------------------
s = new(BLUE)
text(s, 0.75, 0.62, 11.8, 0.3, "가치", size=13, bold=True, color="D6E5F8")
text(s, 0.75, 1.0, 11.8, 1.8, "라이브러리가 바뀔 때마다,\n근거와 함께 확인된 코드", size=42, bold=True, color=WHITE, spacing=1.1)
for i, (t, d) in enumerate([("시간 절감", "에러를 하나씩 검색하는 대신, 근거가 붙은 답을 바로 확인"),
                            ("신뢰", "같은 모델로 0% → 57%. 바뀐 줄의 93%에 근거, 실패하면 실패라고 알림"),
                            ("확장", "대응표 · 문서 · 검사 기준만 바꾸면 다른 라이브러리에도 적용")]):
    x = 0.75 + i * 4.0
    line(s, x, 4.7, x + 3.75, 4.7, color="8DB6EA", width=1.5)
    text(s, x, 4.9, 3.75, 0.45, t, size=19, bold=True, color=WHITE)
    text(s, x, 5.4, 3.75, 0.9, d, size=14, color="E4EEFB", spacing=1.35)
text(s, 0.75, 6.92, 11.8, 0.3, f"LangChain 마이그레이션 도우미 · {page[0]}", size=11, color="D6E5F8")
notes(s, "[13:30~14:15] 가치를 세 가지로 정리하겠습니다. 첫째, 개발자가 버전 에러를 하나씩 검색하는 시간을 줄여 줍니다. "
         "둘째, 바뀐 줄마다 근거와 이유, 검사 결과가 붙어 있어서 믿고 쓸 수 있습니다. 셋째, 구조가 대응표와 문서, 검사 기준에만 의존해서 "
         "빠르게 바뀌는 다른 라이브러리에도 그대로 적용할 수 있습니다.")

# 17. 팀 · 마무리 -----------------------------------------------------------------
s = new(NAVY)
text(s, 0.75, 0.62, 11.8, 0.3, "팀", size=13, bold=True, color=SKY)
team = [("1번", "그래프 · 백엔드", "최상위 그래프 · 질문 분류\nanalyzer · 재시도 판단",
         "해결: 노드 간 필드 · 분기 키 통일"),
        ("2번", "데이터 · 검색", "대응표 · 청킹 · Chroma\n하이브리드 검색 · 목표 버전 판정",
         "해결: 133MB 벡터 DB → Chroma Cloud"),
        ("3번", "변환 · 검증", "State · rewriter\nverifier 11가지 검사",
         "해결: 옛 근거 ID 복사 · import 오탐 차단"),
        ("4번", "화면 · DB · 평가 · 발표", "Streamlit 화면 · TiDB\n진행 표시 · 평가 도구",
         "해결: 배포 Secrets · 공정한 채점")]
for i, (n, t, d, fix) in enumerate(team):
    x = 0.75 + i * 3.0
    box(s, x, 1.05, 2.8, 2.6, fill=NAVY2, line=None)
    text(s, x + 0.25, 1.2, 2.3, 0.3, f"{n} · [이름]", size=12, color="8A9AAD")
    text(s, x + 0.25, 1.55, 2.3, 0.45, t, size=16, bold=True, color="F2F1EC")
    text(s, x + 0.25, 2.05, 2.3, 0.8, d, size=12, color="B9C3CF", spacing=1.3)
    text(s, x + 0.25, 2.95, 2.3, 0.6, fix, size=11, color=SKY, spacing=1.25)
text(s, 0.75, 4.6, 11.8, 1.1, "감사합니다", size=54, bold=True, color="F2F1EC")
text(s, 0.75, 5.8, 11.8, 0.4, "질문 받겠습니다", size=17, color="B9C3CF")
text(s, 0.75, 6.25, 11.8, 0.6, "팀 저장소 github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-3rd-4Team\n"
                              "배포 langchain-migration-assistant-btn5chcr8ragnwts68rmhf.streamlit.app", size=13, color="8A9AAD", spacing=1.3)
notes(s, "[14:15~15:00] 저희 팀은 이렇게 역할을 나눠 진행했습니다. 감사합니다. 질문 받겠습니다. "
         "[예상 질문] 통과하면 정답인가 → 16장 한계, 11가지 코드 검사까지 / 30개로 충분한가 → 유형 · 난이도별 경향 확인이 목적 / "
         "왜 LLM에게 검증을 맡기지 않았나 → 검증 LLM도 같은 옛 지식 / 근거를 지어낼 수 있지 않나 → verifier가 이번에 보여 준 근거 ID만 인정 / "
         "왜 1분이나 걸리나 → 검사 실패 시 최대 3회 다시 고치기 때문, 개선 예정 / 대화 기록은 어디에 → TiDB users · chat_history")

# 부록 (질문 받을 때 · 발표 시간에 포함 안 함) ------------------------------------------
def appendix_head(s, no, title):
    text(s, 0.75, 0.62, 11.8, 0.3, f"부록 {no} · 질문 대응용", size=13, bold=True, color=BLUE)
    text(s, 0.75, 0.95, 11.8, 0.8, title, size=30, bold=True)
    text(s, 0.75, 6.92, 11.8, 0.3, "LangChain 마이그레이션 도우미 · 부록 · 자세히: docs/프로젝트_최종_보고서.md", size=11, color=MUTED)


# 부록 1. LLM + RAG 파이프라인
s = new(LIGHT)
appendix_head(s, 1, "LLM + RAG 파이프라인 한 장 정리")
text(s, 0.75, 1.85, 6, 0.35, "오프라인: 근거 만들기 (2번, 1회)", size=14, bold=True, color=BLUE)
off = [("PyPI 코드\n도구 목록 42개\n+ CLI 규칙 2,650", 0.75), ("import 대응표 9,155\n메서드 대응표 42", 3.15),
       ("문서 271 + 옛 가이드 24\nMDX 정리 · 제목 분할", 5.55), ("청크 11,945\n최대 4,000자", 7.95),
       ("임베딩 1536\n→ Chroma Cloud", 10.35)]
for i, (t, x) in enumerate(off):
    box(s, x, 2.25, 2.2, 1.0)
    text(s, x + 0.12, 2.32, 1.96, 0.9, t, size=11.5, spacing=1.2, align=PP_ALIGN.CENTER)
    if i < len(off) - 1:
        arrow(s, x + 2.2, 2.75, x + 2.4, 2.75)
text(s, 0.75, 3.5, 6, 0.35, "온라인: 질문 하나 (1 · 2 · 3번)", size=14, bold=True, color=BLUE)
on = [("classifier\nmigration · search\n· general", "LLM · 1번", 0.75), ("① analyzer\n코드 · 목표 버전\n바꿀 부분 (JSON)", "LLM temp 0 · 1번", 3.15),
      ("② retriever\n정확 매칭 → 메서드\n→ 유사 → 하이브리드", "RRF k=60 · 상위 5 · 2번", 5.55),
      ("③ rewriter\n근거만 써서 다시 쓰기\n줄마다 근거 ID", "LLM temp 0 · 구조화 · 3번", 7.95),
      ("④ verifier\nLLM 없이 11가지\n실패 → ② (최대 3회)", "검사만 · 3번", 10.35)]
for i, (t, tag, x) in enumerate(on):
    box(s, x, 3.9, 2.2, 1.25, fill=NAVY if i == 4 else WHITE, line=None if i == 4 else LINE)
    text(s, x + 0.12, 3.97, 1.96, 0.95, t, size=11.5, spacing=1.2, align=PP_ALIGN.CENTER,
         color="F2F1EC" if i == 4 else INK)
    text(s, x, 5.2, 2.2, 0.3, tag, size=10, color=MUTED, align=PP_ALIGN.CENTER)
    if i < len(on) - 1:
        arrow(s, x + 2.2, 4.5, x + 2.4, 4.5)
text(s, 0.75, 5.7, 11.8, 0.9, "State 하나로 전달: old_code · analysis · target_version → evidences · shown_evidence_ids → new_code · changes(근거 ID) · unresolved\n"
                             "→ verify_result · attempt · exclude_ids(틀린 근거 누적) → 화면 결과 패널 · TiDB", size=12, color=GRAY, spacing=1.35)
notes(s, "")

# 부록 2. 파일 구조
s = new(LIGHT)
appendix_head(s, 2, "파일 구조와 담당")
table(s, 0.75, 1.85, 11.83, [
    ["경로", "하는 일", "담당"],
    ["src/graph/supervisor.py · migration.py", "최상위 그래프(분류 → 세 갈래) · 변환 파이프라인(재시도)", "1번"],
    ["src/graph/nodes/ classifier · general · analyzer", "질문 분류 · 일반 답 · 바꿀 부분 찾기", "1번"],
    ["src/rag/ docs_collect · import_map · chunking · embedding · retrieval", "문서 수집 · 대응표 · 목표 버전 판정 · 청킹 · Chroma · 하이브리드 검색", "2번"],
    ["src/graph/nodes/ retriever · search", "근거 검색 · LangChain 질문 답변", "2번"],
    ["src/graph/state.py · nodes/ rewriter · verifier", "State · 근거를 붙여 다시 쓰기 · 11가지 검사", "3번"],
    ["streamlit_app.py · src/ui/", "화면 · 그래프 호출 · 진행 표시 · 결과 패널 · TiDB", "4번"],
    ["eval/ · tools/bot_check.py · docs/", "평가 질문 · 실행 · 채점 · 화면 점검 · 보고서", "4번"],
    ["data/raw · data/processed", "도구 목록 42 · 문서 · 대응표 9,155 · 청크 11,945", "2번"],
], [5.0, 5.73, 1.1], size=12.5, row_h=0.52)
notes(s, "")

# 부록 3. 역할별 트러블슈팅
s = new(LIGHT)
appendix_head(s, 3, "역할별로 막혔던 것과 푼 방법")
probs = [("1번 · 그래프", ["analyzer 출력 필드 불일치 → 다음 단계 필드에 맞춤 (PR #7)",
                          "분기 키 불일치 → general · search · migration 통일 (PR #14)",
                          "LLM이 코드펜스로 감쌈 → 후처리",
                          "목표 버전 해석 불가 → 최신 1.4.5로"]),
         ("2번 · 데이터 · 검색", ["133MB 로컬 DB → Chroma Cloud (PR #10)",
                                 "re-export · pydantic_v1 경로 → 정의부 추적 · 모듈 매핑",
                                 "같은 메서드 이름 여러 클래스 → 질의 단서로 순위",
                                 "다운그레이드 파트너 패키지 → 판정 수정 (PR #13)"]),
         ("3번 · 변환 · 검증", ["옛 근거 ID 복사 → 보여 준 근거만 인정",
                               "venv에서 정상 경로도 import 실패 → 정적 심볼 검사",
                               "검증 통과 후 실행 실패 → 9 · 10 · 11번 검사 추가",
                               "구조화 출력 누락 → 재시도 · rewrite_failed"]),
         ("4번 · 화면 · 평가", ["app.py 충돌 → streamlit_app.py 분리",
                               "배포 키 오류 → Secrets 먼저 읽기 · 성공만 캐시",
                               "1분 대기 → 진행 단계 실시간 표시",
                               "공정한 비교 → LLM 없는 공통 채점 8항목"])]
for i, (t, items) in enumerate(probs):
    x = 0.75 + i * 2.99
    box(s, x, 1.85, 2.84, 4.75)
    text(s, x + 0.2, 2.0, 2.45, 0.4, t, size=15, bold=True, color=BLUE)
    text(s, x + 0.2, 2.5, 2.45, 4.0, "\n\n".join(items), size=11.5, color=GRAY, spacing=1.3)
notes(s, "")

# 진행 바 + 섹션 표시 (표지 · 목차 · 마무리 · 부록 제외) ----------------------------------------
SECTION_OF = {3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 2, 12: 2, 13: 2, 14: 2, 15: 2, 16: 3, 17: 3, 18: 3}
total = 19   # 본편 장 수 (부록은 진행 바에서 뺌)
for no, sl in enumerate(prs.slides, start=1):
    if no not in SECTION_OF:
        continue
    dark = no in (12,)
    blue_bg = no == 18
    track = "34445A" if dark else ("4A80C4" if blue_bg else "E1E0D9")
    fill = SKY if dark else (WHITE if blue_bg else BLUE)
    bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.44), prs.slide_width, Inches(0.06))
    bar.fill.solid(); bar.fill.fore_color.rgb = rgb(track); bar.line.fill.background()
    done = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.44),
                               int(prs.slide_width * no / total), Inches(0.06))
    done.fill.solid(); done.fill.fore_color.rgb = rgb(fill); done.line.fill.background()
    k = SECTION_OF[no]
    label = "   ".join((f"● {SECTIONS[i][1]}" if i == k else SECTIONS[i][1]) for i in range(4))
    text(sl, 6.6, 0.62, 6.0, 0.3, label, size=10, color=("8A9AAD" if dark else ("D6E5F8" if blue_bg else MUTED)),
         align=PP_ALIGN.RIGHT)

# 대본 (script_v4.py) 을 노트로 ------------------------------------------------------
sys.path.insert(0, HERE)
from script_v4 import SCRIPT  # noqa: E402
assert len(SCRIPT) == len(prs.slides), (len(SCRIPT), len(prs.slides))
for sl, (tm, scr, hook, body, bridge) in zip(prs.slides, SCRIPT):
    sl.notes_slide.notes_text_frame.text = (f"[{tm}]  화면: {scr}\n훅: {hook}\n\n{body}" +
                                            (f"\n\n→ 넘기는 말: {bridge}" if bridge else ""))

prs.save(OUT)
print("저장:", OUT, "슬라이드", len(prs.slides))
