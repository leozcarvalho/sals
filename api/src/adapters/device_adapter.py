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

    def __init__(self, ip: str, timeout: float = 0.5):
        """
        :param ip: endereço IP da placa
        :param timeout: tempo máximo de espera em segundos (default 0.5s)
        """
        self.ip = ip
        self.timeout = timeout
        self.session = requests.Session()  # mantém TCP aberto
        logger.info(f"DeviceService iniciado para IP {self.ip} com timeout {self.timeout}s")

    def _request(self, command: str = None, params: dict = None) -> ApiResponse:
        """
        Envia comando AT ou parâmetros para a placa.
        
        - Se 'command' for fornecido sem 'params', envia como ?COMMAND
        - Se 'params' for fornecido, envia como ?key1=val1&key2=val2
        """
        url = f"http://{self.ip}/get"
        logger.info(f"Enviando requisição para {url} com command={command} params={params}")   
        try:
            if params:
                # Ex: valvula1, valvula2
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif command:
                # Ex: AT, ATZ, AT_SSID
                response = self.session.get(f"{url}?{command}", timeout=self.timeout)
            else:
                raise ValueError("É necessário fornecer 'command' ou 'params'")

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
        logger.debug(f"Executando healthcheck para {self.ip}")
        return self._request("AT")

    def restart(self) -> ApiResponse:
        """
        Reinicia a placa.
        """
        logger.debug(f"Enviando comando restart para {self.ip}")
        return self._request("ATZ")
