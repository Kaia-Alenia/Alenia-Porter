#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "          🚀 Installing Alenia Porter CLI...            "
echo "=========================================================="

# Configuración de rutas
REPO_URL="https://github.com/Kaia-Alenia/Alenia-Porter.git"
INSTALL_DIR="$HOME/.alenia-porter"
BIN_DIR="$HOME/.local/bin"

# 1. Verificar dependencias del sistema
echo "[1/4] Verificando dependencias necesarias..."
command -v python3 >/dev/null 2>&1 || { echo >&2 "❌ Python3 no está instalado. Instálalo para continuar."; exit 1; }
command -v ffmpeg >/dev/null 2>&1 || { echo >&2 "❌ FFmpeg no está instalado. Instálalo para continuar."; exit 1; }
command -v git >/dev/null 2>&1 || { echo >&2 "❌ Git no está instalado. Instálalo para continuar."; exit 1; }
command -v go >/dev/null 2>&1 || { echo >&2 "❌ Go no está instalado (Necesario para compilar)."; exit 1; }
echo "✅ Dependencias correctas (Python3, FFmpeg, Git, Go)."

# 2. Descargar o actualizar el código
echo "[2/4] Obteniendo el código más reciente desde GitHub..."
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Actualizando instalación existente..."
    cd "$INSTALL_DIR" && git pull origin main
else
    echo "Clonando repositorio..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# 3. Compilar la herramienta CLI
echo "[3/4] Construyendo el motor principal de Porter..."
cd "$INSTALL_DIR"
go build -o porter cmd/ap/main.go

# 4. Configurar el acceso global
echo "[4/4] Configurando el comando global 'porter'..."
mkdir -p "$BIN_DIR"
ln -sf "$INSTALL_DIR/porter" "$BIN_DIR/porter"

# Asegurar que .local/bin esté en el PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "⚠️ Advertencia: $BIN_DIR no está en tu PATH."
    echo "Agrega la siguiente línea a tu archivo ~/.bashrc o ~/.zshrc:"
    echo "export PATH=\"\$PATH:$BIN_DIR\""
fi

echo "=========================================================="
echo " ✨ ¡Instalación Completa! ✨"
echo " Ahora puedes escribir 'porter' en cualquier terminal."
echo "=========================================================="
