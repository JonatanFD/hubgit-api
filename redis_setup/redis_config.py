import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Redis usando variables de entorno
# Forzar el uso de la IP 10.0.1.4 como valor por defecto
REDIS_HOST = os.getenv('REDIS_HOST', '10.0.1.4')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_DB = int(os.getenv('REDIS_DB', '0'))

# URL de conexión para redis-om
if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

print(f"Redis URL configurada: {REDIS_URL}")

def configure_redis_om():
    """Configura la conexión de redis-om estableciendo la variable de entorno REDIS_OM_URL"""
    os.environ['REDIS_OM_URL'] = REDIS_URL
    print(f"REDIS_OM_URL configurada: {REDIS_URL}")
    return REDIS_URL
