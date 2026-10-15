import json
from candidates import C
refs = {
 "easy": "https://docs.langchain.com/oss/python/migrate/langchain-v1",
 "medium": "https://docs.langchain.com/oss/python/migrate/langchain-v1 (langchain-classic 섹션)",
 "hard": "https://docs.langchain.com/oss/python/migrate/langchain-v1 (create_agent 섹션)",
}
data = [{
  "id": cid, "difficulty": d, "old_code": old, "why_broken": why,
  "target_imports": new, "reference": refs[d],
  "verified_new_fails": True, "verified_old": False,
} for cid, d, old, why, new in C]
out = r"C:\Users\playdata2\Desktop\skn35 report\langchain_migration\eval\testset_sample.json"
json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(data))
