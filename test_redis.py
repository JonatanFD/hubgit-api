#!/usr/bin/env python3
"""
Script para probar la conexión a Redis antes de ejecutar la aplicación
"""
import os
import sys
import redis
from dotenv import load_dotenv

def test_redis_connection():
    """Prueba la conexión a Redis"""
    load_dotenv()
    
    redis_host = os.getenv('REDIS_HOST', '10.0.1.4')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_password = os.getenv('REDIS_PASSWORD', None)
    redis_db = int(os.getenv('REDIS_DB', '0'))
    
    print(f"🔍 Testing Redis connection...")
    print(f"   Host: {redis_host}")
    print(f"   Port: {redis_port}")
    print(f"   DB: {redis_db}")
    print(f"   Password: {'SET' if redis_password else 'NOT SET'}")
    
    try:
        # Crear conexión con timeout
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=redis_db,
            decode_responses=True,
            socket_connect_timeout=10,
            socket_timeout=10
        )
        
        # Probar conexión
        ping_result = r.ping()
        print(f"✅ Redis PING: {ping_result}")
        
        # Obtener información del servidor
        info = r.info()
        print(f"✅ Redis Version: {info.get('redis_version', 'unknown')}")
        print(f"✅ Connected clients: {info.get('connected_clients', 0)}")
        
        # Probar operaciones básicas
        r.set('test_key', 'test_value')
        test_value = r.get('test_key')
        r.delete('test_key')
        
        print(f"✅ Basic operations test: {test_value == 'test_value'}")
        print("🎉 Redis connection test PASSED!")
        
        return True
        
    except redis.ConnectionError as e:
        print(f"❌ Redis connection error: {e}")
        print("   Make sure Redis is running on the specified host and port")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_redis_connection()
    sys.exit(0 if success else 1)
