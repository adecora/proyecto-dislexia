#!/bin/bash

# publish: Publica la herramienta `word2speech` en el índice de paquetes Python
# Usage: publish <testpypi|pypi>

if [[ -z "$1" || ("$1" != "testpypi" && "$1" != "pypi") ]]; then
  echo "Usage: publish <testpypi|pypi>" >&2
  exit 1
fi

# Modicamos el README para índices de paquetes
cp README-pypi.md README.md

# Limpiar build anterior
rm -rf dist/ build/ *.egg-info/

case "$1" in
  testpypi)
    echo "Publicando a TestPyPI..."

    # Construir el paquete
    uvx --from build pyproject-build

    # Subir a TestPyPI
    uvx twine upload --repository testpypi dist/*

    ;;
  pypi)
    echo "Publicando a PyPI..."
    cp README-pypi.md README.md
    # Modificar el README para PyPI
    sed -i 's|--pip-args="--extra-index-url https://pypi.org/simple/" --index-url https://test.pypi.org/simple/ || ' README.md

    # Construir el paquete
    uvx --from build pyproject-build

    # Subir a PyPI
    uvx twine upload dist/*
    ;;
esac

git restore README.md
