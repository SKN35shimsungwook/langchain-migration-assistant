from pathlib import Path
import sys
p = Path(sys.argv[1]) / "src" / "ui" / "versions.py"
s = p.read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b, 1)
rep('''def detect(code: str) -> dict:
    """코드가 어느 옛 버전 시기인지 범위로 짐작한다."""
    candidates = list(ALL)''', '''ALL_WITH_NEW = [*ALL, "1.x"]


def _span(vs: list[str]) -> str:
    return vs[0] if len(vs) == 1 else f"{vs[0]}~{vs[-1]}"


def detect(code: str) -> dict:
    """코드가 어느 버전 시기인지 범위로 짐작한다.

    2번 버전별 도구 목록이 있으면 1.x 까지 포함해 "이 경로들이 모두 있는 버전"을 찾고,
    없으면 대응표의 seen_in(옛 버전만)과 패키지 단서로 짐작한다.
    """
    from . import version_map as vm
    paths = [p for _, p in import_paths(code)]
    if paths and vm.available():
        having = vm.versions_having(paths)
        if having:
            clues = []
            for p in paths:
                vs = vm.versions_having([p])
                if len(vs) < len(ALL_WITH_NEW):
                    clues.append(f"`{p.rsplit('.', 1)[1]}` ({_span(vs)}에만 있음)")
            return {"candidates": having, "clues": clues, "source": "2번 버전 목록"}
    candidates = list(ALL)''')
rep('''    if c == ALL:
        return (f"이 코드는 **LangChain {span}** 시기 코드로 보여요. 쓰인 기능들이 옛 버전 전체에 있어서 "
                "범위를 더 좁히지는 못했어요. 변환 결과는 같으니 걱정하지 않으셔도 돼요.")''', '''    if c == ["1.x"]:
        return "이 코드는 이미 **LangChain 1.x** 코드로 보여요. 옛 버전으로 되돌리려면 위에서 변환할 버전을 고르세요."
    if c in (ALL, ALL_WITH_NEW):
        return (f"이 코드는 **LangChain {span}** 시기 코드로 보여요. 쓰인 기능들이 그 버전들에 모두 있어서 "
                "범위를 더 좁히지는 못했어요. 변환 결과는 같으니 걱정하지 않으셔도 돼요.")''')
p.write_text(s, encoding="utf-8")
print("edited")
