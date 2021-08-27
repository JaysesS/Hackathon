class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'HAHAHAH_FLASH))'
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_reset_on_return": "rollback"
    }
    SQLALCHEMY_DATABASE_URI = "postgresql://flash:dydka@localhost:5432/database"
