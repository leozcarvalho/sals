import logging
from typing import Dict
import requests
from src.schemas.api_response import ApiResponse
from src.domain import exceptions as exc

logger = logging.getLogger(__name__)

class DeviceService:
    """
    Serviço genérico para comunicação com placas em LAN.
    """

    def __init__(self, ip: str, url_template: str, query_string: str, timeout: float = 0.5):
        """
        :param ip: endereço IP da placa
        :param timeout: tempo máximo de espera em segundos (default 0.5s)
        """
        self.ip = ip
        self.url = url_template.replace("{ip}", ip)
        self.query_string = query_string
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, endpoint: str, expect: str = None) -> ApiResponse:
        try:
            url = f"{self.url}?{endpoint}"
            logger.debug(f"Enviando requisição GET: {url}")
            response = self.session.get(url, timeout=self.timeout)
            logger.debug(f"Resposta ({response.status_code}): {response.text.strip()}")
            response.raise_for_status()

            success = True if expect is None else (expect in response.text)
            return ApiResponse(success=success, data=response.text.strip())
        except requests.Timeout:
            logger.error(f"Timeout ao conectar com dispositivo {self.ip}")
            return ApiResponse(success=False, error=f"Dispositivo {self.ip} não respondeu no tempo limite")
        except requests.RequestException as e:
            logger.error(f"Erro de conexão com dispositivo {self.ip}: {e}")
            return ApiResponse(success=False, error=f"Falha de conexão com {self.ip}")

    def send_value(self, value: str) -> ApiResponse:
        return self._request(self.query_string.replace("{value}", str(value)))

    def read_value(self) -> ApiResponse:
        return self._request(self.query_string)

    def healthcheck(self) -> ApiResponse:
        return self._request("AT", expect="OK")

    def restart(self) -> ApiResponse:
        return self._request("ATZ", expect="Reiniciando")

    def tare(self) -> ApiResponse:
        return self._request("AT_CAL_ZERO", expect="Atencao")

    def calibrate(self, weight: float) -> ApiResponse:
        return self._request(f"AT_CAL_PESO={weight}", expect="Atencao")