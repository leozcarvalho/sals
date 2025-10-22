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


    def send_value(self, value: str) -> Dict[str, str]:
        return ApiResponse(success=True, data="teste")
        try:
            url = f"{self.url}?{self.query_string.replace('{value}', str(value))}"
            print(url)
            response = self.session.get(url, timeout=self.timeout)
            print(f"RESPONSE: {response.text}")
            response.raise_for_status()
            return ApiResponse(success=True, data=response.text)
        except requests.Timeout:
            logger.error(f"Timeout ao conectar com dispositivo {self.ip}")
            raise exc.Timeout(f"Dispositivo {self.ip} não respondeu no tempo limite")
        except requests.RequestException as e:
            logger.error(f"Erro de conexão com dispositivo {self.ip}: {e}")
            raise exc.ConnectionError(f"Falha de conexão com {self.ip}")

    def healthcheck(self) -> ApiResponse:
        """
        Healthcheck simples da placa.
        """
        print(f"Executando healthcheck para {self.url}")
        response = self.session.get(f"{self.url}?AT", timeout=self.timeout)
        if response.text == 'OK':
            return ApiResponse(success=True, data=response.text)
        return ApiResponse(success=False, data=response.text)

    def restart(self) -> ApiResponse:
        """
        Reinicia a placa.
        """
        print(f"Reiniciando dispositivo {self.url}")
        response = self.session.get(f"{self.url}?ATZ", timeout=self.timeout)
        if response.text == 'Reiniciando...':
            return ApiResponse(success=True, data=response.text)
        return ApiResponse(success=False, data=response.text)
