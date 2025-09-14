from sqlalchemy.orm import Session
from src.cruds.repo import Repository
from src.domain import Kitchen, FeederValve
from sqlalchemy import or_, exists, select, case
from src.domain import exceptions as exc
from src.domain import (DevicePin, ShedRoom, Installation, KitchenProduct)
from src.schemas.device_pins import DevicePin as DevicePinSchema

class DevicePinRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(DevicePin, session)

    def get_pins_binary_and_decimal(self, installation_id: int):
        """
        pins: lista de objetos DevicePin
        total_bits: número total de bits da placa (32)
        retorna: (decimal_value, binary_string)
        """
        pins = self.get_list(filters={"installation_id": installation_id})
        total_bits = len(pins)
        decimal_value = 0
        # inicializa string binária com zeros
        binary_list = ['0'] * total_bits

        for pin in pins:
            if pin.is_active:
                # a posição do bit no decimal é number-1
                bit_index = pin.number - 1
                decimal_value |= (1 << bit_index)
                # marca o bit na string
                binary_list[total_bits - 1 - bit_index] = '1'  # MSB à esquerda

        binary_string = ''.join(binary_list)
        return decimal_value, binary_string
    
    def activate_pin(self, id: int, actor=None):
        pin = self.check_exists(id, actor)
        return self.update(id, {"is_active": True}, actor)

    def deactivate_pin(self, id: int, actor=None):
        pin = self.check_exists(id, actor)
        return self.update(id, {"is_active": False}, actor)
    
    def toggle_pin(self, id: int, actor=None):
        pin = self.check_exists(id, actor)
        new_state = not pin.is_active
        return self.update(id, {"is_active": new_state}, actor)

    def deactivate_all_pins(self, installation_id: int, actor=None):
        pins = self.get_list(filters={"installation_id": installation_id})
        for pin in pins:
            self.update(pin.id, {"is_active": False}, actor)
        return True

    def _get_in_use_subqueries(self):
        kitchen_subq = select(Kitchen.id).where(
            or_(
                Kitchen.scale_pin_id == DevicePin.id,
                Kitchen.pump_pin_id == DevicePin.id,
                Kitchen.shaker_pin_id == DevicePin.id,
            )
        )
        feeder_subq = select(FeederValve.id).where(FeederValve.device_pin_id == DevicePin.id)

        room_subq = select(ShedRoom.id).where(ShedRoom.entrance_pin_id == DevicePin.id)

        kitchen_product_subq = select(KitchenProduct.id).where(KitchenProduct.device_pin_id == DevicePin.id)

        return kitchen_subq, feeder_subq, room_subq, kitchen_product_subq

    def build_filter(self, query, filters = {}):
        # Pega o filtro in_use
        in_use_filter = filters.pop("in_use", None) if filters else None

        kitchen_subq, feeder_subq, shed_subq, kitchen_product_subq = self._get_in_use_subqueries()
        if in_use_filter is not None:
            if in_use_filter:
                query = query.filter(exists(kitchen_subq) | exists(feeder_subq) | exists(shed_subq) | exists(kitchen_product_subq))
            else:
                query = query.filter(~(exists(kitchen_subq) | exists(feeder_subq) | exists(shed_subq) | exists(kitchen_product_subq)))

        # Chama o super para aplicar outros filtros
        return super().build_filter(query, filters)

    def build_query(self):
        query = self.db_session.query(DevicePin)
        kitchen_subq, feeder_subq, shed_subq, kitchen_product_subq = self._get_in_use_subqueries()
        query = self.db_session.query(
            DevicePin,
            case(
                (exists(kitchen_subq) | exists(feeder_subq) | exists(shed_subq) | exists(kitchen_product_subq), True),
                else_=False
            ).label("in_use"),
            Installation.name.label("installation_name"),
        )
        return query
    
    def format_results(self, results):
        output = []
        for dp, in_use, installation_name in results:
            output.append(DevicePinSchema(**dp.model_dump(), in_use=in_use, installation_name=installation_name))
        return output

    def get_pin_usage(self, pin_id: int):
        """
        Retorna uma string com a entidade e campo onde o pino está em uso.
        Retorna None se não estiver sendo usado.
        """

        # Room
        room = self.db_session.query(ShedRoom).filter(ShedRoom.entrance_pin_id == pin_id).first()
        if room:
            return f"entrada da sala {room.name}"

        # Kitchen
        kitchen = self.db_session.query(Kitchen).filter(Kitchen.shaker_pin_id == pin_id).first()
        if kitchen:
            return f"misturador da cozinha {kitchen.name}"

        kitchen = self.db_session.query(Kitchen).filter(Kitchen.pump_pin_id == pin_id).first()
        if kitchen:
            return f"bomba da cozinha {kitchen.name}"

        kitchen = self.db_session.query(Kitchen).filter(Kitchen.scale_pin_id == pin_id).first()
        if kitchen:
            return f"balança da cozinha {kitchen.name}"

        valve = self.db_session.query(FeederValve).filter(FeederValve.device_pin_id == pin_id).first()
        if valve:
            return f"válvula de alimentação {valve}"

        return None

    def _is_valid_pin(self, id: int) -> bool:
        """Valida se o pino está livre para uso."""
        device_pin = self.check_exists(id)
        usage = self.get_pin_usage(device_pin.id)
        if usage:
            raise exc.InvalidData(f"Pino {device_pin.name} está em uso em: {usage}")
        return True

    def get_grouped_not_used_device_pins(self):
        results = self.get_list()
        grouped = {}
        for pin in results:
            board = pin.installation_name if pin.installation_name else f"Instalação {pin.installation_id}"
            if board not in grouped:
                grouped[board] = []
            grouped[board].append({
                "id": pin.id,
                "name": pin.name,
                "number": pin.number,
                "is_active": pin.is_active,
                "in_use": pin.in_use
            })

        output = [{"board": board, "pins": pins} for board, pins in grouped.items()]
        return output
