FROM python:3.10-slim

WORKDIR /app

# Copiar primero requirements.txt
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar el resto del código
COPY . /app/

CMD ["python", "app.py"]
