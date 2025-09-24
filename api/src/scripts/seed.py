from pathlib import Path
import logging
from sqlmodel import SQLModel
from alembic import command
from alembic.config import Config

from src.core.db import session_scope, engine
from src.domain.permissions import PermissionEnum
from src.core.config import settings

# Fixtures
from tests.fixtures.hardware_kind_fixture import create_hardware_kind
from tests.fixtures.hardware_point_types_fixture import create_hardware_point_type
from tests.fixtures.hardware_connection_template_fixture import create_hardware_connection_template
from tests.fixtures.profile_fixture import create_profile
from tests.fixtures.hardware_device_fixture import create_hardware_device
from tests.fixtures.user_fixture import create_user
from tests.fixtures.kitchen_fixture import create_kitchen
from tests.fixtures.installation_fixture import create_installation
from tests.fixtures.shed_fixture import create_shed
from tests.fixtures.shed_room_fixture import create_shed_room
from tests.fixtures.room_stall_fixture import create_room_stall
from tests.fixtures.stall_feeder_fixture import create_stall_feeder
from tests.fixtures.feeder_valve_fixture import create_feeder_valve
from tests.fixtures.product_fixture import create_product
from tests.fixtures.product_tank_fixture import create_product_tank

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

global PINS_COUNT
PINS_COUNT = 0


def reset_database():
    """
    Dropa e recria todas as tabelas. Protegido para não rodar em produção.
    """
    if not settings.ENVIRONMENT == "development":
        raise RuntimeError("reset_database só pode ser usado em ambiente de desenvolvimento")

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    logger.info("[DB] Tabelas recriadas com sucesso")


def stamp_alembic_head():
    """
    Define Alembic para versão 'head' para sincronizar migrations.
    """
    alembic_ini_path = Path(__file__).parent.parent.parent / "alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    command.stamp(alembic_cfg, "head")
    logger.info("[DB] Alembic sincronizado com a versão head")



# ---------- DATA CREATION ----------
def create_profiles(db):
    create_profile(db)
    create_profile(
        db,
        name="Engenharia",
        permissions=[
            PermissionEnum.MANAGE_HARDWARE_KIND,
            PermissionEnum.MANAGE_HARDWARE_DEVICE,
            PermissionEnum.MANAGE_HARDWARE_POINT_TYPE,
            PermissionEnum.MANAGE_HARDWARE_CONNECTION_TEMPLATE,
            PermissionEnum.MANAGE_DEVICE_PIN,
            PermissionEnum.MANAGE_INSTALLATION,
        ],
    )
    create_profile(
        db,
        name="Supervisor",
        permissions=[
            PermissionEnum.MANAGE_HARDWARE_KIND,
            PermissionEnum.MANAGE_HARDWARE_DEVICE,
            PermissionEnum.MANAGE_HARDWARE_POINT_TYPE,
            PermissionEnum.MANAGE_HARDWARE_CONNECTION_TEMPLATE,
            PermissionEnum.MANAGE_DEVICE_PIN,
            PermissionEnum.MANAGE_INSTALLATION,
        ],
    )
    logger.info("[SEED] Perfis criados/atualizados com sucesso")


def create_users(db):
    admin = create_user(db, name="Usuário Admin", email="sals@admin.com")
    eng = create_user(db, name="Usuário Engenharia", email="sals@engenharia.com", profile_id=2)
    logger.info(f"[SEED] Usuários criados: {admin.id}, {eng.id}")
    return eng


def create_hardware_kinds(db, user):
    hw_kind = create_hardware_kind(db, user)
    balanca_kind = create_hardware_kind(db, user, kind="Entrada balança")
    logger.info(f"[SEED] Hardware Kinds criados: {hw_kind.id}, {balanca_kind.id}")
    return hw_kind, balanca_kind


def create_hardware_devices(db, user, hw_kind, balanca_kind, point_type, template):
    device = create_hardware_device(
        db,
        actor=user,
        hardware_kind_id=hw_kind.id,
        point_type_id=point_type.id,
        connection_template_id=template.id,
    )
    balanca = create_hardware_device(
        db,
        actor=user,
        hardware_kind_id=balanca_kind.id,
        point_type_id=point_type.id,
        connection_template_id=template.id,
    )
    logger.info(f"[SEED] Hardware Devices criados: {device.id}, {balanca.id}")
    return device, balanca


