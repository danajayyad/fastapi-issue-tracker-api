from fastapi import FastAPI
from .database.database import Base, engine
from .routers import auth, projects


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(projects.router)