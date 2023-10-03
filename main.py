import os
import sys
from fastapi import FastAPI
from typing import Optional, List, Dict, Set, Tuple, Union, Any, Literal, Text
from pydantic import BaseModel  # Models to specify the data types.
from datetime import datetime
import socket
import asyncio

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
print(project_root)

app = FastAPI()

# This is a model for the user, contains all the information needed for login.


class User(BaseModel):
    username: str
    password: str


async def receive_new_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "localhost"
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen()
    print(host, port)
    print("Server is listening for connections...")
    client_socket, addr = server_socket.accept()
    print("Connection established with:", str(addr))

    while True:
        try:
            client_socket, addr = server_socket.accept()
            print("Connection established with:", str(addr))

            while True:
                data = client_socket.recv(4096).decode()
                print("From user:", str(data))
                client_socket.send(data.encode())
        except Exception as e:
            server_socket.close()
            print("Connection closed:", str(e))
            client_socket.close()
            break


async def run_socket_server():
    while True:
        await receive_new_socket()


@app.get("/")
async def root():
    await run_socket_server()
    # return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}


# @app.post("/login")
# async def login(user, password) -> bool:
#     is_valid = False
#     print(user, password, end=" ")
#     print('is valid?', is_valid)
#     is_valid = login(user, password)
#     print('is vlaid?', is_valid,)
#     return is_valid


# @app.post("/register")
# async def register():
#     return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}
