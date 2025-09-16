#!/bin/bash

case "$1" in
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
  seed)
    echo "🌱 Populando o banco de dados com dados iniciais..."
    docker compose run --rm api python -m src.scripts.seed
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
  script)
    if [ -z "$2" ]; then
      echo "❌ Informe o caminho do script"
      echo "👉 Exemplo: ./run.sh script nome.py"
      exit 1
    fi
    echo "📜 Executando script: $2"
    docker compose run --rm api python3 -m src.scripts."$2"
    ;;

  test)
    echo "🧪 Rodando testes com pytest..."
    pytest "$2"
    ;;

  coverage)
    echo "📊 Rodando coverage..."
    coverage run -m pytest "$2"
    coverage report -m
    ;;
  coverage-html)
    echo "📊 Gerando relatório HTML de coverage..."
    coverage run -m pytest "$2"
    coverage html
    echo "Relatório HTML gerado em htmlcov/index.html"
    ;;
  *)
    echo "Uso: ./run.sh {server|revision <msg>|upgrade|downgrade <rev>|test|coverage}"
    exit 1
    ;;
esac
