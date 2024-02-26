from pytest import fixture
from src.config.db import engine
from src.models import Base

from sqlalchemy import text
from sqlalchemy.orm import scoped_session, sessionmaker


def _clear_db():
   with engine.connect() as conn:
      trans = conn.begin()

      tables = ','.join(table.name for table in reversed(Base.metadata.sorted_tables))
      conn.execute(text(f"TRUNCATE {tables} RESTART IDENTITY;"))
      trans.commit()


@fixture
def session():
    _clear_db()
    session = scoped_session(sessionmaker(bind=engine))
    yield session
    session.close()
    _clear_db()
