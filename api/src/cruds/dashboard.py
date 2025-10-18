from sqlalchemy.orm import Session
from src.domain import exceptions as exc
from src.domain import (Kitchen, Shed)

class DashboardRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_data_from_svg(self):
        data = []

        sheds = self.session.query(Shed.name).all()
        kitchens = self.session.query(Kitchen.name).all()
        for shed in sheds:
            shed_data = {
                "name": shed.name,
                "svg": None
            }
            data.append(shed_data)
        for kitchen in kitchens:
            kitchen_data = {
                "name": kitchen.name,
                "svg": None
            }
            data.append(kitchen_data)
        return data
