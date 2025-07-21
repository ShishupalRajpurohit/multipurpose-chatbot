import os
import chainlit as cl
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq 

load_dotenv(find_dotenv()) 

model = ChatGroq(model_name="meta-llama/llama-4-maverick-17b-128e-instruct",  # Fast, free model from Groq
                 temperature=0.0,
                 groq_api_key=os.environ["GROQ_API_KEY"],  # API key from your .env file
                )

@cl.on_message
async def message_handler(message: cl.message):
    user_input = message.content #user input
    response = model.generate_content(user_input)
    await cl.on_message(content= response.text).send()