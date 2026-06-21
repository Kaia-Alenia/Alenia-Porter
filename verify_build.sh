#!/bin/bash
set -e
PYTHONPATH=src /tmp/porter-venv/bin/python3 -m nuitka --standalone --enable-plugin=tk-inter --include-package=alenia_porter --include-data-dir=src/alenia_porter/assets=alenia_porter/assets --output-filename=AleniaPorter porter_launcher.py
if [ ! -f "porter_launcher.dist/alenia_porter/assets/locales/locales.json" ]; then
    exit 1
fi
porter_launcher.dist/AleniaPorter --headless
