import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'e7d21abac1602651114761c1cd93b24e'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Q!]'
    FLASKY_MAIL_SENDER = 'qquestionaire@163.com'
    FLASKY_ADMIN = 'qquestionaire@163.com'
    FLASK_POSTS_PER_PAGE = 10
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    # MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'qquestionaire@163.com'
    MAIL_PASSWORD = 'TRIFPWOKJEUEPIFE'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-test.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}