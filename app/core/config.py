
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Application Settings
    APP_NAME: str = "ERP AI Assistant"

    # AI Assistant Database Settings
    AI_DB_HOST: str = "localhost"
    AI_DB_PORT: int = 3306
    AI_DB_USER: str = "root"
    AI_DB_PASSWORD: str = ""
    AI_DB_NAME: str = "ai_assistant_db"

    # ERP Database Settings
    ERP_DB_HOST: str = "localhost"
    ERP_DB_PORT: int = 3306
    ERP_DB_USER: str = "root"
    ERP_DB_PASSWORD: str = ""
    ERP_DB_NAME: str = "erp_ai_assistant_test"

    # Legacy Database Settings
    # Kept temporarily until database.py is migrated.
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "erp_ai_assistant_test"

    # LLM General Settings
    LLM_PROVIDER: Literal["ollama", "openai", "kimi"] = "ollama"

    LLM_TEMPERATURE: float = Field(
        default=0.1,
        ge=0,
        le=2
    )

    LLM_MAX_TOKENS: int = Field(
        default=500,
        gt=0
    )

    LLM_TIMEOUT: int = Field(
        default=120,
        gt=0
    )

    # Ollama Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen3:4b-instruct-2507-q4_K_M"

    # OpenAI Settings
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = ""

    # Kimi Settings
    KIMI_API_KEY: str = ""
    KIMI_BASE_URL: str = "https://api.moonshot.ai/v1"
    KIMI_MODEL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
