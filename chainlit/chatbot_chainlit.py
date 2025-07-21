import os
from dotenv import load_dotenv
from chainlit import on_message, Message
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load API key from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# LLM configuration
llm = ChatGroq(
    api_key=groq_api_key,
    model="meta-llama/llama-4-maverick-17b-128e-instruct"
)

# Prompt template
prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant. Answer the following question:\n\n{question}"
)

# Handle incoming messages
@on_message
async def handle_message(message):
    chain = prompt | llm
    response = chain.invoke({"question": message.content})

    await Message(content=response.content).send()
