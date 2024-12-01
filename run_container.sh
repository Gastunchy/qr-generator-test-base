#!/bin/bash

# Configuración
IMAGE_NAME="mi-imagen"

# Obtener todas las versiones disponibles de la imagen
VERSIONS=$(docker images --format '{{.Tag}}' "$IMAGE_NAME" | sort -V)

# Extraer la última versión
LATEST_VERSION=$(echo "$VERSIONS" | tail -n 1)

# Validar si existe alguna versión
if [ -z "$LATEST_VERSION" ]; then
  echo "No se encontraron versiones de la imagen $IMAGE_NAME."
  exit 1
fi

# Ejecutar un contenedor con la última versión
docker run -d --name "${IMAGE_NAME}_container" "$IMAGE_NAME:$LATEST_VERSION"

if [ $? -eq 0 ]; then
  echo "Contenedor ejecutado con la imagen $IMAGE_NAME:$LATEST_VERSION."
else
  echo "Error al ejecutar el contenedor con la imagen $IMAGE_NAME:$LATEST_VERSION."
  exit 1
fi
