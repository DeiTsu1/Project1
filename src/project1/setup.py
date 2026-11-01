from fastapi import FastAPI

from project1.router import router

app = FastAPI()
app.include_router(router)