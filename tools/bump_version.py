import os
import sys

LICENSE_TEXT = """
GNU General Public License v3 (GPL v3)
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

def get_files_to_check(root_dir):
    ignored_dirs = [".git", "node_modules", "venv", "__pycache__", ".github", "dist", "build"]
    allowed_extensions = [".py", ".toml", ".json", ".go", ".md", ".txt", ".sh", ".yml", ".yaml"]
    target_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for ig in ignored_dirs:
            if ig in dirnames:
                dirnames.remove(ig)
        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            if ext in allowed_extensions or filename == "Makefile":
                target_files.append(os.path.join(dirpath, filename))
    return target_files

def update_version(old_version, new_version, root_dir):
    import re
    files = get_files_to_check(root_dir)
    changed_files = []
    
    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            old_esc = re.escape(old_version)
            
            if filename in ["pyproject.toml", "uv.lock"]:
                lines = content.split('\n')
                for i in range(min(50, len(lines))):
                    if re.search(rf'^version\s*=\s*"{old_esc}"', lines[i]):
                        lines[i] = re.sub(rf'^version\s*=\s*"{old_esc}"', f'version = "{new_version}"', lines[i])
                new_content = '\n'.join(lines)
            elif filename in ["package.json", "package-lock.json"]:
                lines = content.split('\n')
                for i in range(min(50, len(lines))):
                    if re.search(rf'"version"\s*:\s*"{old_esc}"', lines[i]):
                        lines[i] = re.sub(rf'"version"\s*:\s*"{old_esc}"', f'"version": "{new_version}"', lines[i])
                new_content = '\n'.join(lines)
            elif filename == "__init__.py":
                new_content = re.sub(rf'__version__\s*=\s*"{old_esc}"', f'__version__ = "{new_version}"', content)
            elif filename.endswith(".go"):
                new_content = re.sub(rf'const\s+version\s*=\s*"{old_esc}"', f'const version = "{new_version}"', content)
            elif filename.lower().endswith(('.md', '.txt')) or 'readme' in filename.lower():
                if old_version in content:
                    new_content = content.replace(old_version, new_version)
            
            if content != new_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                changed_files.append(filepath)
                print("Actualizado: " + filepath)
        except Exception:
            pass
            
    return changed_files

def main():
    print(LICENSE_TEXT)
    print("Herramienta de actualizacion de versiones de Alenia Porter")
    old_version = input("Ingrese la version actual (ejemplo: 6.6.0 o 1.6.0): ").strip()
    new_version = input("Ingrese la nueva version (ejemplo: 6.6.0 o 1.6.0): ").strip()
    
    if not old_version or not new_version:
        print("Versiones invalidas. Saliendo.")
        sys.exit(1)
        
    if old_version == new_version:
        print("Las versiones son identicas. No hay nada que hacer.")
        sys.exit(0)
        
    print("Buscando y reemplazando '" + old_version + "' por '" + new_version + "'...")
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    changed = update_version(old_version, new_version, root_dir)
    
    print("Total de archivos modificados: " + str(len(changed)))
    if len(changed) == 0:
        print("No se encontraron coincidencias para la version ingresada.")

if __name__ == "__main__":
    main()
