# Contributing to Alenia Porter

We love community contributions! Here is how you can help:

## 🎨 Creating New Themes
You can add your own visual identity to Alenia Porter by creating a new JSON file in the `themes/` directory.

### How to do it:
1. Copy an existing theme like `default.json`.
2. Edit the color hex codes (`bg_main`, `accent`, etc.).
3. Point to your own transparent assets in the `assets/` folder.
4. Your theme will automatically appear in the app's theme cycle (the 🎨 button).

## 💻 Improving the Code
If you want to optimize the conversion logic or enhance the UI:

### Files to edit:
- `main.py`: Contains all the UI logic, window management, and theme application.
- `porter_logic.py`: Contains the core conversion engine (FFmpeg calls and file processing).
- `clean_assets.py`: If you want to improve how images are processed and cleaned.

### Guidelines:
- **No comments in scripts:** Please do not add comments to the `.py` files. Keep the code clean and self-explanatory.
- **Maintain the License:** All contributions must respect the ALENIA STUDIOS TOOL LICENSE.

## 🌍 Translations
To add a new language, simply add a new key to the JSON structure within `locales/`.

---
Thank you for helping Alenia Porter grow! 🐧✨
