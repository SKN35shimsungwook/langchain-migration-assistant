import sys
body = open("README_body.md", encoding="utf-8").read()
TITLE = """# LangChain 버전 마이그레이션 코드 어시스턴트

> 옛 버전 LangChain 코드를 넣고 바꿀 버전을 고르면, **그 버전에서 돌아가는 코드로 고쳐 주고 정말 돌아가는지 검사까지 하는** 코드 마이그레이션 챗봇

**문서 근거**(import · 메서드 대응표, 최신 공식 문서 검색)로 고치고, **검사 근거**(verifier 11가지, LLM 없이)로 확인합니다.
검사에 실패하면 실패 이유를 들고 근거를 다시 찾아 최대 3번 고칩니다. 바뀐 줄마다 근거 ID가 붙습니다.
"""
INFO = """| | |
|---|---|
| 과제 주제 | LLM을 연동한 내외부 문서 기반 질의응답 시스템 |
| 팀 | SKN35 3rd 4Team |
| 발표 | 2026-10-15 |
| 팀 저장소 | [SKNETWORKS-FAMILY-AICAMP/SKN35-3rd-4Team](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-3rd-4Team) |
"""
TEAM = """## 팀

공개 저장소라서 팀원은 **역할 번호로만** 적습니다.

| 역할 | 담당 |
|---|---|
| 1번 | 그래프 · 백엔드 (LangGraph 연결, 질문 분류, analyzer, 재시도 판단, dev 병합) |
| 2번 | 데이터 · 검색 (문서 수집, import · 메서드 대응표, 청킹, Chroma, 하이브리드 검색, retriever) |
| 3번 | 변환 · 검증 (State, rewriter, verifier 11가지 검사) |
| 4번 | 화면 · DB · 평가 (Streamlit 화면, TiDB 대화 기록, 평가 질문 36개 · 점검 도구) + 보고서 · README · 발표 |

## 참고 자료

- [LangChain v1 마이그레이션 가이드](https://docs.langchain.com/oss/python/migrate/langchain-v1)
- Ashik et al., [When LLMs Lag Behind: Knowledge Conflicts from Evolving APIs in Code Generation](https://arxiv.org/abs/2604.09515), 2026
- [GitChameleon 2.0: Evaluating AI Code Generation Against Python Library Version Incompatibilities](https://arxiv.org/abs/2507.12367), 2025
- Wu et al., [VersiCode: Towards Version-controllable Code Generation](https://arxiv.org/abs/2406.07411), 2024
"""
FOLDERS = """```text
├── streamlit_app.py        # 4번 화면 입구 (app.py 는 1번의 그래프 실행 시험용)
├── app.py · check_nodes.py # 1번 · 3번 시험 스크립트
├── src/
│   ├── graph/              # 1번 · 3번: graph.py(질문 분류 입구) · supervisor.py(변환 파이프라인) · state.py · nodes/
│   ├── prompt/             # 1번 · 3번: analyzer · rewriter · classifier 프롬프트
│   ├── rag/                # 2번: 문서 수집 · 대응표 · 청킹 · 임베딩 · 검색
│   └── ui/                 # 4번: client.py(그래프 호출 · 진행 표시) · result_view.py(결과 패널) · db.py(TiDB) · mock.py(그래프 없을 때)
├── data/                   # 2번: processed/(대응표 · 청크) · raw/(문서 · 버전별 도구 목록)
├── eval/                   # 4번: questions.json(36개) · build_questions.py · check_questions.py
├── tools/bot_check.py      # 4번: 화면 · DB 자동 점검 19가지
└── docs/                   # 4번: 화면 실행 방법 · DB 설계(ERD) · 머지 가이드 · 결과 모양
```
"""
DOCS = """| 문서 | 내용 |
|---|---|
| [docs/화면_실행방법.md](docs/화면_실행방법.md) | 화면 실행 · 비밀 값 · 자동 점검 · 자주 나는 문제 |
| [docs/DB_설계.md](docs/DB_설계.md) | ERD (users, chat_history), 화면이 DB를 쓰는 방법, 이전 설계 |
| [eval/README.md](eval/README.md) | 평가 질문 36개 구성과 검사 방법 |
| [docs/머지_가이드.md](docs/머지_가이드.md) | 팀 저장소와 겹치는 파일, 가져갈 기능 · 뺄 기능 |
| 발표 자료 · 테스트 계획 및 결과 보고서 | 발표 당일 제출본 (PPT · PDF) |
"""
CHECK = """### 점검 재현

```bash
python tools/bot_check.py
```

```bash
python eval/check_questions.py --py <LangChain 1.x python> --map data/processed/import_map.jsonl --symbols data/raw/symbols
```

`bot_check.py`는 임시 SQLite로 화면을 실행해 19가지를 확인합니다(TiDB · 유료 API 사용 안 함). 마지막 줄 `19/19 통과`가 정상입니다.
"""

