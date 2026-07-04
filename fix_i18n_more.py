import json

app_file = "frontend/src/App.tsx"
with open(app_file, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    "Formatos de salida (carpeta)": '{t("outputFormatsFolder", "Formatos de salida (carpeta)")}',
    "Selecciona cada pestaña para configurar su formato": '{t("selectTabFormat", "Selecciona cada pestaña para configurar su formato")}',
    "¡Listo! Archivos Guardados en Origen": '{t("savedInSource", "¡Listo! Archivos Guardados en Origen")}',
    "Privacidad de Datos": '{t("dataPrivacy", "Privacidad de Datos")}',
    "Tu alias anónimo asignado:": '{t("yourAlias", "Tu alias anónimo asignado:")}'
}

for k, v in replacements.items():
    content = content.replace(f">{k}<", f">{v}<")

with open(app_file, "w", encoding="utf-8") as f:
    f.write(content)

# Update locales.json
with open("src/alenia_porter/assets/locales/locales.json", "r", encoding="utf-8") as f:
    locales = json.load(f)

for lang in locales:
    if "updateNow" not in locales[lang]:
        if lang == "es":
            locales[lang]["updateNow"] = "Actualizar Ahora"
        elif lang == "en":
            locales[lang]["updateNow"] = "Update Now"
        elif lang == "fr":
            locales[lang]["updateNow"] = "Mettre à jour"
        else:
            locales[lang]["updateNow"] = "Update"

with open("src/alenia_porter/assets/locales/locales.json", "w", encoding="utf-8") as f:
    json.dump(locales, f, indent=4, ensure_ascii=False)

print("More i18n fixed.")
