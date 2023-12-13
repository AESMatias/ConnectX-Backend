import uvicorn
from starlette.responses import RedirectResponse
from fastapi import FastAPI
from app.routes.admin import admin
from app.routes.user import user
from app.routes.auth import auth
import asyncio
from concurrent.futures import ThreadPoolExecutor
from sessions.server import Server

app = FastAPI()
app.include_router(admin)
app.include_router(auth)
app.include_router(user)
server = Server()

@app.on_event("startup")
async def main():
    with ThreadPoolExecutor() as executor:
        executor.submit(server.start_server)


@app.get("/" , tags=["root"])
async def root():
    return RedirectResponse(url="/docs/")


def run_uvicorn():
    uvicorn.run(app, host="localhost", port=8000)


def run_asyncio():
    asyncio.run(main())

if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        executor.submit(run_uvicorn)
        executor.submit(run_asyncio)
