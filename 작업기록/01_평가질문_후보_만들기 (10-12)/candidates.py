C = [
 # id, difficulty, old_code, why_broken, hint_new_imports
 ("easy_01","easy",
"""from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
print(llm)""",
 "OpenAI 채팅 모델이 langchain-openai 패키지로 분리됨",
 "from langchain_openai import ChatOpenAI"),
 ("easy_02","easy",
"""from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
print(llm)""",
 "langchain.llms 모듈이 1.x에서 제거됨. OpenAI 연동은 langchain-openai로 분리",
 "from langchain_openai import OpenAI"),
 ("easy_03","easy",
"""from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage

prompt = PromptTemplate.from_template("{topic}에 대해 설명해줘")
messages = [SystemMessage(content="너는 선생님이다"), HumanMessage(content="안녕")]
print(prompt, messages)""",
 "프롬프트와 메시지 클래스가 langchain-core로 이동, langchain.schema 제거",
 "from langchain_core.prompts import PromptTemplate\nfrom langchain_core.messages import HumanMessage, SystemMessage"),
 ("easy_04","easy",
"""from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
loader = TextLoader("sample.txt", encoding="utf-8")
print(splitter, loader)""",
 "텍스트 분할기는 langchain-text-splitters, 문서 로더는 langchain-community로 분리",
 "from langchain_text_splitters import RecursiveCharacterTextSplitter\nfrom langchain_community.document_loaders import TextLoader"),
 ("easy_05","easy",
"""from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

embeddings = OpenAIEmbeddings()
print(embeddings, FAISS)""",
 "임베딩은 langchain-openai, 벡터스토어는 langchain-community로 분리",
 "from langchain_openai import OpenAIEmbeddings\nfrom langchain_community.vectorstores import FAISS"),
 ("medium_01","medium",
"""from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(temperature=0)
prompt = PromptTemplate(input_variables=["product"], template="{product}을 만드는 회사 이름을 지어줘")
chain = LLMChain(llm=llm, prompt=prompt)
# result = chain.run(product="양말")""",
 "LLMChain이 1.x langchain에서 제거됨 (langchain-classic으로 이동). 최신 방식은 LCEL prompt | llm",
 "from langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import PromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser"),
 ("medium_02","medium",
"""from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
# conversation.predict(input="안녕")""",
 "ConversationChain과 Memory 클래스가 1.x langchain에서 제거됨. 대화 기록은 메시지 목록이나 LangGraph 체크포인터로 관리",
 "from langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder\nfrom langchain_core.chat_history import InMemoryChatMessageHistory"),
 ("medium_03","medium",
"""from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

llm = OpenAI(temperature=0)
title_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template("{topic}에 대한 블로그 제목"))
body_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template("제목: {title}\\n본문을 써줘"))
overall = SimpleSequentialChain(chains=[title_chain, body_chain])
# overall.run("LangChain")""",
 "SimpleSequentialChain이 제거됨. 최신 방식은 LCEL로 체인을 이어 붙임",
 "from langchain_openai import OpenAI\nfrom langchain_core.prompts import PromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser"),
 ("medium_04","medium",
"""from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

vectorstore = FAISS.from_texts(["LangChain은 LLM 프레임워크다"], OpenAIEmbeddings())
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=vectorstore.as_retriever())
# qa.run("LangChain이 뭐야?")""",
 "RetrievalQA가 제거됨. 최신 방식은 retriever와 prompt를 LCEL로 직접 연결",
 "from langchain_openai import ChatOpenAI, OpenAIEmbeddings\nfrom langchain_community.vectorstores import FAISS\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.runnables import RunnablePassthrough"),
 ("hard_01","hard",
"""from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool

def get_word_length(word: str) -> str:
    return str(len(word))

tools = [Tool(name="word_length", func=get_word_length, description="단어 길이를 센다")]
llm = ChatOpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
# agent.run("'LangChain'은 몇 글자야?")""",
 "initialize_agent, AgentType이 1.x에서 제거됨. 최신 방식은 langchain.agents.create_agent",
 "from langchain_openai import ChatOpenAI\nfrom langchain.agents import create_agent\nfrom langchain.tools import tool"),
 ("hard_02","hard",
"""from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain import hub

@tool
def multiply(a: int, b: int) -> int:
    \"\"\"두 수를 곱한다\"\"\"
    return a * b

prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI(temperature=0)
agent = create_openai_functions_agent(llm, [multiply], prompt)
executor = AgentExecutor(agent=agent, tools=[multiply], verbose=True)
# executor.invoke({"input": "3 곱하기 7은?"})""",
 "AgentExecutor, create_openai_functions_agent, langchain.hub가 1.x에서 제거됨. create_agent로 대체",
 "from langchain_openai import ChatOpenAI\nfrom langchain.agents import create_agent\nfrom langchain.tools import tool"),
 ("hard_03","hard",
"""from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI(temperature=0)
tools = load_tools(["llm-math"], llm=llm)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=memory, verbose=True)
# agent.run("내 이름은 철수야. 12 곱하기 3은?")""",
 "initialize_agent, load_tools, Memory가 모두 제거됨. create_agent + 체크포인터(InMemorySaver)로 대화 기억",
 "from langchain_openai import ChatOpenAI\nfrom langchain.agents import create_agent\nfrom langgraph.checkpoint.memory import InMemorySaver"),
]
