from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from src.config.settings import (
    POSTGRESQL_DB,
    POSTGRESQL_HOST,
    POSTGRESQL_PASS,
    POSTGRESQL_PORT,
    POSTGRESQL_USER,
)

url = URL.create(
    drivername="postgresql",
    username=POSTGRESQL_USER,
    password=POSTGRESQL_PASS,
    port=POSTGRESQL_PORT,
    host=POSTGRESQL_HOST,
    database=POSTGRESQL_DB,
)

engine = create_engine(url)

Session = sessionmaker(bind=engine)
