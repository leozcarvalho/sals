from pathlib import Path
import logging
from sqlmodel import SQLModel
from alembic import command
from alembic.config import Config
from random import randint
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
from tests.fixtures.kitchen_tank_fixture import create_kitchen_tank
from tests.fixtures.installation_fixture import create_installation
from tests.fixtures.feeder_valve_fixture import create_feeder_valve
from tests.fixtures.product_fixture import create_product
from tests.fixtures.product_tank_fixture import create_product_tank
from tests.fixtures.formula_fixture import create_formula
from tests.fixtures.feeding_curve_fixture import create_feeding_curve
from tests.fixtures.feeding_curve_detail_fixture import create_feeding_curve_detail
from tests.fixtures.moviment_kinds_fixture import create_moviment_kind
from tests.fixtures.shed_fixture import create_shed
from src.cruds.trato import TratoRepository
from src.schemas.trato import TratoCreate


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
    create_user(db, name="Usuário Engenharia", email="sals@engenharia.com", profile_id=2)
    logger.info(f"[SEED] Usuários criados")
    return admin


def create_hardware_point_types(db, user):
    create_hardware_point_type(db, actor=user)
    create_hardware_point_type(db, actor=user, points_quantity=1, kind="bit")
    create_hardware_point_type(db, actor=user, points_quantity=16, kind="bit")
    logger.info("[SEED] Hardware Point Types criados")

def create_hardware_kinds(db, user):
    create_hardware_kind(db, user, name='Saída', kind="output")
    create_hardware_kind(db, user, name='Entrada', kind="input")

def create_hardware_connection_templates(db, user):
    create_hardware_connection_template(db, actor=user, name="Template de Conexão (VA32)", template_url="http://{ip}/get", query_string="valvula1={value}&valvula2=0")
    create_hardware_connection_template(db, actor=user, name="Template de Conexão Relé", template_url="http://{ip}/get", query_string="rele={value}")
    create_hardware_connection_template(db, actor=user, name="Template de Conexão Balança", template_url="http://{ip}/get", query_string="peso")

def create_hardware_devices(db, user):
    create_hardware_device(
        db,
        name="VA32",
        actor=user,
        hardware_kind_id=1,
        point_type_id=1,
        connection_template_id=1,
    )
    create_hardware_device(
        db,
        name="Balança Industrial",
        actor=user,
        hardware_kind_id=2,
        point_type_id=2,
        connection_template_id=3,
    )
    create_hardware_device(
        db,
        name="Placa de relé",
        actor=user,
        hardware_kind_id=1,
        point_type_id=3,
        connection_template_id=2,
    )

def create_installations(db, user):
    create_installation(db, actor=user, name="VA32", ip_address="192.168.60.100", device_id=1)
    create_installation(db, actor=user, name="Pesagem", ip_address="192.168.60.250", device_id=2)
    create_installation(db, actor=user, name="RE16", ip_address="192.168.60.252", device_id=3)
    logger.info("[SEED] Instalações criadas")



def create_products(db, user):
    create_product(db, actor=user, name="Água", description="Água natural", moisture_percentage=0, kind="liquid", density=1000, is_active=True)
    create_product(db, actor=user, name="Milho", description="Milho em grão", moisture_percentage=12, kind="solid", density=650, is_active=True)
    create_product(db, actor=user, name="Soja", description="Soja em grão", moisture_percentage=8, kind="solid", density=790, is_active=True)
    create_product(db, actor=user, name="Sorgo", description="Sorgo em grão", moisture_percentage=10, kind="solid", density=800, is_active=True)
    create_product(db, actor=user, name="Premix 01", description="Premix", moisture_percentage=0, kind="solid", density=1200, is_active=True)
    logger.info("[SEED] Produtos criados")


def create_product_tanks(db, user):
    global PINS_COUNT
    create_product_tank(db, actor=user, name="TQ01", description="Silo Externo 01", pin_id=PINS_COUNT, product_id=2)
    create_product_tank(db, actor=user, name="TQ02", description="Silo Externo 02", pin_id=PINS_COUNT+1, product_id=2)
    create_product_tank(db, actor=user, name="TQ03", description="Soli Externo 03", pin_id=PINS_COUNT+2, product_id=3)
    create_product_tank(db, actor=user, name="CX01", description="Caixa Dágua", pin_id=PINS_COUNT+3, product_id=1)
    create_product_tank(db, actor=user, name="TQPX01", description="Silo de Premix", pin_id=PINS_COUNT+4, product_id=5)
    logger.info("[SEED] Tanques de produtos criados")

