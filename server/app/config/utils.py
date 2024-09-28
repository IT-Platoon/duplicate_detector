from os import environ

from app.config.default import DefaultSettings
from app.config.production import ProductionSettings


def get_settings() -> DefaultSettings:
    env = environ.get("ENV", "local")
    if env == "local":
        return DefaultSettings()
    if env == "prod":
        return ProductionSettings()
    return DefaultSettings()
