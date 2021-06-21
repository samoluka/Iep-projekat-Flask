from datetime import timedelta;

# import os;
#
# path = os.environ["DATABASE_URL"]

class Configuration ( ):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@localhost:3307/application"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta ( minutes = 60 );
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta ( days = 30 );