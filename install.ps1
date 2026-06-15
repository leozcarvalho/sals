#Requires -Version 5.1
<#
.SYNOPSIS
    Instalador do sistema SALS para Windows.
.DESCRIPTION
    Verifica pre-requisitos (Git e Docker Desktop), clona o repositorio,
    configura o ambiente e sobe os containers via Docker Compose.
.EXAMPLE
    .\install.ps1
    .\install.ps1 -InstallPath "D:\sals"
#>

param(
    [string]$InstallPath = "C:\sals"
)

$REPO_URL = "https://github.com/leozcarvalho/sals.git"
$ErrorActionPreference = "Stop"

function Write-Header {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Instalador SALS" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Message)
    Write-Host "[*] $Message" -ForegroundColor Yellow
}

function Write-Ok {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Fail {
    param([string]$Message)
    Write-Host "[ERRO] $Message" -ForegroundColor Red
}

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

# ── Pre-requisitos ────────────────────────────────────────────────────────────

function Assert-Git {
    Write-Step "Verificando Git..."
    if (Test-Command "git") {
        $v = git --version
        Write-Ok "Git encontrado: $v"
        return
    }
    Write-Fail "Git nao encontrado."
    Write-Host ""
    Write-Host "Instale o Git por um dos metodos abaixo e execute este script novamente:" -ForegroundColor White
    Write-Host "  1) winget install Git.Git" -ForegroundColor Cyan
    Write-Host "  2) Baixe em: https://git-scm.com/download/win" -ForegroundColor Cyan
    exit 1
}

function Assert-Docker {
    Write-Step "Verificando Docker Desktop..."
    if (-not (Test-Command "docker")) {
        Write-Fail "Docker Desktop nao encontrado."
        Write-Host ""
        Write-Host "Instale o Docker Desktop e execute este script novamente:" -ForegroundColor White
        Write-Host "  https://www.docker.com/products/docker-desktop/" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Apos instalar, certifique-se de que o Docker Desktop esta rodando." -ForegroundColor White
        exit 1
    }

    # Verifica se o daemon esta respondendo
    $dockerRunning = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "Docker Desktop esta instalado mas nao esta rodando."
        Write-Host "Abra o Docker Desktop e aguarde ele inicializar, depois execute este script novamente." -ForegroundColor White
        exit 1
    }

    $v = docker --version
    Write-Ok "Docker encontrado: $v"
}

# ── Clone ─────────────────────────────────────────────────────────────────────

function Clone-Repo {
    Write-Step "Clonando repositorio em '$InstallPath'..."

    if (Test-Path $InstallPath) {
        $existing = Get-ChildItem $InstallPath -ErrorAction SilentlyContinue
        if ($existing) {
            Write-Host ""
            $resp = Read-Host "  O diretorio '$InstallPath' ja existe e nao esta vazio. Deseja apagar e recloner? (s/N)"
            if ($resp -match "^[sS]$") {
                Remove-Item $InstallPath -Recurse -Force
            } else {
                Write-Ok "Usando diretorio existente."
                return
            }
        }
    }

    git clone $REPO_URL $InstallPath
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "Falha ao clonar o repositorio."
        exit 1
    }
    Write-Ok "Repositorio clonado com sucesso."
}

# ── Ambiente ─────────────────────────────────────────────────────────────────

function Setup-Env {
    $envPath = Join-Path $InstallPath "api\.env"

    if (Test-Path $envPath) {
        Write-Ok "Arquivo .env ja existe, mantendo configuracao atual."
        return
    }

    Write-Step "Criando arquivo de configuracao api\.env..."

    $secretKey = [System.Convert]::ToBase64String((1..32 | ForEach-Object { [byte](Get-Random -Max 256) }))

    $envContent = @"
DATABASE_URL=sqlite:///./data/db.sqlite
DEBUG=False
SECRET_KEY=$secretKey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
ENVIRONMENT=production
"@

    Set-Content -Path $envPath -Value $envContent -Encoding UTF8
    Write-Ok "Arquivo .env criado."
}

function Ensure-DataDir {
    $dataDir = Join-Path $InstallPath "api\data"
    if (-not (Test-Path $dataDir)) {
        New-Item -ItemType Directory -Path $dataDir | Out-Null
        Write-Ok "Diretorio api\data criado."
    }
}

# ── Docker Compose ────────────────────────────────────────────────────────────

function Start-Containers {
    Write-Step "Construindo e subindo os containers (pode demorar na primeira vez)..."

    Push-Location $InstallPath
    try {
        docker compose -f docker-compose.windows.yml up -d --build
        if ($LASTEXITCODE -ne 0) {
            Write-Fail "Falha ao subir os containers."
            exit 1
        }
    } finally {
        Pop-Location
    }

    Write-Ok "Containers rodando."
}

# ── Status ────────────────────────────────────────────────────────────────────

function Show-Status {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   SALS instalado com sucesso!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Acesse o sistema pelo navegador:" -ForegroundColor White
    Write-Host "  Frontend:  http://localhost:5173" -ForegroundColor Cyan
    Write-Host "  API:       http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  API docs:  http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Comandos uteis:" -ForegroundColor White
    Write-Host "  Parar:     docker compose -f docker-compose.windows.yml down" -ForegroundColor Gray
    Write-Host "  Logs API:  docker logs sals_api -f" -ForegroundColor Gray
    Write-Host "  Logs Vue:  docker logs sals_vue -f" -ForegroundColor Gray
    Write-Host ""
}

# ── Main ──────────────────────────────────────────────────────────────────────

Write-Header
Assert-Git
Assert-Docker
Clone-Repo
Setup-Env
Ensure-DataDir
Start-Containers
Show-Status
