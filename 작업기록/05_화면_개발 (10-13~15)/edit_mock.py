from pathlib import Path
import sys

p = Path(sys.argv[1]) / "src" / "ui" / "mock.py"
s = p.read_text(encoding="utf-8")
NL = chr(92) + "n"


def rep(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b, 1)


rep('''def find_evidence(path: str) -> dict | None:
    """대응표에서 옛 경로를 찾는다. 2번 검색기가 있으면 실제 대응표, 없으면 예시표."""
    try:''', '''def find_evidence(path: str, target: str = "1.x") -> dict | None:
    """옛 경로의 목표 버전 위치를 찾는다.

    1.x 로 갈 때: 2번 import 대응표(imap-…) → 없으면 2번 버전별 도구 목록 → 없으면 예시표
    그 밖의 버전으로 갈 때(되돌리기 포함): 2번 버전별 도구 목록 (version_map.py)
    """
    from . import version_map as vm
    if target != "1.x":
        if not vm.available():
            return None
        t = vm.translate(path, target)
        return {"old": path, "new": t["new"], "kind": t["kind"], "evidence_id": f"ver-{target}:{t['new'] or path}",
                "source": "version_symbols", "alternative": None, "real": True}
    try:''')
rep('''        hit = lookup(path)
        if hit is None:
            return None''', '''        hit = lookup(path)
        if hit is None:
            if vm.available():
                t = vm.translate(path, "1.x")
                return {"old": path, "new": t["new"], "kind": t["kind"], "evidence_id": f"ver-1.x:{t['new'] or path}",
                        "source": "version_symbols", "alternative": None, "real": True}
            return None''')
rep('''def fake_rewrite(code: str, evidences: list[dict]) -> str:''',
    '''def fake_rewrite(code: str, evidences: list[dict], target: str = "1.x") -> str:''')
rep('    out = "' + NL + '".join(lines)\n    out = re.sub(',
    '    out = "' + NL + '".join(lines)\n    if target != "1.x":          # LCEL · invoke 흉내는 1.x 로 갈 때만\n'
    '        return out\n    out = re.sub(')
rep('''    evidences = []
    paths = import_paths(code)
    for line, path in paths:
        ev = find_evidence(path)''', '''    from . import version_map as vm
    evidences = []
    paths = import_paths(code)
    for line, path in paths:
        ev = find_evidence(path, target_version)''')
rep('''    if not evidences:
        message = ("LangChain import 줄을 찾지 못했습니다.''', '''    if not evidences and paths and target_version != "1.x" and not vm.available():
        message = ("1.x 가 아닌 버전으로 바꾸려면 2번의 버전별 도구 목록(data/raw/symbols)이 필요해요. "
                   "팀 저장소에서 실행하면 모든 버전 방향으로 바꿀 수 있어요.")
        return {"target_version": target_version, "original_code": code, "migrated_code": code,
                "changes": [], "steps": _steps(len(paths), ok=False),
                "verification": {"success": False, "attempts": 0, "message": message}, "mode": "mock"}
    if not evidences:
        message = ("LangChain import 줄을 찾지 못했습니다.''')
rep('''    migrated = fake_rewrite(code, evidences)''', '''    migrated = fake_rewrite(code, evidences, target_version)''')
rep('''                "alternative": ev.get("alternative"), "real_evidence": ev["real"]} for ev in evidences]''',
    '''                "alternative": ev.get("alternative"), "real_evidence": ev["real"]}
               for ev in evidences if ev["kind"] != "same"]       # 목표 버전에도 그대로 있는 줄은 변경표에서 뺌''')
p.write_text(s, encoding="utf-8")
print("edited")
