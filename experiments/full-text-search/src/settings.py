from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    sql_host: str = "localhost"
    sql_database: str = "postgres"
    sql_username: str = "postgres"
    sql_password: str = "postgres"
    sql_port: int = 5432

    @property
    def sql_dsn(self) -> str:
        return f"postgresql+psycopg://{self.sql_username}:{self.sql_password}@{self.sql_host}:{self.sql_port}/{self.sql_database}"


Settings = _Settings()
