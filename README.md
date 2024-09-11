# Proyecto dislexia 

Genera audios a partir de palabras (reales o falsas), para que puedan ser utilizadas en un estudio sobre la dislexia.

Un proyecto de Alejandro Varela de Cora.

### Reconstrucción de los datos

No es necesario porque el documento JSON con los datos requeridos para probar el proyecto está incluido en el repositorio.

Pero para reprocesar los ficheros originales XLSX, instala `csvkit` 2.0.1 en tu sistema y conviértelos a su versión CSV:

```shell
./bin/convert.sh
```

Después, corre el programa que los toma y emite por `stdout` la estructura de datos JSON resultante:

```shell
./bin/parse.py > data.json
```
