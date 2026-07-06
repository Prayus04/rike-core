from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    rikeEnv: str = "development"
    rikeHost: str = "0.0.0.0"
    rikePort: int = 8000
    rikeDataDir: str = "/data"

    class Config:
        env_file = ".env"


settings = Settings()
