import csv


def parse_file(file):
    with open(file) as fd:
        reader = csv.reader(fd)
        # Omitimos las cabeceras del fichero de palabras
        next(reader)
        for row in reader:
            for word in row:
                # Evitamos las celdas vacías
                if word:
                    yield word
