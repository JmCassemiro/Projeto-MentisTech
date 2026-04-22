from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.empresa import Empresa
from app.repositories.base_repository import BaseRepository


class EmpresaRepository(BaseRepository[Empresa]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Empresa)

    def create(self, *, nome_fantasia: str, cnpj: str) -> Empresa:
        empresa = Empresa(nome_fantasia=nome_fantasia, cnpj=cnpj)
        return self.add(empresa)

    def get_by_cnpj(self, cnpj: str) -> Empresa | None:
        stmt = select(Empresa).where(Empresa.cnpj == cnpj)
        return self.db.scalar(stmt)

    def update_empresa(
        self,
        empresa: Empresa,
        *,
        nome_fantasia: str | None = None,
        cnpj: str | None = None,
    ) -> Empresa:
        return self.update(empresa, nome_fantasia=nome_fantasia, cnpj=cnpj)
