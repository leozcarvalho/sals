from sqlalchemy.orm import Session
from src.domain import Moviment, MovimentKind, RoomStall
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
                    stall = self.db_session.get(RoomStall, moviment.stall_origin_id)
                    stall.animals_quantity += moviment.quantity
                case "SAIDA":
                    stall = self.db_session.get(RoomStall, moviment.stall_origin_id)
                    if stall.animals_quantity - moviment.quantity < 0:
                        raise exc.InvalidData("Não é possível movimentar para um valor negativo.")
                    stall.animals_quantity -= moviment.quantity
                case "TRANSFERENCIA":
                    stall_origin = self.db_session.get(RoomStall, moviment.stall_origin_id)
                    stall_destination = self.db_session.get(RoomStall, moviment.stall_destination_id)
                    if stall_origin.animals_quantity - moviment.quantity < 0:
                        raise exc.InvalidData("Não é possível movimentar para um valor negativo.")
                    stall_origin.animals_quantity -= moviment.quantity
                    stall_destination.animals_quantity += moviment.quantity
