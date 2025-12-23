from sqlalchemy.orm import Session, joinedload
from src.domain.svg import SVG
from src.cruds.repo import Repository
from sqlalchemy import select, case
from src.domain import Kitchen, Shed, DevicePin, Installation, Sala, Baia, Comedouro, FeederValve
from src.schemas.svg import SVGRead
from src.domain import exceptions as exc

class SvgRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(SVG, session)
    
    def replace_variables(self, content: str, variables: list):
        for var in variables:
            content = content.replace(var["key"], var["value"])
        return content
    
    def get_owner_svg_id(self, owner_type: str, owner_id: int):
        svg = self.db_session.query(SVG).filter(SVG.owner_type == owner_type, SVG.owner_id == owner_id).first()
        if not svg:
            return None
        return svg.id

    def svg_with_variables(self, svg_id: int, replace_variables: bool = False):
        svg = self.check_exists(svg_id)
        variables = self.get_variables(svg_id)

        # Necessário para não alterar o conteúdo original do SVG no banco
        content = svg.content
        if replace_variables:
            content = self.replace_variables(svg.content, variables)

        return SVGRead(
            id=svg.id,
            name=svg.name,
            owner_type=svg.owner_type,
            owner_id=svg.owner_id,
            content=content,
            created_at=svg.created_at,
            updated_at=svg.updated_at,
            created_by=svg.created_by,
            updated_by=svg.updated_by,
        )

    @staticmethod
    def map_pin_option(pin, label_prefix=""):
        return {
            "label": pin.name or pin.arbitrary_name,
            "value": getattr(pin, "id", getattr(pin, "pin_id", None)),
            "is_active": pin.is_active,
        }

    @staticmethod
    def map_variable(label, key, value):
        return {"label": label, "key": key, "value": value}


    def get_list(self, skip = 0, limit = None, filters = None, order_by = ..., actor=None):
        query = (
            select(
                SVG.id,
                SVG.name,
                SVG.owner_type,
                SVG.owner_id,
                SVG.content,
                SVG.created_at,
                SVG.updated_at,
                SVG.created_by,
                SVG.updated_by,
                case(
                    (
                        SVG.owner_type == "sheds",
                        select(Shed.name).where(Shed.id == SVG.owner_id).scalar_subquery(),
                    ),
                    (
                        SVG.owner_type == "kitchens",
                        select(Kitchen.name).where(Kitchen.id == SVG.owner_id).scalar_subquery(),
                    ),
                    (
                        SVG.owner_type == "installations",
                        select(Installation.name).where(Installation.id == SVG.owner_id).scalar_subquery(),
                    ),
                    else_=None,
                ).label("owner_name"),
            )
            .select_from(SVG)
        )
        result_query = self.db_session.exec(query).all()
        result = []
        for row in result_query:
            result.append({
                "id": row.id,
                "name": row.name,
                "owner_type": row.owner_type,
                "owner_id": row.owner_id,
                "content": row.content,
                "created_by": row.created_by,
                "updated_by": row.updated_by,
                "created_at": row.created_at,
                "updated_at": row.updated_at,
                "owner_name": row.owner_name,
            })
        return result

    def get_options(self, svg_id: int):
        svg = self.check_exists(svg_id)
        options = []
        if svg.owner_type == "kitchens":
            owner = self.db_session.get(Kitchen, svg.owner_id)
            options.extend([
                self.map_pin_option(owner.shaker_pin, f'Misturador - '),
                self.map_pin_option(owner.pump_pin, f'Bomba - '),
                self.map_pin_option(owner.scale_pin, f'Balança - '),
            ])
            for tank in owner.tanks:
                options.append(self.map_pin_option(tank.tank.device_pin, f'Tanque {tank.tank.product.name} - {tank.tank.device_pin.name}'))
            return options

        if svg.owner_type == "sheds":
            shed = self.db_session.get(Shed, svg.owner_id)
            comedouros = self.db_session.query(FeederValve).join(Comedouro).join(Baia).join(Sala).filter(Sala.shed_id == shed.id).all()
            for comedouro in comedouros:
                options.append(self.map_pin_option(comedouro.device_pin, "Válvula de Alimentação - "))
            salas = self.db_session.query(Sala).filter(Sala.shed_id == shed.id).all()
            for sala in salas:
                options.append(self.map_pin_option(sala.entrance_pin, f'Bit de Entrada ({sala.name}) - '))
            return options

        if svg.owner_type == "installations":
            pins = self.db_session.query(DevicePin).filter(DevicePin.installation_id == svg.owner_id).all()
            return [self.map_pin_option(pin, "Bit ") for pin in pins]
        return options


    def get_variables(self, svg_id: int):
        svg = self.check_exists(svg_id)
        variables = []

        if svg.owner_type == "kitchens":
            owner = self.db_session.get(Kitchen, svg.owner_id)
            if not owner:
                return []
            for tank in owner.tanks:
                variables.extend([
                    self.map_variable(f"Nome do Tanque ({tank.tank.name})", f"TN{tank.id}", tank.tank.name),
                    self.map_variable(f"Nome do Produto ({tank.tank.name} - {tank.tank.product.name})", f"PN{tank.id}", tank.tank.product.name),
                ])

        if svg.owner_type == "sheds":
            shed = self.db_session.query(Shed).options(joinedload(Shed.salas)).filter(Shed.id == svg.owner_id).first()
            if not shed:
                return []

            comedouros = self.db_session.query(Comedouro).join(Baia).join(Sala).filter(Sala.shed_id == shed.id).all()
            for comedouro in comedouros:
                variables.append(self.map_variable(f"Nome do Comedouro ({comedouro.name})", f"R{comedouro.id}", comedouro.name))

            for sala in shed.salas:
                variables.append(self.map_variable(f"Nome da Sala ({sala.name})", f"S{sala.id}", sala.name))

            baias = self.db_session.query(Baia).join(Sala).filter(Sala.shed_id == shed.id).all()
            for baia in baias:
                variables.append(self.map_variable(f"Nome da Baia ({baia.name})", f"B{baia.id}", baia.name))

        if svg.owner_type == "installations":
            installation = self.db_session.get(Installation, svg.owner_id)
            if not installation:
                return []
            variables.append(self.map_variable("Endereço IP", "IP", installation.ip_address))
            if installation.hardware_kind == "input":
                variables.append(self.map_variable("Valor lido", "VAL", installation.last_value))
        
        return variables
