from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, SmallInteger, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model for authentication"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    groq_api_key = Column(Text, nullable=True)  # Encrypted user API key
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    usage_logs = relationship("UsageLog", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")


class Chat(Base):
    """Chat session model"""
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(200), default='New Chat')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    files = relationship("File", back_populates="chat", cascade="all, delete-orphan")


class Message(Base):
    """Message model for chat history"""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    model = Column(String(50), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    latency_ms = Column(Integer, nullable=True)  # Response time in milliseconds
    search_used = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    chat = relationship("Chat", back_populates="messages")
    feedback = relationship("Feedback", back_populates="message", cascade="all, delete-orphan")


class File(Base):
    """Uploaded files model"""
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=True)  # In bytes
    file_type = Column(String(10), nullable=True)  # pdf, docx, csv, etc.
    chunks_count = Column(Integer, nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chat = relationship("Chat", back_populates="files")
    embeddings = relationship("EmbeddingMetadata", back_populates="file", cascade="all, delete-orphan")


class EmbeddingMetadata(Base):
    """Embedding metadata for tracking vector storage"""
    __tablename__ = 'embeddings_metadata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey('files.id', ondelete='CASCADE'), nullable=False)
    collection_name = Column(String(100), nullable=True)
    embedding_model = Column(String(100), default='all-MiniLM-L6-v2')
    chunks_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    file = relationship("File", back_populates="embeddings")


class UsageLog(Base):
    """API usage and performance logs"""
    __tablename__ = 'usage_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    endpoint = Column(String(100), nullable=True)
    request_data = Column(JSON, nullable=True)  # Store as JSON
    response_time_ms = Column(Integer, nullable=True)
    status_code = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="usage_logs")


class Feedback(Base):
    """User feedback on messages"""
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('messages.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating = Column(SmallInteger, nullable=False)  # -1 for thumbs down, 1 for thumbs up
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    message = relationship("Message", back_populates="feedback")
    user = relationship("User", back_populates="feedback")


# Legacy model - keeping for migration compatibility
class ChatHistory(Base):
    """Legacy chat history model - will be migrated to new schema"""
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