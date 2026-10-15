import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from src.ui import db
from sqlalchemy import text
with db.engine().connect() as c:
    rows = c.execute(text("SELECT user_id, session_id, created_at, LEFT(question, 50), LEFT(answer, 80) FROM chat_history "
                          "WHERE created_at > '2026-10-15 05:00:00' ORDER BY created_at")).fetchall()
for r in rows:
    print(r[0], r[1][:8], f"{r[2]:%H:%M:%S}", "| Q:", (r[3] or "").replace("\n", " "), "| A:", (r[4] or "").replace("\n", " "))
