from fastapi import FastAPI

from .auth.router import router as authRouter
from .users.router import router as usersRouter
from .roles.router import router as rolesRouter
from .events.router import router as eventsRouter
from .tutoring.router import router as tutoringRouter

app = FastAPI()

app.include_router(authRouter, prefix="/api")
app.include_router(usersRouter, prefix="/api")
app.include_router(rolesRouter, prefix="/api")
app.include_router(eventsRouter, prefix="/api")
app.include_router(tutoringRouter, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "It's good!"}
