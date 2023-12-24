import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi import Depends
from decouple import config
from app.routes.user import user
from app.routes.auth import auth
from app.routes.admin import admin
from sessions.friends import friend
from sessions.server import Server
from starlette.responses import RedirectResponse
from concurrent.futures import ThreadPoolExecutor
from sessions.loader import post_message_to_chat
from sessions.loader import post_message_to_p2p
from sessions.loader import post_message_to_chat_p2p


app = FastAPI()
server = Server()
app.include_router(admin)
app.include_router(auth)
app.include_router(user)
app.include_router(friend)


@app.on_event("startup")
async def main():
    with ThreadPoolExecutor() as executor:
        executor.submit(server.start_server)

@app.get("/" , tags=["root"])
async def root():
    return RedirectResponse(url="/docs/")

@app.get("/active", tags=["utils"])
def get_active_users(server: Server = Depends(lambda: server)):
    users = server.return_names()
    return users

@app.get("/messages", tags=["utils"])
def get_messages():
    return post_message_to_chat()

@app.post("/messages/p2p/message", tags=["utils"])
def post_messages_p2p(username: str, message_text: str, username2: str):
    return post_message_to_p2p(username, message_text, username2)

@app.get("/messages/p2p", tags=["utils"])
def get_messages_p2p(username: str, username2: str):
    return post_message_to_chat_p2p(username, username2)

def run_uvicorn():
    uvicorn.run(app, host=config('UVICORN_HOST'), port=config('UVICORN_PORT', cast=int))

def run_asyncio():
    asyncio.run(main())

if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        executor.submit(run_uvicorn)
        executor.submit(run_asyncio)
