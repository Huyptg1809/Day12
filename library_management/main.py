from fastapi import FastAPI
from database import engine, Base
from models import author_model, book_model
from routers import book_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API - Day 12")

app.include_router(book_router.router)
