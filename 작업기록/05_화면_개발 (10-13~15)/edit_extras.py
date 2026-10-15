from pathlib import Path
import re
import sys

root = Path(sys.argv[1])


def edit(rel, pairs):
    p = root / rel
    s = p.read_text(encoding="utf-8")
    for a, b in pairs:
        assert a in s, (rel, a)
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8")


# 1. extras/version_detect.py: 버전 목록은 ..versions 에서, mock 은 ..mock 에서
edit("src/ui/extras/version_detect.py", [
    ('''"""버전 정보: 시작 화면의 마인드맵 요약, 코드의 옛 버전 자동 감지.

- 요약 숫자: version_summary.json (2번 import 대응표를 버전 · 영역별로 센 것)
- 자동 감지: 대응표의 seen_in(그 기능이 있던 옛 버전 목록)을 코드의 import 마다 겹쳐 본다.
  팀 저장소에 data/processed/import_map.jsonl 이 있으면 그것을, 없으면 아래 작은 예시를 쓴다.
"""''', '''"""[선택 기능 · 4번 영역 아님] 지금 코드가 어느 버전 시기인지 자동 감지.

- 2번 버전별 도구 목록(version_map.py)이 있으면 1.x 까지 포함해 "이 경로들이 모두 있는 버전"을 찾는다.
- 없으면 2번 import 대응표의 seen_in(그 기능이 있던 옛 버전 목록)과 패키지 단서로 짐작한다.
  대응표도 없으면 아래 작은 예시를 쓴다.
"""'''),
    ('from .mock import import_paths', 'from ..mock import import_paths\nfrom ..versions import ALL, ALL_WITH_NEW'),
    ('''SUMMARY = json.loads((Path(__file__).with_name("version_summary.json")).read_text(encoding="utf-8"))
''', ''),
    ('''ALL = [v["version"] for v in SUMMARY["versions"]]          # 옛 버전, 오래된 순
''', ''),
    ('    from .mock import SAMPLE_MAP', '    from ..mock import SAMPLE_MAP'),
    ('''ALL_WITH_NEW = [*ALL, "1.x"]


''', ''),
])

# 2. extras/followups.py 설명
edit("src/ui/extras/followups.py", [
    ('"""LLM 보조 기능: 연상 질문 만들기, 코드 없는 질문에 짧게 답하기.',
     '"""[선택 기능 · 4번 영역 아님] LLM 대화 기능: 연상 질문 만들기, 코드 없는 질문에 짧게 답하기.'),
])
edit("src/ui/extras/version_map.py", [
    ('"""버전 ↔ 버전 import 대응 (어느 방향이든).', '"""[선택 기능 · 4번 영역 아님] 버전 ↔ 버전 import 대응 (어느 방향이든).'),
])

# 3. mock.py: version_map 은 선택 기능
s = (root / "src/ui/mock.py").read_text(encoding="utf-8")
assert s.count("    from . import version_map as vm") == 2
s = s.replace("    from . import version_map as vm", '    from .extras import load\n    vm = load("version_map")')
s = s.replace("        if not vm.available():\n            return None", "        if vm is None or not vm.available():\n            return None")
s = s.replace("            if vm.available():\n                t = vm.translate(path, \"1.x\")",
              "            if vm is not None and vm.available():\n                t = vm.translate(path, \"1.x\")")
s = s.replace('target_version != "1.x" and not vm.available():', 'target_version != "1.x" and (vm is None or not vm.available()):')
(root / "src/ui/mock.py").write_text(s, encoding="utf-8")

# 4. client.py
edit("src/ui/client.py", [
    ('from .versions import ALL_WITH_NEW, SUMMARY, detect', 'from .extras import load\nfrom .versions import ALL_WITH_NEW, LATEST'),
    ('LATEST = SUMMARY["latest"]                    # 예: {"langchain": "1.4.4", "langchain-core": "1.6.10"}\n', ''),
    ('    result["detected"] = detect(code)',
     '    detector = load("version_detect")          # 선택 기능. 없으면 감지 결과는 비어 있음\n'
     '    result["detected"] = detector.detect(code) if detector else {"candidates": [], "clues": [], "source": None}'),
])
print("edited")
