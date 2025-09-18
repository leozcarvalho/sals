import asyncio
from datetime import datetime
from src.core.db import session_scope
from src.cruds.healthcheck_priority import HealthcheckPriorityRepository
from src.cruds.installations import InstallationRepository
from src.cruds.users import UsersRepository
from apscheduler.schedulers.blocking import BlockingScheduler

async def run_healthcheck(installation):
    with session_scope() as session:
        actor = UsersRepository(session).get(1)
        repo = InstallationRepository(session)
        try:
            print(f"🔍 Testando placa {installation.id} ({installation.ip_address})...")
            repo.health_check(installation.id, actor)
            print(f"✅ Placa {installation.id} online")
        except Exception as e:
            print(f"❌ Placa {installation.id} offline ({e})")
        print(f"[{datetime.now()}] Executando healthcheck {installation.id}")
        await asyncio.sleep(0.1)

async def run_priority(priority_id):
    with session_scope() as session:
        priority = HealthcheckPriorityRepository(session).get(priority_id)
        repo = InstallationRepository(session)
        installations = repo.get_list(filters={"healthcheck_priority_id": priority.id})
        await asyncio.gather(*(run_healthcheck(i) for i in installations))
        print(f"[{datetime.now()}] Próxima execução de '{priority.name}' em {priority.interval_milliseconds} segundos")

def schedule_priorities():
    scheduler = BlockingScheduler()
    with session_scope() as session:
        repo = HealthcheckPriorityRepository(session)
        priorities = repo.get_list()

        for priority in priorities:
            # Agendar cada prioridade pelo interval_milliseconds
            scheduler.add_job(
                lambda p=priority.id: asyncio.run(run_priority(p)),
                'interval',
                seconds=priority.interval_milliseconds / 1000,
                next_run_time=datetime.now()  # inicia imediatamente
            )
            print(f"Agendado '{priority.name}' a cada {priority.interval_milliseconds} segundos")

    scheduler.start()

if __name__ == "__main__":
    schedule_priorities()

