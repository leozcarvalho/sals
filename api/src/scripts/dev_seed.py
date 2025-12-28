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
from tests.fixtures.shed_fixture import create_shed
from tests.fixtures.sala_fixture import create_sala
from tests.fixtures.baia_fixture import create_baia
from tests.fixtures.comedouro_fixture import create_comedouro
from tests.fixtures.feeder_valve_fixture import create_feeder_valve
from tests.fixtures.product_fixture import create_product
from tests.fixtures.product_tank_fixture import create_product_tank
from tests.fixtures.formula_fixture import create_formula
from tests.fixtures.feeding_curve_fixture import create_feeding_curve
from tests.fixtures.feeding_curve_detail_fixture import create_feeding_curve_detail
from tests.fixtures.batch_fixture import create_batch
from tests.fixtures.moviment_kinds_fixture import create_moviment_kind
from tests.fixtures.svg_fixture import create_svg

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
    create_hardware_connection_template(db, actor=user, name="Template de Conexão 1", template_url="http://{ip}/get", query_string="valvula1={value}&valvula2=0")
    create_hardware_connection_template(db, actor=user, name="Template de Conexão 2", template_url="http://{ip}/get", query_string="rele={value}")
    create_hardware_connection_template(db, actor=user, name="Template de Conexão Avançado", template_url="http://{ip}/get", query_string="peso")

def create_hardware_devices(db, user):
    create_hardware_device(
        db,
        actor=user,
        hardware_kind_id=1,
        point_type_id=1,
        connection_template_id=1,
    )
    create_hardware_device(
        db,
        actor=user,
        hardware_kind_id=2,
        point_type_id=2,
        connection_template_id=3,
    )
    create_hardware_device(
        db,
        actor=user,
        name="Placa de relé",
        hardware_kind_id=1,
        point_type_id=3,
        connection_template_id=2,
    )

def create_installations(db, user):
    create_installation(db, actor=user, name="VA32", ip_address="192.168.60.100", device_id=1)
    create_installation(db, actor=user, name="Pesagem", ip_address="192.168.60.250", device_id=2)
    create_installation(db, actor=user, name="RE16", ip_address="192.168.60.252", device_id=3)
    logger.info("[SEED] Instalações criadas")


def create_kitchens(db, user):
    global PINS_COUNT
    create_kitchen(db, actor=user, name="CZ01", shaker_pin_id=1, pump_pin_id=2, scale_pin_id=3)
    #create_kitchen(db, actor=user, name="CZ02", shaker_pin_id=4, pump_pin_id=5, scale_pin_id=6)
    PINS_COUNT = 4
    logger.info("[SEED] Cozinhas criadas")


def create_comedouros(db, baia_id, user):
    global PINS_COUNT
    for i in range(1, randint(2, 6)):
        comedouro = create_comedouro(db, actor=user, name=f"C{i}", baia_id=baia_id, max_weight=1000.0)
        if PINS_COUNT < 25:
            create_feeder_valve(db, actor=user, device_pin_id=PINS_COUNT, comedouro_id=comedouro.id)
            PINS_COUNT += 1
    logger.info("[SEED] Comedouros de baia criados")

def create_baias(db, sala_id, user):
    for i in range(1, randint(2, 6)):
        baia = create_baia(db, actor=user, name=f"B{i}", sala_id=sala_id)
        create_comedouros(db, baia.id, user)
    logger.info("[SEED] Baias de sala criadas")

def create_salas(db, shed_id, user):
    global PINS_COUNT
    for i in range(1, randint(2, 6)):
        sala = create_sala(db, actor=user, name=f"S{i}", shed_id=shed_id, entrance_pin_id=PINS_COUNT)
        PINS_COUNT += 1
        create_baias(db, sala.id, user)
    logger.info("[SEED] Salas de galpão criadas")

def create_sheds(db, user):
    for i in range(1, 5):
        shed = create_shed(db, actor=user, name=f"G{i}")
        create_salas(db, shed.id, user)
    logger.info("[SEED] Galpões criados")