def create_installations(db, user):
    create_installation(db, actor=user, name="Instalação Central", ip_address="192.168.60.100")
    create_installation(db, actor=user, name="Instalação Secundária", ip_address="177.122.01.100")
    logger.info("[SEED] Instalações criadas")


def create_kitchens(db, user):
    global PINS_COUNT
    create_kitchen(db, actor=user, name="CZ01", shaker_pin_id=1, pump_pin_id=2, scale_pin_id=3)
    create_kitchen(db, actor=user, name="CZ02", shaker_pin_id=4, pump_pin_id=5, scale_pin_id=6)
    PINS_COUNT = 7
    logger.info("[SEED] Cozinhas criadas")


def create_stall_feeders(db, room_stall_id, user):
    global PINS_COUNT
    for i in range(1, 4):
        feeder = create_stall_feeder(db, actor=user, name=f"Comedouro {i}", room_stall_id=room_stall_id, max_weight=1000.0)
        if PINS_COUNT < 25:
            create_feeder_valve(db, actor=user, device_pin_id=PINS_COUNT, stall_feeder_id=feeder.id)
            PINS_COUNT += 1
    logger.info("[SEED] Comedouros de baia criados")

def create_room_stalls(db, shed_room_id, user):
    for i in range(1, 5):
        stall = create_room_stall(db, actor=user, name=f"Baia {i}", shed_room_id=shed_room_id)
        create_stall_feeders(db, stall.id, user)
    logger.info("[SEED] Baias de sala criadas")

def create_shed_rooms(db, shed_id, user):
    global PINS_COUNT
    for i in range(1, 5):
        room = create_shed_room(db, actor=user, name=f"Sala {i}", shed_id=shed_id, entrance_pin_id=PINS_COUNT)
        PINS_COUNT += 1
        create_room_stalls(db, room.id, user)
    logger.info("[SEED] Salas de galpão criadas")

def create_sheds(db, user):
    for i in range(1, 5):
        shed = create_shed(db, actor=user, name=f"Galpão {i}")
        create_shed_rooms(db, shed.id, user)
    logger.info("[SEED] Galpões criados")

def create_products(db, user):
    create_product(db, actor=user, name="Água", description="Água natural", moisture_percentage=0, kind="liquid", density=1000, is_active=True)
    create_product(db, actor=user, name="Milho", description="Milho em grão", moisture_percentage=12, kind="solid", density=600, is_active=True)
    create_product(db, actor=user, name="Soja", description="Soja em grão", moisture_percentage=0, kind="solid", density=800, is_active=True)
    create_product(db, actor=user, name="Farelo de soja", description="Farelo de soja", moisture_percentage=10, kind="solid", density=500, is_active=True)
    logger.info("[SEED] Produtos criados")


def create_product_tanks(db, user):
    # Cria tanques para cada produto cadastrado
    # Supondo que IDs dos produtos são 1=Água, 2=Milho, 3=Soja, 4=Farelo de soja
    global PINS_COUNT
    create_product_tank(db, actor=user, name="Tanque Água", description="Tanque para água", pin_id=PINS_COUNT, product_id=1)
    create_product_tank(db, actor=user, name="Tanque Milho", description="Tanque para milho", pin_id=PINS_COUNT+1, product_id=2)
    create_product_tank(db, actor=user, name="Tanque Soja", description="Tanque para soja", pin_id=PINS_COUNT+2, product_id=3)
    create_product_tank(db, actor=user, name="Tanque Farelo de soja", description="Tanque para farelo de soja", pin_id=PINS_COUNT+3, product_id=4)
    logger.info("[SEED] Tanques de produtos criados")


def seed():
    with session_scope() as db:
        try:
            create_profiles(db)
            user = create_users(db)
            hw_kind, balanca_kind = create_hardware_kinds(db, user)
            point_type = create_hardware_point_type(db, user)
            logger.info(f"[SEED] Hardware Point Type criado: {point_type.id}")
            template = create_hardware_connection_template(db, user)
            logger.info(f"[SEED] Hardware Connection Template criado: {template.id}")
            devices = create_hardware_devices(db, user, hw_kind, balanca_kind, point_type, template)
            create_installations(db, user)
            create_kitchens(db, user)
            create_sheds(db, user)
            create_products(db, user)
            create_product_tanks(db, user)

            db.commit()
            logger.info("[SEED] Seed executado com sucesso")
        except Exception as e:
            db.rollback()
            logger.error(f"[SEED] Erro ao executar seed: {e}")
            raise


if __name__ == "__main__":
    reset_database()
    seed()
