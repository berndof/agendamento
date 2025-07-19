import logging
import os

logger = logging.getLogger(__name__)

def get_database_url() -> str:
    db_data: dict[str, str] = {
        "host": os.getenv("POSTGRES_HOST", "postgres"),
        "port": "5432",
        "user": os.getenv("POSTGRES_USER", ""),
        "password": os.getenv("POSTGRES_PASSWORD", ""),
        "db_name": os.getenv("POSTGRES_DB", ""),
    }

    for key, value in db_data.items():
        if not value:
            raise ValueError(
                f"Missing environment variable for Postgres connection: {key}"
            )

    return (
        f"postgresql+asyncpg://{db_data['user']}:{db_data['password']}"
        f"@{db_data['host']}:{db_data['port']}/{db_data['db_name']}"
    )
