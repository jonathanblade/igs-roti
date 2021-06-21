from fastapi import FastAPI

from .router import router

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(router, prefix="/api")
