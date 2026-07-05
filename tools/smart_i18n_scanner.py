#!/usr/bin/env python3
import os
import re
import sys

def scan_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    results = []
    
    # Text nodes: >...<
    text_pattern = re.compile(r'>\s*([^<{]+?[a-zA-ZáéíóúÁÉÍÓÚñÑ][^<{]*?)\s*<')
    # Attributes like placeholder="..." or title="..."
    attr_pattern = re.compile(r'\b(placeholder|title|label|alt)="([^"{]+?[a-zA-ZáéíóúÁÉÍÓÚñÑ][^"{]*?)"')

    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Ignorar lineas de imports
        if line.strip().startswith('import '):
            continue
        # Ignorar comentarios JSX y TS
        if '{/*' in line or '*/}' in line or '//' in line:
            continue
            
        for match in text_pattern.finditer(line):
            text = match.group(1).strip()
            # Filtramos si es solo className u otras cadenas tecnicas
            if len(text) > 1 and not re.match(r'^[A-Z0-9_\-\s\.]+$', text): 
                results.append((i+1, "Text Node", text))
                
        for match in attr_pattern.finditer(line):
            attr = match.group(1)
            text = match.group(2).strip()
            if len(text) > 1:
                results.append((i+1, f'Attr: {attr}', text))
                
    return results

def main():
    print("=========================================")
    print("  Scanner Inteligente de Textos (i18n)  ")
    print("=========================================")
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(root_dir, "frontend", "src")
    
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        
    print(f"Buscando textos hardcodeados en: {target_dir}\n")
    
    total_found = 0
    for dirpath, dirnames, filenames in os.walk(target_dir):
        for filename in filenames:
            if filename.endswith(('.tsx', '.ts')):
                filepath = os.path.join(dirpath, filename)
                res = scan_file(filepath)
                if res:
                    rel_path = os.path.relpath(filepath, root_dir)
                    print(f"--- Archivo: {rel_path} ---")
                    for line_num, t_type, text in res:
                        print(f"  Línea {line_num:4d} | {t_type:12s} | '{text}'")
                    print("")
                    total_found += len(res)
                    
    print(f"Total de textos sospechosos encontrados: {total_found}")
    print("Nota: Revise manualmente si requieren envolverse en {t('key')}.")

if __name__ == '__main__':
    main()
