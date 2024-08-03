from fastapi import FastAPI

from .routers import users
from .routers import auth
from .routers import roles
from .events.router import router as eventsRouter

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(roles.router, prefix="/api")
app.include_router(eventsRouter, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "It's good!"}
