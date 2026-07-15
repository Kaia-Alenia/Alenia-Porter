#!/bin/bash
# Alenia Porter - update script (binary release)
# Used by the CLI /update command when installed from a release package.
set -e

OS="$(uname -s)"
if [ "$OS" = "Linux" ]; then
    ARCHIVE="AleniaPorter-Linux.tar.gz"
elif [ "$OS" = "Darwin" ]; then
    ARCHIVE="AleniaPorter-macOS.zip"
else
    echo "Sistema operativo no soportado: $OS"
    exit 1
fi

echo "Buscando la última versión de Alenia Porter..."
URL="https://github.com/Kaia-Alenia/Alenia-Porter/releases/latest/download/${ARCHIVE}"

if command -v curl &> /dev/null; then
    curl -L "$URL" -o "/tmp/${ARCHIVE}"
elif command -v wget &> /dev/null; then
    wget -q --show-progress "$URL" -O "/tmp/${ARCHIVE}"
else
    echo "Error: se necesita curl o wget para descargar la actualización."
    exit 1
fi

rm -rf "/tmp/porter_update_temp"
mkdir -p "/tmp/porter_update_temp"

if [ "$OS" = "Linux" ]; then
    tar -xzf "/tmp/${ARCHIVE}" -C "/tmp/porter_update_temp"
else
    unzip -o "/tmp/${ARCHIVE}" -d "/tmp/porter_update_temp"
fi

EXTRACTED_DIR="/tmp/porter_update_temp"
INNER_DIR=$(ls -d /tmp/porter_update_temp/*/ 2>/dev/null | head -n 1 || true)
if [ -n "$INNER_DIR" ]; then
    EXTRACTED_DIR="$INNER_DIR"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Instalando en $SCRIPT_DIR ..."
rm -f "$SCRIPT_DIR/porter" "$SCRIPT_DIR/ap" "$SCRIPT_DIR/AleniaPorter" "$SCRIPT_DIR/AleniaPorter.exe"
cp -a "$EXTRACTED_DIR/." "$SCRIPT_DIR/"
chmod +x "$SCRIPT_DIR/AleniaPorter" "$SCRIPT_DIR/porter" "$SCRIPT_DIR/launch.sh" 2>/dev/null || true

# Si hay instalación en ~/.local/share/porter también actualizamos
if [ -d "$HOME/.local/share/porter" ]; then
    rm -f "$HOME/.local/share/porter/porter"
    cp -a "$EXTRACTED_DIR/." "$HOME/.local/share/porter/"
    chmod +x "$HOME/.local/share/porter/porter" "$HOME/.local/share/porter/AleniaPorter" 2>/dev/null || true
fi

rm -rf "/tmp/${ARCHIVE}" "/tmp/porter_update_temp"
echo "¡Actualización completa! Por favor, sal (/exit) y reinicia Porter."
