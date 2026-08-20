#!/bin/bash
set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${CYAN}✦ Construyendo releases de Alenia Porter...${NC}"

DIST_DIR="dist"
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

build_target() {
    local GOOS=$1
    local GOARCH=$2
    local TARGET_NAME="porter-${GOOS}-${GOARCH}"
    local ARCHIVE_NAME="${TARGET_NAME}.tar.gz"
    local BUILD_DIR="${DIST_DIR}/${TARGET_NAME}"

    echo -e "Construyendo para ${GOOS}/${GOARCH}..."

    # Crear estructura temporal
    mkdir -p "${BUILD_DIR}"
    
    # Compilar el binario de Go
    GOOS=$GOOS GOARCH=$GOARCH go build -o "${BUILD_DIR}/porter" ./cmd/ap

    # Copiar la carpeta src y legacy (Python e IDE)
    cp -r src "${BUILD_DIR}/"
    cp -r legacy "${BUILD_DIR}/"

    # Comprimir en tar.gz
    tar -czf "${DIST_DIR}/${ARCHIVE_NAME}" -C "${DIST_DIR}" "${TARGET_NAME}"

    # Limpiar directorio temporal
    rm -rf "${BUILD_DIR}"

    echo -e "${GREEN}✔ Creado: ${DIST_DIR}/${ARCHIVE_NAME}${NC}"
}

# Mac (Apple Silicon)
build_target "darwin" "arm64"
# Mac (Intel)
build_target "darwin" "amd64"
# Linux (Intel/AMD)
build_target "linux" "amd64"

echo -e "${GREEN}✦ ¡Todas las releases han sido construidas en la carpeta '${DIST_DIR}/'!${NC}"
