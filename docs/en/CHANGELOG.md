# Changelog

## [6.8.0] - Main Project
### Fixed
- **i18n Coverage** — Added missing translation keys and replaced hardcoded text in `App.tsx` to ensure full localization when switching languages.
- **Critical: GPU encoder crash (FFmpeg return code 255)** — Hardware encoders (`h264_nvenc`, `h264_qsv`, `h264_amf`, `vp9_nvenc`, `vp9_qsv`) are now validated with a real test frame before being selected. On systems without NVIDIA CUDA or compatible GPU, the engine correctly falls back to software encoders (`libx264`, `libvpx-vp9`) instead of crashing.
- **Video-to-GIF conversion broken** — Safe mode retry (triggered after an FFmpeg failure) was incorrectly inserting `-hwaccel none` before the GIF's `filter_complex` palette pipeline, causing the retry to also fail. GIF encoding is now excluded from the hardware acceleration flag injection.
- **Safe mode always uses software encoders** — When safe mode is active, `libx264` and `libvpx-vp9` are used directly for MP4 and WebM respectively, without querying hardware encoders.
- Fixed `App.tsx` compilation error caused by a malformed `startBatchQueueProcessing` function after a previous refactor.

## [1.8.0] - CLI
### Added
- Implemented `/me` command to view and edit user alias, UUID, and telemetry settings.
- Added persistent configuration system for CLI (`config.json`) with Windows `LOCALAPPDATA` support, storing UI language, alias, and telemetry consent.
### Fixed
- Completed i18n localization covering all hardcoded strings (e.g., CLI usage descriptions, `operations.go` output, and `/me` command).
- Verified correct argument passthrough from `startEngineCmd` (Go) to `headless.py` (Python engine) — `--vformat`, `--aformat`, `--iformat`, `--vextra`, `--aextra`, `--iextra` flags are forwarded correctly.
- `porter optimize` non-interactive mode works correctly end-to-end after the engine fix.

---

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

## [1.8.0] - CLI
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
