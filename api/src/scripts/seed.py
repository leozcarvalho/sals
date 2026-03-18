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
from tests.fixtures.valve_fixture import create_valve
from tests.fixtures.product_fixture import create_product
from tests.fixtures.product_tank_fixture import create_product_tank
from tests.fixtures.formula_fixture import create_formula
from tests.fixtures.feeding_curve_fixture import create_feeding_curve
from tests.fixtures.feeding_curve_detail_fixture import create_feeding_curve_detail
from tests.fixtures.moviment_kinds_fixture import create_moviment_kind
from tests.fixtures.shed_fixture import create_shed
from tests.fixtures.sala_fixture import create_sala
from tests.fixtures.baia_fixture import create_baia


from src.cruds.trato import TratoRepository
from src.schemas.trato import TratoCreate


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


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
    create_product_tank(db, actor=user, name="TQ01", description="Silo Externo 01", pin_id=None, product_id=2)
    create_product_tank(db, actor=user, name="TQ02", description="Silo Externo 02", pin_id=None, product_id=2)
    create_product_tank(db, actor=user, name="TQ03", description="Soli Externo 03", pin_id=None, product_id=3)
    create_product_tank(db, actor=user, name="CX01", description="Caixa Dágua", pin_id=None, product_id=1)
    create_product_tank(db, actor=user, name="TQPX01", description="Silo de Premix", pin_id=None, product_id=5)
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
    #dia curva, id formula, peso suino, alimento por animal
    CURVE_DETAILS_DATA = [[22,1,22.8,1.21],[23,1,23.4,1.23],[24,1,24.0,1.25],[25,1,24.6,1.27],[26,1,25.2,1.30],[27,1,25.8,1.32],
                          [28,1,26.4,1.34],[29,1,27.0,1.36],[30,1,27.6,1.37],[31,1,28.3,1.38],[32,1,28.9,1.39],[33,1,29.5,1.39],[34,1,30.1,1.40],
                          [35,1,30.8,1.41],[36,1,31.4,1.42],[37,1,32.1,1.44],[38,1,32.7,1.46],[39,1,33.4,1.48],[40,1,34.1,1.51],[41,1,34.8,1.53],
                          [42,1,35.4,1.55],[43,1,36.1,1.57],[44,1,36.8,1.60],[45,1,37.5,1.63],[46,1,38.2,1.66],[47,1,39.0,1.70],[48,1,39.7,1.73],
                          [49,1,40.4,1.76],[50,1,41.1,1.79],[51,1,41.9,1.81],[52,1,42.6,1.83],[53,1,43.4,1.85],[54,1,44.1,1.88],[55,1,44.9,1.90],
                          [56,1,45.6,1.92],[57,2,46.4,1.94],[58,2,47.2,1.96],[59,2,48.0,1.98],[60,2,48.8,2.00],[61,2,49.5,2.03],[62,2,50.3,2.05],
                          [63,2,51.1,2.07],[64,3,51.9,2.09],[65,3,52.7,2.10],[66,3,53.6,2.11],[67,3,54.4,2.12],[68,3,55.2,2.14],[69,3,56.0,2.15],
                          [70,3,56.9,2.16],[71,3,57.7,2.17],[72,3,58.6,2.17],[73,3,59.4,2.18],[74,3,60.3,2.18],[75,3,61.2,2.19],[76,3,62.1,2.19],
                          [77,3,62.9,2.20],[78,3,63.8,2.20],[79,3,64.7,2.22],[80,3,65.6,2.25],[81,3,66.5,2.27],[82,3,67.5,2.30],[83,3,68.4,2.32],
                          [84,3,69.3,2.35],[85,4,70.2,2.37],[86,4,71.1,2.39],[87,4,72.1,2.40],[88,4,73.0,2.42],[89,4,74.0,2.44],[90,4,74.9,2.46],
                          [91,4,75.9,2.47],[92,4,76.8,2.49],[93,4,77.8,2.51],[94,4,78.8,2.53],[95,4,79.8,2.55],[96,4,80.7,2.57],[97,4,81.7,2.59],
                          [98,4,82.7,2.61],[99,4,83.7,2.63],[100,4,84.7,2.65],[101,4,85.8,2.67],[102,4,86.8,2.69],[103,4,87.8,2.71],[104,4,88.8,2.73],
                          [105,4,89.9,2.75],[106,5,90.9,2.77],[107,5,92.0,2.78],[108,5,93.0,2.80],[109,5,94.1,2.82],[110,5,95.2,2.84],[111,5,96.3,2.86],
                          [112,5,97.3,2.88],[113,5,98.4,2.90],[114,5,99.5,2.90],[115,5,100.6,2.90],[116,5,101.7,2.90],[117,5,102.8,2.90],[118,5,103.9,2.90],
                          [119,5,105.0,2.90],[120,5,106.1,2.90],[121,5,107.2,2.90],[122,5,108.4,2.90],[123,5,109.5,2.90],[124,5,110.7,2.90],[125,5,111.8,2.90],
                          [126,5,113.0,2.90],[127,5,114.1,2.90],[128,5,114.8,2.90],[129,5,115.4,2.90],[130,5,116.1,2.90],[131,5,116.8,2.90],[132,5,117.5,2.90],
                          [133,5,118.1,2.90],[134,5,118.8,2.90],[135,5,119.5,2.90],[136,5,120.1,2.90],[137,5,120.8,2.90],[138,5,121.5,2.90],[139,5,122.2,2.90],
                          [140,5,122.8,2.90],[141,5,123.5,2.90]]

    curve = create_feeding_curve(db,
            actor=user,
            name="AURORA_CR_TE_AJ_01",
            description=f"Curva fornecida pela Aurora, ajustada dia a dia"
        )
    
    for detail in CURVE_DETAILS_DATA:
        create_feeding_curve_detail(db,
            actor=user,
            feeding_curve_id=curve.id,
            age_day=detail[0],
            formula_id=detail[1],
            animal_weight=detail[2],
            formula_mass_per_animal=detail[3],
            is_active=True
        )

    logger.info("[SEED] Curvas de alimentação criadas")

