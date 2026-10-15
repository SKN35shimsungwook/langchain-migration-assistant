import ast, subprocess, sys
from candidates import C
PY=sys.argv[1]
def run(src):
    p=subprocess.run([PY,"-W","ignore","-c",src],capture_output=True,text=True,timeout=60,encoding="utf-8")
    return p.returncode==0,(p.stderr.strip().splitlines() or [""])[-1]
for cid,_,old,_,_ in C:
    print(cid)
    for n in ast.walk(ast.parse(old)):
        if isinstance(n,(ast.Import,ast.ImportFrom)):
            s=ast.unparse(n); ok,e=run(s)
            print("   ","OK  " if ok else "FAIL",s, "" if ok else "| "+e[:70])
print("classic checks")
for s in ["from langchain_classic.chains import LLMChain, ConversationChain, SimpleSequentialChain, RetrievalQA",
          "from langchain_classic.memory import ConversationBufferMemory",
          "from langchain_classic.agents import initialize_agent, AgentType, AgentExecutor, load_tools, create_openai_functions_agent",
          "from langchain_classic import hub"]:
    ok,e=run(s); print("   ","OK  " if ok else "FAIL",s,"" if ok else "| "+e[:80])
