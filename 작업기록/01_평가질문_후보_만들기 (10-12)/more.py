import json, sys

REF = "https://docs.langchain.com/oss/python/migrate/langchain-v1"
M = [
 # ---------------- easy (5) ----------------
 ("easy_06", "easy",
'''from langchain.schema.output_parser import StrOutputParser
from langchain.schema import Document

parser = StrOutputParser()
doc = Document(page_content="LangChain 문서", metadata={"source": "a.txt"})
print(parser, doc)''',
 "langchain.schema 하위 모듈이 제거됨. 출력 파서와 Document는 langchain-core로 이동",
 "from langchain_core.output_parsers import StrOutputParser\nfrom langchain_core.documents import Document"),

 ("easy_07", "easy",
'''from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0)
with get_openai_callback() as cb:
    pass  # llm.invoke("안녕")
    print(cb.total_tokens)''',
 "langchain.callbacks 모듈이 제거됨. get_openai_callback은 langchain-community로 이동",
 "from langchain_community.callbacks import get_openai_callback\nfrom langchain_openai import ChatOpenAI"),

 ("easy_08", "easy",
'''from langchain.document_loaders import PyPDFLoader, WebBaseLoader, CSVLoader

pdf_loader = PyPDFLoader("report.pdf")
web_loader = WebBaseLoader("https://example.com")
csv_loader = CSVLoader("data.csv")
print(pdf_loader, web_loader, csv_loader)''',
 "문서 로더가 langchain-community로 분리됨",
 "from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, CSVLoader"),

 ("easy_09", "easy",
'''from langchain.prompts import ChatPromptTemplate, FewShotPromptTemplate, PromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate

system = SystemMessagePromptTemplate.from_template("너는 {role}이다")
human = HumanMessagePromptTemplate.from_template("{question}")
chat_prompt = ChatPromptTemplate.from_messages([system, human])
example_prompt = PromptTemplate.from_template("Q: {q}\\nA: {a}")
few_shot = FewShotPromptTemplate(examples=[{"q": "1+1", "a": "2"}], example_prompt=example_prompt,
                                 suffix="Q: {input}\\nA:", input_variables=["input"])
print(chat_prompt, few_shot)''',
 "langchain.prompts 모듈이 제거됨. 모든 프롬프트 템플릿은 langchain-core로 이동",
 "from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, PromptTemplate\nfrom langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate"),

 ("easy_10", "easy",
'''from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import Chroma

bm25 = BM25Retriever.from_texts(["LangChain", "LangGraph"])
print(bm25, EnsembleRetriever, Chroma)''',
 "langchain.retrievers, langchain.vectorstores가 제거됨. BM25는 langchain-community, EnsembleRetriever는 langchain-classic으로 이동",
 "from langchain_community.retrievers import BM25Retriever\nfrom langchain_classic.retrievers import EnsembleRetriever\nfrom langchain_community.vectorstores import Chroma"),

 # ---------------- medium (6) ----------------
 ("medium_05", "medium",
'''from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

vectorstore = FAISS.from_texts(["LangChain 1.0은 2025년에 출시됐다"], OpenAIEmbeddings())
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(), vectorstore.as_retriever(), memory=memory)
# qa({"question": "LangChain 1.0은 언제 나왔어?"})''',
 "ConversationalRetrievalChain과 Memory가 제거됨. 대화 기록을 포함한 RAG는 LCEL과 MessagesPlaceholder로 직접 구성",
 "from langchain_openai import ChatOpenAI, OpenAIEmbeddings\nfrom langchain_community.vectorstores import FAISS\nfrom langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder\nfrom langchain_core.runnables import RunnablePassthrough"),

 ("medium_06", "medium",
'''from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

docs = [Document(page_content="첫 번째 문단"), Document(page_content="두 번째 문단")]
chain = load_summarize_chain(ChatOpenAI(temperature=0), chain_type="stuff")
# chain.run(docs)''',
 "load_summarize_chain과 langchain.docstore가 제거됨. 요약은 LCEL(prompt | llm | parser)로 구성",
 "from langchain_openai import ChatOpenAI\nfrom langchain_core.documents import Document\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser"),

 ("medium_07", "medium",
'''from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chains import LLMChain

schemas = [ResponseSchema(name="name", description="사람 이름"),
           ResponseSchema(name="age", description="나이")]
parser = StructuredOutputParser.from_response_schemas(schemas)
prompt = PromptTemplate(template="{text}에서 정보를 뽑아줘\\n{format}", input_variables=["text"],
                        partial_variables={"format": parser.get_format_instructions()})
chain = LLMChain(llm=ChatOpenAI(temperature=0), prompt=prompt, output_parser=parser)
# chain.run(text="철수는 20살이다")''',
 "langchain.output_parsers와 LLMChain이 제거됨. 구조화 출력은 Pydantic 모델 + with_structured_output 사용",
 "from langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import PromptTemplate\nfrom pydantic import BaseModel, Field"),

 ("medium_08", "medium",
'''from langchain.chat_models import ChatOpenAI
from langchain.chains.router import MultiPromptChain

prompt_infos = [
    {"name": "math", "description": "수학 질문", "prompt_template": "수학 선생님으로서 답해줘: {input}"},
    {"name": "history", "description": "역사 질문", "prompt_template": "역사 선생님으로서 답해줘: {input}"},
]
chain = MultiPromptChain.from_prompts(ChatOpenAI(temperature=0), prompt_infos, verbose=True)
# chain.run("임진왜란은 언제 일어났어?")''',
 "MultiPromptChain(라우터 체인)이 제거됨. 분기는 RunnableBranch나 RunnableLambda로 구성",
 "from langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.runnables import RunnableBranch, RunnableLambda\nfrom langchain_core.output_parsers import StrOutputParser"),

 ("medium_09", "medium",
'''from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

llm = OpenAI(temperature=0)
review_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template("{product} 리뷰를 써줘"), output_key="review")
summary_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template("요약해줘: {review}"), output_key="summary")
overall = SequentialChain(chains=[review_chain, summary_chain],
                          input_variables=["product"], output_variables=["review", "summary"])
# overall({"product": "무선 이어폰"})''',
 "SequentialChain과 output_key 방식이 제거됨. 중간 결과를 함께 넘기려면 RunnablePassthrough.assign 사용",
 "from langchain_openai import OpenAI\nfrom langchain_core.prompts import PromptTemplate\nfrom langchain_core.runnables import RunnablePassthrough\nfrom langchain_core.output_parsers import StrOutputParser"),

 ("medium_10", "medium",
'''from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.schema import Document

docs = [Document(page_content="LangGraph는 상태 기반 에이전트 프레임워크다")]
chain = load_qa_chain(ChatOpenAI(temperature=0), chain_type="stuff")
# chain.run(input_documents=docs, question="LangGraph가 뭐야?")''',
 "load_qa_chain이 제거됨. 문서 기반 질의응답은 문서를 프롬프트에 넣는 LCEL 체인으로 구성",
 "from langchain_openai import ChatOpenAI\nfrom langchain_core.documents import Document\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser"),

 # ---------------- hard (7) ----------------
 ("hard_04", "hard",
'''from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain import hub

@tool
def get_weather(city: str) -> str:
    """도시의 날씨를 알려준다"""
    return f"{city}는 맑음"

prompt = hub.pull("hwchase17/react")
agent = create_react_agent(ChatOpenAI(temperature=0), [get_weather], prompt)
executor = AgentExecutor(agent=agent, tools=[get_weather], handle_parsing_errors=True)
# executor.invoke({"input": "서울 날씨 어때?"})''',
 "create_react_agent(langchain 버전), AgentExecutor, hub가 제거됨. ReAct 에이전트는 create_agent로 대체",
 "from langchain_openai import ChatOpenAI\nfrom langchain.agents import create_agent\nfrom langchain.tools import tool"),

 ("hard_05", "hard",
'''from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """두 수를 더한다"""
    return a + b

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 계산을 도와주는 비서다"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])
agent = create_tool_calling_agent(ChatOpenAI(temperature=0), [add], prompt)
executor = AgentExecutor(agent=agent, tools=[add], verbose=True)
# executor.invoke({"input": "15 더하기 27은?"})''',
 "create_tool_calling_agent와 AgentExecutor가 제거됨. agent_scratchpad 프롬프트 없이 create_agent(model, tools, system_prompt=...)로 대체",
 "from langchain_openai import ChatOpenAI\nfrom langchain.agents import create_agent\nfrom langchain.tools import tool"),

 ("hard_06", "hard",
'''from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///shop.db")
llm = ChatOpenAI(temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)
# agent.run("가장 많이 팔린 상품은?")''',
 "create_sql_agent와 langchain.sql_database가 제거됨. SQL 도구는 langchain-community에서 가져와 create_agent에 연결",
 "from langchain_openai import ChatOpenAI\nfrom langchain.agents import create_agent\nfrom langchain_community.agent_toolkits import SQLDatabaseToolkit\nfrom langchain_community.utilities import SQLDatabase"),

 ("hard_07", "hard",
'''from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool

@tool
def remember_name(name: str) -> str:
    """사용자 이름을 기록한다"""
    return f"{name}님 반가워요"

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 친절한 비서다"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])
memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
agent = create_tool_calling_agent(ChatOpenAI(), [remember_name], prompt)
executor = AgentExecutor(agent=agent, tools=[remember_name], memory=memory)
# executor.invoke({"input": "내 이름은 영희야"})''',
 "AgentExecutor의 memory 방식이 제거됨. 대화 기억은 create_agent + 체크포인터(InMemorySaver)와 thread_id로 관리",
 "from langchain_openai import ChatOpenAI\nfrom langchain.agents import create_agent\nfrom langchain.tools import tool\nfrom langgraph.checkpoint.memory import InMemorySaver"),

 ("hard_08", "hard",
'''from langchain.llms import OpenAI
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor
from langchain.chains import LLMChain

def search(query: str) -> str:
    return "검색 결과: " + query

tools = [Tool(name="Search", func=search, description="검색할 때 사용")]
prompt = ZeroShotAgent.create_prompt(tools, prefix="질문에 답해라.", suffix="질문: {input}\\n{agent_scratchpad}",
                                     input_variables=["input", "agent_scratchpad"])
llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
# executor.run("LangChain 최신 버전은?")''',
 "ZeroShotAgent, AgentExecutor, LLMChain 기반 커스텀 에이전트가 모두 제거됨. create_agent로 대체",
 "from langchain_openai import ChatOpenAI\nfrom langchain.agents import create_agent\nfrom langchain.tools import tool"),

 ("hard_09", "hard",
'''from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import create_retriever_tool, create_conversational_retrieval_agent
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

vectorstore = FAISS.from_texts(["환불은 7일 이내 가능하다"], OpenAIEmbeddings())
retriever_tool = create_retriever_tool(vectorstore.as_retriever(), "policy_search", "회사 정책을 검색한다")
agent = create_conversational_retrieval_agent(ChatOpenAI(temperature=0), [retriever_tool], verbose=True)
# agent({"input": "환불 기간이 어떻게 돼?"})''',
 "create_conversational_retrieval_agent가 제거됨. 검색 도구를 만들어 create_agent에 연결 (Agentic RAG)",
 "from langchain_openai import ChatOpenAI, OpenAIEmbeddings\nfrom langchain_community.vectorstores import FAISS\nfrom langchain_core.tools import create_retriever_tool\nfrom langchain.agents import create_agent"),

 ("hard_10", "hard",
'''from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.tools.render import format_tool_to_openai_function
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import StructuredTool

def word_count(text: str) -> int:
    return len(text.split())

tools = [StructuredTool.from_function(word_count, description="단어 수를 센다")]
llm = ChatOpenAI(temperature=0).bind(functions=[format_tool_to_openai_function(t) for t in tools])
prompt = ChatPromptTemplate.from_messages([("human", "{input}"), MessagesPlaceholder("agent_scratchpad")])
agent = (
    {"input": lambda x: x["input"],
     "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"])}
    | prompt | llm | OpenAIFunctionsAgentOutputParser()
)
executor = AgentExecutor(agent=agent, tools=tools)
# executor.invoke({"input": "'나는 오늘 공부한다'는 몇 단어야?"})''',
 "LCEL로 직접 조립한 OpenAI Functions 에이전트(format_scratchpad, output_parsers, AgentExecutor)가 제거됨. create_agent 한 줄로 대체",
 "from langchain_openai import ChatOpenAI\nfrom langchain.agents import create_agent\nfrom langchain_core.tools import StructuredTool"),
]

sample = json.load(open(sys.argv[1], encoding="utf-8"))
new = [{"id": i, "difficulty": d, "old_code": o, "why_broken": w, "target_imports": t,
        "reference": REF, "verified_new_fails": False, "verified_old": False} for i, d, o, w, t in M]
order = {"easy": 0, "medium": 1, "hard": 2}
allitems = sorted(sample + new, key=lambda x: (order[x["difficulty"]], x["id"]))
json.dump(allitems, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(new), len(allitems))
