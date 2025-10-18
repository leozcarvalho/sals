from sqlalchemy.orm import Session
from src.domain.svg import SVG
from src.cruds.repo import Repository
from sqlalchemy import select, case
from src.domain import Kitchen, Shed, Device

class SvgRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(SVG, session)

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
                        SVG.owner_type == "hardware-devices",
                        select(Device.name).where(Device.id == SVG.owner_id).scalar_subquery(),
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
            print(row.owner_name)
        return result
