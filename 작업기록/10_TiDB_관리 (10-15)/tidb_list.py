import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from src.ui import db
from sqlalchemy import text
print("연결:", db.backend_name())
eng = db.engine()
with eng.connect() as c:
    users = c.execute(text("SELECT user_id, created_at FROM users ORDER BY created_at")).fetchall()
    rows = c.execute(text("SELECT user_id, COUNT(*) n, COUNT(DISTINCT session_id) s, MIN(created_at) a, MAX(created_at) b FROM chat_history GROUP BY user_id")).fetchall()
stat = {r[0]: r for r in rows}
print(f"사용자 {len(users)}명 · 대화 행 {sum(r[1] for r in rows)}개")
print("아이디 | 가입 | 질문 수 | 세션 수 | 마지막 대화")
for u, created in users:
    r = stat.get(u)
    print(f"{u} | {created:%m-%d %H:%M} | {r[1]} | {r[2]} | {r[4]:%m-%d %H:%M}" if r else f"{u} | {created:%m-%d %H:%M} | 0 | 0 | -")
print("users에 없는 대화 주인:", [r[0] for r in rows if r[0] not in {u for u, _ in users}])
