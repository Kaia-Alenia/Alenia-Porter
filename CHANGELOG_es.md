# Changelog

## [6.8.0] - Proyecto Principal
### Corregido
- **Crítico: crash de encoders de GPU (código de retorno 255 de FFmpeg)** — Los encoders de hardware (`h264_nvenc`, `h264_qsv`, `h264_amf`, `vp9_nvenc`, `vp9_qsv`) ahora se verifican con un frame de prueba real antes de ser seleccionados. En sistemas sin GPU NVIDIA/CUDA compatible, el motor cae correctamente a encoders de software (`libx264`, `libvpx-vp9`) en lugar de fallar con crash.
- **Conversión de video a GIF rota** — El reintento en modo seguro (activado tras un fallo de FFmpeg) insertaba incorrectamente `-hwaccel none` antes del pipeline `filter_complex` de paleta del GIF, haciendo que el reintento también fallara. El encoder GIF ahora está excluido de la inyección del flag de aceleración por hardware.
- **Modo seguro siempre usa encoders de software** — Cuando el modo seguro está activo, se usan directamente `libx264` y `libvpx-vp9` para MP4 y WebM, sin consultar encoders de hardware.
- Corregido error de compilación en `App.tsx` causado por una función `startBatchQueueProcessing` malformada tras una refactorización previa.

## [1.8.0] - CLI
### Corregido
- Verificado el paso correcto de argumentos desde `startEngineCmd` (Go) hacia `headless.py` (motor Python) — los flags `--vformat`, `--aformat`, `--iformat`, `--vextra`, `--aextra`, `--iextra` se reenvían correctamente.
- El modo no interactivo `porter optimize` funciona correctamente de extremo a extremo tras el fix del motor.

---

## [6.6.0] - Proyecto Principal
### Corregido
- Se corrigió el script de actualización automática (`update.sh`) en Linux para evitar errores de "archivo ocupado" al reemplazar el binario.
- Se mejoró la lógica de auto-actualización en el CLI `ap` para extraer correctamente `.tar.gz` y `.zip`.
- Se corrigió el flujo del botón de actualización en la interfaz web para descargar correctamente el binario.
- Se agregaron comandos de instalación con PowerShell para usuarios de Windows en `docs/index.html`.
- Se agregó un nuevo script escáner avanzado para i18n (`tools/i18n_check.py`).
- Corrección de errores de compilación en el frontend por traducciones anidadas.

## [1.8.0] - CLI
### Corregido
- Resolución de bugs generales y mejoras de estabilidad.
- Correcciones menores en el manejo de FFmpeg.

---

## [6.4.0] - Proyecto Principal
### Corregido
- Mejoras generales y optimización en las rutas de código.

## [1.5.0] - CLI
### Corregido
- Mejoras generales y optimización en la interfaz por consola.
