# SALS — Sistema de Automação para Alimentação de Suínos

Sistema de automação e controle de alimentação de suínos, desenvolvido para gerenciar a produção de ração líquida (papa), o acionamento de válvulas via hardware Modbus e o acompanhamento de lotes por curva de alimentação.

## Funcionalidades

- **Cozinhas e tanques** — cadastro de cozinhas de ração com tanques de insumos (água, milho, soja, sorgo, premix etc.)
- **Galpões, salas e baias** — estrutura hierárquica completa da granja
- **Lotes e curvas de alimentação** — acompanhamento dia a dia do peso e do consumo de ração por animal, baseado em curvas nutricionais configuráveis
- **Fórmulas** — receitas com percentuais de cada ingrediente por fase (alojamento, crescimento, terminação)
- **Tratos** — agendamento de horários de alimentação com percentual de ração por trato
- **Automação via Modbus TCP** — acionamento de placas de relés (dosadores) e leitura de sensores de peso via protocolo Modbus
- **Instalações** — mapeamento de dispositivos físicos (endereço IP, tipo, canais)
- **Gestão de usuários e perfis** — controle de acesso por permissões (Admin, Engenharia, Supervisor)

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Frontend | Vue 3 + Vite + PWA |
| Backend | FastAPI + SQLModel + Alembic |
| Banco de dados | SQLite |
| Hardware | Modbus TCP (pymodbus) |
| Infraestrutura | Docker Compose |

---

## Instalação

### Pré-requisitos

- [Git](https://git-scm.com/download/win)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Linux / macOS

```bash
git clone https://github.com/leozcarvalho/sals.git
cd sals
docker compose up -d --build
```

### Windows

Execute o PowerShell como **Administrador** e rode:

```powershell
# Habilitar execução de scripts (apenas na primeira vez)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Baixar e executar o instalador
Invoke-WebRequest https://raw.githubusercontent.com/leozcarvalho/sals/main/install.ps1 -OutFile install.ps1
.\install.ps1
```

O script verifica os pré-requisitos, clona o repositório em `C:\sals`, configura o ambiente e sobe os containers automaticamente.

Para instalar em outro diretório:

```powershell
.\install.ps1 -InstallPath "D:\sals"
```

---

## Acessando o sistema

Após subir os containers:

| Serviço | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000 |
| Documentação da API | http://localhost:8000/docs |

Login padrão após rodar o seed:

| Campo | Valor |
|-------|-------|
| E-mail | `sals@admin.com` |
| Senha | `123456` |

---

## Configuração (`api/.env`)

O arquivo `api/.env` é criado automaticamente pelo instalador. Para ajuste manual:

```env
DATABASE_URL=sqlite:///./data/db.sqlite
DEBUG=False
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
ENVIRONMENT=production
```

---

## Comandos úteis

```bash
# Subir os containers
docker compose up -d --build

# Parar os containers
docker compose down

# Ver logs da API
docker logs api -f

# Ver logs do frontend
docker logs vue -f

# Popular o banco com dados iniciais
docker exec api python -m src.scripts.seed

# Criar uma migration
docker exec api alembic revision --autogenerate -m "descricao"

# Aplicar migrations
docker exec api alembic upgrade head
```

No Windows, substitua `docker compose` por `docker compose -f docker-compose.windows.yml`.
