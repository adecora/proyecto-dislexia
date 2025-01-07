# Proyecto dislexia 

Genera audios a partir de palabras (reales o falsas), para que puedan ser utilizadas en un estudio sobre la dislexia.

Un proyecto de Alejandro Varela de Cora.

### Entorno software

El código necesario para recontruir el entorno software esta descrito en el fichero [environment.yml](./environment.yml). Se puede instalar usando [miniconda](https://docs.anaconda.com/miniconda):

```shell
$ conda env create -f environment.yml
```
Para entornos windows replicamos el entorno ejecutando el fichero [windows-env.yml](./windows-env.yml):

```cmd
> conda env create -f windows-env.yml
```

El paquete `word2speech` es una [herramienta CLI](https://es.wikipedia.org/wiki/Interfaz_de_l%C3%ADnea_de_comandos) para convertir palabras en audios, para poder empezar a utlizarla es necesario clonar el repositorio:

```shell
$ git clone https://github.com/adecora/proyecto-dislexia.git

# Navegamos a la carpeta padre de paquete word2speech
$ cd proyecto-dislexia

# Activamos el entorno conda creado
$ conda activate proyecto

# Ahora podemor usar el paquete python word2speech
$ python -m word2speech --help
usage: __main__.py [-h] [--config config.yml] [--token 12345]
                   [--email user@domain.com] [--voice Alvaro]
                   [--format {ogg,wav,mp3}] [--speed default: 1.0]
                   [--pitch default: 0] [--emotion {good,neutral,evil}]
                   [--bitrate default: 48000] [--contour x,y]
                   [--outfile fichero]
                   palabra/fichero

Herramienta de línea de comandos para transformar palabras
o ficheros (json) en audios.

Argumentos posicionales:
  palabra/fichero       Palabra/fichero a convertir

Argumentos opcionales:
  -h, --help            Muestra este mensaje de ayuda y sale.
  --config config.yml   Archivo de configuración YAML
  --token 12345         Token de autentificación
  --email user@domain.com
                        Correo electrónico
  --voice Alvaro        Voz a utilizar
  --format {ogg,wav,mp3}
                        Formato del fichero resultante (default: mp3)
  --speed default: 1.0  Velocidad de reproducción (rango de 0.1 a 2.0)
  --pitch default: 0    Tono de voz (rango de -20 a 20)
  --emotion {good,neutral,evil}
                        Emoción de la voz (default: neutral)
  --bitrate default: 48000
                        Tasa de muestreo (rango de 8000 a 192000 Hz)
  --contour x,y, -c x,y
                        
                        Detalle de entonación de la palabra, se pueden escoger hasta 5 puntos.
                            x - Porcentaje de duración de la palabra (0 a 100)
                            y - Procentaje de entonación (-100 a 100)
  --outfile fichero, -o fichero
                        Guarda el audio con el nombre fichero
```

### Reconstrucción de los datos

No es necesario porque el documento JSON con los datos requeridos para probar el proyecto está incluido en el repositorio. Se incluyen los ficheros [data.json](./data.json) y un subset [data-reduce.json](./data-reduce.json).

Para reprocesar los ficheros originales XLSX, y convertirlos a su versión CSV:

```shell
$ ./bin/convert.sh
```

Si estamos en windows tenemos que ejecutar el `batch file` equivalente:

```cmd
>.\bin\convert.bat
```

Después, corre el programa que los toma y emite por `stdout` la estructura de datos JSON resultante:

```shell
$ ./bin/parse.py > data.json

$ cat data-reduce.json
{
  "palabras": [
    "abrazo",
    "bebida",
    "órganos"
  ],
  "nopalabras": [
    "babados",
    "bacela",
    "plátaco"
  ] 
}
```

El fichero resultante tiene una clave, palabra y nopalabra, por directorio y dentro una lista con las palabras cuyo audio va a generar en cada directorio.

### Ejemplos de uso

Para empezar a utilizar el módulo `word2speech` es necesario configurar los parámetros obligatorios **token, email y [voz](https://speechgen.io/en/voices/)** para hacer consultas a la [API de speechgen](https://speechgen.io/en/node/api/). Esto se puede hacer a través del [fichero de configuración](./config-example.yml) o de la línea de comandos.

```yml
# Parámetros obligatorios.
token: 12345
email: user@domain.com
voice: Alvaro
```

El resto de parámetros son opcionales, se pueden consultar en el fichero [config-example.yml](./config-example.yml) o con el comando `$ python -m word2speech --help`.

Ya estamos listo para empezar a generar audios con el paquete `word2speech`:

```shell
$ python -m word2speech --config config-example.yml palabra
[14:46:59]: Generando el audio de la palabra "palabra"
[14:47:05]: Audio generado "out.mp3" (coste: 0, saldo: 64305)

$ python -m word2speech --config config-example.yml data-reduce.json
[14:50:45]: Generando el audio de la palabra "abrazo"
[14:50:46]: Audio generado "palabras/abrazo.mp3" (coste: 0, saldo: 64305)
[14:50:46]: Generando el audio de la palabra "bebida"
[14:50:46]: Audio generado "palabras/bebida.mp3" (coste: 0, saldo: 64305)
[14:50:46]: Generando el audio de la palabra "órganos"
[14:50:47]: Audio generado "palabras/organos.mp3" (coste: 0, saldo: 64305)
[14:50:47]: Generando el audio de la palabra "babados"
[14:50:47]: Audio generado "nopalabras/babados.mp3" (coste: 0, saldo: 64305)
[14:50:47]: Generando el audio de la palabra "bacela"
[14:50:48]: Audio generado "nopalabras/bacela.mp3" (coste: 0, saldo: 64305)
[14:50:48]: Generando el audio de la palabra "plátaco"
[14:50:49]: Audio generado "nopalabras/plataco.mp3" (coste: 0, saldo: 64305)
```
