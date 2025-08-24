#!/usr/bin/env python
"""
Herramienta de Generación de Audio Adaptativo mediante TTS para la mejora de la
conciencia en dificultades específicas del aprendizaje.
"""

import logging
import sys

import click

from .config import config
from .modules import Word2Speech

log = logging.getLogger(__name__)


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Mostrar version")
@click.option("--verbose", "-v", is_flag=True, help="Verbose logging")
@click.pass_context
def cli(ctx, version, verbose):
    """word2speech: TTS adaptativo para el tratamiento de la dislexia."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s: %(message)s", force=True)
    else:
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s", datefmt="%H:%M:%S", force=True)

    if version:
        click.echo("word2speech version 1.0.3")
        return

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("text")
@click.option("-o", "--output", default="out", help="Nombre del archivo de salida")
@click.option("--voice", help="Voz: male/female o nombre específico (p.ej., 'Alvaro')")
@click.option("--speed", type=float, help="Velocidad del habla: 0.1-2.0 (default: 1.0)")
@click.option("--pitch", help="Tono: low/normal/high or -20 to 20 (default: 0)")
@click.option("--emotion", help="Emoción: calm/energetic/neutral (default: neutral)")
@click.option("--format", "audio_format", type=click.Choice(["mp3", "wav", "ogg"]), default="mp3", help="Formato de audio (default: mp3)")
def speak(text, output, voice, speed, pitch, emotion, audio_format):
    """
    Generar voz a partir de texto usando modelos TTS.

    \b
    Ejemplos:
        word2speech speak "hola mundo"
        word2speech speak "hola" --voice female --speed 1.2 --emotion calm
    """
    options = config.get_model_config("speechgen.io")
    print(options)
    # TODO: Audio de salida siempre va ser formato wav
    options["format"] = "wav"
    if voice:
        options["voice"] = voice
    if speed:
        options["speed"] = speed
    if pitch:
        options["pitch"] = pitch
    if emotion:
        options["emotion"] = emotion

    try:
        speech = Word2Speech(options)
        log.info(f'Generando audio: "{text}"')
        audio, file_format, cost, balance = speech.convert(text)
        output_file = f"{output}.{file_format}"
        with open(output_file, "wb") as f:
            f.write(audio)

        log.info(f'Audio generado "{output_file}" (coste: {cost}, saldo: {balance})')

    except Exception as e:
        click.echo(f"Error generando audio: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("word")
@click.option("-o", "--output", default="out_spell", help="Nombre del archivo de salida")
@click.option("--pause", default=250, help="Pausa entre sílabas (ms)")
@click.option("--include-word", is_flag=True, help="Incluir palabra completa al final")
def spell(word, output, pause, include_word):
    """Deletrea una palabra sílaba a sílaba"""

    from .modules.deletrear import spell_word

    try:
        spelled_text = spell_word(word, pause)
        if include_word:
            spelled_text += f'<break time="1s" /> {word}'

        log.info(f'Generando deletreo de sílabas: "{word}"')
        log.info(f"Texto deletreado: {spelled_text}")

        options = config.get_model_config("speechgen.io")
        speech = Word2Speech(options)
        audio, file_format, cost, balance = speech.convert(spelled_text)
        output_file = f"{output}.{file_format}"
        with open(output_file, "wb") as f:
            f.write(audio)

        log.info(f'Audio deletreado generado "{output_file}" (coste: {cost}, saldo: {balance})')

    except Exception as e:
        click.echo(f"Error generando audio deletreado: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("word")
@click.option("-o", "--output", default="out_prosody", help="Nombre del archivo de salida")
@click.option("--rate", default="medium", help="Velocidad del habla")
@click.option("--pitch-level", default="medium", help="Nivel de tono")
@click.option("--volume", default="medium", help="Nivel de volumen")
def prosody(word, output, rate, pitch_level, volume):
    """Genera voz con prosodia mejorada usando SSML y AFI"""

    from .modules.prosodia import ssml_for_word

    try:
        ssml_text, ssml_log = ssml_for_word(word, rate=rate, pitch=pitch_level, volume=volume)

        log.info(f'Generando audio enriquecido con prosodia: "{word}"')
        log.info(f"SSML: {ssml_text}")

        options = config.get_model_config("speechgen.io")
        speech = Word2Speech(options)
        audio, file_format, cost, balance = speech.convert(ssml_text)
        output_file = f"{output}.{file_format}"
        with open(output_file, "wb") as f:
            f.write(audio)

        log.info(f'Audio prosódico generado "{output_file}" (coste: {cost}, saldo: {balance})')

    except Exception as e:
        click.echo(f"Error generando audio prosódico: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
