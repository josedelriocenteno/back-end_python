from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Backend Dockerizado"
    app_env: str = "dev"
    database_url: str = "postgresql://user:pass@db:5432/db"

    class Config:
        env_file = ".env"

settings = Settings()
