# word2speech/__main__.py
from word2speech import main

from .modules import create_config

if __name__ == "__main__":
    create_config()
    main()
