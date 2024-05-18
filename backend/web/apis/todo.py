from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from backend.ddd.application.exceptions import TodoNotFound
from backend.ddd.application.todo_application import TodoApplicationService
from backend.ddd.di.factory import get_todo_application
from backend.web.schemas import todo as TodoSchema

# https://fastapi.tiangolo.com/ja/tutorial/bigger-applications/#another-module-with-apirouter
router = APIRouter(
            prefix="/todo", 
            tags=["todo"], 
            responses={
                        404: {
                            "description": "Not found"
                        }
                    }
            )

@router.get("/", response_model=list[TodoSchema.Todo])
def get_todos(todo_application: TodoApplicationService = Depends(get_todo_application)):
    return todo_application.get_todo_list()

@router.post("/", response_model=TodoSchema.Todo)
def create_todo(
    new_todo: TodoSchema.TodoCreate,
    todo_application: TodoApplicationService = Depends(get_todo_application)
    ):
    todo = todo_application.create(new_todo=new_todo)
    return todo

@router.get("/{todo_id}", response_model=TodoSchema.Todo)
def get_todo(
    todo_id: str,
    todo_application: TodoApplicationService = Depends(get_todo_application)
    ):
    try:
        return todo_application.get_todo_by_id(todo_id=todo_id)
    except TodoNotFound:
        raise HTTPException(status_code=404, detail="Todo not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/{todo_id}", response_model=TodoSchema.Todo)
def update_todo(
    update_todo: TodoSchema.TodoUpdate,
    todo_application: TodoApplicationService = Depends(get_todo_application)
    ):
    try:
        return todo_application.update(update_todo=update_todo)
    except TodoNotFound:
        raise HTTPException(status_code=404, detail="Todo not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: str,
    todo_application: TodoApplicationService = Depends(get_todo_application)
    ):
    try:
        todo_application.delete_by_id(todo_id=todo_id)
    except TodoNotFound:
        raise HTTPException(status_code=404, detail="Todo not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")