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
edit("src/ui/version_map.py", [
    ('import json\nfrom functools', 'import json\nimport os\nfrom functools'),
    ('SYMBOLS = ROOT / "data" / "raw" / "symbols"', 'SYMBOLS = Path(os.environ.get("MIGRATION_SYMBOLS_DIR") or ROOT / "data" / "raw" / "symbols")'),
])
edit("eval/check_questions.py", [
    ('''  (--symbols) 1.x 환경에 패키지가 없어 import 가 안 되면, 2번의 버전별 도구 목록(data/raw/symbols)으로 경로를 확인
''', '''  (--symbols) 1.x 환경에 패키지가 없어 import 가 안 되면, 2번의 버전별 도구 목록(data/raw/symbols)으로 경로를 확인
  목표가 1.x 가 아닌 질문(버전 오가기)은 2번 도구 목록으로 정적 확인: 옛 경로 중 하나라도 목표 버전에 없는가,
  기대 경로가 목표 버전에 모두 있는가 (--symbols 필요)
'''),
    ('''    all_lines = sorted({l for q in qs for l in import_lines(q["code"]) + q["expected_imports"]})''',
     '''    if a.symbols:
        import os
        os.environ["MIGRATION_SYMBOLS_DIR"] = a.symbols
        sys.path.insert(0, str(HERE.parent))
    other = [q for q in qs if q.get("target_version", "1.x") != "1.x"]
    qs_new = [q for q in qs if q.get("target_version", "1.x") == "1.x"]
    all_lines = sorted({l for q in qs_new for l in import_lines(q["code"]) + q["expected_imports"]})'''),
    ('''    expected = {l for q in qs for l in q["expected_imports"]}''', '''    expected = {l for q in qs_new for l in q["expected_imports"]}'''),
    ('''    bad = 0
    for q in qs:
        problems = []''', '''    bad = 0
    for q in qs:
        if q in other:
            bad += check_static(q)
            continue
        problems = []'''),
    ('''def main() -> int:''', '''def check_static(q: dict) -> int:
    """목표가 0.x 인 질문: 2번 도구 목록으로 확인."""
    from src.ui import version_map as vm
    tgt = q["target_version"]
    problems = []
    if not vm.available():
        problems.append("--symbols 가 없어서 확인 못 함")
    else:
        olds = old_paths(q["code"])
        if all(vm.has(p, tgt) for p in olds):
            problems.append(f"옛 코드가 {tgt}에서 바꿀 곳이 없음")
        for line in q["expected_imports"]:
            node = ast.parse(line).body[0]
            for x in node.names:
                if not vm.has(f"{node.module}.{x.name}", tgt):
                    problems.append(f"기대 경로가 {tgt}에 없음: {node.module}.{x.name}")
    print(f"[{'OK ' if not problems else 'BAD'}] {q['id']} {q['type']:<12} {q['difficulty']:<3}"
          f" · {q['source_version']} → {tgt} (2번 도구 목록으로 확인)")
    for p in problems:
        print("      -", p)
    return bool(problems)


def main() -> int:'''),
])
print("edited")
