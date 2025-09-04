from typing import Optional, List, Dict
from sqlmodel import Field, Relationship
from sqlalchemy import JSON
from src.domain.base import Base

class Instalation(Base, table=True):
    __tablename__ = "instalations"

    ip_address: str = Field(nullable=False, max_length=45)
    name: str = Field(nullable=False, max_length=255)
    last_seen: Optional[str] = Field(default=None)
    is_online: bool = Field(default=False, nullable=False)
    device_id: int = Field(foreign_key="devices.id", nullable=False)


    device: Optional["Device"] = Relationship(back_populates="instalations")
    pins: List["DevicePin"] = Relationship(
        back_populates="device",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
