from pydantic import BaseModel
from typing import Optional

# Define a Pydantic model for login request
class LoginRequest(BaseModel):
    username: str
    password: str


