from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import todo

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"]
)
app.include_router(todo.router)
