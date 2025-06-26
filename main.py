from fastapi import FastAPI
from redis_setup.build_database import build_db
from redis_om import Migrator

app = FastAPI()
Migrator().run()


@app.get("/")
def read_root():
    return {"Hello": "World MATEO WEBON"}


@app.get("/build")
def build():
    result = build_db()
    return {"build": "success" if result else "failed"}

