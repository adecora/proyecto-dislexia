"""
Sistema de gestión de la configuración.
"""

import logging
import os
from pathlib import Path

import yaml

log = logging.getLogger(__name__)


class Config:
    """Clase para manejar la configuración de word2speech"""

    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.yml"
        self._config = self._load_config()

    def _get_config_dir(self):
        """Obtiene el directorio de configuración"""
        # Primero buscamos en el directorio de trabajo actual
        local_config = Path.cwd() / ".word2speech"
        if local_config.exists():
            return local_config

        # Usamos la configuración global del usuario
        config_home = os.environ.get("XDG_CONFIG_HOME")
        if config_home:
            return Path(config_home) / "word2speech"
        else:
            return Path.home() / ".word2speech"

    def _load_config(self):
        """Carga la configuración desde un fichero"""
        if not self.config_file.exists():
            return {}

        try:
            with open(self.config_file, "r", encoding="utf8") as fd:
                return yaml.safe_load(fd) or {}
        except Exception as e:
            log.warning(f"Fallo al cargar la configuración: {e}")

    def get_model_config(self, model_id):
        """Carga la configuración de un modelo específico"""
        models = self._config.get("models", {})
        return models.get(model_id, {})


config = Config()
