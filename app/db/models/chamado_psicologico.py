from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ChamadoPsicologico(Base):
    __tablename__ = "chamado_psicologico"

    __table_args__ = (
        CheckConstraint(
            "status_envio IN ('pendente', 'enviado', 'erro')",
            name="status_envio_valid",
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
    mensagem_opcional: Mapped[str | None] = mapped_column(Text, nullable=True)
    status_envio: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="pendente",
    )

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
