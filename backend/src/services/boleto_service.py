import hashlib

from datetime import datetime, timedelta
from io import StringIO
from json import dumps
from time import sleep, time
from typing import Dict, List
from fastapi import HTTPException
from sqlalchemy import and_

from src.models import BoletoFile, Boleto
from src.config.db import Session, engine


class BoletoService:

  @staticmethod
  def create_boleto_file(filename: str, file_contents: bytes) -> BoletoFile:
    boleto_file = BoletoFile()
    boleto_file.name = filename
    boleto_file.uploaded_at = datetime.now()

    boleto_file.checksum = hashlib.md5(file_contents).hexdigest()

    boleto_file.size = file_contents.decode('utf-8').count("\n") - 1

    session = Session()

    session.add(boleto_file)
    session.commit()
    session.refresh(boleto_file)

    return boleto_file

  @staticmethod
  def upload_boleto(boleto_file: BoletoFile, file_contents: bytes):
    t0 = time()
    print("=" * 50)
    print("Starting...")

    columns = ('name', 'government_id', 'email', 'debt_amount', 'debt_due_date', 'debt_id', 'boleto_file_id')

    chunk_size = 50000

    file_lines = file_contents.decode('utf-8').splitlines()[1:]

    file_chunks = [file_lines[pos:pos + chunk_size] for pos in range(0, len(file_lines), chunk_size)]

    conn = engine.raw_connection()
    cursor = conn.cursor()
    
    for chunk in file_chunks:
      file_contents_str = f",{boleto_file.id}\n".join(chunk)
      
      buffer = StringIO(f"{file_contents_str},{boleto_file.id}")
      
      cursor.copy_from(buffer, 'boletos', sep=',', columns=columns)
      conn.commit()

    cursor.close()
    conn.close()

    t1 = time()
    print("=" * 50)
    print(f"Total {t1 - t0}s")

  @staticmethod
  def check_upload_boleto(boleto_file_id: int) -> Dict[str, bool | int | float]:
    session = Session()

    boleto_file = session.get(BoletoFile, boleto_file_id)

    if not boleto_file:
      raise HTTPException(status_code=404, detail="Item not found")

    boleto_count = session.query(Boleto).filter_by(boleto_file_id=boleto_file.id).count()
    completed = boleto_file.size == boleto_count
    percent = 100.0 * boleto_count / boleto_file.size

    session.close()

    return {
      "id": boleto_file.id,
      "size": boleto_file.size,
      "inserted": boleto_count,
      "completed": completed,
      "percent": percent
    }

  @staticmethod
  def list_boleto_files() -> List[Dict]:
    session = Session()
    
    boleto_files = session.query(BoletoFile).all()

    session.close()

    return [boleto_file.to_dict() for boleto_file in boleto_files]

  @staticmethod
  def get_boletos_to_send() -> List[Boleto]:
    session = Session()

    today = datetime.now()
    due_date_offset = today + timedelta(days=10)

    condition = and_(Boleto.processed_at == None, Boleto.debt_due_date < due_date_offset)
    boletos = session.query(Boleto).filter(condition).all()

    return boletos

  @staticmethod
  def generate_boleto_attachment(boleto: Dict[str, int | str]) -> bytes:
    # simulate API latency
    sleep(0.1)
    return dumps(boleto).encode('utf-8')

  @staticmethod
  async def send_boleto_email(boleto: Dict[str, int | str], boleto_attachment: bytes) -> bool:
    from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

    conf = ConnectionConfig(
      MAIL_USERNAME ="",
      MAIL_PASSWORD = "",
      MAIL_FROM = "no-reply@goodcheese.com",
      MAIL_PORT = 1025,
      MAIL_SERVER = "mailhog",
      MAIL_STARTTLS = False,
      MAIL_SSL_TLS = False,
      USE_CREDENTIALS = False,
      VALIDATE_CERTS = False
    )

    subject = f"[Good Cheese Boleto] Olá, {boleto['name']}, aqui está seu Boleto!"

    due_date = datetime.fromisoformat(str(boleto["debt_due_date"]))

    body = f"""
      <p> Olá, {boleto["name"]}! </p>
      <p> Aqui está seu boleto com vencimento no dia <b>{due_date.strftime("%d/%m/%Y")}</b>! </p>
      <p> No valor de <b> R$ {int(boleto["debt_amount"])/100:.2f} </b></p>
      <br />
      <br />
      <pre> {boleto_attachment.decode('utf-8')} </pre>
    """
    message = MessageSchema(
      subject=subject,
      recipients= [str(boleto["email"])],
      body=body,
      subtype=MessageType.html
    )

    try:
      fm = FastMail(conf)
      await fm.send_message(message)
    except:
      return False

    return True
