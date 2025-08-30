#!/bin/bash

# pipeline para convertir los ficheros de concienciación fonológica del directorio data/
# al formato requerido por word2speech para procesar la generación en lote de todas las palabras


if [[ $# -eq 0 ]] || [[  "$1" != *.json ]]; then
  echo "Uso: $0 <archivo_salida.json>"
  exit 1
fi

SCRIPT_DIR="$(dirname "$0")"

echo "Convirtiendo los ficheros xlsx a csv..."
bash "${SCRIPT_DIR}/convert.sh"

echo "Generando fichero json para word2speech..."
python "${SCRIPT_DIR}/parse.py" > "$1"
