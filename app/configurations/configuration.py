from pydantic import BaseModel


class Configuration(BaseModel):
    """Stores basic application configuration."""

    version: int = 0
    application_name: str | None = "lavs-api"
    database_name: str = "test.db"
