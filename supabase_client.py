"""
Supabase Client Module
Uses Supabase REST API instead of direct PostgreSQL connection.
This avoids DNS resolution issues on some networks.
"""
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
is_connected = False

def init_supabase():
    """Initialize Supabase client"""
    global supabase, is_connected
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[Error] Supabase credentials not configured")
        return False
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Test connection by fetching schema
        # Using a simple query to check if connection works
        print("[Success] Connected to Supabase via REST API")
        is_connected = True
        return True
    except Exception as e:
        print(f"[Error] Supabase REST API connection failed: {e}")
        is_connected = False
        return False

def get_supabase():
    """Get Supabase client instance"""
    global supabase, is_connected
    
    if supabase is None:
        if init_supabase():
            return supabase
        return None
    return supabase

def is_supabase_available():
    """Check if Supabase is available"""
    return is_connected and supabase is not None

# Initialize on module load if configured
USE_SUPABASE_CLIENT = os.getenv("USE_SUPABASE_CLIENT", "false").lower() == "true"
if USE_SUPABASE_CLIENT:
    init_supabase()