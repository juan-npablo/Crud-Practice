from fastapi import FastAPI, Depends, HTTPException, status, Request
from api.v1 import auth, projects, tasks
from api.deps import get_current_user
from middleware.auth_middleware import AuthMiddleware


app1 = FastAPI()

app1.add_middleware(AuthMiddleware)

# Importing the router from the auth module
app1.include_router(
    auth.router,
    prefix="/v1/auth",
    tags=["auth"]
)

app1.include_router(
    projects.router,
    prefix="/v1/projects",
    tags=["projects"],
    dependencies=[Depends(get_current_user)]
)

app1.include_router(
    tasks.router,
    prefix="/v1/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)]
)

@app1.get("/")
def hello():
    return {"message": "Bienvenido a la API de FastAPI con SQLAlchemy y PostgreSQL"}