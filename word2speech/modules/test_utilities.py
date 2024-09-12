import unicodedata

from utilities import Normalizer


def test_normalizar():
    norm = Normalizer()
    assert norm.normalize("jalapeños") == unicodedata.normalize("NFD", "jalapeños")
    assert norm.normalize("día") == "dia"
    assert norm.normalize("táfuci") == "tafuci"
    assert norm.normalize("NIÑO") == unicodedata.normalize("NFD", "niño")
    assert norm.normalize("ambigüo") == "ambiguo"
