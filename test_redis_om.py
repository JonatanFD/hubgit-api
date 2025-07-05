#!/usr/bin/env python3
"""
Script para verificar que redis-om está usando la configuración correcta
"""
import os
import sys
from dotenv import load_dotenv

def test_redis_om_config():
    """Prueba que redis-om esté usando la configuración correcta"""
    print("🔍 Testing redis-om configuration...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Configurar Redis-OM
    from redis_setup.redis_config import configure_redis_om
    redis_url = configure_redis_om()
    
    print(f"✅ Redis URL configured: {redis_url}")
    print(f"✅ REDIS_OM_URL environment variable: {os.getenv('REDIS_OM_URL', 'NOT_SET')}")
    
    # Importar redis-om después de la configuración
    from redis_om import get_redis_connection
    
    try:
        # Obtener la conexión que está usando redis-om
        redis_conn = get_redis_connection()
        connection_info = redis_conn.connection_pool.connection_kwargs
        
        print(f"✅ redis-om connection info:")
        print(f"   Host: {connection_info.get('host', 'unknown')}")
        print(f"   Port: {connection_info.get('port', 'unknown')}")
        print(f"   DB: {connection_info.get('db', 'unknown')}")
        
        # Probar la conexión
        ping_result = redis_conn.ping()
        print(f"✅ Redis PING through redis-om: {ping_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with redis-om connection: {e}")
        return False

if __name__ == "__main__":
    success = test_redis_om_config()
    sys.exit(0 if success else 1)
