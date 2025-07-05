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

# Expone el puerto por defecto de FastAPI/Uvicorn
EXPOSE 8000

# Comando para ejecutar la app (ajusta si tu archivo principal no es main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
