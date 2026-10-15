import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
import src.ui.client as client
q01 = "회사 서버가 langchain 1.x로 올라가서 이 코드가 안 돌아가요. import만 고쳐 주세요.\n\n```python\nfrom langchain.chat_models import ChatOpenAI\nfrom langchain.prompts import PromptTemplate\n\nllm = ChatOpenAI(model=\"gpt-4o-mini\", temperature=0)\nprompt = PromptTemplate.from_template(\"{topic}을 한 문장으로 설명해줘\")\nprint(llm.invoke(prompt.format(topic=\"벡터 DB\")).content)\n```"
def show(n, a):
    r = a["result"]
    extra = f"검증 {'통과' if r['verification']['success'] else '실패'} · 시도 {r['verification'].get('attempts')}회" if r else (a['reply'] or '')[:60].replace('\n', ' ')
    print(f"{n} {a['kind']:9} | {extra}")
show("1 [A] 안녕 내 이름은 test야            →", client.ask("안녕. 내 이름은 test야.", thread_id="u:A"))
show("2 [A] 방금 내가 이름이 뭐라고 했어?    →", client.ask("방금 내가 이름이 뭐라고 했어?", thread_id="u:A"))
show("3 [B] 방금 내가 이름이 뭐라고 했어?    →", client.ask("방금 내가 이름이 뭐라고 했어?", thread_id="u:B"))
show("4 [A] 예제 q01 (코드 변환)           →", client.ask(q01, thread_id="u:A"))
show("5 [A] 예제 q01 한 번 더 (시도 횟수 새로) →", client.ask(q01, thread_id="u:A"))
show("6 [A] 내 이름 기억해? (변환 뒤에도)    →", client.ask("내 이름 아직 기억해?", thread_id="u:A"))
