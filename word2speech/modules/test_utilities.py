import pytest
import unicodedata

from utilities import Normalizer, Contour


def test_normalizar():
    norm = Normalizer()
    assert norm.normalize("jalapeños") == unicodedata.normalize("NFD", "jalapeños")
    assert norm.normalize("día") == "dia"
    assert norm.normalize("táfuci") == "tafuci"
    assert norm.normalize("NIÑO") == unicodedata.normalize("NFD", "niño")
    assert norm.normalize("ambigüo") == "ambiguo"


def test_contour_succeed():
    contour = Contour([(10, 80), (30, 100), (60, -10)])
    assert (
        format(contour, "Palabra")
        == '<prosody contour="(10%,+80%) (30%,+100%) (60%,-10%)">Palabra</prosody>'
    )


def test_contour_fail():
    with pytest.raises(SystemExit) as exec_info:
        Contour([(10, 80), (30, 100), (60, -10), (65, -20), (70, 0), (80, 15)])

    assert exec_info.type is SystemExit
    assert (
        exec_info.value.args[0]
        == "error: No puede haber más de cinco puntos de entonación"
    )
