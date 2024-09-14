from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    url: str = Field(default="sqlite+aiosqlite:///./db.sqlite3", alias="DATABASE_URL")
    echo: bool = Field(default=True, alias="DATABASE_ECHO")


class RedisConfig(BaseSettings):
    host: str = Field(default="localhost", alias="REDIS_HOST")
    port: int = Field(default=6379, alias="REDIS_PORT")
    db: int = Field(default=0, alias="REDIS_DB")


class ElasticsearchConfig(BaseSettings):
    host: str = Field(default="localhost", alias="ES_HOST")
    port: int = Field(default=9200, alias="ES_PORT")
    id: str = Field(default="id", alias="ES_ID")
    password: str = Field(default="<PASSWORD>", alias="ES_PASSWORD")
    verify_ssl: bool = Field(default=False, alias="ES_VERIFY_SSL")


class CORSConfig(BaseSettings):
    origins: str = Field(default="*", alias="CORS_ORIGINS")
    credentials: bool = Field(default=True, alias="CORS_CREDENTIALS")
    methods: str = Field(default="*", alias="CORS_METHODS")
    headers: str = Field(default="*", alias="CORS_HEADERS")


class WebConfig(BaseSettings):
    host: str = Field(default="0.0.0.0", alias="WEB_HOST")
    port: int = Field(default=8000, alias="WEB_PORT")


db = DatabaseConfig()
cors = CORSConfig()
web = WebConfig()
redis = RedisConfig()
elasticsearch = ElasticsearchConfig()
