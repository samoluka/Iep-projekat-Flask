import os;

# pathRedis = os.environ["REDIS_URL"]
pathRedis = "localhost"
# pathDB = os.environ["DATABASE_URL"]
pathDB = "localhost:3307"

class Configuration():
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{pathDB}/application"
    REDIS_HOST = pathRedis
    REDIS_VOTES_KEY = "votes"
    REDIS_SUBSCRIBE_CHANNEL = "hasVotes"
