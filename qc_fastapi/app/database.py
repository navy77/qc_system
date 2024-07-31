from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

server = os.getenv("SERVER")
database = os.getenv("DATABASE")
user_login = os.getenv("USER_LOGIN")
password = os.getenv("PASSWORD")

encoded_password = urllib.parse.quote_plus(password)

DATABASE_URL = f'mssql+pymssql://{user_login}:{encoded_password}@{server}/{database}'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()