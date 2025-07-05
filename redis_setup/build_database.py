from redis_om import (Field, JsonModel)
import json
import redis
import os
from dotenv import load_dotenv
from typing import List
from domain.entities import *
from redis_setup.redis_config import configure_redis_om

def build_db() -> bool:
    data : dict = json.load(open("./redis_setup/db.json"))
    
    # Cargar variables de entorno y configurar redis-om
    load_dotenv()
    configure_redis_om()
    
    try:
        # Limpiar base de datos usando una conexión Redis directa
        print("Clearing database...")
        
        # Configurar conexión Redis con variables de entorno
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_password = os.getenv('REDIS_PASSWORD', None)
        redis_db = int(os.getenv('REDIS_DB', '0'))
        
        print(f"Connecting to Redis at {redis_host}:{redis_port}")
        
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=redis_db,
            decode_responses=True
        )
        
        # Eliminar todas las claves que empiecen con nuestros prefijos
        prefixes = ['user:*', 'company:*', 'post:*', 'comment:*']
        deleted_count = 0
        
        for prefix in prefixes:
            keys = r.keys(prefix)
            if keys:
                deleted_keys = r.delete(*keys)
                deleted_count += deleted_keys
                print(f"Deleted {deleted_keys} keys with prefix {prefix}")
        
        # También eliminar índices antiguos y claves con módulo completo
        problematic_patterns = [
            '*:index', 
            '*domain.entities*', 
            '*redis_setup*',
            'user:domain.entities.User:*',
            'company:domain.entities.Company:*',
            'post:domain.entities.Post:*',
            'comment:domain.entities.Comment:*'
        ]
        
        for pattern in problematic_patterns:
            keys = r.keys(pattern)
            if keys:
                deleted_keys = r.delete(*keys)
                deleted_count += deleted_keys
                print(f"Deleted {deleted_keys} problematic keys with pattern {pattern}")
        
        print(f"Total deleted: {deleted_count} keys")
        print("Database Cleared Successfully")
        
        # Forzar recreación de índices
        print("Recreating indexes...")
        from redis_om import Migrator
        try:
            # Eliminar índices antiguos manualmente si existen
            old_indexes = r.keys("*:index")
            if old_indexes:
                r.delete(*old_indexes)
                print(f"Deleted {len(old_indexes)} old indexes")
            
            # Ejecutar migrator para crear índices correctos
            Migrator().run()
            print("Indexes recreated successfully")
        except Exception as idx_error:
            print(f"Warning: Index creation error: {idx_error}")
        
    except Exception as e:
        print(f"Error Cleaning Database: {e}")
        return False
    
    print(type(data))

    keys = data.keys()
    print(f"Keys to process: {keys}")
    
    try:
        for key in keys:
            print(f"Processing: {key}")
            if key.startswith("user:"):
                # Crear el usuario con PK específico
                user_data = data[key]
                user = User(**user_data)
                user.pk = user_data['id']  # Asignar PK específico
                user.save()
                print(f"Saved user: {user_data['name']} with ID: {user_data['id']}")
            elif key.startswith("company:"):
                company_data = data[key]
                company = Company(**company_data)
                company.pk = company_data['id']
                company.save()
                print(f"Saved company: {company_data['name']} with ID: {company_data['id']}")
            elif key.startswith("post:"):
                post_data = data[key]
                post = Post(**post_data)
                post.pk = post_data['id']
                post.save()
                print(f"Saved post: {post_data['title']} with ID: {post_data['id']}")
            elif key.startswith("comment:"):
                comment_data = data[key]
                comment = Comment(**comment_data)
                comment.pk = comment_data['id']
                comment.save()
                print(f"Saved comment: {comment_data['id']}")

    except Exception as e:
        print(f"Error Building Database: {e}")
        print(f"Failed on key: {key}")
        print(f"Data for key: {data[key]}")
        return False
  
    print("Database Built Successfully")
    
    return True