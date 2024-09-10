#!/usr/bin/env python
import json
import glob
import sys

from modules.parser import parse_file


files = glob.glob("converted/*_palabras.csv")
palabras = set()
for file in files:
    palabras.update(parse_file(file))

files = glob.glob("converted/*_nopalabras.csv")
nopalabras = set()
for file in files:
    nopalabras.update(parse_file(file))

# La página "no palabras" del fichero contienen las subcabeceras parte_a y parte_b
# las eliminamos del resultado
nopalabras.discard("parte_a")
nopalabras.discard("parte_b")

json.dump(
    {"palabras": sorted(palabras), "nopalabras": sorted(nopalabras)},
    sys.stdout,
    indent=2,
    ensure_ascii=False,
)
