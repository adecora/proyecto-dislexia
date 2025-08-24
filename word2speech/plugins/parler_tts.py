"""
Implementación del modelo TTS Parler-TTS
Utilizando la abstracción de la plantilla TTSModel
"""

from io import BytesIO

from ..config import config
from ..models import TTSModel

try:
    import numpy as np
    import scipy.io.wavfile as wavfile
    import soundfile as sf
    import torch
    from parler_tts import ParlerTTSForConditionalGeneration
    from transformers import AutoTokenizer

    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False


class ParlerModel(TTSModel):
    """Modelo TTS de Parler-TTS con interfaz unificada."""

    def __init__(self):
        if not DEPS_AVAILABLE:
            raise ImportError(
                "Las dependencias de Parler-TTS no están disponibles. Instalalas con: pip install git+https://github.com/huggingface/parler-tts.git"
            )

        super().__init__("parler-tts/parler-tts-mini-multilingual-v1.1", "Parler-TTS Multilingual")
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self._model = None
        self._tokenizer = None
        self._description_tokenizer = None
        # @click.option("--speed", type=float, help="Velocidad del habla: 0.1-2.0 (default: 1.0)")
        # @click.option("--pitch", help="Tono: low/normal/high or -20 to 20 (default: 0)")
        # @click.option("--emotion", help="Emoción: calm/energetic/neutral (default: neutral)")

        # Opciones de prosodia predefinidas
        self.speaker_map = {"male": "Steven's voice", "female": "Olivia's voice"}
        self.emotion_map = {"calm": "warm and soothing", "energetic": "clear and energetic", "neutral": "deep and whispering"}

    @property
    def model(self):
        """Lazy load model."""
        if self._model is None:
            self._model = ParlerTTSForConditionalGeneration.from_pretrained(self.model_id).to(self.device)
        return self._model

    @property
    def tokenizer(self):
        """Lazy load tokenizer."""
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        return self._tokenizer

    @property
    def description_tokenizer(self):
        """Lazy load description tokenizer."""
        if self._description_tokenizer is None:
            self._description_tokenizer = AutoTokenizer.from_pretrained(self.model.config.text_encoder._name_or_path)
        return self._description_tokenizer

    def generate(self, text, **kwargs):
        """Generar audio usando Parler-TTS"""
        # Genera el prompt con la descripción de la voz
        description = self._build_voice_description(**kwargs)

        # Tokeniza las entradas
        input_ids = self.description_tokenizer(description, return_tensors="pt").input_ids.to(self.device)
        prompt_input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(self.device)

        # Genera el audio
        generation = self.model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
        audio_arr = generation.cpu().numpy().squeeze()

        # Guardamos en un buffer y leemos los bytes
        buffer = BytesIO()
        sf.write(buffer, audio_arr, self.model.config.sampling_rate, format="WAV")
        buffer.seek(0)  # Salvaguarda incio del audio
        audio_bytes = buffer.read()

        return (audio_bytes, "wav", 0, 0)

    def supports(self, feature):
        """Comprobar si el modelo admite una función específica"""
        supported_features = {
            "ssml": False,
            "voices": True,  # Acepta female/male
            "contour": False,
            "offline": True,
        }
        return supported_features

    def _build_voice_description(self, **kwargs):
        """Construye la descripción de la voz para Parler-TTS."""
        model_config = config.get_model_config(self.model_id)

        # Parámetros por defecto
        speaker = model_config.get("speaker", "Steven's voice")
        speed = model_config.get("speed", "slow")
        pitch = model_config.get("pitch", "normal")
        emotion = model_config.get("emotion", "deep and whispering")

        if "voice" in kwargs:
            speaker = self.speaker_map.get(kwargs["voice"].lower(), speaker)
        if "speed" in kwargs:
            if kwargs["speed"] <= 0.5:
                speed = "very slow"
            elif kwargs["speed"] >= 1.5:
                speed = "normal"
            else:
                speed = "slow"
        if "pitch" in kwargs:
            try:
                pitch = int(kwargs["pitch"])
                if pitch <= -10:
                    pitch = "low"
                elif pitch >= 10:
                    pitch = "high"
                else:
                    pitch = "normal"
            except ValueError:
                pitch = kwargs["pitch"]
        if "emotion" in kwargs:
            emotion = self.emotion_map.get(kwargs["emotion"].lower(), emotion)

        # Construimos la descripción
        return f"{speaker} is {emotion}, speaking {speed} with a {pitch} pitch, recorded with very smooth intonation for natural prosody."
