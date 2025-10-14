from sqlalchemy.orm import Session
from src.domain import exceptions as exc
from src.domain import (ShedRoom, StallFeeder, RoomStall, Shed)

class DashboardRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_data_from_svg(self):
        data = []

        sheds = self.session.query(Shed).all()

        for shed in sheds:
            shed_data = {
                "id": shed.id,
                "name": shed.name,
                "rooms": []
            }

            rooms = (
                self.session.query(ShedRoom)
                .filter(ShedRoom.shed_id == shed.id)
                .all()
            )

            for room in rooms:
                room_data = {
                    "id": room.id,
                    "name": room.name,
                    "entrance_pin_name": room.entrance_pin.name,
                    "entrance_pin_active": room.entrance_pin.is_active,
                    "stalls": []
                }

                stalls = (
                    self.session.query(RoomStall)
                    .filter(RoomStall.shed_room_id == room.id)
                    .all()
                )

                for stall in stalls:
                    stall_data = {
                        "id": stall.id,
                        "name": stall.name,
                        "feeders": []
                    }

                    feeders = (
                        self.session.query(StallFeeder)
                        .filter(StallFeeder.room_stall_id == stall.id)
                        .all()
                    )

                    stall_data["feeders"] = [
                        {"id": f.id, "name": f.name}
                        for f in feeders
                    ]

                    room_data["stalls"].append(stall_data)

                shed_data["rooms"].append(room_data)

            data.append(shed_data)

        return data
