#!/bin/bash

# Configuración
IMAGE_NAME="mi-imagen" # Nombre de la imagen
VERSION_FILE="version.txt" # Archivo para guardar la versión

# Verificar si el archivo de versión existe
if [ ! -f "$VERSION_FILE" ]; then
  echo "0.0.0" > "$VERSION_FILE" # Crear un archivo de versión inicial
fi

# Leer la última versión
VERSION=$(cat "$VERSION_FILE")

# Incrementar la versión (formato mayor.menor.parche)
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"
PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$PATCH"

# Guardar la nueva versión en el archivo
echo "$NEW_VERSION" > "$VERSION_FILE"

# Construir la imagen con la nueva versión
docker build -t "$IMAGE_NAME:$NEW_VERSION" .

# Confirmar la creación de la imagen
if [ $? -eq 0 ]; then
  echo "Imagen $IMAGE_NAME:$NEW_VERSION creada correctamente."
else
  echo "Error al crear la imagen $IMAGE_NAME:$NEW_VERSION."
  exit 1
fi
