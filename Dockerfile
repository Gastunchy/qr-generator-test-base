# Usa una imagen base de Python
FROM python:3.14.0a2-slim-bullseye

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos y la aplicación
COPY requirements.txt requirements.txt
COPY . .

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]