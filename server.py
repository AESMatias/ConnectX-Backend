import os
import sys
from fastapi import FastAPI
from typing import Optional, List, Dict, Set, Tuple, Union, Any, Literal, Text
from pydantic import BaseModel  # Models to specify the data types.
from datetime import datetime
from login import login

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
print(project_root)

app = FastAPI()

# This is a model for the user, contains all the information needed for login.


class User(BaseModel):
    username: str
    password: str


@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}


@app.post("/login")
async def login(user: str, password: str) -> bool:
    is_valid = False
    print(user, user, end=" ")
    print('is valid?', is_valid)
    is_valid, response_text = login(user, password)
    print('is vlaid?', is_valid, response_text)
    return is_valid


@app.post("/register")
async def register():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}