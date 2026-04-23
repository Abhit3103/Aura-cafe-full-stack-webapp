"""
Check current menu items in database
"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

with engine.connect() as conn:
    result = conn.execute(text("SELECT id, name, price, image, description FROM menu"))
    rows = result.fetchall()
    
    print(f"Found {len(rows)} menu items:\n")
    for row in rows:
        print(f"ID: {row.id}")
        print(f"Name: {row.name}")
        print(f"Price: {row.price}")
        print(f"Image: {row.image if row.image else 'NULL'}")
        print(f"Description: {row.description if row.description else 'NULL'}")
        print("-" * 50)