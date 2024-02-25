from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from . import Boleto


class BoletoFile(Base):
    __tablename__ = "boleto_files"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    checksum: Mapped[str]
    size: Mapped[int]
    uploaded_at: Mapped[datetime]
    processed_at: Mapped[Optional[datetime]]

    boletos: Mapped[List["Boleto"]] = relationship(back_populates="boleto_file")

    def __repr__(self):
        return f"<File(name='{self.name}', size={self.size}, uploaded={self.uploaded_at}, checksum='{self.checksum}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "checksum": self.checksum,
            "size": self.size,
            "uploaded_at": self.uploaded_at,
            "processed_at": self.processed_at,
        }
