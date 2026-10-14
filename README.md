# LangChain 버전 마이그레이션 코드 어시스턴트

옛 버전 LangChain 코드를 넣고 바꿀 버전을 고르면, **그 버전에서 돌아가는 코드로 고쳐 주고 정말 돌아가는지 검사까지 하는 챗봇**입니다.
바뀐 줄마다 근거 ID(대응표 `imap-…`, 메서드 대응표 `mmap-…`, 문서 `doc-…`)가 붙고, 검사에 실패하면 근거를 다시 찾아 최대 3번 고칩니다.

> SKN35 3rd 4Team 팀 프로젝트의 배포용 저장소입니다. 개발은 팀 저장소 [SKNETWORKS-FAMILY-AICAMP/SKN35-3rd-4Team](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-3rd-4Team) 에서 하고, 이 저장소는 그 `sungwook` 브랜치(2026-10-14)를 배포용으로 옮긴 것입니다.

## 구조

```text
Streamlit 화면 (streamlit_app.py)  ─ 로그인 · 대화 목록 · 버전 선택 · 결과 패널 · 확인용 예제 30개
   │  src/ui/client.py → migration_pipeline().invoke({"question": ...})
   ▼
LangGraph:  analyzer → retriever → rewriter → verifier ──통과──▶ 결과
                          ▲                      │
                          └── 실패 이유 · 틀린 근거 제외 ┘ (최대 3회)
대화 기록: TiDB (users, chat_history)
```

| 담당 | 영역 |
|---|---|
| 1번 | 그래프 · 백엔드 (LangGraph 연결, analyzer, 재시도 판단) |
| 2번 | 데이터 · 검색 (import · 메서드 대응표, 청킹, Chroma, 하이브리드 검색, retriever) |
| 3번 | 변환 · 검증 (State, rewriter, verifier 8가지 검사) |
| 4번 | 화면 · DB · 평가 (Streamlit 화면, TiDB 대화 기록, 실무형 질문 36개, 발표) |

## 실행

```powershell
pip install -r requirements.txt
```

```powershell
streamlit run streamlit_app.py
```

비밀 값은 `.env`(내 컴퓨터) 또는 `.streamlit/secrets.toml`(배포)에 넣습니다. 형식은 `.streamlit/secrets.toml.example`.

| 값 | 없으면 |
|---|---|
| `OPENAI_API_KEY`, `CHROMA_API_KEY`, `CHROMA_TENANT`, `CHROMA_DATABASE` | 팀 그래프 대신 화면 쪽 임시 결과 (사이드바에 이유 표시) |
| TiDB (`TIDB_*` 또는 `[tidb]`) | 앱 안 SQLite 에 저장 |

## 배포 (Streamlit Cloud)

1. share.streamlit.io → **Create app** → 이 저장소, 브랜치 `main`, Main file path `streamlit_app.py`
2. Advanced settings → Python **3.12**, Secrets 에 `.streamlit/secrets.toml.example` 내용을 값만 바꿔 붙여 넣기
3. Deploy

## 문서

| 문서 | 내용 |
|---|---|
| [docs/화면_실행방법.md](docs/화면_실행방법.md) | 화면 실행 · 설정 · 자동 점검 |
| [docs/DB_설계.md](docs/DB_설계.md) | ERD (users, chat_history) |
| [eval/README.md](eval/README.md) | 실무형 질문 36개 (확인용 예제 30개 포함) |
