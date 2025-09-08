import requests
from typing import Dict
from src.schemas.api_response import ApiResponse
from src.domain import exceptions as exc

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

    def _request(self, path: str, params: Dict[str, str] = None) -> ApiResponse:
        """
        Método centralizado para todas as requisições HTTP à placa.
        """
        url = f"http://{self.ip}/get?{path}"
        print("Making request to device at url:", url)
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            print("Response from device:", response.text)
            return ApiResponse(success=True, data=response.text)
        except requests.exceptions.RequestException as e:
            # apenas loga o detalhe técnico
            print(f"Falha ao conectar com dispositivo {self.ip}: {e}")
            # lança ConnectionError para middleware traduzir em 503
            raise ConnectionError(f"Não foi possível conectar ao dispositivo {self.ip}")


    def healthcheck(self) -> ApiResponse:
        """
        Healthcheck simples.
        """
        return self._request("AT")

    def restart(self) -> ApiResponse:
        """
        Reinicia a placa.
        """
        return self._request("ATZ")
