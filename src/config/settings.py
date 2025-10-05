"""Application settings and configuration."""

import os
from typing import Optional
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database settings
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/data_pragyan",
        env="DATABASE_URL"
    )
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="data_pragyan", env="DB_NAME")
    db_user: str = Field(default="postgres", env="DB_USER")
    db_password: str = Field(default="postgres", env="DB_PASSWORD")
    
    # AI/LLM settings
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    llm_model: str = Field(default="gemini-2.0-flash-exp", env="LLM_MODEL")
    llm_temperature: float = Field(default=0.1, env="LLM_TEMPERATURE")
    custom_llm_endpoint: Optional[str] = Field(default=None, env="CUSTOM_LLM_ENDPOINT")
    custom_llm_api_key: Optional[str] = Field(default=None, env="CUSTOM_LLM_API_KEY")
    
    # Application settings
    app_env: str = Field(default="development", env="APP_ENV")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    max_upload_size: int = Field(default=200, env="MAX_UPLOAD_SIZE")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")
    
    # Security settings
    secret_key: str = Field(default="dev-secret-key", env="SECRET_KEY")
    allowed_hosts: str = Field(default="localhost,127.0.0.1", env="ALLOWED_HOSTS")
    
    # File storage settings
    upload_dir: Path = Field(default=Path("./uploads"), env="UPLOAD_DIR")
    log_dir: Path = Field(default=Path("./logs"), env="LOG_DIR")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs) -> None:
        """Initialize settings and create directories."""
        super().__init__(**kwargs)
        self.upload_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env.lower() == "production"