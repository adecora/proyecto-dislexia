#!/usr/bin/env python
"""
Herramienta de línea de comandos para transformar palabras
o ficheros (json) en audios.
"""

import argparse
import json
import os.path
import yaml
from requests.exceptions import HTTPError


from modules.transformer import Word2Speech
from modules.utilities import Normalizer


def check_point(point, Error):
    try:
        time, pitch = [int(op) for op in point.split(",")]
        if not 0 <= time <= 100:
            raise Error("El porcentaje de tiempo tiene que estar entre 0 y 100.")
        if not -100 <= pitch <= 100:
            raise Error("El porcentaje de entonación tiene que estar entre -100 y 100.")
        return time, pitch
    except ValueError as error:
        raise Error("Los valores de tiempo y entonación han de ser enteros.") from error


def set_config(file):
    """Lee el fichero de configuración."""
    config = yaml.load(file, yaml.Loader)
    if "contour" in config:
        contour = []
        for point in config["contour"]:
            contour.append(
                check_point(
                    point, lambda msg: SystemExit("error: argument contour: %s" % msg)
                )
            )
        config["contour"] = contour

    file.close()
    return config


def is_valid_file_word(arg):
    """
    Valida que el argumento de entrada sea una palabra o un fichero
    con la estructura correcta.
    """
    if os.path.isfile(arg):
        with open(arg) as f:
            try:
                words = json.load(f)
                for value in words.values():
                    if not isinstance(value, list):
                        raise argparse.ArgumentTypeError(
                            "La estructura del fichero es incorrecta."
                        )
                return words
            except json.JSONDecodeError as error:
                raise argparse.ArgumentTypeError(
                    "El formato del fichero es incorrecto."
                ) from error
    else:
        return arg


def validate_countour_points(arg):
    return check_point(arg, argparse.ArgumentTypeError)


def save_audio(file_name, file_content):
    """Guarda el fichero de audio descargado."""
    with open(file_name, "wb") as audio_file:
        audio_file.write(file_content)


def parse_arguments():
    """Analiza la línea de comandos para los argumentos de entrada."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser._positionals.title = "Argumentos posicionales"
    parser._optionals.title = "Argumentos opcionales"
    parser.add_argument(
        "-h", "--help", action="help", help="Muestra este mensaje de ayuda y sale."
    )
    parser.add_argument(
        dest="word",
        metavar="palabra/fichero",
        type=is_valid_file_word,
        help="Palabra/fichero a convertir",
    )
    parser.add_argument(
        "--config",
        metavar="config.yml",
        type=argparse.FileType("r"),
        help="Archivo de configuración YAML",
    )
    parser.add_argument("--token", metavar="12345", help="Token de autentificación")
    parser.add_argument("--email", metavar="user@domain.com", help="Correo electrónico")
    parser.add_argument("--voice", metavar="Alvaro", help="Voz a utilizar")
    parser.add_argument(
        "--format",
        choices={"mp3", "wav", "ogg"},
        help="Formato del fichero resultante (default: mp3)",
    )
    parser.add_argument(
        "--speed",
        metavar="default: 1.0",
        type=float,
        help="Velocidad de reproducción (rango de 0.1 a 2.0)",
    )
    parser.add_argument(
        "--pitch",
        metavar="default: 0",
        type=int,
        help="Tono de voz (rango de -20 a 20)",
    )
    parser.add_argument(
        "--emotion",
        choices={"good", "evil", "neutral"},
        help="Emoción de la voz (default: neutral)",
    )
    parser.add_argument(
        "--bitrate",
        metavar="default: 48000",
        type=int,
        help="Tasa de muestreo (rango de 8000 a 192000 Hz)",
    )
    parser.add_argument(
        "--contour",
        "-c",
        metavar="x,y",
        action="append",
        type=validate_countour_points,
        help="""
Detalle de entonación de la palabra, se pueden escoger hasta 5 puntos.
    x - Porcentaje de duración de la palabra (0 a 100)
    y - Procentaje de entonación (-100 a 100)
""",
    )
    parser.add_argument(
        "--outfile",
        "-o",
        metavar="fichero",
        default="out",
        help="Guarda el audio con el nombre %(metavar)s",
    )
    return parser.parse_args()


def main():
    """Ejecuta el programa de línea de comandos."""
    args = parse_arguments()

    if args.config:
        config = set_config(args.config)
    else:
        config = {}
    if args.token:
        config.update({"token": args.token})
    if args.email:
        config.update({"email": args.email})
    if args.voice:
        config.update({"voice": args.voice})
    if args.format:
        config.update({"format": args.format})
    if args.speed:
        config.update({"speed": args.speed})
    if args.pitch:
        config.update({"pitch": args.pitch})
    if args.emotion:
        config.update({"emotion": args.emotion})
    if args.bitrate:
        config.update({"bitrate": args.bitrate})
    if args.contour:
        config.update({"contour": args.contour})

    speech = Word2Speech(config)
    try:
        if isinstance(args.word, dict):
            norm = Normalizer()
            for dirname, words in args.word.items():
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                for word in words:
                    file_name = norm.normalize(word)
                    audio, file_format = speech.convert(word)
                    save_audio(f"{dirname}/{file_name}.{file_format}", audio)
        else:
            file_name = args.outfile
            audio, file_format = speech.convert(args.word)
            save_audio(f"{file_name}.{file_format}", audio)
    except HTTPError as error:
        raise SystemExit(error.args[0])


if __name__ == "__main__":
    main()
