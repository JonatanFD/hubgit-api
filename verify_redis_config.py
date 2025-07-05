#!/usr/bin/env python3
"""
Script para verificar que toda la configuración de Redis usa 10.0.1.4
"""
import os
import sys
from dotenv import load_dotenv

def verify_redis_configuration():
    """Verifica que la configuración de Redis esté usando 10.0.1.4"""
    load_dotenv()
    
    print("🔍 Verificando configuración de Redis...")
    print("=" * 50)
    
    # Verificar variables de entorno
    redis_host = os.getenv('REDIS_HOST', '10.0.1.4')
    redis_port = os.getenv('REDIS_PORT', '6379')
    redis_password = os.getenv('REDIS_PASSWORD', None)
    redis_db = os.getenv('REDIS_DB', '0')
    
    print(f"📍 REDIS_HOST: {redis_host}")
    print(f"🔌 REDIS_PORT: {redis_port}")
    print(f"🔑 REDIS_PASSWORD: {'SET' if redis_password else 'NOT SET'}")
    print(f"💾 REDIS_DB: {redis_db}")
    
    # Verificar que la IP sea la correcta
    if redis_host == '10.0.1.4':
        print("✅ Configuración correcta: Usando IP 10.0.1.4")
    else:
        print(f"❌ Configuración incorrecta: Usando {redis_host} en lugar de 10.0.1.4")
        return False
    
    # Verificar configuración de redis-om
    print("\n🔧 Verificando configuración de redis-om...")
    try:
        from redis_setup.redis_config import configure_redis_om, REDIS_HOST, REDIS_URL
        print(f"📍 REDIS_HOST en config: {REDIS_HOST}")
        print(f"🔗 REDIS_URL: {REDIS_URL}")
        
        if REDIS_HOST == '10.0.1.4':
            print("✅ redis_config.py está usando la IP correcta")
        else:
            print(f"❌ redis_config.py está usando {REDIS_HOST} en lugar de 10.0.1.4")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar redis_config.py: {e}")
        return False
    
    print("\n🎉 Todas las configuraciones están usando 10.0.1.4 correctamente!")
    return True

if __name__ == "__main__":
    success = verify_redis_configuration()
    sys.exit(0 if success else 1)
