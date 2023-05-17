from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# https://docs.sqlalchemy.org/en/20/core/pooling.html#disconnect-handling-pessimistic
engine = create_engine(url="postgresql://todo_app:password@postgresql15/tododb", pool_pre_ping=True)

# https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
SessionLocal = sessionmaker(bind=engine, autoflush=False)
