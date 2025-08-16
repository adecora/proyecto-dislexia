# Proyecto dislexia

Genera audios a partir de palabras (reales o falsas), para el tratamiento de pacientes con dislexia u otras dificultades específicas de aprendizaje.

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
usage: __main__.py [-h] [--config config.yml] [--token 12345] [--email user@domain.com] [--voice Alvaro]
                   [--format {wav,mp3,ogg}] [--speed default: 1.0] [--pitch default: 0] [--emotion {evil,good,neutral}]
                   [--bitrate default: 48000] [--contour x,y] [--outfile fichero]
                   palabra/fichero

Herramienta de línea de comandos para transformar palabras
o ficheros (json) en audios.

positional arguments:
  palabra/fichero       Palabra/fichero a convertir

options:
  -h, --help            show this help message and exit
  --config config.yml   Archivo de configuración YAML
  --token 12345         Token de autentificación
  --email user@domain.com
                        Correo electrónico
  --voice Alvaro        Voz a utilizar
  --format {wav,mp3,ogg}
                        Formato del fichero resultante (default: mp3)
  --speed default: 1.0  Velocidad de reproducción (rango de 0.1 a 2.0)
  --pitch default: 0    Tono de voz (rango de -20 a 20)
  --emotion {evil,good,neutral}
                        Emoción de la voz (default: neutral)
  --bitrate default: 48000
                        Tasa de muestreo (rango de 8000 a 192000 Hz)
  --contour x,y, -c x,y

                        Detalle de entonación de la palabra, se pueden escoger hasta 5 puntos.
                            x - Porcentaje de duración de la palabra (0 a 100)
                            y - Procentaje de entonación (-100 a 100)
  --outfile fichero, -o fichero
                        Guarda el audio con el nombre fichero

Comandos especiales disponibles:
  deletrear             Deletrea palabras (sílaba por sílaba) y genera audio
                        Uso: python -m word2speech deletrear palabra [opciones]
  prosodia              Genera audio con prosodia mejorada usando SSML e IPA
                        Uso: python -m word2speech prosodia palabra [opciones]
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

Si no proporcionamos un fichero de configuración mediante el flag `--config`, la aplicación busca automáticamente primero en la configuración local del proyecto `./.word2speech/config.yml` y después en la configuración global del usuario `~/.word2speech/config.yml`.

Si no encuentra ningún archivo, los parámetros obligatorios (token, email, voice) deben proporcionarse por línea de comandos.

```shell
$ python -m word2speech palabra
[17:19:25]: Generando el audio de la palabra "palabra"
[17:19:26]: Audio generado "out.mp3" (coste: 7, saldo: 61705)

$ python -m word2speech data-reduce.json
[17:19:40]: Generando el audio de la palabra "abrazo"
[17:19:40]: Audio generado "palabras/abrazo.mp3" (coste: 0, saldo: 61705)
[17:19:40]: Generando el audio de la palabra "bebida"
[17:19:40]: Audio generado "palabras/bebida.mp3" (coste: 0, saldo: 61705)
[17:19:41]: Generando el audio de la palabra "órganos"
[17:19:41]: Audio generado "palabras/organos.mp3" (coste: 0, saldo: 61705)
[17:19:41]: Generando el audio de la palabra "babados"
[17:19:41]: Audio generado "nopalabras/babados.mp3" (coste: 0, saldo: 61705)
[17:19:41]: Generando el audio de la palabra "bacela"
[17:19:42]: Audio generado "nopalabras/bacela.mp3" (coste: 0, saldo: 61705)
[17:19:42]: Generando el audio de la palabra "plátaco"
[17:19:42]: Audio generado "nopalabras/plataco.mp3" (coste: 0, saldo: 61705)
```

#### Uso de subcomandos

`word2speech` tiene disponibles 2 subcomandos, `deletrear` y `prosodia`:

- `deletrear`: Genera el audio de una palabra sílaba por sílaba
  ```shell
  $ python -m word2speech deletrear albaricoque
  [17:29:09]: Generando audio deletreado por sílabas de la palabra "albaricoque"
  [17:29:09]: Texto deletreado: al <break time="250ms"/> ba <break time="250ms"/> ri <break time="250ms"/> co <break time="250ms"/> que
  [17:29:13]: Audio deletreado generado "out_deletreo.mp3" (coste: 95, saldo: 61610)

  # El flag --include-word añade la palabra deletreada al final de audio
  $ python -m word2speech deletrear albaricoque --include-word
  [17:30:51]: Generando audio deletreado por sílabas de la palabra "albaricoque"
  [17:30:51]: Texto deletreado: al <break time="250ms"/> ba <break time="250ms"/> ri <break time="250ms"/> co <break time="250ms"/> que <break time="1s"/> albaricoque
  [17:30:53]: Audio deletreado generado "out_deletreo.mp3" (coste: 124, saldo: 61486)
  ```
- `prosodia`: Genera una versión de la palabra con mayor énfasis en la prosodia de la misma mediante el uso de [SSML](https://www.w3.org/TR/speech-synthesis/) para enriquecer la palabra y la trancripción fonética IPA.
  ```shell
  $ python -m word2speech prosodia albaricoque
  [17:35:20]: IPA generado con epitran para 'albaricoque': albaɾikoke
  [17:35:20]: Generando audio con prosodia mejorada de la palabra "albaricoque"
  [17:35:20]: SSML generado: <prosody rate="medium" pitch="medium" volume="medium"><phoneme alphabet="ipa" ph="albaɾikoke">albaricoque</phoneme></prosody>
  [17:35:21]: Audio con prosodia generado "out_prosodia.mp3" (coste: 125, saldo: 61361)
  ```


### Instalar como comando

Se ha empaquetado para que pueda instalarse como un comando invocando directamente `word2speech` para instalarlo se recomienda usar [`pipx`](https://pipx.pypa.io/stable/).

```shell
$ pipx install git+https://github.com/adecora/proyecto-dislexia.git
$ pipx list
venvs are in /home/cora/.local/share/pipx/venvs
apps are exposed on your $PATH at /home/cora/.local/bin
manual pages are exposed at /home/cora/.local/share/man
   package word2speech 1.0.0, installed using Python 3.12.11
    - word2speech
```

Una vez instalado ya puedo invocar direcatmente a `word2speech`

``shell
$ word2speech --config config.yml albaricoque
[20:45:51]: Generando el audio de la palabra "albaricoque"
[20:45:52]: Audio generado "out.mp3" (coste: 11, saldo: 61125)
$ word2speech deletrear --config config.yml --include-word albaricoque
[20:46:08]: Generando audio deletreado por sílabas de la palabra "albaricoque"
[20:46:08]: Texto deletreado: al <break time="250ms"/> ba <break time="250ms"/> ri <break time="250ms"/> co <break time="250ms"/> que <break time="1s"/> albaricoque
[20:46:12]: Audio deletreado generado "out_deletreo.mp3" (coste: 0, saldo: 61125)
$ word2speech prosodia --config config.yml albaricoque
[20:46:30]: IPA generado con epitran para 'albaricoque': albaɾikoke
[20:46:30]: Generando audio con prosodia mejorada de la palabra "albaricoque"
[20:46:30]: SSML generado: <prosody rate="medium" pitch="medium" volume="medium"><phoneme alphabet="ipa" ph="albaɾikoke">albaricoque</phoneme></prosody>
[20:46:30]: Audio con prosodia generado "out_prosodia.mp3" (coste: 0, saldo: 61125)
```

#### Limitación windows

En Windows debido a la codificación de la consola por defecto pueden surgir problemas a la hora de ejecutar el subcomando `prosodia`, la solución pasa por forzar la codificación `UTF-8`

```cmd
> set PYTHONUTF8=1
```

Podemos establecer la codificación `UTF-8` de forma permanente con:

```cmd
> setx PYTHONUTF8 1
```

> **Nota**: Después de ejecutar `setx`, es necesario reiniciar la terminal (o abrir una nueva) para que el cambio tome efecto.
