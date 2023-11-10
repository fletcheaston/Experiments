import uuid

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __table_args__ = {"schema": "experiments/full-text-search"}

    @classmethod
    def __model_name__(cls) -> str:
        return cls.__name__


class Document(Base):
    __tablename__ = "dictionary"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    word = Column(Text, unique=True)
    definitions = Column(Text)


__all__ = [
    "Base",
    "Document",
]
