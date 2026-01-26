from sqlalchemy.orm import Session
from src.domain.trato import Trato
from src.cruds.repo import Repository
from src.schemas.trato import TratoUpdateWithId, TratoCreate
from src.cruds.baia import BaiaRepository


class TratoRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Trato, session)

    def validate_percent(self, tratos: list[Trato]):
        '''Pegar todos os tratos e garantir que a soma dos percentuais seja 100'''
        total_percent = sum(trato.percent for trato in tratos)
        if total_percent != 100:
            raise ValueError(f"A soma dos percentuais deve ser 100, mas é {total_percent}")

    def delete(self, id, actor=None):
        pass  # Deleção de tratos não é permitida

    def refresh_baia_tratos(self):
        #atualizar todas as baias com o valor do tratos
        baia_repo = BaiaRepository(self.db_session)
        baias = baia_repo.get_list()
        tratos = self.get_list()
        for baia in baias:
            baia.t1 = tratos[0].percent
            baia.t2 = tratos[1].percent
            baia.t3 = tratos[2].percent
            baia.t4 = tratos[3].percent
            baia.t5 = tratos[4].percent
            baia.t6 = tratos[5].percent
            baia_repo.update(baia.id, baia.model_dump())
        return baias

    def bulk_save(self, trato_data: list[TratoCreate], actor=None):
        self.validate_percent(trato_data)
        for trato in trato_data:
            self.save(trato.model_dump(), actor=actor)
        self.refresh_baia_tratos()
        return trato_data

    def bulk_update(self, trato_updates: list[TratoUpdateWithId], actor=None):
        updated_tratos = []
        self.validate_percent(trato_updates)
        for trato_data in trato_updates:
            trato = self.update(trato_data.id, trato_data.model_dump(), actor=actor)
            updated_tratos.append(trato)
        self.refresh_baia_tratos()
        return updated_tratos