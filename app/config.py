from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    openai_api_key: str
    twilio_account_sid:str
    twilio_auth_token: str
    service_account_file: str
    scopes: str
    spreadsheet_id: str
    range_name: str
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str
    assistant_id: str
    model: str

    class Config:
        env_file = ".env"

settings = Settings()
