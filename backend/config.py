from fastapi import FastAPI
from pydantic_settings import SettingsConfigDict
from pydantic_settings import BaseSettings

app = FastAPI()

class Settings(BaseSettings):
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str

    model_config = SettingsConfigDict(env_file=".env")

    