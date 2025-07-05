#!/bin/bash
"""
Script de inicio para la aplicación FastAPI
Este script verifica la conexión a Redis antes de iniciar la aplicación
"""
echo "🚀 Starting HubGit API..."

# Probar conexión a Redis
echo "🔍 Testing Redis connection..."
python test_redis.py

if [ $? -eq 0 ]; then
    echo "✅ Redis connection successful, starting FastAPI..."
    exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "❌ Redis connection failed, exiting..."
    exit 1
fi
