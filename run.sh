#!/bin/bash

# Ativar o ambiente virtual, se existir
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

case "$1" in
  server)
    echo "🚀 Iniciando servidor FastAPI..."
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ;;
  
  revision)
    if [ -z "$2" ]; then
      echo "❌ Informe uma mensagem para a revisão"
      echo "👉 Exemplo: ./run.sh revision 'minha_migration'"
      exit 1
    fi
    echo "📦 Criando revisão Alembic: $2"
    alembic revision --autogenerate -m "$2"
    ;;
  
  upgrade)
    echo "⬆️  Rodando upgrade no banco..."
    alembic upgrade head
    ;;
  
  downgrade)
    if [ -z "$2" ]; then
      echo "❌ Informe uma versão para dar downgrade"
      echo "👉 Exemplo: ./run.sh downgrade -1"
      exit 1
    fi
    echo "⬇️  Fazendo downgrade para $2"
    alembic downgrade "$2"
    ;;

  *)
    echo "Uso: ./run.sh {server|revision <msg>|upgrade|downgrade <rev>}"
    exit 1
    ;;
esac