def create_moviment_kinds(db, user):
    create_moviment_kind(db, actor=user, kind="ENTRADA", code="ENTRADA DE LOTE")
    create_moviment_kind(db, actor=user, kind="SAIDA", code="SAIDA DE LOTE")
    create_moviment_kind(db, actor=user, kind="SAIDA", code="OBITO")
    create_moviment_kind(db, actor=user, kind="TRANSFERENCIA", code="TRANSFERENCIA ENTRE BAIAS")
    logger.info("[SEED] Tipos de movimentação criados")

def criar_galpoes(db, user):
    create_shed(db, actor=user, name="G3", kitchen_id=1)
    create_shed(db, actor=user, name="G4", kitchen_id=1)
    logger.info("[SEED] Galpões criados")

def criar_salas(db, user):
    create_sala(db, actor=user, name="S01", shed_id=1)
    create_sala(db, actor=user, name="S01", shed_id=2)
    logger.info("[SEED] Salas criadas")

def criar_baias(db, user):
    #44 baias pra cada sala
    for i in range(1, 45):
        create_baia(db, actor=user, name=f"B{i:02d}", sala_id=1)
        create_baia(db, actor=user, name=f"B{i:02d}", sala_id=2)


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
            create_product_tanks(db, user)
            create_formulas(db, user)
            create_kitchen(db, user)
            criar_galpoes(db, user)
            criar_salas(db, user)
            criar_baias(db, user)
            create_moviment_kinds(db, user)
            create_feeding_curves(db, user)
            create_tratos(db, user)
            logger.info("[SEED] Seed executado com sucesso")
        except Exception as e:
            logger.error(f"[SEED] Erro ao executar seed: {e}")
            raise


if __name__ == "__main__":
    reset_database()
    seed()
