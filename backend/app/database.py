import os
<<<<<<< HEAD
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
=======

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
>>>>>>> 5c74acb (Add customer API endpoints and new order tables)

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = None
<<<<<<< HEAD
SessionLocal: Optional[sessionmaker[Session]] = None
=======
SessionLocal = None
>>>>>>> 5c74acb (Add customer API endpoints and new order tables)
Base = declarative_base()

if DATABASE_URL:
    connect_args = (
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    )
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    if SessionLocal is None:
        raise RuntimeError(
            "DATABASE_URL is not set. Set DATABASE_URL before calling get_db()"
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
