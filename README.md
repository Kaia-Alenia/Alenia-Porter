# Alenia Porter
**by Alenia Studios**

## 1. Description
Alenia Porter is an automated media optimizer designed specifically for game developers. It batch-converts, compresses, and perfectly formats your media assets to be seamlessly integrated into popular game engines like Ren'Py and Godot, ensuring optimal performance and compatibility for your projects.

## 2. Architecture & Performance
Built with efficiency in mind, Alenia Porter integrates the **Alenia Zenith** speculative background engine. This technology delegates heavy visual and audio processing loads to ensure ultra-fast startup times and is heavily optimized to run smoothly on workstations with limited memory (specifically designed and tested for 8GB RAM environments).

## 3. Installation & Usage

### For Users (Ready to Use)
No Python installation or environment setup is required.
1. Navigate to the **Releases** tab in this repository.
2. Download the standalone executable for your operating system (Windows `.exe`, Linux `.bin`, or macOS `.app`).
3. Run the application directly.

### For Developers (Build from Source)
If you want to modify the code or compile the binary yourself:

1. Clone the repository:
   ```bash
   git clone https://github.com/Kaia-Alenia/Alenia-Porter.git
   cd porter
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application from the source code:
   ```bash
   python main.py
   ```
*(Note: Cloud compilation via GitHub Actions using Nuitka is configured in `.github/workflows/build.yml`)*

## 4. Supported Languages & Translators
- 🇺🇸 **English** - Translated by KXLT (Alenia Studios)
- 🇪🇸 **Spanish** - Translated by KXLT (Alenia Studios)
- 🇫🇷 **French** - Translated by KXLT (Alenia Studios)
- 🇯🇵 **Japanese** - Translated by KXLT (Alenia Studios)
- 🇨🇳 **Chinese** - Translated by KXLT (Alenia Studios)
- 🇷🇺 **Russian** - Translated by KXLT (Alenia Studios)
- `[Space available for new contributors]`

*We actively invite the community to contribute with new translations to make Alenia Porter accessible worldwide!*

## 5. Contributions & Roadmap
We welcome community collaboration! You can help us improve Alenia Porter in the following areas:
- **Interface (UI):** Enhancing the user experience and aesthetics.
- **Logic:** Optimizing batch conversion algorithms and core performance.
- **Languages:** Adding new localizations.

**Roadmap:** Our goal is to progressively expand support and integration with various game engines. However, all new features and tests are conducted meticulously due to our studio's current hardware limitations (8GB RAM workstations) to ensure the tool remains lightweight for everyone.

## 6. License and Legal Terms
This software is distributed under the **Alenia Studios Tool License**. By using or modifying this tool, you agree to the following terms:

1. **Your files are yours:** The audio, video, or data files processed by this Software remain 100% your property. No attribution to Alenia Studios is required in your final project for simply using this tool to process your assets.
2. **Always free (Recommend us!):** This Software is completely free for commercial and non-commercial projects. If you find it useful, we strongly encourage you to recommend it to other developers.
3. **Code Attribution:** If you modify, fork, or distribute the source code of this Software, you must provide appropriate credit to Alenia Studios and the respective community translators.
4. **No Resale:** Standalone redistribution, sublicensing, or resale of this Software or its source code for profit is strictly prohibited. It must remain free.
5. **No AI Training:** The source code, documentation, and logic of this Software may not be used, scraped, or included in datasets for the training of Artificial Intelligence models or machine learning algorithms.
