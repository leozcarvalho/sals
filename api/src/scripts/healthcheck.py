import asyncio
from datetime import datetime, timezone
from src.core.db import session_scope
from src.cruds.installations import InstallationRepository
from src.cruds.healthcheck_priority import HealthcheckPriorityRepository
from src.domain import User

async def healthcheck_level(priority_data, actor_id):
    """
    Loop contínuo para um nível específico.
    priority_data: dict com keys id, level, interval_seconds
    actor_id: ID do usuário sistema
    """
    while True:
        with session_scope() as session:
            actor = session.get(User, actor_id)
            installation_repo = InstallationRepository(session)

            installations = installation_repo.get_list(
                filters={"healthcheck_priority_id": priority_data["id"]}
            )

            print(f"\n🔔 Healthcheck nível {priority_data['level']} - {len(installations)} instalações")

            for inst in installations:
                try:
                    print(f"🔍 Testando placa {inst.id} ({inst.ip_address})...")
                    installation_repo.health_check(inst.id, actor)
                    print(f"✅ Placa {inst.id} online")
                except Exception as e:
                    print(f"❌ Placa {inst.id} offline ({e})")

        print(f"⏱ Aguardando {priority_data['interval_seconds']}s para o próximo check do nível {priority_data['level']}")
        await asyncio.sleep(priority_data['interval_seconds'])

async def main():
    with session_scope() as session:
        priority_repo = HealthcheckPriorityRepository(session)
        actor = session.get(User, 1)  # Usuário sistema

        # Carrega apenas os campos essenciais para não ter DetachedInstanceError
        raw_priorities = priority_repo.get_list(order_by={"level": "asc"})
        priorities = [
            {"id": p.id, "level": p.level, "interval_seconds": p.interval_seconds}
            for p in raw_priorities
        ]

    # Cria uma tarefa concorrente para cada nível
    tasks = [healthcheck_level(priority, actor_id=1) for priority in priorities]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
