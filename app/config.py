from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")
    bot_token: str
    perfume_backend_api_token: str
    supabase_url: str
    supabase_key: str
    user_email: str
    user_password: str


app_settings = AppSettings()
