import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'HAHAHAH_FLASH))'
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_reset_on_return": "rollback"
    }
    DOCKER_DB_HOST = os.environ.get("POSTGRES_HOST")
    DB_HOST = DOCKER_DB_HOST if DOCKER_DB_HOST else "localhost"
    SQLALCHEMY_DATABASE_URI = f"postgresql://flash:dydka@{DB_HOST}:5432/database"
