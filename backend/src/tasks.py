from datetime import datetime
from typing import Dict

from celery import Celery
from celery.schedules import crontab

from src.config.settings import REDIS_SERVER_URI
from src.services.boleto_service import BoletoService

celery = Celery("tasks", broker=REDIS_SERVER_URI, backend=REDIS_SERVER_URI)
celery.autodiscover_tasks()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Everyday 3 a.m.
    sender.add_periodic_task(crontab(hour=3, minute=0), process_boletos.s())


@celery.task
def process_boletos():
    boletos_tuple = BoletoService.get_boletos_to_send()

    for boleto_tuple in boletos_tuple[:10000]:
        boleto_dict = dict(
            zip(
                [
                    "id",
                    "name",
                    "government_id",
                    "email",
                    "debt_amount",
                    "debt_due_date",
                ],
                boleto_tuple,
            )
        )
        boleto_dict["debt_due_date"] = boleto_dict["debt_due_date"].isoformat()
        generate_boleto_and_send_mail.apply_async([boleto_dict])


@celery.task(rate_limit="100000/s")
def generate_boleto_and_send_mail(boleto: Dict[str, int | str]):
    boleto_attachment = BoletoService.generate_boleto_attachment(boleto)

    send_mail.apply_async([boleto, boleto_attachment])


@celery.task
def send_mail(boleto: Dict[str, int | str], boleto_attachment: bytes):
    def update_boleto_processed():
        from src.config.db import Session
        from src.models.boleto import Boleto

        session = Session()

        boleto_obj = session.get_one(Boleto, boleto["id"])

        boleto_obj.processed_at = datetime.now()

        session.add(boleto_obj)
        session.commit()

        session.close()

    BoletoService.send_boleto_email(boleto, boleto_attachment, update_boleto_processed)
