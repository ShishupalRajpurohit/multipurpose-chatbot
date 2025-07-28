import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import os
import time
from dotenv import load_dotenv
from chainlit import on_message, Message
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# from data.sqldb_database import SessionLocal
from table.sqldb_models import ChatHistory
from table.sqldb_database import SessionLocal

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# LLM Configuration
llm = ChatGroq(
    api_key=groq_api_key,
    model="meta-llama/llama-4-maverick-17b-128e-instruct"
)

# Prompt Template
prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant. Answer the following question:\n\n{question}"
)

# Function to save to database
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
    chain = prompt | llm

    start_time = time.time()
    response = chain.invoke({"question": message.content})
    response_time = round(time.time() - start_time, 3)

    await Message(content=response.content).send()

    save_chat(
        session_id=str(message.session_id),
        user_query=message.content,
        bot_response=response.content,
        model_used="meta-llama/llama-4-maverick-17b-128e-instruct",
        response_time=response_time
    )
