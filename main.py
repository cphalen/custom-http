import os

from fastapi import FastAPI, HTTPException
# from custom.webserver import API, HTTPException
from redis import Redis

app = FastAPI()
# app = API()
conn = Redis.from_url(os.getenv("REDIS_URL", "redis://hw1-redis-test/0"))


@app.get("/hello")
def hello_view(name: str = "Toph"):
    return {"message": f"Hello there, {name}!"}


@app.post("/bender")
def add_bender(name: str, element: str):
    if not name or not element:
        raise HTTPException(
            status_code=400, detail="bender name or element is malformed"
        )
    conn.set(name, element)
    return {"message": f"Set element for {name}!"}


@app.get("/bender")
def get_bender(name: str):
    if len(name) == 0:
        raise HTTPException(status_code=400, detail="Bender must have a name.")
    value = conn.get(name).decode()
    if value is None:
        raise HTTPException(status_code=404, detail="bender not found.")

    return {"name": name, "element": value}
