from datetime import datetime

class Todo:
    def __init__(
        self, id: str, 
        title: str, 
        description: str, 
        is_done: bool,
        create_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.title = title
        self.description = description
        self.is_done = is_done
        self.create_at = create_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"Todo(id={self.id!r}, title={self.title!r}, description={self.description!r}, is_done={self.is_done!r}, create_at={self.create_at!r}, updated_at={self.updated_at!r})"

    def __eq__(self, other: object):
        if not isinstance(other, Todo):
            raise ValueError("Comparing Todo with a non-Todo object")
        return self.id == other.id