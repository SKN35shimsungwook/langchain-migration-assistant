import re
HEADER = """<div align="center">

# LangChain 버전 마이그레이션 코드 어시스턴트

**옛 버전 LangChain 코드를 넣으면, 원하는 버전에서 돌아가는 코드로 고치고 근거와 검사 결과까지 보여 주는 챗봇**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.4.5-1C3C3C?logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1.2-1C3C3C)
![Streamlit](https://img.shields.io/badge/Streamlit-1.6x-FF4B4B?logo=streamlit&logoColor=white)
![TiDB](https://img.shields.io/badge/TiDB-Cloud-E30C34)
![Chroma](https://img.shields.io/badge/Chroma-Cloud-F2A33A)
![검사](https://img.shields.io/badge/자동_점검-19%2F19-2EA44F)
![질문](https://img.shields.io/badge/평가_질문-36%2F36_검사-2EA44F)

{links}

</div>

<!-- 데모 GIF 자리: 화면에서 확인용 예제를 보내 결과 패널이 나오는 15초 녹화를 docs/images/demo.gif 로 넣고 아래 주석을 풀어 주세요
<p align="center"><img src="docs/images/demo.gif" width="860" alt="확인용 예제를 보내면 근거 ID가 붙은 변환 결과가 나오는 화면"></p>
-->

> **문서 근거**(import · 메서드 대응표, 최신 공식 문서 검색)로 고치고, **검사 근거**(verifier 11가지, LLM 없이)로 확인합니다.
> 검사에 실패하면 실패 이유를 들고 근거를 다시 찾아 최대 3번 고칩니다. 바뀐 줄마다 근거 ID가 붙습니다.

"""
AGENT = """### 9-0. AI 에이전트에게 맡기기

Claude Code 같은 코딩 에이전트에 아래 글을 그대로 붙여 넣으면 설치부터 실행까지 해 줍니다. (비밀 값은 직접 넣으세요)

```text
https://github.com/SKN35shimsungwook/langchain-migration-assistant 를 내려받아서
README의 "9-1. 내 컴퓨터" 순서대로 설치하고 streamlit_app.py 를 실행해 줘.
.env 는 만들기만 하고 값은 비워 둬. 내가 직접 넣을게.
실행되면 사이드바의 연결 상태 배지 두 개를 알려 줘.
```

"""

def upgrade(path, links, agent=True):
    s = open(path, encoding="utf-8").read()
    start = s.index("| | |")                               # 정보 표부터는 그대로
    s = HEADER.format(links=links) + s[start:]
    if agent:
        s = s.replace("### 9-1. 내 컴퓨터", AGENT + "### 9-1. 내 컴퓨터", 1)
    open(path, "w", encoding="utf-8").write(s)

upgrade("README_deploy.md",
        "[**배포 화면**]([배포 주소]) · [구조](#3-시스템-구조) · [화면 · DB](#4-화면과-대화-기록-4번) · [평가](#5-평가-방법) · "
        "[결과](#6-결과) · [실행](#9-실행-방법) · [팀 저장소](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-3rd-4Team)")

s = open("README_draft.md", encoding="utf-8").read()
note, rest = s.split("\n\n", 1)
open("README_draft.md", "w", encoding="utf-8").write(rest)
upgrade("README_draft.md",
        "[구조](#3-시스템-구조) · [화면 · DB](#4-화면과-대화-기록-4번) · [평가](#5-평가-방법) · [결과](#6-결과) · "
        "[실행](#9-실행-방법) · [배포 저장소](https://github.com/SKN35shimsungwook/langchain-migration-assistant)", agent=False)
s = open("README_draft.md", encoding="utf-8").read()
open("README_draft.md", "w", encoding="utf-8").write(note + "\n\n" + s)
print("ok")
