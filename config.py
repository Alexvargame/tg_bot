import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )
    bot_token: str

settings = Settings()
#BOT_TOKEN = os.getenv('BOT_TOKEN')
# BOT_TOKEN = '7400807567:AAHRlyXQLvGigGDm4QBjEJakirk4QO-pl1c'