#!/usr/bin/env python3
"""
Script para configurar Redis y resolver problemas de permisos/snapshots
"""
import os
import redis
from dotenv import load_dotenv

def configure_redis_server():
    """Configura Redis para evitar problemas de snapshots RDB"""
    load_dotenv()
    
    redis_host = os.getenv('REDIS_HOST', '10.0.1.4')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_password = os.getenv('REDIS_PASSWORD', None)
    redis_db = int(os.getenv('REDIS_DB', '0'))
    
    try:
        print(f"🔧 Configuring Redis server at {redis_host}:{redis_port}")
        
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=redis_db,
            decode_responses=True,
            socket_connect_timeout=10
        )
        
        # Configurar Redis para evitar problemas de snapshots
        try:
            # Opción 1: Deshabilitar stop-writes-on-bgsave-error
            r.config_set('stop-writes-on-bgsave-error', 'no')
            print("✅ Disabled stop-writes-on-bgsave-error")
        except Exception as e:
            print(f"⚠️  Could not disable stop-writes-on-bgsave-error: {e}")
        
        try:
            # Opción 2: Configurar un directorio de trabajo válido
            r.config_set('dir', '/tmp')
            print("✅ Set Redis working directory to /tmp")
        except Exception as e:
            print(f"⚠️  Could not set working directory: {e}")
        
        try:
            # Opción 3: Deshabilitar snapshots RDB temporalmente
            r.config_set('save', '')
            print("✅ Disabled RDB snapshots")
        except Exception as e:
            print(f"⚠️  Could not disable RDB snapshots: {e}")
        
        # Probar que Redis funciona ahora
        r.ping()
        print("✅ Redis configuration successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error configuring Redis: {e}")
        return False

if __name__ == "__main__":
    configure_redis_server()
