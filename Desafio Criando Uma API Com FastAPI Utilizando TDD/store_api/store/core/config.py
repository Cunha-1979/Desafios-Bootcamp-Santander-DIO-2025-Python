from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"

    # MongoDB
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_DB: str
    MONGO_USER: str
    MONGO_PASSWORD: str

    # URL completa opcional
    DATABASE_URL: str = None

    model_config = SettingsConfigDict(env_file=".env")

    def get_database_url(self) -> str:
        """Constrói DATABASE_URL se não estiver definido"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"


settings = Settings()

