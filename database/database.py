from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:localdb@localhost:5432/localdb"
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,
    max_overflow=10,
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Thread-safe session
db_session = scoped_session(SessionLocal)


def init_db():
    """Initialize database tables"""
    from .models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def drop_all_tables():
    """Drop all tables (use with caution!)"""
    from .models import Base
    Base.metadata.drop_all(bind=engine)
    print("⚠️ All tables dropped")


@contextmanager
def get_db():
    """
    Context manager for database sessions
    Usage:
        with get_db() as db:
            db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_db_session():
    """
    Get database session (for dependency injection)
    Usage in Flask:
        db = get_db_session()
        try:
            # your code
        finally:
            db.close()
    """
    return SessionLocal()


# Test connection function
def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


# Initialize database on import (optional - comment out if not needed)
if __name__ == "__main__":
    print("Testing database connection...")
    test_connection()
    print("\nInitializing database tables...")
    init_db()