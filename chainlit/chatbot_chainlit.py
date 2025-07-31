import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from chainlit import on_message, Message

from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from database.models import ChatHistory
from database.database import SessionLocal

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# LLM Configuration
llm = ChatGroq(
    api_key=groq_api_key,
    model="meta-llama/llama-4-maverick-17b-128e-instruct"
)

# Embedding & Retriever
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS vectorstore (make sure it's already created)
retriever = FAISS.load_local(
    "vectorstore/db_faiss",  
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
).as_retriever()


# RAG Chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Save chat to DB
def save_chat(session_id, user_query, bot_response, model_used, response_time):
    db = SessionLocal()
    chat_entry = ChatHistory(
        session_id=session_id,
        user_query=user_query,
        bot_response=bot_response,
        model_used=model_used,
        response_time=response_time
    )
    db.add(chat_entry)
    db.commit()
    db.close()

# Chainlit Message Handler
@on_message
async def handle_message(message):
    start_time = time.time()
    
    response = rag_chain.invoke({"query": message.content})
    response_time = round(time.time() - start_time, 3)

    # Send the response to the user
    await Message(content=response["result"]).send()

    # Save to database
    save_chat(
        session_id=str(message.session_id),
        user_query=message.content,
        bot_response=response["result"],
        model_used="meta-llama/llama-4-maverick-17b-128e-instruct",
        response_time=response_time
    )
