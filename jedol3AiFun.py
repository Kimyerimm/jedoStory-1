import json
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.document_loaders import WebBaseLoader,UnstructuredURLLoader
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv;load_dotenv() # openai_key  .env 선언 사용 
import jedol1Fun as jshs
from datetime import datetime, timedelta
from langchain.memory import ChatMessageHistory
import jedol2ChatDbFun as chatDB

def vectorDB_create(vector_folder=""):
    # AI 역할
    documents=[ Document(
                page_content=f"""
                오늘은 {jshs.today_date_and_weekday(week="true")}이다.
                나는 제주과학고등학교 1학년에 재학 중입니다.
                나의 이름은 '제돌이'입니다.
                나의 나이는 16세입니다.
                나는 인공지능 기초를 재미있게 배우고 있습니다. 
                나는 코딩을 잘 합니다.
                학교에 관련된 궁금한 점이 있으면 질문하십시요.\n\n""", 
                metadata={'source': 'jedolStory'}
                )
    ]


    
    # 학교연혁 
    # txt 파일 사용용
    loader = TextLoader("data\history.txt", encoding='utf-8')
    # html 사용
    loader = WebBaseLoader(web_path="https://jeju-s.jje.hs.kr/jeju-s/0102/history")

    page=loader.load()[0]
    page.page_content=jshs.html_parsing_text(
                    page_content=page.page_content,
                    start_str="학교연혁 연혁 기본 리스트 년 도 날 짜 내 용",
                    end_str="열람하신 정보에 대해 만족하십니까",
                    length=20,
                    removeword=[]
                    )

    documents.append( Document(
                        page_content=page.page_content,
                        metadata=page.metadata
                        )
                    )

    # print(page)
    # quit()
    # 주소
    loader = WebBaseLoader(web_path="https://jeju-s.jje.hs.kr/jeju-s/0102/history")
    page=loader.load()[0]
    page.page_content=jshs.html_parsing_text(
                    page_content=page.page_content,
                    start_str="우[",
                    end_str="Copyright",
                    length=20,
                    removeword=[]
                    )
    documents.append( Document(
                        page_content=page.page_content,
                        metadata=page.metadata
                        )
                    )

    # 식단-----------------------
    

    today = datetime.now().today()
    date1 = today - timedelta(days=2)
    date2 = today + timedelta(days=5)
    date1=date1.strftime('%Y-%m-%d')
    date2=date2.strftime('%Y-%m-%d')
    loader = WebBaseLoader(web_path=f"https://api.salvion.kr/of=T10&sc=9290066&ac=date&sd={date1}&ed={date2}&code=all")

    page=loader.load()[0]
    page_content= json.loads(page.page_content)
    page_content= jshs.getMealMenuNeis(page_content=page_content)

    documents.append( Document(
                        page_content=page_content,
                        metadata=page.metadata
                        )
                    )

    # 학사일정-------------------------------------------
    documents.append( Document(
                            page_content=jshs.school_schedule(datetime.now().today().year),
                            metadata={'source': '홈페이지'}
                        )
                    )

    #  문서를 페이지로 -----------------------------------
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size =1000, # 이 숫자는 매우 중요
            chunk_overlap =0, # 필요에 따라 사용
            separators=["\n\n","\n",", "], # 결국 페이지 분리를 어떻게 하느냐 가 답변의 질을 결정
            length_function =jshs.tiktoken_len
    )

    pages = text_splitter.split_documents(documents)

    # jshs.splitter_pages_viewer(pages);quit()

    vectorDB = FAISS.from_documents(pages , OpenAIEmbeddings())
    vectorDB.save_local(vector_folder)
    return  vector_folder

def ai_reponse( vector_folder, query, token ):
    
    vectorDB = FAISS.load_local(vector_folder, OpenAIEmbeddings())

    llm_model = ChatOpenAI(model_name="gpt-4", temperature=0)  

    chain = load_qa_chain(llm_model, chain_type="stuff")
    
    docs = vectorDB.similarity_search(query)

   # AI 역할
    chat_history=chatDB.query_history(token)

    if  chat_history !="":
        print( "token=",token )
        print( chat_history )
        chat_history=Document(
                        page_content=f" {  chat_history }", 
                        metadata={'source': 'chat history'}
                        )   
        docs.append(chat_history)

    res = chain.run(input_documents=docs, question=query)
    new_history=' 질문: '+ query +'\n  답변: '+ res
    chatDB.update_history(token,new_history,4000)
         
    return res

if __name__ == "__main__":
      today = str( datetime.now().date().today())
      print( f"vectorDB-faiss-jshs-{today}")
      token="run-jedolAi_function" 
      chatDB.setup_db()
      chatDB.new_user(token)
      print(ai_reponse(f"vectorDB-faiss-jshs-{today}", "안녕 ?",token))