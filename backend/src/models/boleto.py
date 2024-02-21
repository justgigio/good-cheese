from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey

from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
  from . import BoletoFile


class Boleto(Base):
  __tablename__ = 'boletos'
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  government_id: Mapped[str]
  email: Mapped[str]
  debt_amount: Mapped[int]
  debt_due_date: Mapped[datetime]
  debt_id: Mapped[str]
  processed_at: Mapped[Optional[datetime]]

  boleto_file_id: Mapped[int] = mapped_column(ForeignKey('boleto_files.id'))

  boleto_file: Mapped["BoletoFile"] = relationship(back_populates="boletos")

  def __repr__(self):
    return f"<Boleto(name='{self.name}', email='{self.email}', debt_amount={self.debt_amount}, debt_due_date='{self.debt_due_date}')>"

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "government_id": self.government_id,
      "email": self.email,
      "debt_amount": self.debt_amount,
      "debt_due_date": self.debt_due_date.isoformat(),
      "debt_id": self.debt_id,
      "processed_at": self.processed_at and self.processed_at.isoformat()
    }