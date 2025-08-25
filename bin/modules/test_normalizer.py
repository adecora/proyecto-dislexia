import unicodedata

from normalizer import normalizer


def test_normalizar():
    assert normalizer.normalize("jalapeños") == unicodedata.normalize("NFD", "jalapeños")
    assert normalizer.normalize("día") == "dia"
    assert normalizer.normalize("táfuci") == "tafuci"
    assert normalizer.normalize("NIÑO") == unicodedata.normalize("NFD", "niño")
    assert normalizer.normalize("ambigüo") == "ambiguo"
