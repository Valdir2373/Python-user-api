import os
from dotenv import load_dotenv

load_dotenv()

class ConfigEnv:
    def get(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise KeyError(f"Variável de ambiente '{key}' não está definida.")
        return value