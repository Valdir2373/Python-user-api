from dataclasses import dataclass
from src.infra.config.ConfigEnv import ConfigEnv

@dataclass(frozen=True)
class IVariablesPostgres:
    host: str
    port: int
    user: str
    password: str
    database: str

class ConfigDB:
    def __init__(self, config: ConfigEnv):
        self._config = config

    def get_variables_postgresql(self) -> IVariablesPostgres:

        return IVariablesPostgres(
            host=self._config.get("POSTGRES_HOST"),
            port=int(self._config.get("POSTGRES_PORT")),
            user=self._config.get("POSTGRES_USER"),
            password=self._config.get("POSTGRES_PASSWORD"),
            database=self._config.get("POSTGRES_DATABASE")
        )