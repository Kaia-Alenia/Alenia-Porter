import json
import os

path = '/media/alejandro/D/tool/porter/src/alenia_porter/assets/locales/locales.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_en = {
    "update_success_msg": "Alenia Porter updated from GitHub! Please exit (/exit) and restart.",
    "update_error_no_curl": "Error: 'curl' or 'wget' is required to update.",
    "cli_usage_optimize": "Usage: porter optimize [options] <directory_or_file>",
    "cli_options": "Options",
    "cli_target_video": "Target video format",
    "cli_target_audio": "Target audio format",
    "cli_target_image": "Target image format",
    "cli_extra_video": "Extra video ffmpeg args",
    "cli_extra_audio": "Extra audio ffmpeg args",
    "cli_extra_image": "Extra image ffmpeg args",
    "cli_lang": "UI language",
    "me_uuid": "UUID:"
}

new_es = {
    "update_success_msg": "¡Alenia Porter actualizado desde GitHub! Por favor, sal (/exit) y reinicia.",
    "update_error_no_curl": "Error: Se requiere 'curl' o 'wget' para actualizar.",
    "cli_usage_optimize": "Uso: porter optimize [opciones] <directorio_o_archivo>",
    "cli_options": "Opciones",
    "cli_target_video": "Formato de video destino",
    "cli_target_audio": "Formato de audio destino",
    "cli_target_image": "Formato de imagen destino",
    "cli_extra_video": "Argumentos extra de video ffmpeg",
    "cli_extra_audio": "Argumentos extra de audio ffmpeg",
    "cli_extra_image": "Argumentos extra de imagen ffmpeg",
    "cli_lang": "Idioma de interfaz",
    "me_uuid": "UUID:"
}

for k, v in new_en.items():
    if k not in data['en']:
        data['en'][k] = v

for k, v in new_es.items():
    if k not in data['es']:
        data['es'][k] = v

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated locales.json")
