import requests
import logging
from typing import Dict
from src.schemas.api_response import ApiResponse
from src.domain import exceptions as exc

logger = logging.getLogger(__name__)  # logger do módulo

class DeviceService:
    """
    Serviço genérico para comunicação com placas.
    """

    def __init__(self, ip: str, timeout: int = 5):
        """
        :param ip: endereço IP da placa
        :param timeout: tempo máximo de espera em segundos
        """
        self.ip = ip
        self.timeout = timeout
        logger.info(f"DeviceService iniciado para IP {self.ip} com timeout {self.timeout}s")

    def _request(self, path: str, params: Dict[str, str] = None) -> ApiResponse:
        """
        Método centralizado para todas as requisições HTTP à placa.
        """
        url = f"http://{self.ip}/get?{path}"
        logger.info(f"Making request to device at url: {url} with params: {params}")
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"Response from device {self.ip}: {response.text}")
            return ApiResponse(
                success=True,
                data=response.text,
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Falha ao conectar com dispositivo {self.ip}: {e}")
            raise ConnectionError(f"Não foi possível conectar ao dispositivo {self.ip}")

    def healthcheck(self) -> ApiResponse:
        """
        Healthcheck simples.
        """
        logger.info(f"Executando healthcheck para dispositivo {self.ip}")
        return self._request("AT")

    def restart(self) -> ApiResponse:
        """
        Reinicia a placa.
        """
        logger.info(f"Enviando comando de restart para dispositivo {self.ip}")
        return self._request("ATZ")
