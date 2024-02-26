from decouple import config

ENVIRONMENT = config("ENVIRONMENT", default="dev")

REDIS_SERVER_HOST = config("REDIS_SERVER_HOST", default="redis")
REDIS_SERVER_PORT = config("REDIS_SERVER_PORT", default=6379)
REDIS_SERVER_URI = config(
    "REDIS_SERVER_URI", default=f"redis://{REDIS_SERVER_HOST}:{REDIS_SERVER_PORT}/0"
)

POSTGRESQL_HOST = config("POSTGRESQL_HOST", default="db")
POSTGRESQL_PORT = config("POSTGRESQL_PORT", default=5432)
POSTGRESQL_USER = config("POSTGRESQL_USER", default="postgres")
POSTGRESQL_PASS = config("POSTGRESQL_PASS", default="postgres")

if ENVIRONMENT == "dev":
    POSTGRESQL_DB = config("POSTGRESQL_DB", default="good_cheese_development")
elif ENVIRONMENT == "test":
    POSTGRESQL_DB = config("POSTGRESQL_DB_TEST", default="good_cheese_test")
else:
    raise Exception("Invalid ENVIRONMENT value. Valid options: ['dev', 'test']")
