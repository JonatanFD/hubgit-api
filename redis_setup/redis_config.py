import os
from redis_om import get_redis_connection

# Configuración de Redis usando variables de entorno
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_DB = int(os.getenv('REDIS_DB', '0'))

# URL de conexión para redis-om
if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# Configurar redis-om para usar nuestra conexión personalizada
def configure_redis_om():
    """Configura la conexión de redis-om con los parámetros especificados"""
    os.environ['REDIS_OM_URL'] = REDIS_URL
    return get_redis_connection(url=REDIS_URL)
