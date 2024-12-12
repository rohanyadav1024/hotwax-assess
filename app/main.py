from fastapi import FastAPI,HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import orders, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router)
app.include_router(auth.router)