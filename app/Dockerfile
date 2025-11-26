FROM python:3.10-slim

WORKDIR /app

# Copiar primero requirements.txt (que ahora está dentro de app/)
COPY app/requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . /app/

CMD ["python", "app.py"]
