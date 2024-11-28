import unicodedata
import sys
import re


class Normalizer:
    """
    Normaliza las palabras, eliminado las marcas diacríticas
    excepto para la ñ (U+0303) y la ç (U+0327).
    """

    def __init__(self):
        self.cmb_chrs = dict.fromkeys(
            c
            for c in range(sys.maxunicode)
            if unicodedata.combining(chr(c)) and c not in (0x0303, 0x0327)
        )

    def normalize(self, word):
        s = word.lower()
        a = unicodedata.normalize("NFD", s)
        b = a.translate(self.cmb_chrs)
        re.sub("[^a-z0-9ñç]", "", b)
        return b


class Contour:
    """
    Genera el contructor de entonación con los valores indicados, alrededor
    de la palabra.
        - contour: Puntos de entonación
        - word: Palabra a convertir
    """

    _template = '<prosody contour="{d.contour}">{word}</prosody>'

    def __init__(self, contour):
        if len(contour) > 5:
            raise SystemExit("error: No puede haber más de cinco puntos de entonación")
        self.contour = " ".join(f"({x}%,{y:+}%)" for x, y in contour)

    def __format__(self, word):
        return self._template.format(d=self, word=word)
