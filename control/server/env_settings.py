from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False
    version: str = ""
    secret_key: str = ""

    ############################################################################
    # SQL database settings
    sql_database_name: str = ""
    sql_database_user: str = ""
    sql_database_password: str = ""
    sql_database_host: str = ""

    ############################################################################
    # Config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


SETTINGS = Settings()
