# backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file, especially for local development
load_dotenv()

# --- PRODUCTION-AWARE DATABASE URL ---
# Deployment platforms like Render provide a single DATABASE_URL.
# We prioritize using it if it exists.
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not provided (i.e., we are running locally with docker-compose),
# we construct it from the individual parts in our .env file.
if not DATABASE_URL:
    print("DATABASE_URL not found, building from local .env variables...")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_HOST = "db" # This is the service name from our docker-compose.yml
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

# Final check to ensure we have a database URL
if not DATABASE_URL or "None" in DATABASE_URL: # Check for None string from os.getenv
    raise ValueError("Database configuration is missing or invalid!")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A base class for our models to inherit from
Base = declarative_base()

# Dependency to get a database session in our endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()