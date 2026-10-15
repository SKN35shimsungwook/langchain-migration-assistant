from pathlib import Path
import sys
root = Path(sys.argv[1])
def edit(rel, pairs):
    p = root / rel
    s = p.read_text(encoding="utf-8")
    for a, b in pairs:
        assert a in s, (rel, a)
        s = s.replace(a, b, 1)
    p.write_text(s, encoding="utf-8")

edit("src/ui/client.py", [
    ('from .versions import SUMMARY, detect', 'from .versions import ALL_WITH_NEW, SUMMARY, detect'),
    ('TARGET_VERSIONS = SUMMARY["targets"]          # 지금 2번 대응표의 목표는 1.x 하나',
     'TARGET_VERSIONS = ALL_WITH_NEW               # 어느 버전으로든 (옛 버전으로 되돌리기 포함)'),
])
edit("app.py", [
    ('from src.ui.versions import ALL, describe', 'from src.ui.versions import ALL_WITH_NEW, describe'),
    ('KIND_LABEL = {"native": "최신 위치", "classic_fallback": "옛 창고(classic)", "unresolved": "못 찾음"}',
     'KIND_LABEL = {"native": "최신 위치", "moved": "위치 이동", "same": "그대로", "classic_fallback": "옛 창고(classic)",\n'
     '              "unresolved": "못 찾음"}\nORDER = ALL_WITH_NEW'),
    ('''    changes = result["changes"]
    classic = [c for c in changes if c["kind"] == "classic_fallback"]''',
     '''    changes = result["changes"]
    if not changes:
        return f"바꿀 import가 없어요. 쓰인 기능이 LangChain {result['target_version']}에도 그대로 있어요."
    classic = [c for c in changes if c["kind"] == "classic_fallback"]'''),
    ('''        extra += f" {len(missing)}개는 1.x에서 옮길 곳을 찾지 못했어요."''',
     '''        extra += f" {len(missing)}개는 {result['target_version']}에 같은 기능이 없어서 그대로 두었어요."'''),
    ('''    return (f"import {len(changes)}줄을 찾아 고쳤어요.{extra}''',
     '''    src = result["source_version"] or (result["detected"]["candidates"] or [None])[-1]
    back = src in ORDER and ORDER.index(result["target_version"]) < ORDER.index(src)
    head = f"LangChain {result['target_version']}로 되돌리면서 " if back else ""
    return (f"{head}import {len(changes)}줄을 찾아 고쳤어요.{extra}'''),
    ('''        note = version_note(result) if result["changes"] else None''',
     '''        note = version_note(result) if result["verification"]["success"] else None'''),
    ('''    source = ver_src.selectbox("옛 버전", [AUTO, *ALL], key="source_pick")
    target = ver_tgt.selectbox("변환할 버전", TARGET_VERSIONS, key="target_pick",
                               format_func=lambda v: f"LangChain {v} (최신 {LATEST['langchain']})")
    source = None if source == AUTO else source''',
     '''    source = ver_src.selectbox("지금 코드 버전", [AUTO, *ALL_WITH_NEW], key="source_pick")
    target = ver_tgt.selectbox("변환할 버전", TARGET_VERSIONS, index=len(TARGET_VERSIONS) - 1, key="target_pick",
                               format_func=lambda v: f"LangChain {v} (최신 {LATEST['langchain']})" if v == "1.x"
                               else f"LangChain {v}")
    source = None if source == AUTO else source
    if source == target:
        st.warning("지금 코드 버전과 변환할 버전이 같아요. 변환할 버전을 바꿔 주세요.", icon=":material/info:")'''),
    ('''                    if st.button(f"{q['type']} · {q['request'][:38]}", key=f"starter_{i}", width="stretch"):
                        ss["pending"] = f"{q['request']}\n\n```python\n{q['code']}```"''',
     '''                    st.button(f"{q['type']} · {q['request'][:38]}", key=f"starter_{i}", width="stretch",
                              on_click=use_starter, args=(q,))'''),
    ('''def logout() -> None:''', '''def use_starter(q: dict) -> None:
    """예시 질문: 질문의 버전으로 맞추고 보낸다 (위젯이 그려지기 전에 실행되는 콜백)."""
    ss["source_pick"] = q["source_version"] if q["source_version"] in ALL_WITH_NEW else AUTO
    ss["target_pick"] = q.get("target_version", "1.x")
    ss["pending"] = f"{q['request']}\n\n```python\n{q['code']}```"


def logout() -> None:'''),
])
print("edited")
