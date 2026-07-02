# Alenia Porter v5.9 🐧

[![Build Status](https://github.com/Kaia-Alenia/Alenia-Porter/actions/workflows/build.yml/badge.svg)](https://github.com/Kaia-Alenia/Alenia-Porter/actions/workflows/build.yml)
[![Pages Deploy](https://github.com/Kaia-Alenia/Alenia-Porter/actions/workflows/pages.yml/badge.svg)](https://github.com/Kaia-Alenia/Alenia-Porter/actions/workflows/pages.yml)
[![GitHub release](https://img.shields.io/github/v/release/Kaia-Alenia/Alenia-Porter?include_prereleases&color=accent)](https://github.com/Kaia-Alenia/Alenia-Porter/releases)
[![Downloads](https://img.shields.io/github/downloads/Kaia-Alenia/Alenia-Porter/total)](https://github.com/Kaia-Alenia/Alenia-Porter/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)](https://github.com/Kaia-Alenia/Alenia-Porter/releases)
[![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)](https://github.com/Kaia-Alenia/Alenia-Porter/releases)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)](https://github.com/Kaia-Alenia/Alenia-Porter/releases)

**High-performance universal media optimizer.**

Alenia Porter is a professional, cross-platform, standalone tool designed to automate the optimization, compression, and preparation of media assets (images, video, and audio).

## Universal Expansion: From Game Engines to General Purpose

Originally, Alenia Porter was designed as a resource optimizer dedicated exclusively to game engines such as Ren'Py and Godot. Starting with this version, the tool has transitioned into a **general-purpose media optimizer**.

### Why this transition?
- **Engine Independence:** The legacy logic generated restrictive configuration files (such as `audio_defines.rpy` and `video_defines.rpy` in Ren'Py) that corrupted destination projects during massive conversions. We now delegate asset indexing natively to whatever game engine or framework you use, making it compatible with any environment.
- **Expanded Target Audience:** Being open-source under the GPL v3 license, we expand the reach to musicians, video editors, web developers, and content creators who require ultra-fast compression to high-fidelity formats like OGG, OPUS, WEBM, and WEBP without noticeable quality loss or complex pipelines.

## How It Works and What It Does

Alenia Porter acts as a local orchestrator over industry-standard processing tools (such as FFmpeg). When you select a directory:

1. **Efficient Scanning:** Recursively scans all compatible media files, organizing them by type (Image, Video, and Audio).
2. **Concurrent Conversion:** Distributes processing using concurrent threads and parallel processes to bypass hardware bottlenecks, forcing strict resource control (a single thread per encoder instance) to avoid CPU contention on low-end systems.
3. **Adaptive Optimization:**
   - **Images:** Converts and compresses images to modern high-performance formats.
   - **Video:** Encodes video sequences into WebM/OGV containers optimized for web and lightweight players.
   - **Audio:** Transcodes audio tracks to OGG or OPUS, drastically reducing storage size while preserving the acoustic spectrum.
4. **Processing Resilience:** Implements a crash control system and performance telemetry that generates automatic reports in case of unexpected interruptions.

## Telemetry and Privacy

To measure tool performance and understand which file formats are optimized most by the community, Alenia Porter incorporates a basic asynchronous telemetry system.

- **Absolute Privacy:** **We do not collect personal or sensitive information** (such as real names, passwords, emails, processed files, or hard drive data).
- **Collected Data:** Only the unique, anonymous installation identifier (UUID), the user's chosen nickname, operating system type, execution mode (GUI/CLI), the extension of the optimized format (e.g. "mp3", "webp"), total processed file count, and elapsed time in seconds are sent.
- **Transparency:** All aggregated statistical information is sent securely to consolidate public benchmarks on the tool's performance across different platforms.

## Key Features

- **Standalone Tool (Zero Dependencies):** Packaged executables include internal binaries (such as FFmpeg), allowing it to run without installing Python or additional system dependencies.
- **Cross-Platform:** Full compatibility with Windows, macOS, and Linux.
- **Dynamic Themes:** UI color customization with multiple themes loaded dynamically from JSON files.
- **Custom Nickname:** Generation and input of readable names for usage statistics and telemetry, managed from the profile menu.
- **CI/CD Security:** Strict validation in GitHub Actions using automated smoke tests on virtual displays (xvfb) to ensure no unstable version reaches production.

## How to Use (IDE Edition)

1. Run the **AleniaPorter** executable.
2. Customize your nickname on the first run to link your local optimization stats.
3. Select your preferred audio format (OGG or OPUS).
4. Click "Select Folder to Convert" and choose the source folder to optimize.
5. Processed files are generated directly while respecting the original folder structure.

## CLI Installation

The Command-Line Interface is written in Go, optimized for headless environments and CI/CD pipelines.

**Linux & macOS:**
```bash
curl -fsSL https://kaia-alenia.github.io/Alenia-Porter/install.sh | bash
```
*(Ensure `~/.local/bin` is in your PATH)*

Once installed, simply type `porter` in your terminal to see all available options.

## CLI vs IDE Edition

| Feature | IDE Edition (GUI) | CLI Edition |
|---------|-------------------|-------------|
| **Target Audience** | Content creators, video editors, designers | DevOps, backend devs, CI/CD automation |
| **Interface** | Dynamic theming, visual drag-and-drop | Minimalist terminal output |
| **Architecture** | Python with embedded binaries | Native Go binary (Zero dependencies) |
| **Integration** | Standalone Desktop App | Shell scripts, GitHub Actions, Makefiles |
| **Performance** | High | Ultra-high (Minimal overhead) |

---

**License:** GNU General Public License v3 (GPL v3).
*Designed to be free, transparent, and accessible to the developer and creator community.*

**Official Alenia Studios Email:** contact.aleniastudios@gmail.com

**Developed and translated by Kaia-Alenia Studios**
US ES FR JP CN RU BR DE
