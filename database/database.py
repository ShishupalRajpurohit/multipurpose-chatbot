from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Replace this with your actual DB credentials or load from .env
DATABASE_URL = "postgresql+psycopg2://postgres:localdb@localhost:5432/localdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
