from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=True)
    user_query = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    model_used = Column(String(100), nullable=True)
    response_time = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_type = Column(String(50), nullable=True)
    meta_data = Column(Text, nullable=True)
