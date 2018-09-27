import os


class Config:

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('APP_SECRET')
    DATABASE_URL = os.getenv('DATABASE_URL')



class DevelopmentConfig(Config):

    DEBUG = True


class TestingConfig(Config):

    TESTING = True
    DEBUG = True
    DATABASE_URL = "postgresql://postgres:ruth4boaz@localhost:5432/mt_trackr_test_db"




app_configuration = {
    "dev": DevelopmentConfig,
    "testing": TestingConfig
}
