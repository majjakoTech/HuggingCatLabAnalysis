import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

load_dotenv()

host=os.getenv("DB_HOST");
username=os.getenv("DB_USERNAME");
password=os.getenv("DB_PASSWORD");
port=os.getenv("DB_PORT");
db_name=os.getenv("DB_NAME");

DATABASE_URL=f"postgresql://{username}:{password}@{host}:{port}/{db_name}"

engine=create_engine(DATABASE_URL)
SessionLocale=sessionmaker(bind=engine)
session=SessionLocale()

Base=declarative_base()

def get_postgres_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()
