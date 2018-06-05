import os


class Config:

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('APP_SECRET')


class DevelopmentConfig(Config):

    DEBUG = True


class TestingConfig(Config):

    TESTING = True
    DEBUG = True


app_configuration = {
    "dev": DevelopmentConfig,
    "testing": TestingConfig
}
