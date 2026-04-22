from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.usuario import Usuario
from app.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Usuario)

    def create(
        self,
        *,
        empresa_id: int,
        nome_completo: str,
        email_corporativo: str,
        cargo: str,
        senha_hash: str,
    ) -> Usuario:
        usuario = Usuario(
            empresa_id=empresa_id,
            nome_completo=nome_completo,
            email_corporativo=email_corporativo,
            cargo=cargo,
            senha_hash=senha_hash,
        )
        return self.add(usuario)

    def get_by_email(self, email: str) -> Usuario | None:
        stmt = select(Usuario).where(Usuario.email_corporativo == email)
        return self.db.scalar(stmt)

    def list_by_empresa(
        self,
        empresa_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Usuario]:
        stmt = (
            select(Usuario)
            .where(Usuario.empresa_id == empresa_id)
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def update_usuario(
        self,
        usuario: Usuario,
        *,
        nome_completo: str | None = None,
        cargo: str | None = None,
        senha_hash: str | None = None,
    ) -> Usuario:
        return self.update(
            usuario,
            nome_completo=nome_completo,
            cargo=cargo,
            senha_hash=senha_hash,
        )
