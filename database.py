from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Try Supabase REST API client first
USE_SUPABASE_CLIENT = os.getenv("USE_SUPABASE_CLIENT", "false").lower() == "true"

if USE_SUPABASE_CLIENT:
    try:
        from supabase_client import is_supabase_available, get_supabase
        
        if is_supabase_available():
            print("[Success] Using Supabase REST API client")
            # For REST API, we'll use SQLite as the ORM engine but route queries through Supabase
            DATABASE_URL = "sqlite:///./cafe.db"
            engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        else:
            raise Exception("Supabase REST API not available")
    except ImportError:
        print("[Error] Supabase client not available, falling back to direct connection")
        USE_SUPABASE_CLIENT = False

if not USE_SUPABASE_CLIENT:
    # Get database URL from environment variable
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set in .env file")

    # Try to create engine and test connection
    try:
        # Create engine with connection pool settings suitable for Supabase
        engine = create_engine(
            DATABASE_URL,
            connect_args={"sslmode": "require"},  # SSL is required for Supabase
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True  # Enable connection health checks
        )
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[Success] Connected to Supabase database")
    except Exception as e:
        print(f" Supabase connection failed: {e}")
        print("Falling back to local SQLite database")
        DATABASE_URL = "sqlite:///./cafe.db"
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
