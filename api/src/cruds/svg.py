from sqlalchemy.orm import Session
from src.domain.svg import SVG
from src.cruds.repo import Repository
from sqlalchemy import select, case
from src.domain import Kitchen, Shed, DevicePin, Installation, ShedRoom, RoomStall, StallFeeder, FeederValve
from src.schemas.svg import SVGCreate
from src.domain import exceptions as exc

class SvgRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(SVG, session)
    
    def replace_variables(self, content: str, variables: dict):
        for key, value in variables.items():
            content = content.replace(key, value)
        return content
    
    def get_owner_svg_id(self, owner_type: str, owner_id: int):
        svg = self.db_session.query(SVG).filter(SVG.owner_type == owner_type, SVG.owner_id == owner_id).first()
        if not svg:
            return None
        return svg.id

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
        options = {'variables': [], 'options': []}
        if svg.owner_type == "kitchens":
            owner = self.db_session.get(Kitchen, svg.owner_id)
            options['options'].extend([
                {
                    "label": f'Misturador - {owner.shaker_pin.name}',
                    "value": owner.shaker_pin_id,
                    "is_active": owner.shaker_pin.is_active
                },
                {
                    "label": f'Bomba - {owner.pump_pin.name}',
                    "value": owner.pump_pin_id,
                    "is_active": owner.pump_pin.is_active
                },
                {
                    "label": f'Balança - {owner.scale_pin.name}',
                    "value": owner.scale_pin_id,
                    "is_active": owner.scale_pin.is_active
                },
            ])
            for tank in owner.tanks:
                options['options'].append({
                    "label": f'Tanque {tank.tank.product.name} - {tank.tank.device_pin.name}',
                    "value": tank.tank.pin_id,
                    "is_active": tank.tank.device_pin.is_active
                })
            
                options['variables'].extend([
                    {
                        "label": f"Nome do Tanque ({tank.tank.name})",
                        "key": f"tn_{tank.id}",
                        "value": tank.tank.name
                    },
                    {
                        "label": f"Nome do Produto ({tank.tank.product.name})",
                        "key": f"pn_{tank.id}",
                        "value": tank.tank.product.name
                    },
                ])
            return options
        
        if svg.owner_type == "sheds":
            shed = self.db_session.get(Shed, svg.owner_id)
            feeders = self.db_session.query(FeederValve).join(StallFeeder).join(RoomStall).join(ShedRoom).filter(ShedRoom.shed_id == shed.id).all()
            for feeder in feeders:
                options['options'].append({
                    "label": f'Válvula de Alimentação - {feeder.device_pin.name}',
                    "value": feeder.device_pin_id,
                    "is_active": feeder.device_pin.is_active
                })
            return options
        
        if svg.owner_type == "installations":
            pins = self.db_session.query(DevicePin).filter(DevicePin.installation_id == svg.owner_id).all()
            for pin in pins:
                options["options"].append({
                    "label": f'Bit {pin.name}',
                    "value": pin.id,
                    "is_active": pin.is_active
                })
            return options
        return options
