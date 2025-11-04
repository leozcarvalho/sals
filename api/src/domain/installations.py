from typing import Optional, List
from sqlmodel import Field, Relationship
from src.domain.base import Base
from pydantic import computed_field

class Installation(Base, table=True):
    __tablename__ = "installations"

    ip_address: str = Field(nullable=False, max_length=45)
    name: str = Field(nullable=False, max_length=255)
    last_seen: Optional[str] = Field(default=None)
    is_online: bool = Field(default=False, nullable=False)
    last_value: Optional[str] = Field(default="0")
    device_id: int = Field(foreign_key="devices.id", nullable=False)
    healthcheck_priority_id: int = Field(foreign_key="healthcheck_priorities.id", nullable=True)

    device: Optional["Device"] = Relationship(back_populates="installations")
    pins: List["DevicePin"] = Relationship(
        back_populates="installation",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    healthcheck_priority: Optional["HealthcheckPriority"] = Relationship(back_populates="installations")

    @computed_field
    @property
    def binary_value(self) -> str:
        if not self.pins:
            return "0"
        return "".join(
            "1" if pin.is_active else "0"
            for pin in sorted(self.pins, key=lambda p: p.number)
        )[::-1]

    @computed_field
    @property
    def decimal_value(self) -> int:
        return int(self.binary_value, 2)
    
    @property
    def hardware_kind(self) -> "HardwareKind":
        return self.device.hardware_kind.kind
