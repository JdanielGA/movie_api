from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    email: str =  Field(default='user@email.com', min_length=5, max_length=50)
    password: str = Field(default='password', min_length=5, max_length=50)