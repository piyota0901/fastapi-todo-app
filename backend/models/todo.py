from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, String, Text, Uuid

from backend.db.base_class import Base


class Todo(Base):
    __tablename__ = "todos"

    id: Any = Column(Uuid, primary_key=True, default=uuid4)
    title = Column(String(20), nullable=False)
    comment = Column(Text, nullable=False)
    is_done = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.now(), nullable=False)
