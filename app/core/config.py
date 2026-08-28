from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./todosapp.db"
    ALGORITHM: str =  "HS256"
    ACCESS_TOEKN_EXPIRY_MINUTES: int = 30
    SECRET_KEY : str
    model_config = SettingsConfigDict(env_file = ".env")
    
settings = Settings()