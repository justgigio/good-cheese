from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from src.config.settings import POSTGRESQL_DB, POSTGRESQL_HOST, POSTGRESQL_PORT, POSTGRESQL_USER, POSTGRESQL_PASS

url = URL.create(
    drivername="postgresql",
    username=POSTGRESQL_USER,
    password=POSTGRESQL_PASS,
    port=POSTGRESQL_PORT,
    host=POSTGRESQL_HOST
)

engine = create_engine(url)

conn = engine.connect()

conn.execute(text("commit"))
conn.execute(text(f"CREATE DATABASE {POSTGRESQL_DB}"))
conn.close()
