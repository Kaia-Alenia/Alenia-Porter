# Changelog

## [6.6.0] - Main Project
### Fixed
- Fixed auto-update script (`update.sh`) on Linux to prevent "file busy" errors when replacing the binary.
- Improved CLI `ap` self-update logic to properly download and extract `.tar.gz` and `.zip` releases.
- Fixed update button flow in the frontend UI to properly fallback or download the binary.
- Added PowerShell installation commands for Windows users in `docs/index.html`.
- Added improved i18n scanner script (`tools/i18n_check.py`).
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
