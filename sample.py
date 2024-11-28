import argparse

parser = argparse.ArgumentParser(description=__doc__, add_help=False)
parser._positionals.title = "Argumentos posicionales"
parser._optionals.title = "Argumentos opcionales"
parser.add_argument(
    "-h", "--help", action="help", help="Muestra este mensaje de ayuda y sale."
)
parser.add_argument(
    dest="word",
    metavar="palabra/fichero",
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
    metavar="",
    action="append",
    help="Tasa de muestreo (rango de 8000 a 192000 Hz)",
)
parser.add_argument(
    "--outfile",
    "-o",
    metavar="fichero",
    default="out",
    help="Guarda el audio con el nombre %(metavar)s",
)

args = parser.parse_args()
