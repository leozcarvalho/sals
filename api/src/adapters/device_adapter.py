import requests
from typing import Dict
from src.schemas.api_response import ApiResponse

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
            print("Response:", response.text)
            return ApiResponse(success=True, data=response.text)
        except requests.RequestException as e:
            print("Error occurred while making request:", e)
            return ApiResponse(success=False, error=str(e))


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
