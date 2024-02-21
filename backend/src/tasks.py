from datetime import datetime
from typing import Dict
from src.models.boleto import Boleto
from src.services.boleto_service import BoletoService
from src.config.settings import REDIS_SERVER_URI

from celery import Celery
from celery.schedules import crontab

celery = Celery('tasks', broker=REDIS_SERVER_URI, backend=REDIS_SERVER_URI)
celery.autodiscover_tasks()

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  # Everyday 3 a.m.
  sender.add_periodic_task(crontab(hour=3, minute=0), process_boletos.s())

@celery.task
def process_boletos():
  boletos = BoletoService.get_boletos_to_send()

  for boleto in boletos:
    send_boleto_mail.apply_async([boleto.to_dict()])


@celery.task
async def send_boleto_mail(boleto: Dict[str, int | str]):
  file = BoletoService.generate_boleto_attachment(boleto)
  ok = await BoletoService.send_boleto_email(boleto, file)

  if ok:
    from src.config.db import Session

    session = Session()

    boleto_obj = session.get_one(Boleto, boleto["id"])
    
    boleto_obj.processed_at = datetime.now()

    session.add(boleto_obj)
    session.commit()

    session.close()
