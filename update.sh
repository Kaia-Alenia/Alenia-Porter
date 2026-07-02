#!/bin/bash
set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${CYAN}✦ Actualizando Alenia Porter CLI...${NC}"

git pull origin main || echo "No se pudo hacer git pull, pero se recompilará el ejecutable."

go build -o porter cmd/ap/main.go

echo -e "${GREEN}✔ ¡Actualización completa! Por favor, reinicia Porter.${NC}"
