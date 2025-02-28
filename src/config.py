import os



class Config:

    SECRET_KEY=os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):

    DEBUG=True
    MYSQL_HOST=os.getenv('MYSQL_HOST')
    MYSQL_DB=os.getenv('MYSQL_DB')
    MYSQL_USER=os.getenv('MYSQL_USER')
    MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD')

class ProductionConfig(Config):

    DEBUG=False
    MYSQL_HOST=os.getenv('MYSQL_HOST')
    MYSQL_DB=os.getenv('MYSQL_DB')
    MYSQL_USER=os.getenv('MYSQL_USER')
    MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD')

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}