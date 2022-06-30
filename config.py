import os


class Config:
    # later work on external db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    basedir = os.path.abspath(os.path.dirname(__file__))


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    ACCOUNT = os.environ.get("ACCOUNT_ADDRESS_PROD")
    ACCOUNT_KEY = os.environ.get("PRIVATE_KEY_PROD")
    ETHEREUM_ENDPOINT_URI = os.environ.get("ETHEREUM_ENDPOINT_URI_PROD")
    SMART_CONTRACT_ADDRESS = os.environ.get("ETHEREUM_CONTRACT_ADDRESS")
    CHAIN_ID = 4

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True
    ACCOUNT = os.environ.get("ACCOUNT_ADDRESS_DEV")
    ACCOUNT_KEY = os.environ.get("PRIVATE_KEY_DEV")
    ETHEREUM_ENDPOINT_URI = os.environ.get("ETHEREUM_ENDPOINT_URI_DEVELOPMENT")
    SMART_CONTRACT_ADDRESS = os.environ.get("ETHEREUM_CONTRACT_ADDRESS")
    CHAIN_ID = 1337
