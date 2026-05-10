from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AegisID"
    API_V1_STR: str = "/api/v1"
    W3UP_TOKEN: str
    FERNET_KEY: str
    CONTRACT_ADDRESS: str
    WEB3_PROVIDER_URI: str
    CHAIN_ID: int = 11155111

    class Config:
        env_file = ".env"

settings = Settings()
