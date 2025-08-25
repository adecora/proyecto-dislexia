import re
import sys
import unicodedata


class Normalizer:
    """
    Normaliza las palabras, eliminado las marcas diacríticas
    excepto para la ñ (U+0303) y la ç (U+0327).
    """

    def __init__(self):
        self.cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)) and c not in (0x0303, 0x0327))

    def normalize(self, word):
        s = word.lower()
        a = unicodedata.normalize("NFD", s)
        b = a.translate(self.cmb_chrs)
        re.sub("[^a-z0-9ñç]", "", b)
        return b


# Instanciamos la clase
normalizer = Normalizer()
