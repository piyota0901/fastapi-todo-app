from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from backend.ddd.domain.entities.todo import Todo


class Base(DeclarativeBase):
    """
    # https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models
    """
    pass


class TodoModel(Base):
    """Todo Database model.
    # https://docs.sqlalchemy.org/en/20/orm/quickstart.html
    """
    __tablename__ = 'todos'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    is_done: Mapped[bool] = mapped_column(nullable=False)
    create_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
    
    def to_entity(self) -> Todo:
        return Todo(
            id=self.id,
            title=self.title,
            description=self.description,
            is_done=self.is_done,
            create_at=self.create_at,
            updated_at=self.updated_at
        )
    
    def __repr__(self):
        return f"TodoModel(id={self.id!r}, title={self.title!r}, description={self.description!r}, is_done={self.is_done!r}, create_at={self.create_at!r}, updated_at={self.updated_at!r})"
    
    @classmethod
    def from_entity(cls, todo: Todo) -> 'TodoModel':
        return cls(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            is_done=todo.is_done,
            create_at=todo.create_at,
            updated_at=todo.updated_at
        )