#!/bin/bash
# Alenia Porter - launcher script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Intentar ejecutable nativo
if "$SCRIPT_DIR/AleniaPorter" 2>/tmp/ap_err; then
    exit 0
fi

# Fallback: lanzar desde código fuente (solo usa Python del sistema, NO el webview del paquete)
SOURCE_ROOTS=(
    "/media/alejandro/D/tool/porter"
    "$HOME/.local/share/porter-src"
)
for SRC in "${SOURCE_ROOTS[@]}"; do
    SRCPY="$SRC/src"
    if [ -d "$SRCPY/alenia_porter" ] && [ -f "$SRC/src/alenia_porter/gui_web.py" ]; then
        exec python3 "$SRC/src/alenia_porter/gui_web.py"
    fi
done

cat /tmp/ap_err >&2
echo "No se pudo iniciar. Instala python3-gi y gir1.2-webkit2-4.1 o lanza desde el código fuente." >&2
exit 1
