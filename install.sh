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

# Detectar OS y Arquitectura
OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"
if [ "$ARCH" = "x86_64" ]; then
    ARCH="amd64"
elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    ARCH="arm64"
fi

if [ "$OS" != "linux" ] && [ "$OS" != "darwin" ]; then
    echo "Sistema operativo no soportado: $OS"
    exit 1
fi

TARGET_DIR="AleniaPorter"
if [ "$OS" = "linux" ]; then
    ARCHIVE="AleniaPorter-Linux.tar.gz"
else
    ARCHIVE="AleniaPorter-macOS.zip"
fi

REPO_URL="https://github.com/Kaia-Alenia/Alenia-Porter"
DOWNLOAD_URL="${REPO_URL}/releases/latest/download/${ARCHIVE}"

echo "Descargando Alenia Porter para ${OS}-${ARCH}..."
if command -v curl &> /dev/null; then
    curl -L "$DOWNLOAD_URL" -o "/tmp/${ARCHIVE}"
elif command -v wget &> /dev/null; then
    wget -q --show-progress "$DOWNLOAD_URL" -O "/tmp/${ARCHIVE}"
else
    echo "Error: Se requiere 'curl' o 'wget' para descargar la aplicación."
    exit 1
fi

echo "Extrayendo archivos en $INSTALL_DIR..."
if [ "$OS" = "linux" ]; then
    tar -xzf "/tmp/${ARCHIVE}" -C "/tmp"
else
    unzip -q -o "/tmp/${ARCHIVE}" -d "/tmp"
fi

# Copia el contenido de la carpeta descomprimida al directorio de instalación
cp -a "/tmp/${TARGET_DIR}/." "$INSTALL_DIR/"

# Limpiar temporales
rm -rf "/tmp/${ARCHIVE}" "/tmp/${TARGET_DIR}"

# Asegurar que sea ejecutable
chmod +x "$INSTALL_DIR/porter"

if ! command -v ffmpeg &> /dev/null; then
    if [ "$OS" = "linux" ]; then
        echo "Descargando binarios estáticos de FFmpeg para Linux..."
        wget -q https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -O /tmp/ffmpeg.tar.xz
        tar -xf /tmp/ffmpeg.tar.xz -C /tmp
        mv /tmp/ffmpeg-*-static/ffmpeg "$BIN_DIR/"
        mv /tmp/ffmpeg-*-static/ffprobe "$BIN_DIR/"
        rm -rf /tmp/ffmpeg.tar.xz /tmp/ffmpeg-*-static
        echo -e "${GREEN}FFmpeg instalado correctamente en $BIN_DIR.${NC}"
    elif [ "$OS" = "darwin" ]; then
        echo -e "${CYAN}FFmpeg no encontrado. Se recomienda instalarlo usando Homebrew: brew install ffmpeg${NC}"
    fi
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
