import logging
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException, ConnectionException
from src.schemas.api_response import ApiResponse

logger = logging.getLogger(__name__)


class DeviceService:
    """
    Comunicação com placas via Modbus TCP (porta 502).

    hardware_kind='output'  → placa de relés  (FC15 write multiple coils)
    hardware_kind='input'   → sensor de peso  (FC03 read holding registers)

    Mantém uma conexão TCP persistente por instância para evitar overhead de
    reconexão e incompatibilidade com dispositivos que limitam reconexões rápidas.
    """

    def __init__(
        self,
        ip: str,
        hardware_kind: str,
        port: int = 502,
        slave_id: int = 1,
        total_relays: int = 30,
        timeout: float = 2.0,
    ):
        self.ip = ip
        self.hardware_kind = hardware_kind
        self.port = port
        self.slave_id = slave_id
        self.total_relays = total_relays
        self.timeout = timeout
        self._client: ModbusTcpClient | None = None

    def _get_client(self) -> ModbusTcpClient:
        if self._client is None or not self._client.connected:
            self._client = ModbusTcpClient(
                self.ip, port=self.port, timeout=self.timeout, retries=0
            )
            if not self._client.connect():
                self._client = None
                raise OSError(f"Não foi possível conectar ao dispositivo {self.ip}:{self.port}")
        return self._client

    def close(self):
        if self._client is not None:
            self._client.close()
            self._client = None

    def send_value(self, value: int) -> ApiResponse:
        """Ativa os relés correspondentes ao valor decimal (placa de saída)."""
        try:
            coils = [(value >> i) & 1 for i in range(self.total_relays)]
            client = self._get_client()
            result = client.write_coils(0, coils, slave=self.slave_id)
            if result.isError():
                logger.error(f"[{self.ip}] Erro Modbus write_coils: {result}")
                return ApiResponse(success=False, error=str(result))
            return ApiResponse(success=True, data=str(value))
        except (ConnectionException, OSError, ModbusIOException) as e:
            logger.error(f"[{self.ip}] send_value falhou: {e}")
            self.close()
            return ApiResponse(success=False, error=str(e))

    def read_value(self) -> ApiResponse:
        """Lê o peso do sensor em kg (placa de entrada)."""
        try:
            client = self._get_client()
            result = client.read_holding_registers(0, count=2, slave=self.slave_id)
            if result.isError():
                logger.error(f"[{self.ip}] Erro Modbus read_holding_registers: {result}")
                return ApiResponse(success=False, error=str(result))
            r0, r1 = result.registers
            raw = (r1 << 16) + r0
            if raw > 2_147_483_647:
                raw -= 4_294_967_296
            peso = round(raw / 100.0, 2)
            return ApiResponse(success=True, data=str(peso))
        except (ConnectionException, OSError, ModbusIOException) as e:
            logger.error(f"[{self.ip}] read_value falhou: {e}")
            self.close()
            return ApiResponse(success=False, error=str(e))

    def healthcheck(self) -> ApiResponse:
        """Testa conectividade TCP com a placa."""
        try:
            self._get_client()
            return ApiResponse(success=True, data="OK")
        except Exception as e:
            logger.error(f"[{self.ip}] healthcheck falhou: {e}")
            return ApiResponse(success=False, error=str(e))

    def restart(self) -> ApiResponse:
        """Desliga todos os relés (estado seguro). Apenas para placas de saída."""
        if self.hardware_kind != "output":
            return ApiResponse(success=False, error="Reinicialização não suportada para este tipo de dispositivo")
        try:
            coils = [False] * self.total_relays
            client = self._get_client()
            result = client.write_coils(0, coils, slave=self.slave_id)
            if result.isError():
                logger.error(f"[{self.ip}] Erro Modbus restart: {result}")
                return ApiResponse(success=False, error=str(result))
            return ApiResponse(success=True, data="Reiniciando")
        except (ConnectionException, OSError, ModbusIOException) as e:
            logger.error(f"[{self.ip}] restart falhou: {e}")
            self.close()
            return ApiResponse(success=False, error=str(e))

    def tare(self) -> ApiResponse:
        return ApiResponse(success=False, error="Tara não implementada para o protocolo Modbus")

    def calibrate(self, weight: float) -> ApiResponse:
        return ApiResponse(success=False, error="Calibração não implementada para o protocolo Modbus")
