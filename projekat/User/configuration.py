import os;

path = os.environ["REDIS_URL"]
# path = "localhost"

class Configuration():
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3307/application"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    REDIS_HOST = path
    REDIS_VOTES_KEY = "votes"
    REDIS_SUBSCRIBE_CHANNEL = "hasVotes"
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta ( minutes = 60 );
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta ( days = 30 );
