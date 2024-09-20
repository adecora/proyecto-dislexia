# Proyecto dislexia 

Genera audios a partir de palabras (reales o falsas), para que puedan ser utilizadas en un estudio sobre la dislexia.

Un proyecto de Alejandro Varela de Cora.

### Reconstrucción de los datos

No es necesario porque el documento JSON con los datos requeridos para probar el proyecto está incluido en el repositorio.

El código se ejecuta en el entorno software descrito por `environment.yml`. Se puede instalar usando [miniconda](https://docs.anaconda.com/miniconda/):

```shell
conda env create -f environment.yml
```

Para reprocesar los ficheros originales XLSX, y convertirlos a su versión CSV:

```shell
./bin/convert.sh
```

Después, corre el programa que los toma y emite por `stdout` la estructura de datos JSON resultante:

```shell
./bin/parse.py > data.json
```
