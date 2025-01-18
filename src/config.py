from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8"
    )

    bot_token: str
    supabase_url: str
    supabase_key: str
    user_email: str
    user_password: str


# from pydantic import HttpUrl, Field
# from pydantic_settings import BaseSettings, SettingsConfigDict
# class AppConfig(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         case_sensitive=True,
#         extra="forbid",
#     )
