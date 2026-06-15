from pymodbus.client import ModbusTcpClient
import time

IP = "192.168.60.99"
PORT = 502
SLAVE_ID = 0


def ler_peso():
    client = ModbusTcpClient(IP, port=PORT)

    if not client.connect():
        print("Erro conexão")
        return None

    try:
        result = client.read_holding_registers(0, count=2, slave=SLAVE_ID)

        if result.isError():
            print("Erro Modbus:", result)
            return None

        r0, r1 = result.registers

        # ✅ MODO CORRETO IDENTIFICADO
        valor = (r1 << 16) + r0

        # tratar sinal (int32)
        if valor > 2147483647:
            valor -= 4294967296

        # escala
        peso = valor / 100.0

        return peso

    finally:
        client.close()


if __name__ == "__main__":
    while True:
        peso = ler_peso()

        if peso is not None:
            print(f"Peso: {peso:.2f} kg")
        else:
            print("Falha leitura")

        time.sleep(0.4)