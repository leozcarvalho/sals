import os
from pathlib import Path
from sqlmodel import SQLModel
from sqlalchemy import create_engine
from src import domain
from src.domain.permissions import PermissionEnum

from src.cruds.profile import ProfileRepository
from src.cruds.users import UsersRepository
from src.cruds.hardware_kind import HardwareKindRepository
from src.cruds.instalations import InstalationRepository
from src.cruds.hardware_connection_template import HardwareConnectionTemplateRepository
from src.cruds.hardware_point_types import HardwarePointTypeRepository
from src.cruds.hardware_device import HardwareDeviceRepository
from src.cruds.kitchen import KitchenRepository

from tests.fixtures.user_fixture import USER
from tests.fixtures.hardware_kind_fixture import HARDWARE_KIND
from tests.fixtures.hardware_point_types_fixture import HARDWARE_POINT_TYPE
from tests.fixtures.hardware_connection_template_fixture import HARDWARE_CONNECTION_TEMPLATE

from alembic import command
from alembic.config import Config
from src.core.config import settings

db_path = Path("data/db.sqlite")
db_path.parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def reset_database():
    """
    Dropa e Cria todas as tabelas definidas nos modelos SQLModel.
    """
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    print("[DB] Tabelas criadas")


def stamp_alembic_head():
    """
    Define o Alembic para a versão 'head', garantindo que a migration esteja em sincronia.
    """
    alembic_ini_path = Path(__file__).parent.parent.parent / "alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
    command.stamp(alembic_cfg, "head")
    print("[DB] Alembic stamp na versão head")

def create_profiles(db):
    repo = ProfileRepository(db)
    profiles_data = [
        {
            "name": "Administrador",
            "permissions": [p.value for p in PermissionEnum],
        },
        {
            "name": "Engenharia",
            "permissions": [
                "MANAGE_HARDWARE_KIND",
                "MANAGE_HARDWARE_DEVICE",
                "MANAGE_HARDWARE_POINT_TYPE",
                "MANAGE_HARDWARE_CONNECTION_TEMPLATE",
                "MANAGE_DEVICE_PIN",
                "MANAGE_INSTALATION",
            ],
        },
    ]

    for pdata in profiles_data:
        repo.save(pdata)
        
    print("[SEED] Perfis criados/atualizados com sucesso")

def create_user(db):
    repo = UsersRepository(db)
    user_data = USER.model_dump()
    user = repo.save(user_data)
    print(f"[SEED] Usuário criado: {user.id}")
    return user

def create_hardware_kinds(db, user):
    repo = HardwareKindRepository(db)
    hw_kind = repo.save(HARDWARE_KIND.model_dump(), actor=user)
    balanca_kind_data = HARDWARE_KIND.model_dump().copy()
    balanca_kind_data["kind"] = "Balança"
    balanca_kind = repo.save(balanca_kind_data, actor=user)
    print(f"[SEED] Hardware Kinds criados: {hw_kind.id}, {balanca_kind.id}")
    return hw_kind, balanca_kind

def create_hardware_point_type(db, user):
    repo = HardwarePointTypeRepository(db)
    point_type = repo.save(HARDWARE_POINT_TYPE.model_dump(), actor=user)
    print(f"[SEED] Hardware Point Type criado: {point_type.id}")
    return point_type

def create_hardware_connection_template(db, user):
    repo = HardwareConnectionTemplateRepository(db)
    template = repo.save(HARDWARE_CONNECTION_TEMPLATE.model_dump(), actor=user)
    print(f"[SEED] Hardware Connection Template criado: {template.id}")
    return template

def create_hardware_devices(db, user, hw_kind, balanca_kind, point_type, template):
    repo = HardwareDeviceRepository(db)
    device = repo.save({
        "name": "Dispositivo de Teste",
        "hardware_kind_id": hw_kind.id,
        "point_type_id": point_type.id,
        "connection_template_id": template.id,
    }, actor=user)
    balanca = repo.save({
        "name": "Balança de Teste",
        "hardware_kind_id": balanca_kind.id,
        "point_type_id": point_type.id,
        "connection_template_id": template.id,
    }, actor=user)
    print(f"[SEED] Hardware Devices criados: {device.id}, {balanca.id}")
    return device, balanca

def create_instalations(db, user, devices):
    repo = InstalationRepository(db)
    ip_list = ["192.168.60.100", "177.122.01.100"]
    for device in devices:
        repo.save({
            "name": "Dispositivo teste",
            "device_id": device.id,
            "ip_address": ip_list[devices.index(device) % len(ip_list)]
        }, actor=user)
    print(f"[SEED] Instalations criados")

def create_kitchens(db, user):
    repo = KitchenRepository(db)
    kitchens_data = [
        {"name": "Cozinha Teste", "shaker_pin_id": 1, "pump_pin_id": 2, "scale_pin_id": 3, "product_pin_id": 4},
        {"name": "Cozinha Teste 2", "shaker_pin_id": 5, "pump_pin_id": 6, "scale_pin_id": 7, "product_pin_id": 8},
    ]
    for data in kitchens_data:
        repo.save(data, actor=user)
    print(f"[SEED] Cozinhas criadas")

# ---------- EXECUÇÃO DO SEED ----------
def seed():
    from sqlalchemy.orm import Session
    db = Session(bind=engine)
    try:
        profiles = create_profiles(db)
        user = create_user(db)

        hw_kind, balanca_kind = create_hardware_kinds(db, user)
        point_type = create_hardware_point_type(db, user)
        template = create_hardware_connection_template(db, user)
        devices = create_hardware_devices(db, user, hw_kind, balanca_kind, point_type, template)
        create_instalations(db, user, devices)
        create_kitchens(db, user)

        db.commit()
        print("[SEED] Seed executado com sucesso")
    except Exception as e:
        db.rollback()
        print(f"[SEED] Erro ao executar seed: {e}")
        raise
    finally:
        db.close()

# ---------- MAIN ----------
if __name__ == "__main__":
    reset_database()
    seed()
    stamp_alembic_head()
