#!/bin/bash
# Script de inicio simple que no intenta configurar Redis
# Útil cuando no tienes permisos de administrador en Redis

echo "🚀 Starting HubGit API (Simple Mode)..."

# Solo probar conexión básica
echo "🔍 Testing basic Redis connection..."
python -c "
import redis
import os
from dotenv import load_dotenv

load_dotenv()
redis_host = os.getenv('REDIS_HOST', '10.0.1.4')
redis_port = int(os.getenv('REDIS_PORT', '6379'))

try:
    r = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)
    # Intentar un comando que no modifique datos
    r.ping()
    print('✅ Basic Redis connection successful')
except Exception as e:
    print(f'⚠️  Redis connection issue: {e}')
    print('⚠️  Starting FastAPI anyway...')
"

echo "🚀 Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
