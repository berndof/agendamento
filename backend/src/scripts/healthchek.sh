#!/bin/sh
#TODO load .env
HOST=localhost
PORT=9090
URL="http://${HOST}:${PORT}/healthcheck"

echo "[healthcheck] Testando URL: $URL"

# Realiza a requisição com timeout e tratamento
if curl --fail --silent --max-time 2 "$URL" > /dev/null; then
  echo "[healthcheck] ✅ Serviço disponível"
  exit 0
else
  echo "[healthcheck] ❌ Falha ao acessar ${URL}"
  exit 1
fi