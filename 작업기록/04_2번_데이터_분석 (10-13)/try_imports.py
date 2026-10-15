import json, sys, importlib, warnings
warnings.filterwarnings("ignore")
rows = json.load(open(sys.argv[1], encoding="utf-8"))
ok = bad = 0
for old, new, kind in rows:
    mod, name = new.rsplit(".", 1)
    try:
        getattr(importlib.import_module(mod), name); ok += 1
    except Exception as e:
        bad += 1; print("FAIL", kind, new, type(e).__name__, str(e)[:80])
print("ok", ok, "fail", bad)
