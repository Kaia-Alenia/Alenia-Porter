# Alenia Porter v3.0

Alenia Porter is a high-performance, ultra-lightweight media optimizer designed specifically for indie game developers. It batch-converts audio directories into highly compressed OGG/OPUS files and converts videos (MP4, MKV, WebM, AVI, MOV) into streaming-optimized WebM (VP9 codec / Opus audio) while maintaining a minimal RAM footprint (under 10MB), making it highly optimized for 8GB RAM workstations. It also auto-generates engine-ready script registries (`.rpy` for Ren'Py and `AudioRegistry.gd` for Godot).

---

## 🚀 Setting Up Your Repository & Linking to GitHub

To sync your local development folder to the cloud on Linux Mint, establish your Git connection and configure your credentials safely.

### 1. Configure Git Identity & Cache Credentials
Run these commands once to identify yourself and securely store your Personal Access Token (PAT) so you do not have to write it repeatedly:
```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
git config --global credential.helper store
```

### 2. Connect and Commit
Initialize Git inside your project root and link it to your GitHub repository:
```bash
git init
git remote add origin https://github.com/Kaia-Alenia/Alenia-Porter.git
git branch -M main
git add .
git commit -m "Lanzamiento inicial de Alenia Porter v3.0"
git push -u origin main
```

---

## 🤖 CI/CD Automated Cloud Builds (GitHub Actions)

Since heavy binaries like `ffmpeg.exe` and `ffprobe.exe` are excluded via `.gitignore` to stay well below GitHub's 100MB file limit, compiling is handled automatically in the cloud.

Every time you push a Git tag starting with the letter `v` (e.g., `v3.0`):
1. **Actions Trigger**: GitHub Actions activates when you push a version tag, running a virtual machine (`windows-latest`) with Python 3.11.
2. **FFmpeg On-The-Fly**: The runner executes an automated, comment-free PowerShell script to download the official FFmpeg essentials package, extract it on-the-fly, locate `ffmpeg.exe` and `ffprobe.exe` recursively, and place them inside the compiled application package.
3. **Standalone Packaging**: PyInstaller compiles a standalone executable directory with parameters `--onedir`, `--windowed`, and `--contents-directory internal`, copying the legal `LICENSE` document automatically.
4. **Zipped Artifacts & Releases**: The package is archived into `AleniaPorter.zip` and automatically uploaded both to the workflow artifacts and attached directly to a new public GitHub Release under the corresponding tag name.

### 🏷️ How to Trigger a Release (Tag Push)
To publish a new release, tag your commit and push it to the remote repository:
```bash
git add .
git commit -m "Prepare v3.0 release"
git tag -a v3.0 -m "Release Alenia Porter v3.0"
git push origin main
git push origin v3.0
```

### 📥 Downloading Your Compiled Executable
1. Go to the **Releases** section on the right side of your GitHub repository page (or navigate to the **Actions** tab).
2. Look for the latest release (e.g., **v3.0**).
3. Under the release description, click on **AleniaPorter.zip** to download the pre-packaged, ready-to-run executable.

---

## 🐧 Cross-Platform Linux Extraction (Addressing Path Separators)

When extracting Windows-compiled zip packages on Linux Mint, standard extractors can break. This happens because Windows uses backslashes (`\`) for folders, which Linux standard tools read as part of flat file names, resulting in an unorganized folder structure.

To restore folders and subdirectories perfectly:

1. Install `unar` (The Unarchiver), which is designed to convert path separators on-the-fly:
   ```bash
   sudo apt update
   sudo apt install unar
   ```
2. Navigate to your downloads directory and extract the inner archive (`AleniaPorter.zip`):
   ```bash
   unar AleniaPorter.zip
   ```
This generates a clean `AleniaPorter` directory with `internal/`, `bin/`, and `locales/` structured natively. You can now execute the `.exe` inside Bottles or Wine on Linux with perfect performance.

---

## ⚖️ Licencia y Aspecto Legal (CC BY 4.0 + Additional Terms)

This software is distributed under the **Alenia Studios Standard License**:
- **Attribution**: You must give appropriate credit to Alenia Studios, provide a link to the license, and indicate if changes were made.
- **Strict AI Restriction**: You are strictly prohibited from using this source code, tool scripts, or compiled binaries for machine learning, artificial intelligence model training, or algorithmic synthesis pipelines.
- **Commercial Resale**: Direct resale or repackaging of this tool for profit is strictly prohibited.

---

## ☕ Support Alenia Studios
Thank you for using the tools from the Alenia Hub ecosystem. If you find this software helpful, support our continuous development on our official Patreon:
* [Patreon - Alenia Studios](https://www.patreon.com/cw/alenia_studios)