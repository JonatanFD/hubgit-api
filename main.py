from datetime import datetime, timezone
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from redis_setup.build_database import build_db
from redis_setup.redis_config import configure_redis_om
from redis_om import Migrator

from resources.create_post_resource import CreatePostResource
from services.repositories.posts_service import PostsService
from services.repositories.users_service import UsersService

# Cargar variables de entorno PRIMERO
load_dotenv()

# Configurar Redis-OM DESPUÉS de cargar las variables de entorno
redis_url = configure_redis_om()
print(f"Redis configurado con URL: {redis_url}")

app = FastAPI()

@app.get("/")
def read_root():
    try:
        users = UsersService.getUsers()
        return {
            "Hello": "World from FastAPI in Virtual Machine",
            "users": users,
            "redis_host": os.getenv('REDIS_HOST', '10.0.1.4'),
            "redis_port": os.getenv('REDIS_PORT', '6379')
        }
    except Exception as e:
        return {
            "error": "Failed to connect to Redis or fetch users",
            "details": str(e),
            "redis_host": os.getenv('REDIS_HOST', '10.0.1.4'),
            "redis_port": os.getenv('REDIS_PORT', '6379')
        }


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
    return {"message": "Test endpoint working"}


@app.get("/config-test")
def config_test():
    """Endpoint para verificar la configuración de variables de entorno"""
    return {
        "environment_variables": {
            "REDIS_HOST": os.getenv('REDIS_HOST', 'NOT_SET'),
            "REDIS_PORT": os.getenv('REDIS_PORT', 'NOT_SET'),
            "REDIS_PASSWORD": "SET" if os.getenv('REDIS_PASSWORD') else "NOT_SET",
            "REDIS_DB": os.getenv('REDIS_DB', 'NOT_SET'),
            "REDIS_OM_URL": "SET" if os.getenv('REDIS_OM_URL') else "NOT_SET"
        }
    }


@app.get("/redis-test")
def redis_test():
    """Endpoint para probar la conexión con Redis"""
    try:
        import redis
        redis_host = os.getenv('REDIS_HOST', '10.0.1.4')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_password = os.getenv('REDIS_PASSWORD', None)
        redis_db = int(os.getenv('REDIS_DB', '0'))
        
        # Probar conexión directa
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=redis_db,
            decode_responses=True
        )
        
        # Hacer ping a Redis
        ping_result = r.ping()
        
        # Obtener información del servidor
        info = r.info()
        
        return {
            "redis_connection": "success",
            "ping": ping_result,
            "redis_host": redis_host,
            "redis_port": redis_port,
            "redis_version": info.get('redis_version', 'unknown'),
            "connected_clients": info.get('connected_clients', 0)
        }
    except Exception as e:
        return {
            "redis_connection": "failed",
            "error": str(e),
            "redis_host": os.getenv('REDIS_HOST', '10.0.1.4'),
            "redis_port": os.getenv('REDIS_PORT', '6379')
        }

