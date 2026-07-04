#!/bin/bash
set -e

echo "Buscando actualizaciones de Alenia Porter CLI..."

git fetch origin main > /dev/null 2>&1 || true

LOCAL=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
REMOTE=$(git rev-parse origin/main 2>/dev/null || echo "unknown")

if [ "$LOCAL" != "unknown" ]; then
    BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
    if [ "$BEHIND" -eq 0 ]; then
        echo "Ya tienes la última versión instalada (o tienes cambios locales)."
        exit 0
    fi
fi

echo "Actualizando código..."
git pull origin main || echo "No se pudo hacer git pull, pero se intentará compilar."

echo "Compilando nueva versión..."
go build -o /tmp/porter_new ./cmd/ap
if [ -d "$HOME/.local/share/porter" ]; then
    rm -f "$HOME/.local/share/porter/porter"
    cp -a /tmp/porter_new "$HOME/.local/share/porter/porter"
fi
if [ -d "$HOME/.alenia-porter" ]; then
    rm -f "$HOME/.alenia-porter/porter"
    cp -a /tmp/porter_new "$HOME/.alenia-porter/porter"
fi
cp -a /tmp/porter_new ./porter
rm -f /tmp/porter_new

echo "¡Actualización completa! Por favor, sal (/exit) y reinicia Porter."
