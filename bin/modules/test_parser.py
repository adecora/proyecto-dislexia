from parser import parse_file


def test_parser():
    expected_result = ["uno", "dos", "tres", "cuatro", "cinco", "seis"]
    actual_result = [word for word in parse_file("test_data/palabras.csv")]
    assert actual_result == expected_result
