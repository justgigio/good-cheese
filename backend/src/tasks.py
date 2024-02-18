from src.config.settings import REDIS_SERVER_URI

from celery import Celery

celery = Celery('tasks', broker=REDIS_SERVER_URI, backend=REDIS_SERVER_URI)
celery.autodiscover_tasks()

@celery.task
def process_boletos(id: int):
  return True
