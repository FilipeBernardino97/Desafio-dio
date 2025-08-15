from decouple import config

class Settings:
    DATABASE_URL: str = config("DATABASE_URL")

settings = Settings()