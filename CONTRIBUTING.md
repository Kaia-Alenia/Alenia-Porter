# Contributing to Alenia Porter 🐧

We appreciate your interest in helping Alenia Studios! Here is how you can contribute to the project:

## Theme Development
Create your own visual style by adding a new JSON file to the `themes/` directory. You can customize colors and link specific character sprites from the `assets/` folder.

## Code Contributions
Help us optimize the conversion engine or enhance the user interface:
- **UI Logic:** Managed in `main.py` (Strictly no comments allowed).
- **Core Engine:** Managed in `porter_logic.py` (Strictly no comments allowed).
- **Architecture:** Powered by the internal Zenith Core.

## Asset Specifications
To maintain UI integrity, please follow these exact dimensions:

| Asset Type | Path/Example | Dimensions (px) | Notes |
| :--- | :--- | :--- | :--- |
| **Main Character** | `kaia_default.png` | **180 × 260** | Main UI assistant (bottom-right). |
| **Success/Info Character** | `kaia_success.png` | **140 × 180** | Used in popup windows. |
| **Progress Icon** | `kaia_mini.png` | **24 × 24** | Icon that follows the progress bar. |
| **Studio Logo** | `studio_logo.png` | **200 × 50** | Branding at the bottom. |
| **App Icon** | `logo.ico` | **256 × 256** | Standard Windows icon format. |

---
## Localization
Help us reach more developers by adding new languages to the `locales/` system.

**Current Languages:**
US English | ES Español | FR Français | JP 日本語 | CN 简体中文 | RU Русский | BR Português | DE Deutsch

> [!IMPORTANT]
> **Translated by KXLT Alenia Studios**
> *Professional localization and community support.*

---
### Contribution Guidelines
- **Zero Dependencies:** Ensure the code remains free of external Python libraries (like Pillow).
- **No Comments in Scripts:** Keep the source code clean and self-documenting.
- **Licensing:** All contributions must comply with the ALENIA STUDIOS TOOL LICENSE.

Thank you for being part of Alenia Studios!
