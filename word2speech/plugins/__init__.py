from .speechgen import SpeechGenModel


def discover_models():
    """Descubre y registra todos los modelos disponibles."""
    from ..models import registry

    # Registramos el modelo de SpeechGen
    speechgen = SpeechGenModel()
    registry.register(speechgen, aliases=["speechgen", "default"])


__all__ = ["discover_models", "SpeechGenModel"]
