import os
import sys
import uvicorn
from fastapi import FastAPI, BackgroundTasks
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


active_sockets = []


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print('reader', reader)
    print('writer', writer)
    print("Connection established with:", str(addr))

    while True:
        data = await reader.read(4096)
        if not data:
            print('NO DATA RECEIVED')
            break
        data = data.decode('utf-8')
        print('DATAAAAAA ', data)
        print(f"From user {str(addr)}:", str(data))
        writer.write(data.encode('utf-8'))
        await writer.drain()

    print("Connection closed:", str(addr))
    writer.close()


@app.on_event("startup")
async def main():
    host = "localhost"
    port = 12345
    server = await asyncio.start_server(handle_client, host, port)
    async with server:
        print("Server is listening for connections...")
        await server.serve_forever()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(app, host="0.0.0.0", port=8000)
