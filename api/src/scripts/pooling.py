import logging
from time import monotonic, sleep
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from src.core.db import session_scope
from src.cruds.installations import InstallationRepository

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)

def handle_installation(repo, installation):
    if installation.hardware_kind == "output":
        if installation.binary_value != installation.last_value:
            device_service = repo._get_device_service(installation)
            response = device_service.send_value(installation.decimal_value)
            if response.success:
                repo.update(installation.id, {"last_value": installation.binary_value})
                logging.info(f"[{installation.id}] relé → {installation.decimal_value} (bin={installation.binary_value})")
            else:
                logging.warning(f"[{installation.id}] falha ao enviar relé: {response.error}")
        else:
            logging.debug(f"[{installation.id}] relé em sincronia ({installation.decimal_value})")

    elif installation.hardware_kind == "input":
        device_service = repo._get_device_service(installation)
        response = device_service.read_value()
        if response.success:
            current_value = response.data
            logging.info(f"[{installation.id}] peso: {current_value} kg")
            if current_value != installation.last_value:
                repo.update(installation.id, {"last_value": current_value})
                logging.info(f"[{installation.id}] peso salvo: {installation.last_value} → {current_value} kg")
        else:
            logging.warning(f"[{installation.id}] erro ao ler peso: {response.error}")

def process_installations():
    with session_scope() as session:
        repo = InstallationRepository(session)
        installation_ids = [inst.id for inst in repo.get_list()]

    with ThreadPoolExecutor(max_workers=8) as executor:
        for inst_id in installation_ids:
            executor.submit(safe_handle, inst_id)

def safe_handle(inst_id):
    try:
        with session_scope() as session:
            repo = InstallationRepository(session)
            installation = repo.check_exists(inst_id)
            handle_installation(repo, installation)
    except Exception as e:
        logging.exception(f"Erro ao processar instalação {inst_id}: {e}")

def main():
    while True:
        start = monotonic()
        try:
            process_installations()
        except Exception as e:
            logging.exception(f"Erro geral no loop: {e}")
        elapsed = monotonic() - start
        sleep(max(0, 1 - elapsed))

if __name__ == "__main__":
    main()