from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")
    bot_token: str
    perfume_backend_api_token: str
    supabase_url: str
    supabase_key: str
    user_email: str
    user_password: str

    @field_validator("bot_token")
    def fixed_bot_token(cls, v: str = ":") -> str:
        return v.encode("utf-8").decode("unicode_escape")

    @field_validator("supabase_url")
    def fixed_supabase_url(cls, v: str = ":") -> str:
        return v.encode("utf-8").decode("unicode_escape")


app_settings = AppSettings()
