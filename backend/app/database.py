from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = 'sqlite:///dining_hall.db'

MockSession = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(DATABASE_URL))

class Base(DeclarativeBase):
    pass

def get_db():
    db = MockSession()
    try:
        yield db
    finally:
        db.close()