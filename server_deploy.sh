#!/bin/bash
set -e

APP_DIR="$HOME/sals"
FRONT_DIR="$APP_DIR/app"

echo ""
echo "========================================"
echo " DEPLOY PRODUCAO - SALS"
echo "========================================"
echo ""

# === 1. Atualiza codigo ===
echo "[1/4] Atualizando codigo do Git..."
cd "$APP_DIR"
git pull origin main

# === 2. Build do frontend ===
echo ""
echo "[2/4] Buildando frontend Vue..."
cd "$FRONT_DIR"
npm ci --silent
npm run build

# === 3. Rebuild e restart da API ===
echo ""
echo "[3/4] Rebuilding e subindo API..."
cd "$APP_DIR"
docker compose build api
docker compose up -d api

# Aguarda o container estar saudavel
echo "Aguardando API iniciar..."
sleep 3
if ! docker ps --filter "name=sals_api" --filter "status=running" | grep -q sals_api; then
    echo "ERRO: Container sals_api nao subiu. Logs:"
    docker logs sals_api --tail 30
    exit 1
fi

# === 4. Nginx ===
echo ""
echo "[4/4] Recarregando Nginx..."
sudo nginx -t
sudo systemctl reload nginx

echo ""
echo "========================================"
echo " Deploy concluido com sucesso!"
echo "========================================"
