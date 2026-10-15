"""2번 브랜치 데이터 분석 (읽기 전용 사본 기준). 결과를 JSON + 텍스트로 출력."""
import ast
import json
import sqlite3
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

D = Path(sys.argv[1])          # scy_data
TESTSET = Path(sys.argv[2])    # 우리 testset.json
OUT = Path(sys.argv[3])        # 결과 json

def jl(p):
    return [json.loads(l) for l in (D / p).read_text(encoding="utf-8").splitlines() if l.strip()]

R = {}

# ---------- 1. 원문 문서 ----------
latest = jl("data/raw/docs/latest_manifest.jsonl")
mig = jl("data/raw/docs/migration_manifest.jsonl")
R["docs"] = {
    "latest_count": len(latest),
    "latest_bytes": sum(x["bytes"] for x in latest),
    "latest_sections": Counter(x["section"].split(" / ")[1] if " / " in x["section"] else x["section"] for x in latest).most_common(12),
    "latest_has_v1_guide": [x["url"] for x in latest if "migrate" in x["url"]],
    "migration_count": len(mig),
    "migration_groups": Counter(x["group"] for x in mig).most_common(),
    "migration_era": Counter(x["era"] for x in mig).most_common(),
    "integrations_share": sum(1 for x in latest if "/integrations/" in x["url"]),
}

# ---------- 2. 버전별 심볼 ----------
sym = {}
for f in sorted((D / "data/raw/symbols").glob("*.jsonl")):
    sym[f.stem] = sum(1 for _ in f.open(encoding="utf-8"))
R["symbols"] = sym

# ---------- 3. import 대응표 ----------
im = jl("data/processed/import_map.jsonl")
R["import_map"] = {
    "count": len(im),
    "kind": Counter(x["kind"] for x in im).most_common(),
    "import_status": Counter(x["import_status"] for x in im).most_common(),
    "granularity": Counter(x["granularity"] for x in im).most_common(),
    "sources": Counter(s for x in im for s in x["sources"]).most_common(),
    "new_package": Counter((x["new"] or "None").split(".")[0] for x in im).most_common(10),
    "old_package": Counter(x["old"].split(".")[0] for x in im).most_common(6),
    "dup_old": sum(1 for k, v in Counter(x["old"] for x in im).items() if v > 1),
    "has_alternative": sum(1 for x in im if x.get("alternative")),
    "import_errors_sample": Counter((x.get("import_error") or "")[:60] for x in im if x["import_status"] != "ok").most_common(5),
}

# ---------- 4. 청크 ----------
ch = jl("data/processed/chunks.jsonl")
chars = [c["chars"] for c in ch]
by_src = defaultdict(list)
for c in ch:
    by_src[c["source"]].append(c["chars"])
texts = Counter(c["text"] for c in ch)
R["chunks"] = {
    "count": len(ch),
    "fields": sorted({k for c in ch for k in c}),
    "source": {k: {"n": len(v), "median_chars": int(st.median(v)), "max": max(v), "min": min(v)} for k, v in by_src.items()},
    "era": Counter(c.get("era") for c in ch).most_common(),
    "has_code": Counter(c.get("has_code") for c in ch).most_common(),
    "chars_median": int(st.median(chars)),
    "chars_p90": sorted(chars)[int(len(chars) * .9)],
    "chars_max": max(chars),
    "tiny_lt80": sum(1 for x in chars if x < 80),
    "huge_gt4000": sum(1 for x in chars if x > 4000),
    "dup_texts": sum(v - 1 for v in texts.values() if v > 1),
    "has_url": sum(1 for c in ch if c.get("url") or c.get("source_url")),
    "has_evidence_like_id": sum(1 for c in ch if c.get("chunk_id")),
}
R["chunks"]["sample_doc_chunk"] = next(({k: (v[:200] if isinstance(v, str) else v) for k, v in c.items()} for c in ch if c["source"] != "import_map"), None)

# ---------- 5. Chroma ----------
con = sqlite3.connect(D / "data/vectordb/chroma/chroma.sqlite3")
cur = con.cursor()
tables = [r[0] for r in cur.execute("select name from sqlite_master where type='table'")]
info = {"tables": len(tables)}
try:
    info["collections"] = cur.execute("select name, dimension from collections").fetchall()
except Exception as e:
    info["collections_err"] = str(e)
try:
    info["embeddings"] = cur.execute("select count(*) from embeddings").fetchone()[0]
    info["meta_keys"] = cur.execute("select key, count(*) from embedding_metadata group by key order by 2 desc").fetchall()[:25]
except Exception as e:
    info["emb_err"] = str(e)
R["chroma"] = info

# ---------- 6. 우리 시험지와 대조 ----------
ts = json.loads(TESTSET.read_text(encoding="utf-8"))
used = Counter()
per_item = {}
for t in ts:
    syms = []
    for n in ast.walk(ast.parse(t["old_code"])):
        if isinstance(n, ast.ImportFrom):
            syms += [f"{n.module}.{a.name}" for a in n.names]
    used.update(syms)
    per_item[t["id"]] = (t["difficulty"], syms)
targets = defaultdict(set)
for t in ts:
    for n in ast.walk(ast.parse(t["target_imports"])):
        if isinstance(n, ast.ImportFrom):
            for a in n.names:
                targets[a.name].add(n.module)
by_old = {}
for x in im:
    by_old.setdefault(x["old"], x)
covered = [o for o in used if o in by_old]
agree, differ, classic = [], [], []
for o in covered:
    x = by_old[o]
    name = o.rsplit(".", 1)[1]
    new_mod = (x["new"] or "").rsplit(".", 1)[0]
    if x["kind"] != "native":
        classic.append((o, x["new"], x["kind"]))
    if new_mod in targets.get(name, set()):
        agree.append(o)
    else:
        differ.append((o, x["new"], x["kind"], sorted(targets.get(name, []))))
missing = sorted((o for o in used if o not in by_old), key=lambda o: -used[o])
diff_cov = {}
for d in ("easy", "medium", "hard"):
    items = [v for v in per_item.values() if v[0] == d]
    full = sum(1 for _, s in items if all(x in by_old for x in s))
    diff_cov[d] = {"items": len(items), "all_symbols_covered": full}
R["testset"] = {
    "kinds": len(used), "occurrences": sum(used.values()),
    "covered_kinds": len(covered), "covered_occ": sum(used[o] for o in covered),
    "agree": len(agree), "differ": differ, "classic_or_other": classic,
    "missing": [(o, used[o]) for o in missing],
    "by_difficulty": diff_cov,
}

# 근거 문서: 우리 시험지에 나오는 옛 체인 · 메모리 · 에이전트 가이드가 있는가
need = {"LLMChain": "llm_chain", "ConversationChain": "conversation_chain", "RetrievalQA": "retrieval_qa",
        "ConversationalRetrievalChain": "conversation_retrieval_chain", "ConversationBufferMemory": "conversation_buffer_memory",
        "initialize_agent / AgentExecutor": "migrate_agent", "MultiPromptChain": "multi_prompt_chain",
        "LLMRouterChain": "llm_router_chain", "MapReduce": "map_reduce_chain"}
paths = " ".join(x["path"] for x in mig)
R["guide_coverage"] = {k: (v in paths) for k, v in need.items()}

OUT.write_text(json.dumps(R, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print(json.dumps(R, ensure_ascii=False, indent=1, default=str)[:12000])
