#!/usr/bin/env python
"""
Herramienta de Generación de Audio Adaptativo mediante TTS para la mejora de la
conciencia en dificultades específicas del aprendizaje.
"""

import logging
import sys

import click

from .config import config
from .models import registry
from .modules import Word2Speech
from .plugins import discover_models

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

    # Registra todos los modelos disponibles
    discover_models()

    if version:
        click.echo("word2speech version 1.0.3")
        return

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("text")
@click.option("-m", "--model", default="speechgen.io", help="Modelo TTS a usar (default: speechgen.io)")
@click.option("-o", "--output", default="out", help="Nombre del archivo de salida")
@click.option("--voice", help="Voz: male/female o nombre específico (p.ej., 'Alvaro')")
@click.option("--speed", type=float, help="Velocidad del habla: 0.1-2.0 (default: 1.0)")
@click.option("--pitch", help="Tono: low/normal/high or -20 to 20 (default: 0)")
@click.option("--emotion", help="Emoción: calm/energetic/neutral (default: neutral)")
def speak(text, model, output, voice, speed, pitch, emotion):
    """
    Generar voz a partir de texto usando modelos TTS.

    \b
    Ejemplos:
        word2speech speak "hola mundo"
        word2speech speak "hola" --voice female --speed 1.2 --emotion calm

    \b
    Para listar los modelos:
        word2speech models
    """
    tts_model = registry.get(model)
    if not tts_model:
        click.echo(f"Moldelo '{model}' no encontrado.", err=True)
        click.echo("Usa 'word2speech models' para ver los modelos disponibles.", err=True)
        sys.exit(1)

    options = {}
    if voice:
        options["voice"] = voice
    if speed:
        options["speed"] = speed
    if pitch:
        try:
            options["picth"] = int(pitch)
        except ValueError:
            picth_map = {"low": -10, "normal": 0, "high": 10}
            options["picth"] = picth_map.get(pitch.lower(), 0)
    if emotion:
        options["emotion"] = emotion

    try:
        log.info(f'Generando audio: "{text}"')
        audio, file_format, cost, balance = tts_model.generate(text, **options)

        output_file = f"{output}.{file_format}"
        with open(output_file, "wb") as f:
            f.write(audio)

        log.info(f'Audio generado "{output_file}" (coste: {cost}, saldo: {balance})')

    except Exception as e:
        click.echo(f"Error generando audio: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("word")
@click.option("-m", "--model", default="speechgen.io", help="Modelo TTS a usar (default: speechgen.io)")
@click.option("-o", "--output", default="out_spell", help="Nombre del archivo de salida")
@click.option("--pause", default=250, help="Pausa entre sílabas (ms)")
@click.option("--include-word", is_flag=True, help="Incluir palabra completa al final")
def spell(word, model, output, pause, include_word):
    """Deletrea una palabra sílaba a sílaba"""
    tts_model = registry.get(model)
    if not tts_model:
        click.echo(f"Moldelo '{model}' no encontrado.", err=True)
        click.echo("Usa 'word2speech models' para ver los modelos disponibles.", err=True)
        sys.exit(1)

    from .modules.deletrear import spell_word

    try:
        spelled_text = spell_word(word, pause)
        if include_word:
            spelled_text += f'<break time="1s" /> {word}'

        log.info(f'Generando deletreo de sílabas: "{word}"')
        log.info(f"Texto deletreado: {spelled_text}")

        audio, file_format, cost, balance = tts_model.generate(spelled_text)
        output_file = f"{output}.{file_format}"

        with open(output_file, "wb") as f:
            f.write(audio)

        log.info(f'Audio deletreado generado "{output_file}" (coste: {cost}, saldo: {balance})')

    except Exception as e:
        click.echo(f"Error generando audio deletreado: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("word")
@click.option("-m", "--model", default="speechgen.io", help="Modelo TTS a usar (default: speechgen.io)")
@click.option("-o", "--output", default="out_prosody", help="Nombre del archivo de salida")
@click.option("--rate", default="medium", help="Velocidad del habla")
@click.option("--pitch-level", default="medium", help="Nivel de tono")
@click.option("--volume", default="medium", help="Nivel de volumen")
def prosody(word, model, output, rate, pitch_level, volume):
    """Genera voz con prosodia mejorada usando SSML y AFI"""
    tts_model = registry.get(model)
    if not tts_model:
        click.echo(f"Moldelo '{model}' no encontrado.", err=True)
        click.echo("Usa 'word2speech models' para ver los modelos disponibles.", err=True)
        sys.exit(1)

    from .modules.prosodia import ssml_for_word

    try:
        ssml_text, ssml_log = ssml_for_word(word, rate=rate, pitch=pitch_level, volume=volume)

        log.info(f'Generando audio enriquecido con prosodia: "{word}"')
        log.info(f"SSML: {ssml_text}")

        audio, file_format, cost, balance = tts_model.generate(ssml_text)
        output_file = f"{output}.{file_format}"

        with open(output_file, "wb") as f:
            f.write(audio)

        log.info(f'Audio prosódico generado "{output_file}" (coste: {cost}, saldo: {balance})')

    except Exception as e:
        click.echo(f"Error generando audio prosódico: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("model_name", required=False)
def models(model_name):
    """Lista los models TTS disponibles o muestra información detallada de un modelo."""
    available_models = registry.list_models()
    if not available_models:
        click.echo("No hay modelos TTS disponibles.")
        return

    # Muestra información detallada de un modelo
    if model_name:
        pass

    # Lista todos los modelos diponibles:
    click.echo("Modelos TTS disponibles:\n")

    for model in available_models:
        aliases = ", ".join(k for k, v in registry._aliases.items() if v is model.model_id)

        if aliases:
            click.echo(f"• {model.model_id} ({aliases})")
        else:
            click.echo(f"• {model.model_id}")

        # Ejemplos de uso
        if model.model_id == "speechgen.io":
            click.echo('  Uso: word2speech speak "text" --voice Alvaro --emotion good')
            click.echo("  Setup: word2speech keys set speechgen TU_TOKEN")
            click.echo("  Setup: word2speech keys set speechgen-email TU_EMAIL")


@cli.group()
def keys():
    """Manejo de las APIs para los modelos TTS."""
    pass


@keys.command("set")
@click.argument("provider")
@click.argument("key")
def keys_set(provider, key):
    """
    Configura la clave API.

    Para SpeechGen.io, es necesario:
      word2speech keys set speechgen TU_TOKEN
      word2speech keys set speechgen-email TU_EMAIL
    """
    config.set_api_key(provider, key)
    click.echo(f"Establecida clave API para: {provider}")

    if provider == "speechgen":
        click.echo("No olvides configurar también tu email:")
        click.echo("  word2speech keys set speechgen-email TU_EMAIL")
    elif provider == "speechgen-email":
        click.echo("No olvides configurar también tu token:")
        click.echo("  word2speech keys set speechgen TU_TOKEN")


@keys.command("list")
def keys_list():
    """Lista las claves API configuradas."""
    keys_dict = config.list_keys()
    if not keys_dict:
        click.echo("No hay claves API configuradas.")
        return

    click.echo("Claves API configuradas:")
    for provider, masked_key in keys_dict.items():
        click.echo(f"  {provider}: {masked_key}")


if __name__ == "__main__":
    cli()
