#!/bin/bash
set -e

# ===========================
# Configurações
# ===========================
APP_DIR="$HOME/sals"
FRONT_DIR="$APP_DIR/app"
BACK_DIR="$APP_DIR/api"
BACK_CONTAINER_NAME="api"
BACK_PORT=8000

# ===========================
# Passo 1: Atualiza código do Git
# ===========================
echo "Atualizando código do Git..."
cd $APP_DIR
git reset --hard
git clean -fd
git pull origin main

# ===========================
# Passo 2: Atualiza front-end
# ===========================
echo "Atualizando front-end..."
cd $FRONT_DIR

# Se dist/ já estiver comitado, apenas recarregar Nginx
# Se quiser rebuildar no servidor, descomente:
# npm install
# npm run build

# ===========================
# Passo 3: Atualiza backend
# ===========================
echo "Atualizando backend..."
cd $BACK_DIR

# Para Docker:
# Para parar container antigo, se existir
if [ "$(docker ps -q -f name=$BACK_CONTAINER_NAME)" ]; then
    echo "Parando container antigo..."
    docker stop $BACK_CONTAINER_NAME
    docker rm $BACK_CONTAINER_NAME
fi

# Build e run do container
echo "Subindo container backend..."
docker run -d \
    --name $BACK_CONTAINER_NAME \
    -p $BACK_PORT:8000 \
    -v $BACK_DIR:/api \
    -w /api \
    python:3.11 \
    bash -c "pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir python-multipart && uvicorn main:app --host 0.0.0.0 --port 8000"

# ===========================
# Passo 4: Recarrega Nginx
# ===========================
echo "Recarregando Nginx..."
sudo nginx -t
sudo systemctl reload nginx

echo "Deploy completo concluído!"
