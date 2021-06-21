class Configuration():
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@localhost:3307/application"
    REDIS_HOST = "localhost"
    REDIS_VOTES_KEY = "votes"
    REDIS_SUBSCRIBE_CHANNEL = "hasVotes"
