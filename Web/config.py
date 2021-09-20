class Config(object):
    DEBUG = False
    TESTING = False

    # Twitter API Auth
    CONSUMER_KEY = "8THhE0IirLhdxgCUlax3zFzVr"
    CONSUMER_SECRET = "UKyOJQAs8rzua87jj0BDMmfCwvK5LE9kThShTREUXgsffOiO8l"

    ### DB AUTHENTICATION ###

    # MongoDB Auth Information
    # Please Specify mongodb connection url
    MONGODB_URL = "mongodb://admin:Bigdata123%23@194.233.64.254:27017" # Standart mongodb url without refering to db
    # Specify MongoDB Database
    MONGODB_DB = "buzzer"

class ProductionConfig(Config):
    PRODTEST = True

class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_URL = "mongodb://buzzer:12345@localhost:27017"

class TestingConfig(Config):
    TESTING = True
 