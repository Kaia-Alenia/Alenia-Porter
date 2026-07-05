# Contribuir a Alenia Porter

¡Gracias por tu interés en contribuir a Alenia Porter! Este es un proyecto open-source diseñado para la comunidad de desarrolladores indie y estamos felices de recibir tus aportes.

## Cómo empezar
1. Haz un fork de este repositorio.
2. Clona tu fork localmente: `git clone https://github.com/TU-USUARIO/alenia-porter.git`
3. Instala las dependencias y crea tu entorno local (preferimos `uv`).
4. Haz tus cambios en una rama descriptiva: `git checkout -b fix/mi-mejora` o `git checkout -b feat/nueva-funcion`

## Estructura del Código
- **`src/alenia_porter/media_engine.py`**: El motor puro que envuelve a FFmpeg y maneja el procesamiento de los medios, Smart Caching y Aceleración por Hardware.
- **`src/alenia_porter/porter.py`**: Lógica secundaria, utilidades y telemetría.
- **`src/alenia_porter/cli.py`**: El punto de entrada para la GUI (Tkinter) de la aplicación.
- **`cmd/ap/main.go`**: La envoltura CLI escrita en Go para ejecución ultra-rápida en terminal.

## Reglas de Contribución
- **Seguridad primero**: Asegúrate de que tu código no introduce vulnerabilidades. Usamos Snyk en nuestro CI/CD.
- **Testing**: Todo PR importante debe incluir pruebas (pytest).
- **Formato**: Ejecuta linter y mantén la consistencia visual del código.
- **Compatibilidad**: La herramienta debe poder correr en Windows, Linux y macOS sin problemas.

## Enviar un Pull Request
- Detalla los cambios que has realizado en la descripción de tu PR.
- Asegúrate de que las GitHub Actions (build y snyk) pasan exitosamente.
- Un mantenedor de Alenia Studios revisará y fusionará tu código.

¡Gracias por apoyar el ecosistema indie!
