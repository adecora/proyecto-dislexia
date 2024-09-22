from main import set_config


def test_set_config():
    fd = open("config-example.yml")
    config = set_config(fd)
    assert isinstance(config, dict)
    assert config.get("token") == 12345
    assert config.get("email") == "user@domain.com"
    assert config.get("voice") == "Alvaro"
