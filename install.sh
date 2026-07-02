#!/bin/bash
set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${CYAN}✦ Instalando Alenia Porter CLI...${NC}"

INSTALL_DIR="$HOME/.local/share/porter"
BIN_DIR="$HOME/.local/bin"

mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

echo "Copiando archivos a $INSTALL_DIR..."
cp -a . "$INSTALL_DIR"

echo "Compilando ejecutable de Go..."
cd "$INSTALL_DIR"
go build -o porter ./cmd/ap

if ! command -v ffmpeg &> /dev/null; then
    echo "Descargando binarios estáticos de FFmpeg..."
    wget -q https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -O /tmp/ffmpeg.tar.xz
    tar -xf /tmp/ffmpeg.tar.xz -C /tmp
    mv /tmp/ffmpeg-*-static/ffmpeg "$BIN_DIR/"
    mv /tmp/ffmpeg-*-static/ffprobe "$BIN_DIR/"
    rm -rf /tmp/ffmpeg.tar.xz /tmp/ffmpeg-*-static
    echo -e "${GREEN}FFmpeg instalado correctamente en $BIN_DIR.${NC}"
else
    echo "FFmpeg ya está instalado en el sistema."
fi

ln -sf "$INSTALL_DIR/porter" "$BIN_DIR/porter"

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${CYAN}Nota: Agrega $BIN_DIR a tu PATH en ~/.bashrc o ~/.zshrc${NC}"
    echo 'export PATH="$HOME/.local/bin:$PATH"'
fi

echo -e "${GREEN}✔ ¡Instalación completa!${NC}"
echo -e "Puedes ejecutar el CLI desde cualquier lugar escribiendo: ${CYAN}porter${NC}"
