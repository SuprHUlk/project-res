from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_key: str
    mongodb_url: str
    jwt_key: str
    model_config = SettingsConfigDict(env_file=".env")

def get_settings():
    return Settings()