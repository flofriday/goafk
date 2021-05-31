from fastapi import Depends, FastAPI


from .config import get_settings, Settings
from .routers import jobs, debug
from .database import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(jobs.router)
app.include_router(debug.router)


@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return settings


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
