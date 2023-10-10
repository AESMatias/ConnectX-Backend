import os
import sys
import uvicorn
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QRunnable, QThreadPool
from fastapi import FastAPI, BackgroundTasks
from routes.uploadfiles  import uploadfiles
from routes.user import user
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
app.include_router(uploadfiles)
# This is a model for the user, contains all the information needed for login.


class User(BaseModel):
    username: str
    password: str


active_sockets = []


async def send_to_all(message, sender):
    if active_sockets:
        for client_socket in active_sockets:
            if client_socket != sender:
                print('LOOPING', client_socket)
                try:
                    client_socket.write(message.encode('utf-8'))
                    print('MESSAGE LOOPED TO ALL', message)
                    await client_socket.drain()
                except Exception as e:
                    print("Error sending message:", str(e))


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
                print('NO DATA 1 FROM', str(addr))
                pass
            elif data.decode('utf-8') == 'exit'.lower()\
                    or data.decode('utf-8') == 'exit':
                print('NO DATA exit FROM', str(addr))
                pass
            data = data.decode('utf-8')
            print(f"From user {str(addr)}:", str(data))
            await send_to_all(data, writer)
    except Exception as e:
        print("Error:", str(e))
    finally:
        active_sockets.remove(writer)
        writer.close()

    # while True:
    #     data = await reader.read(4096)
    #     if not data:
    #         print('NO DATA RECEIVED')
    #         break
    #     data = data.decode('utf-8')
    #     print('DATAAAAAA ', data)
    #     print(f"From user {str(addr)}:", str(data))
    #     writer.write(data.encode('utf-8'))
    #     await writer.drain()

    # print("Connection closed:", str(addr))
    # writer.close()

def start_server(host, port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = loop.run_until_complete(asyncio.start_server(handle_client, host, port))
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
    return {"message": "Hola mi amor, estas programando solo, Enserio?!"}

def run_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_asyncio():
    asyncio.run(main())

if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        executor.submit(run_uvicorn)
        executor.submit(run_asyncio)