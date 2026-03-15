from sqlalchemy.orm import Session
from src.domain import Moviment, MovimentKind, Baia
from src.cruds.repo import Repository
from src.domain import exceptions as exc

class MovimentRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Moviment, session)

    def save(self, values, actor=None):
        moviment = super().save(values, actor)
        self.exec_moviment(moviment.id, actor)
        return moviment
    
    def update(self, id, values, actor=None):
        moviment = super().update(id, values, actor)
        self.exec_moviment(moviment.id, actor)
        return moviment
    
    def exec_moviment(self, id: int, actor=None):
        moviment = self.get(id)
        if moviment:
            moviment_kind = self.db_session.get(MovimentKind, moviment.moviment_kind_id)
            match moviment_kind.kind:
                case "ENTRADA":
                    baia = self.db_session.get(Baia, moviment.baia_origin_id)
                    baia.animals_quantity += moviment.quantity
                case "SAIDA":
                    baia = self.db_session.get(Baia, moviment.baia_origin_id)
                    if baia.animals_quantity - moviment.quantity < 0:
                        raise exc.InvalidData("Não é possível movimentar para um valor negativo.")
                    baia.animals_quantity -= moviment.quantity
                case "TRANSFERENCIA":
                    baia_origem = self.db_session.get(Baia, moviment.baia_origin_id)
                    baia_destino = self.db_session.get(Baia, moviment.baia_destination_id)
                    if baia_origem.animals_quantity - moviment.quantity < 0:
                        raise exc.InvalidData("Não é possível movimentar para um valor negativo.")
                    baia_origem.animals_quantity -= moviment.quantity
                    baia_destino.animals_quantity += moviment.quantity
