from sqlalchemy.orm import Session, make_transient
from src.domain import Shed, Sala, Baia, Valve
from src.cruds.repo import Repository


class ShedRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Shed, session)

    def clone_shed(self, shed_id: int, actor=None):
        shed = self.get(shed_id)

        if not shed:
            raise Exception("Shed not found")

        # cria o novo shed
        new_shed = Shed(
            name=f"{shed.name} (Clone)",
            created_by=actor.name if actor else shed.created_by,
            updated_by=actor.name if actor else shed.updated_by,
            kitchen_id=shed.kitchen_id,
        )

        self.db_session.add(new_shed)
        self.db_session.flush()

        for sala in shed.salas or []:
            new_sala = Sala(
                name=sala.name,
                shed_id=new_shed.id,
                entrance_pin_id=None,  # evita conflito físico
                created_by=actor.name if actor else sala.created_by,
                updated_by=actor.name if actor else sala.updated_by,
            )
            self.db_session.add(new_sala)
            self.db_session.flush()

            for baia in sala.baias or []:
                new_baia = Baia(
                    name=baia.name,
                    sala_id=new_sala.id,
                    animals_quantity=baia.animals_quantity,
                    t1=baia.t1,
                    t2=baia.t2,
                    t3=baia.t3,
                    t4=baia.t4,
                    t5=baia.t5,
                    t6=baia.t6,
                    created_by=actor.name if actor else baia.created_by,
                    updated_by=actor.name if actor else baia.updated_by,
                )
                self.db_session.add(new_baia)
                self.db_session.flush()

                '''
                for valve in baia.valvulas or []:
                    new_valve = Valve(
                        name=valve.name,
                        baia_id=new_baia.id,
                        device_pin_id=None,  # ⚠️ importante: não clonar hardware
                        max_weight=valve.max_weight,
                        created_by=actor.name if actor else valve.created_by,
                        updated_by=actor.name if actor else valve.updated_by,
                    )
                    self.db_session.add(new_valve)
                '''

        return new_shed