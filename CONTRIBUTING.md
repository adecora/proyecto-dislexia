# GUÍA DE CONTRIBUCIÓN PARA word2speech

¡Gracias por tu interés en contribuir a **word2speech**!, la herramienta de línea de comandos (CLI) desarrollada para la **generación de audio adaptativo** enfocado en el tratamiento de la dislexia.

Tu colaboración es vital para mantener y expandir este ecosistema de *software*. El repositorio de GitHub donde se aloja la herramienta es público, permitiendo que la comunidad participe activamente en su desarrollo.

## Introducción

El proyecto word2speech tiene como objetivo principal la **creación dinámica y personalizada de estímulos auditivos** para reforzar la conciencia fonológica, permitiendo un control granular sobre la prosodia.

Si desea contribuir, por favor siga estos pasos generales:

1.  **Reporte de Problemas o Sugerencias:** Cualquier problema o sugerencia de mejora puede ser trasladada a través de los **Issues** del repositorio de GitHub.
2.  **Implementación de Nuevas Funcionalidades:** Para añadir un nuevo modelo TTS o implementar una nueva funcionalidad, se debe realizar un *fork* del proyecto y solicitar una *pull request*.
3.  **Integración Continua:** El repositorio cuenta con *tests* de integración básicos validados con un flujo de **GitHub Actions** en cada *push*.

## Entorno software

Para asegurar la reproducibilidad y la consistencia del desarrollo, el entorno de trabajo debe ser idéntico para todos los colaboradores

El repositorio contiene el fichero [environment.yml](./environment.yml), el cual permite a cualquier desarrollador crear un entorno [Conda](https://docs.anaconda.com/miniconda) que incluye todas las dependencias requeridas, incluyendo la versión exacta de Python y todas las librerías instaladas. Esto garantiza que se utiliza el mismo entorno de desarrollo para cualquier persona que participe en el proyecto.

Se recomienda utilizar este fichero para configurar su entorno local antes de comenzar a desarrollar.

```shell
$ conda env create -f environment.yml
```

Para entornos windows replicamos el entorno ejecutando el fichero [windows-env.yml](./windows-env.yml):

```cmd
> conda env create -f windows-env.yml
```

## Reconstrucción de los datos

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
    ["abrazo", "abrazo"],
    ["bebida", "bebida"],
    ["organos", "órganos"]
  ],
  "nopalabras": [
    ["babados", "babados"],
    ["bacela", "bacela"],
    ["plataco", "plátaco"],
    ["estupido", "estúpido"]
  ]
}
```

El fichero resultante tiene una clave, palabra y nopalabra, por directorio y dentro una tupla con las el nombre del fichero que se va a generar y el audio que va a generar.
