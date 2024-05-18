import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from injector import Injector

from backend.config.di import RepositoryModule
from backend.infrastructure.database import DATABASE_URL, SessionLocal
from backend.infrastructure.repositories.interfaces import ITodoRepository
from backend.infrastructure.repositories.models.todo import Todo as TodoModel

ALEMBIC_INI_FILE_PATH = Path.cwd().parent.parent.parent/ Path("alembic.ini")
MIGRATION_DIRECTORY_PATH = Path.cwd().parent.parent.parent / Path("alembic")

injector = Injector([RepositoryModule()])

@pytest.fixture(scope="function", autouse=True)
def migration():
    
    # ------------------
    # Alembic configurationをテスト用に設定
    # ------------------
    # https://alembic.sqlalchemy.org/en/latest/api/config.html#configuration
    alembic_cfg = Config(ALEMBIC_INI_FILE_PATH.as_posix())
    alembic_cfg.set_main_option("script_location", MIGRATION_DIRECTORY_PATH.as_posix())
    # https://docs.sqlalchemy.org/en/20/core/engines.html#sqlite
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
    
    # Migrationを実行
    # https://alembic.sqlalchemy.org/en/latest/api/commands.html#commands
    command.upgrade(config=alembic_cfg, revision="heads")
    
    yield
    
    os.remove(DATABASE_URL.split("///")[1])


def test_sample():
    
    todo = TodoModel(
        title="title",
        comment="comment",
    )
    
    with SessionLocal() as session:
        session.add(todo)
        session.commit()
        todos = session.query(TodoModel).all()
        
    print(todos[0])

def test_repository():
    
    todo_repository = injector.get(ITodoRepository)
    
    with SessionLocal() as session:
        todos = todo_repository(session=session).get_all()
    
    print(todos)
        
    
    
