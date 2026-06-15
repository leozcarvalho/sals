import socket
import time
import random

IP3 = "192.168.60.95"
IP2 = "192.168.60.96"
IP1 = "192.168.60.97"
PLACAS = [IP1, IP2, IP3]
PORT = 502
TOTAL_RELES = 30

def enviar_frame(ip, frame, descricao=""):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)  # menor para não travar

        print(f"[{ip}] {descricao} -> conectando...")
        s.connect((ip, PORT))

        s.send(frame)

        try:
            resp = s.recv(1024)
            print(f"[{ip}] OK:", list(resp))
        except:
            print(f"[{ip}] Sem resposta")

        s.close()
        return True

    except Exception as e:
        print(f"[{ip}] ERRO:", str(e))
        return False

def teste_varredura_reles(ip, total=30, delay=0.5):
    print("Iniciando varredura de reles...")

    for i in range(total):
        print(f"Ligando rele {i}")
        ligar_rele(ip, i)
        time.sleep(delay)

        print(f"Desligando rele {i}")
        desligar_rele(ip, i)
        time.sleep(delay)

    print("Varredura finalizada.")

def teste_randomico():
    print("=== TESTE RANDOMICO INICIADO ===")
    
    desligar_todos_reles(IP1)
    desligar_todos_reles(IP2)
    desligar_todos_reles(IP3)

    while True:
        ip = random.choice(PLACAS)
        rele = random.randint(0, TOTAL_RELES - 1)
        acao = random.choice(["ligar", "desligar"])

        if acao == "ligar":
            ligar_rele(ip, rele)
        else:
            desligar_rele(ip, rele)

        # intervalo aleatorio entre ações
        delay = random.uniform(0.1, 1.0)
        time.sleep(delay)


def setar_reles_ativos(ip, reles_ativos, total=30):
    byte_count = (total + 7) // 8
    data_bytes = [0x00] * byte_count

    for r in reles_ativos:
        if 0 <= r < total:
            byte_index = r // 8
            bit_index = r % 8
            data_bytes[byte_index] |= (1 << bit_index)

    frame = [
        0x00, 0x20,
        0x00, 0x00,
        0x00, 7 + byte_count,
        0x01,
        0x0F,
        0x00, 0x00,
        0x00, total,
        byte_count,
        *data_bytes
    ]

    enviar_frame(ip, frame, f"Setar ativos {reles_ativos}")

def desligar_todos_reles(ip, total=30):
    byte_count = (total + 7) // 8
    data_bytes = [0x00] * byte_count

    frame = [
        0x00, 0x10,
        0x00, 0x00,
        0x00, 7 + byte_count,
        0x01,
        0x0F,
        0x00, 0x00,
        0x00, total,
        byte_count,
        *data_bytes
    ]

    frame = bytes(frame)

    enviar_frame(ip, frame, "Desligar todos")

def ligar_rele(ip, rele=0):
    frame = bytes([
        0x00, 0x01,
        0x00, 0x00,
        0x00, 0x06,
        0x01,
        0x05,
        0x00, rele,
        0xFF, 0x00
    ])

    enviar_frame(ip, frame, f"Ligar rele {rele}")

def desligar_rele(ip, rele=0):
    frame = bytes([
        0x00, 0x02,
        0x00, 0x00,
        0x00, 0x06,
        0x01,
        0x05,
        0x00, rele,
        0x00, 0x00
    ])

    enviar_frame(ip, frame, f"Desligar rele {rele}")

if __name__ == "__main__":

#    ligar_rele(IP1, 0)
#    ligar_rele(IP2, 29)
#    teste_varredura_reles(IP3)

#    time.sleep(1.0)

#    desligar_todos_reles(IP1)
#    desligar_todos_reles(IP2)

#    time.sleep(1.0)

#    ligar_rele(IP1, 0)
#    ligar_rele(IP2, 1)
#    ligar_rele(IP1, 2)
#    ligar_rele(IP2, 29)

#    time.sleep(1.0)

#    setar_reles_ativos(IP1, [1, 6, 11, 20])
#    setar_reles_ativos(IP2, [0, 9, 19, 29])

#    time.sleep(1.0)

#    desligar_todos_reles(IP1)
#    desligar_todos_reles(IP2)

#    time.sleep(1.0)

    teste_varredura_reles(IP1)
        
#    teste_randomico()