class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mathenge,./1998@127.0.0.1:5432/biddingsystem'
    SECRET_KEY = 'some=secret-key'

class ProductionConfig(Config):
    DEBUG = False
