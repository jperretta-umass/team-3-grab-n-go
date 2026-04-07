import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.env.get('DATABASE_URL')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
MockSession = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(DATABASE_URL))
Base = DeclarativeBase()