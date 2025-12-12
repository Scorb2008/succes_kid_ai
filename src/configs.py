from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings
from .logger import setup_logger
logger = setup_logger()
class BotConfig(BaseSettings):
    MISTRAL_API_KEY: str = Field(..., validation_alias="MISTRAL_API_KEY")
    BOT_TOKEN: str = Field(..., validation_alias="BOT_TOKEN")
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    @field_validator('MISTRAL_API_KEY', 'BOT_TOKEN')
    @classmethod
    def check_tokens(cls, v: str, info) -> str:
        if not v:
            field_name = info.field_name
            logger.error(f'Токен {field_name} не найден в переменных окружения')
            raise ValueError(f'Токен {field_name} не найден')
        if v.startswith("your_") or "example" in v.lower():
            logger.warning(f'Токен выглядит как пример или placeholder')
        return v

