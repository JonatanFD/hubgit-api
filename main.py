from datetime import datetime, timezone

from fastapi import FastAPI
from redis_setup.build_database import build_db
from redis_om import Migrator

from resources.create_post_resource import CreatePostResource
from services.repositories.posts_service import PostsService

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


@app.get("/companies/{company_id}/posts")
def get_posts_by_company_id(company_id: str):
    company_posts = PostsService().getPostsByCompanyId(company_id)
    return {"posts": company_posts}

@app.put("/companies/{company_id}/posts")
def create_post(company_id: str, post_resource: CreatePostResource):
    post_resource.company_id = company_id

    post = PostsService().create_post_for_company(post_resource)

    PostsService().save_post_for_company(post)

    del post.pk

    return {"post": post}


@app.get("/test")
def test():

    print("")

