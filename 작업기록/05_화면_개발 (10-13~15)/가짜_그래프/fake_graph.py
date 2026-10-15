import sys
sys.path.insert(0, r"C:/Users/playdata2/Desktop/skn35 report/langchain_migration/app")
from backend import _mock, load_testset
def run_migration(code, target_version):
    r = _mock(code, load_testset(), target_version); r.pop("mock"); return r
def broken(code, target_version):
    raise RuntimeError("노드 오류")
