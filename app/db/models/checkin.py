from datetime import datetime
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CheckIn(Base):
    __tablename__ = "check_in"

    __table_args__ = (
        CheckConstraint(
            "nivel_estresse >= 0 AND nivel_estresse <= 100", name="nivel_estresse_range"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuario.id"),
        nullable=False,
        index=True,
    )
    data_hora: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    humor_geral: Mapped[str] = mapped_column(String(50), nullable=False)
    respostas_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    nivel_estresse: Mapped[int] = mapped_column(Integer, nullable=False)
    insights_ia: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    usuario = relationship("Usuario")