deploy = TITLE + """
**바로 가기**: [**배포 화면**]([배포 주소]) · [팀 저장소](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-3rd-4Team) · [화면 실행 방법](docs/화면_실행방법.md) · [DB 설계(ERD)](docs/DB_설계.md) · [평가 질문 36개](eval/README.md)

""" + INFO + """| 이 저장소 | 팀 저장소 `sungwook` 브랜치를 옮긴 **배포용** 저장소 (Streamlit Community Cloud) |

""" + body + """
## 9. 실행 방법

### 9-1. 내 컴퓨터

```bash
pip install -r requirements.txt
```

```bash
streamlit run streamlit_app.py
```

`.env`(또는 `.streamlit/secrets.toml`)에 비밀 값을 넣습니다. 둘 다 Git에 올라가지 않습니다.

```text
OPENAI_API_KEY=...        # analyzer · rewriter
CHROMA_API_KEY=...        # retriever (Chroma Cloud)
CHROMA_TENANT=...
CHROMA_DATABASE=...
TIDB_HOST=...             # 대화 기록 (없으면 로컬 SQLite)
TIDB_PORT=4000
TIDB_USER=...
TIDB_PASSWORD=...
TIDB_DATABASE=langchain_db
```

| 값 | 없으면 |
|---|---|
| `OPENAI_API_KEY`, `CHROMA_*` | 팀 그래프 대신 화면 쪽 임시 결과 (사이드바에 이유 표시) |
| TiDB | 로컬 SQLite에 저장 (사이드바에 이유 표시) |

### 9-2. 배포 (Streamlit Community Cloud)

1. share.streamlit.io → **Create app** → 이 저장소, 브랜치 `main`, Main file path `streamlit_app.py`
2. **Advanced settings** → Python **3.12**, **Secrets**에 [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example) 형식으로 값 넣기 (`키 = "값"`, 키 4줄은 `[tidb]`보다 위에)
3. **Deploy** → 사이드바에 "변환: 팀 챗봇", "기록: TiDB"가 나오면 연결 성공

`requirements.txt`만 쓰도록 `uv.lock`은 넣지 않았습니다 (Streamlit Cloud는 `uv.lock`이 있으면 그걸 먼저 써서 화면 패키지가 빠짐).

""" + CHECK + """
## 10. 폴더 구조

""" + FOLDERS + """
## 11. 문서

""" + DOCS + "\n" + TEAM.replace("## 팀", "## 12. 팀").replace("## 참고 자료", "## 13. 참고 자료")

draft = """> **README 초안 (4번 작성, 2026-10-14)** · 팀 저장소 README는 1번이 관리합니다. 필요한 부분을 골라 README에 옮겨 주세요. 배포용 완성본은 [langchain-migration-assistant](https://github.com/SKN35shimsungwook/langchain-migration-assistant)에 있습니다.

""" + TITLE + """
**바로 가기**: [화면 실행 방법](화면_실행방법.md) · [DB 설계(ERD)](DB_설계.md) · [평가 질문 36개](../eval/README.md) · [머지 가이드](머지_가이드.md) · [배포 저장소](https://github.com/SKN35shimsungwook/langchain-migration-assistant)

""" + INFO + "\n" + body.replace("](docs/", "](").replace("](eval/", "](../eval/") + """
## 9. 실행 방법

Windows PowerShell 5.1은 `&&`를 쓸 수 없으니 **한 줄씩** 실행합니다.

```powershell
git clone -b dev https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-3rd-4Team.git
```

```powershell
cd SKN35-3rd-4Team
```

```powershell
uv sync
```

```powershell
uv pip install -r requirements.txt
```

`.env`에 비밀 값을 넣습니다 (Git에 올리지 않음).

```text
OPENAI_API_KEY=...
CHROMA_API_KEY=...
CHROMA_TENANT=...
CHROMA_DATABASE=...
TIDB_HOST=...
TIDB_PORT=4000
TIDB_USER=...
TIDB_PASSWORD=...
TIDB_DATABASE=langchain_db
```

| 실행 | 명령 |
|---|---|
| 화면 (4번) | `uv run streamlit run streamlit_app.py` |
| 그래프 시험 (1번) | `uv run python app.py` |
| 노드별 시험 (3번) | `uv run python check_nodes.py` |

""" + CHECK.replace("python ", "uv run python ") + """
## 10. 폴더 구조

""" + FOLDERS + """
## 11. 문서

""" + DOCS.replace("](docs/", "](").replace("](eval/", "](../eval/") + "\n" + TEAM.replace("## 팀", "## 12. 팀").replace("## 참고 자료", "## 13. 참고 자료")

open("README_deploy.md", "w", encoding="utf-8").write(deploy)
open("README_draft.md", "w", encoding="utf-8").write(draft)
print(len(deploy.splitlines()), len(draft.splitlines()))
