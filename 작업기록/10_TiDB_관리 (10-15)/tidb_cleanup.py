import json, sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from src.ui import db
from sqlalchemy import text, bindparam
KEEP = ["팀원_아이디_1", "팀원_아이디_2"]   # 남길 아이디 (공개 저장소라 실제 아이디는 가림, 실행 전에 바꿔 넣기)
BACKUP = sys.argv[1]
eng = db.engine()
assert db.backend_name() == "TiDB"
with eng.begin() as c:
    nin = bindparam("keep", expanding=True)
    users = [dict(r._mapping) for r in c.execute(text("SELECT * FROM users WHERE user_id NOT IN :keep").bindparams(nin), {"keep": KEEP})]
    chats = [dict(r._mapping) for r in c.execute(text("SELECT * FROM chat_history WHERE user_id NOT IN :keep").bindparams(nin), {"keep": KEEP})]
    json.dump({"users": users, "chat_history": chats}, open(BACKUP, "w", encoding="utf-8"), ensure_ascii=False, default=str, indent=1)
    d1 = c.execute(text("DELETE FROM chat_history WHERE user_id NOT IN :keep").bindparams(nin), {"keep": KEEP}).rowcount
    d2 = c.execute(text("DELETE FROM users WHERE user_id NOT IN :keep").bindparams(nin), {"keep": KEEP}).rowcount
print(f"백업: 사용자 {len(users)} · 대화 {len(chats)} → {BACKUP}")
print(f"삭제: 대화 {d1}행 · 사용자 {d2}명")
with eng.connect() as c:
    left = c.execute(text("SELECT u.user_id, COUNT(h.uuid) FROM users u LEFT JOIN chat_history h ON h.user_id = u.user_id GROUP BY u.user_id")).fetchall()
    total = c.execute(text("SELECT COUNT(*) FROM chat_history")).scalar()
print("남은 사용자:", [(u, n) for u, n in left], "· 남은 대화 행:", total)
