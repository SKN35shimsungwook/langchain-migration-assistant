import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from langchain_core.messages import HumanMessage
from src.ui.client import _pipeline
graph, why = _pipeline()
text = "안녕. 내 이름은 test야."
final = None
for ns, mode, data in graph.stream({"question": text, "messages": [HumanMessage(content=text)]},
                                   stream_mode=["updates", "values"], subgraphs=True):
    if mode == "updates":
        print("update:", ns, list(data.keys()), {k: (list(v.keys()) if isinstance(v, dict) else type(v).__name__) for k, v in data.items()})
    elif not ns:
        final = data
print("최종 state 키:", sorted(final.keys()))
print("classification:", final.get("classification"), "| verify_result 있음:", final.get("verify_result") is not None,
      "| old_code:", repr((final.get("old_code") or "")[:60]))
