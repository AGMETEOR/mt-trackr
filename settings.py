import os


class Config:

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('APP_SECRET')
    DATABASE_NAME = "mt_trackr_db"


class DevelopmentConfig(Config):

    DEBUG = True


class TestingConfig(Config):

    TESTING = True
    DEBUG = True
    DATABASE_NAME = "mt_trackr_test_db"


app_configuration = {
    "dev": DevelopmentConfig,
    "testing": TestingConfig
}
