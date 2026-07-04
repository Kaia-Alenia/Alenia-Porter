# Changelog

## [6.6.0] - Main Project
### Fixed
- FFmpeg bug resolution for video export and optimization.
- FFmpeg bug resolution for audio conversion.
- Fixed the functionality of the "Update Now" button in the interface (resolved UI freeze and GitHub download issues).
- Fixed compilation errors in the frontend due to nested translation hooks.
- Resolved bug where the app version in the UI was hardcoded, causing false update prompts.
- Fixed the translation function `t()` to properly display default fallback strings instead of translation keys.
- Ensured the "Update Now" button triggers an in-app download instead of opening a web browser when used within the app.
- Created a new intelligent `smart_i18n.py` tool in the `tools/` directory to automatically parse and internationalize JSX text and attributes without breaking code.

## [1.7.0] - CLI
### Fixed
- General bug fixes and stability improvements.
- Minor fixes in FFmpeg handling.

---

## [6.4.0] - Main Project
### Fixed
- General improvements and optimization in code paths.

## [1.5.0] - CLI
### Fixed
- General improvements and optimization in the console interface.
