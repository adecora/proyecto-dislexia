#!/bin/bash

# Genera una carpeta por cada uno de los modelos, con los audios utilizados
# para realizar las validaciones científicas de la calidad de los modelos.
#
#  speechgen/
#  parler/
#  mms/

# Validar que word2speech está instalado
if ! command -v word2speech &> /dev/null; then
    echo "Error: word2speech no está instalado"
    echo "Instala el paquete con: pipx word2speech[.all]"
    exit 1
fi

# Obtener el directorio del script
SCRIPT_DIR="$(dirname "$0")"

# Obtener el directorio padre del script
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

for model in speechgen parler mms; do
  # Editamos el directorio del batch file con los audios  a generar
  sed -i "2s/\".*\"/\"${model}\"/" "${PARENT_DIR}/data-validate.json"

  echo "Genrando los audios con el modelo ${model}..."
  python -m word2speech batch "${PARENT_DIR}/data-validate.json" --model ${model} "$@"
done


# Restaurar el fichero con los datos de validación
git checkout "${PARENT_DIR}/data-validate.json"
