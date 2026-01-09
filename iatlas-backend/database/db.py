from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.ENVIROMENT == "development"
)

SessionLocal = sessionmaker(autocommit=False)

Base = declarative_base()

def get_db():
    """
    Deps para FastAPI
    """

    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close