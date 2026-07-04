from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AHIP API"
    database_url: str = "postgresql+psycopg2://ahip:ahip_password@localhost:5432/ahip_db"
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
