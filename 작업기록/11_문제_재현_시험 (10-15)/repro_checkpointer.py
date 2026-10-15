import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from src.graph.state import MigrationState
from src.graph.nodes.classifier_node import classifier_node
from src.graph.nodes.general_node import general_node
from src.graph.nodes.search_node import search_node
from src.graph.migration import migration
from src.graph.supervisor import prompt_classification
import src.ui.client as client

# 1번이 하는 것처럼 supervisor 와 같은 그래프에 체크포인터(대화 기억)를 붙인 시험용 그래프
b = StateGraph(MigrationState)
b.add_node("classifier", classifier_node); b.add_node("migration", migration())
b.add_node("search", search_node); b.add_node("general", general_node)
b.add_edge(START, "classifier")
b.add_conditional_edges("classifier", prompt_classification, {"migration": "migration", "search": "search", "general": "general"})
for n in ("migration", "search", "general"):
    b.add_edge(n, END)
client._graph = b.compile(checkpointer=MemorySaver())

q01 = "회사 서버가 langchain 1.x로 올라가서 이 코드가 안 돌아가요. import만 고쳐 주세요.\n\n```python\nfrom langchain.chat_models import ChatOpenAI\nfrom langchain.prompts import PromptTemplate\n\nllm = ChatOpenAI(model=\"gpt-4o-mini\", temperature=0)\nprompt = PromptTemplate.from_template(\"{topic}을 한 문장으로 설명해줘\")\nprint(llm.invoke(prompt.format(topic=\"벡터 DB\")).content)\n```"
a1 = client.ask(q01, thread_id="u:A")
print("1) 같은 대화 A · 예제 →", a1["kind"], "| 결과 있음:", bool(a1["result"]))
a2 = client.ask("안녕. 내 이름은 test야.", thread_id="u:A")
print("2) 같은 대화 A · 인사 →", a2["kind"], "| 결과 있음:", bool(a2["result"]), "| 답:", (a2["reply"] or "")[:40])
a3 = client.ask("방금 내가 이름이 뭐라고 했어?", thread_id="u:A")
print("3) 같은 대화 A · 기억 →", a3["kind"], "| 답:", (a3["reply"] or "")[:50])
a4 = client.ask("방금 내가 이름이 뭐라고 했어?", thread_id="u:B")
print("4) 다른 대화 B · 기억 →", a4["kind"], "| 답:", (a4["reply"] or "")[:50])
