# Alenia Porter v5.9 🐧

[![Build Status](https://github.com/Kaia-Alenia/Alenia-Porter/actions/workflows/build.yml/badge.svg)](https://github.com/Kaia-Alenia/Alenia-Porter/actions/workflows/build.yml)
[![Pages Deploy](https://github.com/Kaia-Alenia/Alenia-Porter/actions/workflows/pages.yml/badge.svg)](https://github.com/Kaia-Alenia/Alenia-Porter/actions/workflows/pages.yml)
[![GitHub release](https://img.shields.io/github/v/release/Kaia-Alenia/Alenia-Porter?include_prereleases&color=accent)](https://github.com/Kaia-Alenia/Alenia-Porter/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Optimizador multimedia universal de alto rendimiento.**

Alenia Porter es una herramienta profesional, multiplataforma y autónoma diseñada para automatizar la optimización, compresión y preparación de recursos multimedia (imágenes, video y audio).

## Expansión Universal: De Motores de Juegos a Propósito General

En sus inicios, Alenia Porter fue diseñado como un optimizador de recursos exclusivo para motores de videojuegos como Ren'Py y Godot. A partir de esta versión, la herramienta ha evolucionado para convertirse en un **optimizador multimedia de propósito general**. 

### ¿Por qué esta transición?
- **Independencia de Motores:** La lógica anterior generaba archivos de configuración restrictivos (como `audio_defines.rpy` y `video_defines.rpy` en Ren'Py) que podían corromper proyectos en conversiones masivas. Ahora delegamos la indexación de recursos de manera nativa al motor de juego o framework que utilices, haciéndolo compatible con cualquier entorno.
- **Público Objetivo Ampliado:** Al ser de código abierto bajo la licencia GPL v3, expandimos el alcance para músicos, editores de video, desarrolladores web y creadores de contenido que requieren compresión ultra rápida a formatos de alta fidelidad como OGG, OPUS, WEBM y WEBP sin pérdida apreciable de calidad y sin configurar pipelines complejos.

## Cómo funciona y qué hace

Alenia Porter actúa como un orquestador local sobre herramientas de procesamiento estándar de la industria (como FFmpeg). Cuando seleccionas un directorio:

1. **Escaneo Eficiente:** Explora de manera recursiva todos los archivos multimedia compatibles organizándolos por tipo (Imagen, Video y Audio).
2. **Conversión Concurrente:** Distribuye el procesamiento utilizando hilos y procesos paralelos para sortear limitaciones de hardware, forzando un control estricto de recursos (un solo hilo por instancia de codificador) para evitar la contención de CPU en equipos de gama baja.
3. **Optimización Adaptativa:**
   - **Imágenes:** Convierte y comprime imágenes a formatos modernos de alto rendimiento.
   - **Video:** Codifica secuencias de video a contenedores WebM/OGV optimizados para web y reproductores livianos.
   - **Audio:** Transcodifica pistas de audio a OGG u OPUS reduciendo drástrxamente el peso de almacenamiento final mientras preserva el espectro acústico.
4. **Resiliencia de Procesamiento:** Implementa un sistema de control de fallos y telemetría de rendimiento que genera reportes automáticos en caso de interrupciones inesperadas.

## Telemetría y Privacidad

Para medir el rendimiento de la herramienta y conocer los formatos de archivo más optimizados por la comunidad, Alenia Porter incorpora un sistema básico de telemetría asíncrona.

- **Absoluta Privacidad:** **No recopilamos información personal o sensible** (como nombres reales, contraseñas, correos, archivos procesados o datos del disco duro).
- **Datos Recopilados:** Únicamente se envía el identificador de instalación único y anónimo (UUID), el apodo legible elegido por el usuario (nickname), el tipo de sistema operativo, el modo de ejecución (GUI/CLI), la extensión del formato optimizado (ej. "mp3", "webp"), el conteo total de archivos procesados y el tiempo empleado en segundos.
- **Transparencia:** Toda la información estadística agregada es enviada de forma segura para consolidar benchmarks públicos sobre el rendimiento de la herramienta en distintas plataformas.

## Características Clave

- **Herramienta Autónoma (Zero Dependencies):** Los ejecutables empaquetados incluyen binarios internos (como FFmpeg), permitiendo que funcione sin instalar Python ni dependencias adicionales en el sistema.
- **Multiplataforma:** Total compatibilidad con Windows, macOS y Linux.
- **Temas Dinámicos:** Personalización de colores de la interfaz con múltiples temas cargados dinámicamente desde JSON.
- **Personalización de Nickname:** Generación e ingreso de nombres legibles para estadísticas de uso y telemetría, administrados desde el menú de usuario.
- **Seguridad en Integración Continua (CI/CD):** Validación estricta en GitHub Actions utilizando pruebas de humo automatizadas sobre displays virtuales (xvfb) para asegurar que ninguna versión inestable llegue a producción.

## Cómo usar

1. Ejecuta el archivo ejecutable **AleniaPorter**.
2. Personaliza tu apodo en el primer inicio para vincular tus estadísticas locales de optimización.
3. Selecciona tu formato de audio preferido (OGG u OPUS).
4. Haz clic en "Select Folder to Convert" y elige la carpeta de origen que deseas optimizar.
5. Los archivos procesados se generarán directamente respetando la estructura interna original.

## Roadmap v6.0 (Fases de Desarrollo Activo)

- **Fase 1: Limpieza y Estabilización (v5.9):** Remoción de código obsoleto e integración de pruebas automatizadas xvfb en CI/CD (Completado).
- **Fase 2: Telemetría y Datos (v6.0):** Implementación de UUID local, base de datos PostgreSQL en Render y sistema de Nicknames legibles para benchmarks de velocidad (En progreso).
- **Fase 3: Diagnóstico y Resiliencia (v6.1):** Registro de logs rotativos e implementación de "Safe Mode" si fallan los controladores gráficos.
- **Fase 4: Infraestructura y Comunidad (v6.2):** Auditoría automática con Snyk/Dependabot y automatización avanzada de empaquetado multiplataforma.
- **Fase 8: Modernización de la CLI (Migración a Go):** Creación de un orquestador híbrido escrito en Go para máxima concurrencia y despliegue rápido por terminal.
- **Fase 9: Aceleración por Hardware (GPU Encoders):** Integración y detección automática de NVENC (NVIDIA), AMF (AMD) y QuickSync (Intel) con fallback transparente a CPU.

---

**Licencia:** GNU General Public License v3 (GPL v3).
*Diseñado para ser libre, transparente y accesible para toda la comunidad de desarrolladores y creadores.*

**Correo Oficial de Alenia Studios:** contact.aleniastudios@gmail.com

**Desarrollado y traducido por Kaia-Alenia Studios**
US ES FR JP CN RU BR DE
