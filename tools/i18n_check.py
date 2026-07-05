#!/usr/bin/env python3
import os
import re
import sys

def scan_react_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    results = []
    text_pattern = re.compile(r'>\s*([^<{]+?[a-zA-ZáéíóúÁÉÍÓÚñÑ][^<{]*?)\s*<')
    attr_pattern = re.compile(r'\b(placeholder|title|label|alt)="([^"{]+?[a-zA-ZáéíóúÁÉÍÓÚñÑ][^"{]*?)"')

    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('import '): continue
        if '{/*' in line or '*/}' in line or '//' in line: continue
            
        for match in text_pattern.finditer(line):
            text = match.group(1).strip()
            if len(text) > 1 and not re.match(r'^[A-Z0-9_\-\s\.]+$', text): 
                results.append((i+1, "Text Node", text))
                
        for match in attr_pattern.finditer(line):
            attr = match.group(1)
            text = match.group(2).strip()
            if len(text) > 1:
                results.append((i+1, f'Attr: {attr}', text))
    return results

def scan_go_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    results = []
    # Busca cadenas literales largas que puedan contener español (tiene espacios o caracteres latinos)
    string_pattern = re.compile(r'"([^"\\]*?[áéíóúÁÉÍÓÚñÑ][^"\\]*?)"')
    print_pattern = re.compile(r'(fmt\.Print(?:ln|f)?|log\.(?:Print|Fatal|Panic)(?:ln|f)?|Short:\s*|Long:\s*|Use:\s*)("[^"]+")')

    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('//'): continue
            
        for match in print_pattern.finditer(line):
            func = match.group(1).strip()
            text = match.group(2).strip('"')
            if len(text) > 1 and re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', text):
                results.append((i+1, f'Go: {func}', text))
                
        # Also catch any string with spanish chars
        for match in string_pattern.finditer(line):
            text = match.group(1)
            if len(text) > 2:
                results.append((i+1, 'Go String (Latam)', text))
    return results

def scan_python_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    results = []
    print_pattern = re.compile(r'(print|logger\.(?:info|warn|error|debug))\(\s*(f?"[^"]+"|f?\'[^\']+\')')
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('#'): continue
            
        for match in print_pattern.finditer(line):
            func = match.group(1).strip()
            text = match.group(2).strip('f"\'')
            if len(text) > 1 and re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', text):
                results.append((i+1, f'Py: {func}', text))
    return results


def main():
    print("=========================================")
    print("  Escáner Avanzado de Textos (i18n) v2  ")
    print("=========================================")
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = root_dir
    
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        
    print(f"Buscando textos hardcodeados en: {target_dir}\n")
    
    total_found = 0
    for dirpath, dirnames, filenames in os.walk(target_dir):
        if 'node_modules' in dirpath or '.git' in dirpath or 'venv' in dirpath or '__pycache__' in dirpath or 'dist' in dirpath:
            continue
            
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            res = []
            if filename.endswith(('.tsx', '.ts', '.svelte')):
                res = scan_react_file(filepath)
            elif filename.endswith('.go'):
                res = scan_go_file(filepath)
            elif filename.endswith('.py') and not filename == os.path.basename(__file__):
                res = scan_python_file(filepath)
                
            if res:
                rel_path = os.path.relpath(filepath, root_dir)
                print(f"--- Archivo: {rel_path} ---")
                for line_num, t_type, text in res:
                    print(f"  Línea {line_num:4d} | {t_type:15s} | '{text}'")
                print("")
                total_found += len(res)
                    
    print(f"Total de posibles textos hardcodeados encontrados: {total_found}")
    print("Nota: Revise manualmente si requieren envolverse en la capa i18n correspondientes de su módulo.")

if __name__ == '__main__':
    main()
