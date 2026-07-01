#!/bin/bash
set -e

# ===========================
# Configurações
# ===========================
APP_DIR="$HOME/sals"
BACK_CONTAINER_NAME="api"

# ===========================
# Passo 1: Atualiza código do Git
# ===========================
echo "Atualizando código do Git..."
cd $APP_DIR
git reset --hard
git clean -fd
git pull origin main

# ===========================
# Passo 2: Atualiza backend
# ===========================
echo "Atualizando backend..."
docker compose up -d --build $BACK_CONTAINER_NAME

# ===========================
# Passo 3: Recarrega Nginx
# ===========================
echo "Recarregando Nginx..."
sudo nginx -t
sudo systemctl reload nginx

echo "Deploy completo concluído!"
