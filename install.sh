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

# Retrocompatibilidad: renombrar legacy 'ap' a 'porter' si es necesario
if [ ! -f "$INSTALL_DIR/porter" ] && [ -f "$INSTALL_DIR/ap" ]; then
    mv "$INSTALL_DIR/ap" "$INSTALL_DIR/porter"
fi

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

# Asegurar permisos ejecutables en scripts auxiliares
chmod +x "$INSTALL_DIR/update.sh" "$INSTALL_DIR/launch.sh" "$INSTALL_DIR/AleniaPorter" 2>/dev/null || true

# Crear acceso directo .desktop para el IDE (AleniaPorter)
if [ "$OS" = "linux" ] && [ -f "$INSTALL_DIR/AleniaPorter" ]; then
    DESKTOP_DIR="$HOME/.local/share/applications"
    ICONS_DIR="$HOME/.local/share/icons"
    mkdir -p "$DESKTOP_DIR" "$ICONS_DIR"

    # Copiar icono si existe
    ICON_SRC="$INSTALL_DIR/alenia_porter/assets/images/logo.png"
    ICON_ICO="$INSTALL_DIR/alenia_porter/assets/images/logo.ico"
    if [ -f "$ICON_SRC" ]; then
        cp "$ICON_SRC" "$ICONS_DIR/alenia-porter.png"
        ICON_PATH="$ICONS_DIR/alenia-porter.png"
    elif [ -f "$ICON_ICO" ]; then
        cp "$ICON_ICO" "$ICONS_DIR/alenia-porter.ico"
        ICON_PATH="$ICONS_DIR/alenia-porter.ico"
    else
        ICON_PATH="utilities-file-archiver"
    fi

    cat > "$DESKTOP_DIR/alenia-porter.desktop" << DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=Alenia Porter
GenericName=Audio/Video Converter
Comment=Alenia Porter v6.9 - Conversor de audio y video con IA
Exec=$INSTALL_DIR/launch.sh
Icon=$ICON_PATH
Terminal=false
Categories=AudioVideo;Audio;Video;Utility;
Keywords=audio;video;convert;porter;alenia;ffmpeg;
StartupNotify=true
StartupWMClass=AleniaPorter
DESKTOP
    chmod +x "$DESKTOP_DIR/alenia-porter.desktop"
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
    echo -e "${GREEN}✔ Acceso directo del IDE instalado en el menú de aplicaciones.${NC}"
fi

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${CYAN}Nota: Agrega $BIN_DIR a tu PATH en ~/.bashrc o ~/.zshrc${NC}"
    echo 'export PATH="$HOME/.local/bin:$PATH"'
fi

echo -e "${GREEN}✔ ¡Instalación completa!${NC}"
echo -e "Puedes ejecutar el CLI desde cualquier lugar escribiendo: ${CYAN}porter${NC}"
