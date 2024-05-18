import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

# https://docs.sqlalchemy.org/en/20/core/pooling.html#disconnect-handling-pessimistic
engine = create_engine(url=DATABASE_URL, pool_pre_ping=True)


# https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
# 
session_factory = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