def create_formulas(db, user):
    create_formula(db,
        actor=user,
        name="ALOJAMENTO",
        description="Fórmula de alojamento para adaptação da vinda da creche",
        water_percentage=75, stirring_time=400,
        details=[
          { "product_id": 2, "product_percentage_without_moisture": 100 }  
        ]
    )

    create_formula(db,
        actor=user,
        name="CRESCIMENTO 1",
        description="Fórmula de crescimento fase 1",
        water_percentage=75,
        stirring_time=400,
        details=[
          { "product_id": 2, "product_percentage_without_moisture": 50 },
          { "product_id": 3, "product_percentage_without_moisture": 50 }
        ]
    )

    create_formula(db,
        actor=user,
        name="CRESCIMENTO 2",
        description="CRESCIMENTO FASE 2",
        water_percentage=75,
        stirring_time=400,
        details=[
          { "product_id": 2, "product_percentage_without_moisture": 100 }
        ]
    )

    create_formula(db,
        actor=user,
        name="TERMINAÇÃO",
        description="POLIMENTO DE FIM DE CICLO",
        water_percentage=75,
        stirring_time=400,
        details=[
          { "product_id": 2, "product_percentage_without_moisture": 100 }
        ]
    )

    create_formula(db,
        actor=user,
        name="FINAL",
        description="MANUTENÇÃO ATÉ RETIRADA DO GALPÃO",
        water_percentage=75,
        stirring_time=400,
        details=[
          { "product_id": 2, "product_percentage_without_moisture": 100 }
        ]
    )
    logger.info(f"[SEED] Fórmulas criadas")


def create_feeding_curves(db, user):
    for i in range(1, 3):
        curve = create_feeding_curve(db, actor=user, name=f"Curva {i}", description=f"Descrição da Curva de Alimentação {i}")
        for day in range(1, 29):
            formula_id = 1 if day <= 14 else 2 if day <= 21 else 3
            create_feeding_curve_detail(
                db,
                actor=user,
                feeding_curve_id=curve.id,
                age_day=day,
                formula_id=formula_id,
                formula_mass_per_animal=2.5 + (day * 0.1),  # Exemplo de variação de massa
                animal_weight=0.5 + (day * 0.2),  # Exemplo de variação de peso
            )
    logger.info("[SEED] Curvas de alimentação criadas")

def create_moviment_kinds(db, user):
    create_moviment_kind(db, actor=user, kind="ENTRADA", code="ENTRADA_LOTE")
    create_moviment_kind(db, actor=user, kind="ENTRADA", code="ENTRADA_OUTRO_LOTE")
    create_moviment_kind(db, actor=user, kind="ENTRADA", code="ENTRADA_COMPRA_POSTERIOR")
    create_moviment_kind(db, actor=user, kind="SAIDA", code="SAIDA_LOTE")
    create_moviment_kind(db, actor=user, kind="SAIDA", code="SAIDA_VENDA_AVULSA")
    create_moviment_kind(db, actor=user, kind="SAIDA", code="SAIDA_OUTRO_LOTE")
    create_moviment_kind(db, actor=user, kind="SAIDA", code="SAIDA_MORTE")
    create_moviment_kind(db, actor=user, kind="TRANSFERENCIA", code="MOVE_DETRO_LOTE")
    logger.info("[SEED] Tipos de movimentação criados")

def create_sheds(db, user):
    create_shed(db, actor=user, name="G1", kitchen_id=1)
    create_shed(db, actor=user, name="G2", kitchen_id=1)
    logger.info("[SEED] Galpões criados")

def create_tratos(db, user):
    trato_repo = TratoRepository(db)
    trato_repo.bulk_save([
        TratoCreate(name="T1", hour=6, percent=20),
        TratoCreate(name="T2", hour=12, percent=20),
        TratoCreate(name="T3", hour=18, percent=20),
        TratoCreate(name="T4", hour=22, percent=20),
        TratoCreate(name="T5", hour=22, percent=20),
        TratoCreate(name="T6", hour=22, percent=0),
    ], actor=user)
    logger.info("[SEED] Tratos criados")

def seed():
    with session_scope() as db:
        try:
            create_profiles(db)
            user = create_users(db)
            create_hardware_kinds(db, user)
            create_hardware_point_types(db, user)
            create_hardware_connection_templates(db, user)
            create_hardware_devices(db, user)
            create_installations(db, user)
            create_products(db, user)
            create_formulas(db, user)
            create_kitchen(db, user)
            create_sheds(db, user)
            create_tratos(db, user)
            logger.info("[SEED] Seed executado com sucesso")
        except Exception as e:
            logger.error(f"[SEED] Erro ao executar seed: {e}")
            raise


if __name__ == "__main__":
    reset_database()
    seed()
