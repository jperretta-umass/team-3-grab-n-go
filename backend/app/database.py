import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get('DATABASE_URL')

engine = None
SessionLocal = None
Base = declarative_base()

if DATABASE_URL:
    connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not set. Set DATABASE_URL before calling get_db()")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

