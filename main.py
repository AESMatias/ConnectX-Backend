import os
import sys
import uvicorn
from starlette.responses import RedirectResponse
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QRunnable, QThreadPool
from fastapi import FastAPI, BackgroundTasks
from app.routes.uploadfiles import files
from app.routes.user import user
from app.routes.auth import auth
from typing import Optional, List, Dict, Set, Tuple, Union, Any, Literal, Text
from pydantic import BaseModel  # Models to specify the data types.
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
print(project_root)

app = FastAPI()
app.include_router(user)
app.include_router(files)
app.include_router(auth)
# This is a model for the user, contains all the information needed for login.


class User(BaseModel):
    username: str
    password: str


active_sockets = []


async def send_to_all(message, sender) -> None:
    if active_sockets:
        for client_socket in active_sockets:
            if client_socket != sender:
                try:
                    client_socket.write(message.encode('utf-8'))
                    print('MESSAGE LOOPED TO ALL', message)
                    await client_socket.drain()
                except Exception as e:
                    print("Error sending message:", str(e))
                    await client_socket.drain()


def close_connection(writer, addr) -> bool:
    try:
        if active_sockets:
            for client_socket in active_sockets:
                if client_socket == writer:
                    writer.write('close_the_connection'.encode('utf-8'))
                    print(f'{addr} has been closed')
                    writer.close()
                    active_sockets.remove(writer)
                    return True
    except Exception as e:
        print(f"Error closing connection {addr} with Exception:", str(e))
        return False


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    # print('READER', reader)
    # print('WRITER', writer)
    print("Connection established with:", str(addr))
    active_sockets.append(writer)

    try:
        while True:
            data = await reader.read(4096)
            if not data:
                continue
            elif data.decode('utf-8').lower().endswith('close')\
                    or data.decode('utf-8').lower().endswith('exit'):
                print(f'The user {addr} wants to exit', str(addr))
                has_been_closed = close_connection(writer, addr)
                print('The session has been closed?', has_been_closed)
                await send_to_all(f'The user {addr} has left the chat', writer)
                continue
            data = data.decode('utf-8')
            print(f"From user {str(addr)}:", str(data))
            await send_to_all(data, writer)
    except Exception as e:
        print("Error:", str(e))
    finally:
        print('finally')
        writer.close()
        active_sockets.remove(writer)


def start_server(host, port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = loop.run_until_complete(
        asyncio.start_server(handle_client, host, port))
    try:
        loop.run_until_complete(server.serve_forever())
    except KeyboardInterrupt:
        pass


@app.on_event("startup")
async def main():
    host = "localhost"
    port = 12345
    with ThreadPoolExecutor() as executor:
        executor.submit(start_server, host, port)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs/")


def run_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=8000)


def run_asyncio():
    asyncio.run(main())


if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        executor.submit(run_uvicorn)
        executor.submit(run_asyncio)
