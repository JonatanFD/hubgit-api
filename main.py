from fastapi import FastAPI
from redis_setup.build_database import build_db
from redis_om import Migrator
from domain.entities import User, Company, Post, Comment

app = FastAPI()

# Ejecutar migrator para crear índices correctos
print("Running migrations...")
try:
    Migrator().run()
    print("Migrations completed successfully")
except Exception as e:
    print(f"Migration error: {e}")


@app.get("/")
def read_root():
    return {"Hello": "World MATEO WEBON"}


@app.get("/build")
def build():
    result = build_db()
    return {"build": "success" if result else "failed"}
