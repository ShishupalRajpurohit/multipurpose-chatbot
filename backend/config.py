import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:localdb@localhost:5432/localdb"
    )
    
    # LLM Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DEFAULT_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
    
    # Qdrant Configuration
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    QDRANT_COLLECTION = "multipurpose_chatbot"
    
    # Embeddings
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # File Upload
    UPLOAD_FOLDER = "uploads"
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB in bytes
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'csv', 'xlsx', 'json', 'txt'}
    
    # Search Configuration
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    SEARCH_ENABLED = True
    
    # Chainlit Configuration
    CHAINLIT_URL = os.getenv("CHAINLIT_URL", "http://localhost:8000")
    
    # Flask Configuration
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    @staticmethod
    def init_app():
        """Initialize application directories"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = "sqlite:///test.db"


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}