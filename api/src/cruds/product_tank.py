from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.product_tank import ProductTank
from src.cruds.device_pins import DevicePinRepository
from src.domain.exceptions import InvalidData


class ProductTankRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(ProductTank, db_session)
        self.device_pin_repo = DevicePinRepository(db_session)

    def _validate_pins(self, screw_pin_id, scale_pin_id):
        """Valida existência, disponibilidade e unicidade dos pinos."""
        if screw_pin_id and scale_pin_id and screw_pin_id == scale_pin_id:
            raise InvalidData("O pino da rosca e o pino da balança não podem ser iguais.")
        if screw_pin_id:
            self.device_pin_repo._is_valid_pin(screw_pin_id)
        if scale_pin_id:
            self.device_pin_repo._is_valid_pin(scale_pin_id)

    def save(self, values, actor=None):
        self._validate_pins(
            values.get("screw_pin_id"),
            values.get("scale_pin_id"),
        )
        return super().save(values, actor)

    def update(self, id, values, actor=None):
        current = self.get(id)

        screw_pin_id = values.get("screw_pin_id")
        scale_pin_id = values.get("scale_pin_id")

        # Se dosador_seco for desativado, o pino da balança deve ser removido
        dosador_seco_desativado = (
            "is_dosador_seco" in values
            and not values["is_dosador_seco"]
            and current.is_dosador_seco
        )
        if dosador_seco_desativado:
            values["scale_pin_id"] = None
            scale_pin_id = None

        screw_changed = "screw_pin_id" in values and screw_pin_id != current.screw_pin_id
        scale_changed = "scale_pin_id" in values and scale_pin_id != current.scale_pin_id

        # Valor efetivo de cada pino após o update (novo se alterado, atual caso contrário)
        effective_screw = screw_pin_id if screw_changed else current.screw_pin_id
        effective_scale = scale_pin_id if scale_changed else current.scale_pin_id

        # Valida duplicidade sempre — independente de qual pino mudou
        if effective_screw and effective_scale and effective_screw == effective_scale:
            raise InvalidData("O pino da rosca e o pino da balança não podem ser iguais.")

        # Valida disponibilidade apenas para os pinos que foram alterados
        if screw_changed and screw_pin_id:
            self.device_pin_repo._is_valid_pin(screw_pin_id)
        if scale_changed and scale_pin_id:
            self.device_pin_repo._is_valid_pin(scale_pin_id)

        return super().update(id, values, actor)
