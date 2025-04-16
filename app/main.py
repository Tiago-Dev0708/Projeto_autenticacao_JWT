from fastapi import FastAPI
from app.routers import router

app = FastAPI()

@app.get("/")
def read_root():
    return "Ok, it's working"

app.include_router(router)


