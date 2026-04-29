#!/bin/bash

KEY_PATH="$HOME/.ssh/id_rsa"
SERVER_USER="ubuntu"
SERVER_IP="129.80.204.85"

ACTION=$1

connect() {
  echo "Conectando ao servidor..."

  if [ "$ACTION" == "reset" ]; then
    echo "Executando RESET (seed)..."
    ssh -t -i "$KEY_PATH" "$SERVER_USER@$SERVER_IP" << 'EOF'
      cd ~/sals/api || { echo "Pasta api não encontrada"; exit 1; }
      ./run.sh script seed
EOF
  else
    echo "Executando DEPLOY..."
    ssh -t -i "$KEY_PATH" "$SERVER_USER@$SERVER_IP" << 'EOF'
      cd ~/sals || { echo "Pasta sals não encontrada"; exit 1; }
      chmod +x deploy.sh
      ./deploy.sh
EOF
  fi
}

connect