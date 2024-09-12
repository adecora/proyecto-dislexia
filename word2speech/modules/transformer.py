#!/usr/bin/env python
import os
import requests
from requests.exceptions import HTTPError

from utilities import Normalizer

URL = "https://speechgen.io/index.php?r=api/text"


def send_request(url, data):
    response = requests.post(url, data=data)
    return response.json()


def main(word, out):
    data = {
        "token": os.getenv("API_KEY"),
        "email": os.getenv("EMAIL"),
        "voice": "Alvaro",
        "text": word,
        "format": "mp3",
        "speed": 1.1,
        "pitch": 0,
        "emotion": "good",
    }

    response = send_request(URL, data)
    if response["status"] == 1:
        if "file" in response and "format" in response:
            file_url = response["file"]
            audio = requests.get(file_url).content
            with open(f"{out}.{response['format']}", "wb") as out_file:
                out_file.write(audio)
        else:
            raise HTTPError(f"404 Not Found: {response['error']}")
    else:
        if "login" in response["error"]:
            raise HTTPError(f"401 Unauthorized: {response['error']}")
        else:
            raise HTTPError(f"400 Bad Request: {response['error']}")


if __name__ == "__main__":
    import sys

    norm = Normalizer()
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        raise SystemExit(f"Uso {sys.argv[0]} palabra [salida]")
    main(
        sys.argv[1], norm.normalize(sys.argv[1]) if len(sys.argv) == 2 else sys.argv[2]
    )
