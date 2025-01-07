from word2speech.main import set_config


def test_set_config():
    fd = open("config-example.yml", encoding="utf-8")
    config = set_config(fd)
    assert isinstance(config, dict)
    assert config.get("token") == 12345
    assert config.get("email") == "user@domain.com"
    assert config.get("voice") == "Alvaro"
