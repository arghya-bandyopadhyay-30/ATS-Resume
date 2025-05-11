from fastapi import FastAPI
from src.backend.email_sender.api import email_controller

app = FastAPI()
app.include_router(email_controller.router)
