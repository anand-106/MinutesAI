import os
from arq.connections import RedisSettings
from app.tasks import join_meeting
import dotenv

dotenv.load_dotenv()


redis_dsn = os.getenv("REDIS_URL", "redis://minutesai-redis:6379")


REDIS_SETTINGS = RedisSettings.from_dsn(redis_dsn)

class WorkerSettings:
    functions= [join_meeting]

    redis_settings = REDIS_SETTINGS
    function_timeout = 10800

