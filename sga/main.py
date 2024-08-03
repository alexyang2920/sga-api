from fastapi import FastAPI

from .routers.auth import router as authRouter
from .users.router import router as usersRouter
from .roles.router import router as rolesRouter
from .events.router import router as eventsRouter

app = FastAPI()

app.include_router(authRouter, prefix="/api")
app.include_router(usersRouter, prefix="/api")
app.include_router(rolesRouter, prefix="/api")
app.include_router(eventsRouter, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "It's good!"}
