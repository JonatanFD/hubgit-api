# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia requirements y los instala
COPY requirements.txt .

# Instalación de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente
COPY . .

# Hacer executable el script de inicio
RUN chmod +x start.sh

# Variables de entorno para Redis (pueden ser sobrescritas)
ENV REDIS_HOST=10.0.1.4
ENV REDIS_PORT=6379
ENV REDIS_PASSWORD=
ENV REDIS_DB=0

# Expone el puerto por defecto de FastAPI/Uvicorn
EXPOSE 8000

# Comando para ejecutar la app con verificación de Redis
CMD ["./start.sh"]