def create_products(db, user):
    create_product(db, actor=user, name="Água", description="Água natural", moisture_percentage=0, kind="liquid", density=1000, is_active=True)
    create_product(db, actor=user, name="Milho", description="Milho em grão", moisture_percentage=12, kind="solid", density=600, is_active=True)
    create_product(db, actor=user, name="Soja", description="Soja em grão", moisture_percentage=0, kind="solid", density=800, is_active=True)
    create_product(db, actor=user, name="Sorgo", description="Sorgo em grão", moisture_percentage=10, kind="solid", density=500, is_active=True)
    logger.info("[SEED] Produtos criados")


def create_product_tanks(db, user):
    global PINS_COUNT
    create_product_tank(db, actor=user, name="T01", description="Tanque para água", pin_id=PINS_COUNT, product_id=1)
    create_product_tank(db, actor=user, name="T02", description="Tanque para milho", pin_id=PINS_COUNT+1, product_id=2)
    create_product_tank(db, actor=user, name="T03", description="Tanque para soja", pin_id=PINS_COUNT+2, product_id=3)
    create_product_tank(db, actor=user, name="T04", description="Tanque para sorgo", pin_id=PINS_COUNT+3, product_id=4)
    logger.info("[SEED] Tanques de produtos criados")

def create_formulas(db, user):
    details = [
        { "product_id": 1, "product_percentage_without_moisture": 50 },  # Água
        { "product_id": 2, "product_percentage_without_moisture": 30 },  # Milho
        { "product_id": 3, "product_percentage_without_moisture": 15 },  # Soja  
        { "product_id": 4, "product_percentage_without_moisture": 5 },   # Farelo de soja
    ]
    create_formula(db, actor=user, name="Fórmula Exemplo", description="Fórmula de ração exemplo", water_percentage=10, stirring_time=300, details=details)
    create_formula(db, actor=user, name="Fórmula Avançada", description="Fórmula de ração avançada", water_percentage=20, stirring_time=450, details=details)
    create_formula(db, actor=user, name="Fórmula Premium", description="Fórmula de ração premium", water_percentage=30, stirring_time=600, details=details)
    logger.info(f"[SEED] Fórmula criada")


def create_kitchen_tanks(db, user):
    create_kitchen_tank(db, actor=user, product_tank_id=1, kitchen_id=1)
    create_kitchen_tank(db, actor=user, product_tank_id=2, kitchen_id=1)
    create_kitchen_tank(db, actor=user, product_tank_id=3, kitchen_id=1)
    create_kitchen_tank(db, actor=user, product_tank_id=4, kitchen_id=1)
    logger.info(f"[SEED] Tanques de cozinha criados")

def create_svgs(db, user):
    #svg em /assets
    with open(Path(__file__).parent.parent.parent / "assets" / "CZ1.svg", "r") as f:
        svg_example = f.read()
    create_svg(db, actor=user, name="SVG Cozinha", owner_type="kitchens", owner_id=1, content=svg_example)
    with open(Path(__file__).parent.parent.parent / "assets" / "G1.svg", "r") as f:
        svg_example = f.read()
    create_svg(db, actor=user, name="SVG Galpão", owner_type="sheds", owner_id=1, content=svg_example)
    with open(Path(__file__).parent.parent.parent / "assets" / "placa.svg", "r") as f:
        svg_example = f.read()
    create_svg(db, actor=user, name="SVG Placa 32 bits", owner_type="installations", owner_id=1, content=svg_example)
    with open(Path(__file__).parent.parent.parent / "assets" / "balanca.svg", "r") as f:
        svg_example = f.read()
    create_svg(db, actor=user, name="SVG Balança", owner_type="installations", owner_id=2, content=svg_example)
    logger.info(f"[SEED] SVGs criados")

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
            create_kitchens(db, user)
            create_sheds(db, user)
            create_products(db, user)
            create_product_tanks(db, user)
            create_formulas(db, user)
            create_kitchen_tanks(db, user)
            create_feeding_curves(db, user)
            create_svgs(db, user)
            create_moviment_kinds(db, user)
            logger.info("[SEED] Seed executado com sucesso")
        except Exception as e:
            logger.error(f"[SEED] Erro ao executar seed: {e}")
            raise


if __name__ == "__main__":
    reset_database()
    seed()
