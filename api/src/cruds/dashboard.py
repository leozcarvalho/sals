from sqlalchemy.orm import Session
from src.cruds.svg import SvgRepository
from src.domain import exceptions as exc
from src.domain import (Kitchen, Shed, SVG)

class DashboardRepository:
    def __init__(self, session: Session):
        self.session = session
        self.svg_repository = SvgRepository(session)

    def get_data_from_svg(self):
        data = []
        sheds = self.session.query(Shed).all()
        kitchens = self.session.query(Kitchen).all()
        for shed in sheds:
            shed_data = {
                "name": shed.name,
                "owner_type": "sheds",
                "svg_id": self.svg_repository.get_owner_svg_id("sheds", shed.id)
            }
            data.append(shed_data)
        for kitchen in kitchens:
            kitchen_data = {
                "name": kitchen.name,
                "owner_type": "kitchens",
                "svg_id": self.svg_repository.get_owner_svg_id("kitchens", kitchen.id)
            }
            data.append(kitchen_data)
        return data
