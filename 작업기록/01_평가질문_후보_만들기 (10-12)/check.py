import ast, subprocess, sys, json
from candidates import C

PY = sys.argv[1]

def imports_of(code):
    lines = []
    for n in ast.walk(ast.parse(code)):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            lines.append(ast.unparse(n))
    return "\n".join(lines)

def run(src):
    p = subprocess.run([PY, "-W", "ignore", "-c", src], capture_output=True, text=True, timeout=60, encoding="utf-8")
    err = (p.stderr.strip().splitlines() or [""])[-1]
    return p.returncode == 0, err

out = []
for cid, diff, old, why, new in C:
    ok_old, err_old = run(imports_of(old))
    ok_new, err_new = run(new)
    print(f"{cid}: old_fails={not ok_old} | {err_old[:110]}")
    print(f"    new_ok={ok_new} {err_new[:110]}")
