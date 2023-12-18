import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi import Depends
from decouple import config
from app.routes.user import user
from app.routes.auth import auth
from app.routes.admin import admin
from sessions.server import Server
from starlette.responses import RedirectResponse
from concurrent.futures import ThreadPoolExecutor


app = FastAPI()
server = Server()
app.include_router(admin)
app.include_router(auth)
app.include_router(user)


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

def run_uvicorn():
    uvicorn.run(app, host=config('UVICORN_HOST'), port=config('UVICORN_PORT', cast=int))

def run_asyncio():
    asyncio.run(main())

if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        executor.submit(run_uvicorn)
        executor.submit(run_asyncio)
