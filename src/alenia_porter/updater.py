__license__ = "GNU General Public License v3 (GPL v3)"
import urllib.request
import json
import sys
import os
import platform
import zipfile
import tarfile
import subprocess
import shutil

REPO_API_URL = "https://api.github.com/repos/Kaia-Alenia/Alenia-Porter/releases/latest"

def get_os_asset_name():
    system = platform.system().lower()
    if system == "windows":
        return "AleniaPorter-Windows.zip"
    elif system == "darwin":
        return "AleniaPorter-macOS.zip"
    else:
        return "AleniaPorter-Linux.tar.gz"

def check_for_updates(current_version):
    try:
        req = urllib.request.Request(REPO_API_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            
            latest_version = data.get("tag_name", "")
            if not latest_version or latest_version == current_version:
                return False, None, None
            
            target_asset_name = get_os_asset_name()
            download_url = None
            
            for asset in data.get("assets", []):
                if asset.get("name") == target_asset_name:
                    download_url = asset.get("browser_download_url")
                    break
            
            if download_url:
                return True, latest_version, download_url
            
    except Exception as e:
        print(f"Error checking for updates: {e}")
    
    return False, None, None

def download_and_apply_update(download_url, progress_callback, on_ready_to_restart):
    try:
        temp_dir = "AleniaPorter_UpdateTemp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        system = platform.system().lower()
        is_zip = download_url.endswith(".zip")
        download_path = os.path.join(temp_dir, "update.zip" if is_zip else "update.tar.gz")
        
        def reporthook(blocknum, blocksize, totalsize):
            if totalsize > 0:
                percent = min(100, int((blocknum * blocksize * 100) / totalsize))
                progress_callback(percent)
                
        urllib.request.urlretrieve(download_url, download_path, reporthook)
        
        def is_within_directory(directory, target):
            return not os.path.relpath(os.path.abspath(target), os.path.abspath(directory)).startswith("..")
            
        if is_zip:
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                safe_members = [m for m in zip_ref.namelist() if is_within_directory(temp_dir, os.path.join(temp_dir, m))]
                zip_ref.extractall(temp_dir, members=safe_members)
        else:
            with tarfile.open(download_path, 'r:gz') as tar_ref:
                safe_members = [m for m in tar_ref.getmembers() if is_within_directory(temp_dir, os.path.join(temp_dir, m.name))]
                tar_ref.extractall(temp_dir, members=safe_members)
                
        os.remove(download_path)
        
        extracted_base = os.path.join(temp_dir, "AleniaPorter")
        if not os.path.exists(extracted_base):
            extracted_base = temp_dir
            
        create_and_run_trampoline(extracted_base, system)
        on_ready_to_restart()
        
    except Exception as e:
        print(f"Update failed: {e}")

def create_and_run_trampoline(update_source_dir, system):
    current_dir = os.path.abspath(os.getcwd())
    update_source_dir = os.path.abspath(update_source_dir)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    
    if system == "windows":
        script_path = os.path.join(parent_dir, "update_alenia.bat")
        bat_content = f"""@echo off
timeout /t 3 /nobreak > NUL
taskkill /f /im AleniaPorter.exe > NUL 2>&1
echo Updating Alenia Porter...
if exist "{current_dir}\\assets" rmdir /s /q "{current_dir}\\assets"
if exist "{current_dir}\\themes" rmdir /s /q "{current_dir}\\themes"
if exist "{current_dir}\\bin" rmdir /s /q "{current_dir}\\bin"
if exist "{current_dir}\\porter.py" del /f /q "{current_dir}\\porter.py"
if exist "{current_dir}\\updater.py" del /f /q "{current_dir}\\updater.py"
if exist "{current_dir}\\cli.py" del /f /q "{current_dir}\\cli.py"
if exist "{current_dir}\\porter.pyd" del /f /q "{current_dir}\\porter.pyd"
if exist "{current_dir}\\updater.pyd" del /f /q "{current_dir}\\updater.pyd"
if exist "{current_dir}\\cli.pyd" del /f /q "{current_dir}\\cli.pyd"
xcopy /s /e /y "{update_source_dir}\\*" "{current_dir}\\"
rmdir /s /q "{update_source_dir}"
cd /d "{current_dir}"
start "" "AleniaPorter.exe"
del "%~f0"
"""
        with open(script_path, "w") as f:
            f.write(bat_content)
            
        subprocess.Popen([script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        
    else:
        script_path = os.path.join(parent_dir, "update_alenia.sh")
        exe_name = "./AleniaPorter"
        sh_content = f"""#!/bin/bash
sleep 3
echo "Updating Alenia Porter..."
rm -rf "{current_dir}/assets"
rm -rf "{current_dir}/themes"
rm -rf "{current_dir}/bin"
rm -f "{current_dir}/porter.py" "{current_dir}/updater.py" "{current_dir}/cli.py"
rm -f "{current_dir}/porter.pyd" "{current_dir}/updater.pyd" "{current_dir}/cli.pyd"
cp -R "{update_source_dir}/"* "{current_dir}/"
rm -rf "{update_source_dir}"
cd "{current_dir}"
chmod +x {exe_name}
{exe_name} &
rm -- "$0"
"""
        with open(script_path, "w") as f:
            f.write(sh_content)
            
        os.chmod(script_path, 0o755)
        subprocess.Popen([script_path], start_new_session=True)
