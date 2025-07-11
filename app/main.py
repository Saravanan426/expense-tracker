from fastapi import FastAPI
from . import models, database
from .routes import router

# This is safe to run; will not overwrite your manually created tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(router)
