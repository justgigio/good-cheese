from decouple import config

REDIS_SERVER_HOST = config('REDIS_SERVER_HOST', default='redis')
REDIS_SERVER_PORT = config('REDIS_SERVER_PORT', default=6379)
REDIS_SERVER_URI = config('REDIS_SERVER_URI', default = f"redis://{REDIS_SERVER_HOST}:{REDIS_SERVER_PORT}/0")
