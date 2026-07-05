#!/usr/bin/env python3
"""
smart_i18n.py
Herramienta avanzada para internacionalización (i18n) de archivos TSX/JSX.
Analiza y extrae textos hardcodeados de componentes React y los sustituye
con llamadas a la función t("key", "Texto original").

Características:
- Encuentra texto suelto entre etiquetas (JSX Text).
- Encuentra atributos como placeholder, title, alt.
- Ignora texto que ya está internacionalizado o es código/variable.
- Actualiza automáticamente el archivo TSX.
- Puede (opcionalmente) agregar nuevas claves al archivo de traducciones.

Licencia: GNU General Public License v3 (GPL v3)
"""

import re
import sys
import os
import json
import uuid

def generate_key_from_text(text):
    """Genera una clave (key) amigable a partir del texto."""
    # Eliminar puntuación y caracteres especiales
    clean = re.sub(r'[^\w\s]', '', text).strip()
    words = clean.split()
    if not words:
        return "key_" + uuid.uuid4().hex[:8]
    # Tomar hasta 5 palabras para la clave
    key = "lbl_" + "_".join(words[:5]).lower()
    return key

def process_jsx_text(content, known_keys):
    """Busca texto libre entre etiquetas JSX >Texto<"""
    # Expresión regular para buscar > Texto libre < que no sean puros espacios
    # Evita reemplazar dentro de scripts, estilos, o código con llaves {}
    
    # Patrón: > (texto sin > ni < ni { ni }) <
    pattern = r'>([^<>{]+)<'
    
    def replacer(match):
        text = match.group(1)
        # Ignorar si es puro espacio
        if not text.strip():
            return match.group(0)
            
        # Ignorar si parece código o números o muy corto (opcional)
        if len(text.strip()) < 2 and not text.strip().isalpha():
            return match.group(0)
            
        clean_text = text.strip()
        key = generate_key_from_text(clean_text)
        
        # Mantener los espacios originales alrededor del texto
        left_space = text[:len(text) - len(text.lstrip())]
        right_space = text[len(text.rstrip()):]
        
        known_keys[key] = clean_text
        return f'>{left_space}{{t("{key}", "{clean_text}")}}{right_space}<'

    # Se aplican múltiples pasadas para anidamientos
    new_content = re.sub(pattern, replacer, content)
    return new_content

def process_jsx_attributes(content, known_keys):
    """Busca atributos hardcodeados como placeholder='...' o title='...'"""
    # Atributos comunes que suelen tener texto traducible
    attrs = ['placeholder', 'title', 'alt', 'label']
    
    for attr in attrs:
        # Busca attr="Texto" o attr='Texto'
        pattern = fr'\b{attr}=(["\'])([^"\']+)\1'
        
        def replacer(match):
            quote = match.group(1)
            text = match.group(2)
            
            if not text.strip() or '{' in text or text.startswith('http'):
                return match.group(0)
                
            key = generate_key_from_text(text)
            known_keys[key] = text
            
            # Cambia a attr={t("key", "texto")}
            return f'{attr}={{t("{key}", "{text}")}}'
            
        content = re.sub(pattern, replacer, content)
        
    return content

def update_locales(locales_path, new_keys):
    """Actualiza el archivo locales.json con las nuevas claves encontradas"""
    if not os.path.exists(locales_path):
        print(f"Warning: No se encontró {locales_path}")
        return

    with open(locales_path, 'r', encoding='utf-8') as f:
        try:
            locales = json.load(f)
        except json.JSONDecodeError:
            print("Error al leer locales.json. Asegúrate de que el formato sea correcto.")
            return

    added = 0
    # Por defecto, se añaden a 'es' (español) o a todos los idiomas base
    for lang in locales.keys():
        if isinstance(locales[lang], dict):
            for key, val in new_keys.items():
                if key not in locales[lang]:
                    locales[lang][key] = val  # Se pone el texto original por defecto
                    added += 1

    if added > 0:
        with open(locales_path, 'w', encoding='utf-8') as f:
            json.dump(locales, f, indent=4, ensure_ascii=False)
        print(f"Se añadieron {added} nuevas traducciones a {locales_path}.")
    else:
        print("No hay claves nuevas para añadir a locales.json.")

def main():
    if len(sys.argv) < 2:
        print("Uso: python smart_i18n.py <archivo.tsx> [--update-locales path/to/locales.json]")
        sys.exit(1)
        
    target_file = sys.argv[1]
    locales_file = None
    
    if len(sys.argv) == 4 and sys.argv[2] == "--update-locales":
        locales_file = sys.argv[3]
        
    if not os.path.exists(target_file):
        print(f"Error: {target_file} no encontrado.")
        sys.exit(1)
        
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    extracted_keys = {}
    
    # 1. Reemplazar texto JSX
    content = process_jsx_text(content, extracted_keys)
    
    # 2. Reemplazar atributos HTML
    content = process_jsx_attributes(content, extracted_keys)
    
    # Escribir de vuelta al archivo
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Procesamiento completado para {target_file}.")
    print(f"Se encontraron {len(extracted_keys)} textos internacionalizables.")
    
    if locales_file and extracted_keys:
        update_locales(locales_file, extracted_keys)

if __name__ == "__main__":
    main()
