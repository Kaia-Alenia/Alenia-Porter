__license__ = "GNU General Public License v3 (GPL v3)"
import concurrent.futures
import re
from importlib.resources import files
from contextlib import contextmanager

import sys
import os
import json
import traceback
import subprocess
import encodings.idna
import logging
from logging.handlers import RotatingFileHandler
import time
import datetime

def load_dotenv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    potential_env_paths = [
        os.path.join(base_dir, ".env"),
        os.path.join(os.path.dirname(base_dir), ".env"),
        os.path.join(os.path.dirname(os.path.dirname(base_dir)), ".env")
    ]
    for env_path in potential_env_paths:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            key, val = line.split("=", 1)
                            os.environ[key.strip()] = val.strip()
                        elif line.startswith("postgresql://"):
                            os.environ["DATABASE_URL"] = line
                break
            except:
                pass

load_dotenv()

def get_local_uuid():
    home_dir = os.path.expanduser("~")
    uuid_file_path = os.path.join(home_dir, ".alenia_uuid")
    if os.path.exists(uuid_file_path):
        try:
            with open(uuid_file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except:
            pass
    import uuid
    new_uuid = str(uuid.uuid4())
    try:
        with open(uuid_file_path, "w", encoding="utf-8") as f:
            f.write(new_uuid)
    except:
        pass
    return new_uuid

def generate_nickname():
    import random
    adjectives = [
        "happy", "dashing", "swift", "clever", "brave", "silent", "creative", "active", "smart", "jolly",
        "bold", "wild", "bright", "proud", "kind", "lively", "fierce", "eager", "fancy", "cozy",
        "funky", "epic", "cool", "chill", "golden", "magic", "mystic", "noble", "quick", "rusty",
        "shady", "stellar", "tricky", "unique", "vast", "zesty", "agile", "calm", "dark", "elite",
        "grand", "heroic", "iconic", "jade", "keen", "lucky", "mighty", "neon", "retro", "ultra",
        "crimson", "azure", "solar", "lunar", "cosmic", "cyber", "rapid", "quiet", "merry", "gentle",
        "brazen", "sneaky", "sleepy", "wandering", "hidden", "flying", "jumping", "swimming", "lost",
        "famous", "hidden", "silly", "witty", "wise", "playful", "sunny", "stormy", "winter", "spring",
        "autumn", "summer", "arctic", "desert", "ocean", "jungle", "mountain", "valley", "river", "lake",
        "forest", "moonlight", "starlight", "sunlight", "twilight", "midnight", "dawn", "dusk", "morning",
        "evening", "day", "night", "light", "shadow", "ghost", "spirit", "soul", "heart", "mind"
    ]
    nouns = [
        "tiger", "robot", "fox", "eagle", "panther", "coder", "falcon", "puffin", "koala", "badger",
        "wolf", "deer", "rabbit", "bear", "lion", "hawk", "owl", "dolphin", "whale", "squirrel",
        "shark", "dragon", "ninja", "wizard", "pirate", "ghost", "knight", "cyborg", "mutant", "alien",
        "phantom", "rebel", "sniper", "titan", "vampire", "zombie", "goblin", "orc", "troll", "elf",
        "dwarf", "giant", "mermaid", "yeti", "kraken", "sphinx", "phoenix", "unicorn", "pegasus", "griffin",
        "leopard", "cheetah", "jaguar", "cougar", "lynx", "bobcat", "puma", "ocelot", "caracal", "serval",
        "hound", "terrier", "mastiff", "bulldog", "collie", "poodle", "pug", "beagle", "boxer", "husky",
        "sparrow", "raven", "crow", "dove", "swan", "goose", "duck", "penguin", "ostrich", "emu",
        "turtle", "tortoise", "lizard", "snake", "crocodile", "alligator", "iguana", "gecko", "chameleon", "skink",
        "frog", "toad", "salamander", "newt", "axolotl", "fish", "shark", "ray", "eel", "crab"
    ]
    return f"{random.choice(adjectives)}-{random.choice(nouns)}"

def get_local_nickname():
    home_dir = os.path.expanduser("~")
    nickname_file_path = os.path.join(home_dir, ".alenia_nickname")
    if os.path.exists(nickname_file_path):
        try:
            with open(nickname_file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except:
            pass
    new_nickname = generate_nickname()
    try:
        with open(nickname_file_path, "w", encoding="utf-8") as f:
            f.write(new_nickname)
    except:
        pass
    return new_nickname

def set_local_nickname(nickname):
    home_dir = os.path.expanduser("~")
    nickname_file_path = os.path.join(home_dir, ".alenia_nickname")
    try:
        with open(nickname_file_path, "w", encoding="utf-8") as f:
            f.write(nickname)
        return True
    except:
        return False


def get_config_file_path():
    if os.name == "nt":
        local_app_data_path = os.getenv("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local")
        config_folder_path = os.path.join(local_app_data_path, "AleniaStudios", "AleniaPorter")
    else:
        config_folder_path = os.path.expanduser("~/.config/AleniaStudios/AleniaPorter")
    return os.path.join(config_folder_path, "config.json")

def get_cancel_flag_path():
    if os.name == "nt":
        local_app_data_path = os.getenv("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local")
        config_folder_path = os.path.join(local_app_data_path, "AleniaStudios", "AleniaPorter")
    else:
        config_folder_path = os.path.expanduser("~/.config/AleniaStudios/AleniaPorter")
    return os.path.join(config_folder_path, "alenia_porter_cancel.flag")

def get_telemetry_status():
    config_path = get_config_file_path()
    if not os.path.exists(config_path): return False
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f).get("telemetry_enabled", False)
        except:
            return False

def update_telemetry_stats(file_type, file_count, duration_seconds, headless=False):
    if not get_telemetry_status():
        return
    if not file_type or file_count <= 0:
        return
    try:
        import urllib.request
        import json
        import platform
        payload = {
            "uuid": get_local_uuid(),
            "nickname": get_local_nickname(),
            "os_family": platform.system(),
            "interface_type": "CLI" if headless else "IDE",
            "file_type": file_type,
            "file_count": file_count,
            "duration_seconds": duration_seconds
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://alenia-porter.onrender.com/telemetry/event",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read()
    except Exception as e:
        log_error_to_file(f"Telemetry error: {str(e)}")

def send_feedback_stats(rating, comments):
    if not get_telemetry_status():
        return False
    try:
        import urllib.request
        import json
        payload = {
            "uuid": get_local_uuid(),
            "nickname": get_local_nickname(),
            "rating": rating,
            "comments": comments
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://alenia-porter.onrender.com/telemetry/feedback",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read()
        return True
    except Exception as e:
        log_error_to_file(f"Feedback error: {str(e)}")
        return False

def get_system_ram_gb():
    try:
        if sys.platform.startswith("linux"):
            pages = os.sysconf('SC_PHYS_PAGES')
            page_size = os.sysconf('SC_PAGE_SIZE')
            return int((pages * page_size) / (1024 ** 3))
        elif sys.platform.startswith("darwin"):
            import subprocess
            mem = int(subprocess.check_output(['sysctl', '-n', 'hw.memsize']).strip())
            return int(mem / (1024 ** 3))
        elif os.name == "nt":
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                return int(stat.ullTotalPhys / (1024 ** 3))
    except Exception:
        pass
    return 8

def send_crash_report(error_code, message, stack_trace):
    if not get_telemetry_status():
        return
    try:
        import urllib.request
        import json
        import platform
        user_home = os.path.expanduser("~")
        if user_home and len(user_home) > 1:
            message = message.replace(user_home, "<USER_HOME>")
            stack_trace = stack_trace.replace(user_home, "<USER_HOME>")
            user_home_alt = user_home.replace("\\", "/")
            message = message.replace(user_home_alt, "<USER_HOME>")
            stack_trace = stack_trace.replace(user_home_alt, "<USER_HOME>")
            user_home_escaped = user_home.replace("\\", "\\\\")
            message = message.replace(user_home_escaped, "<USER_HOME>")
            stack_trace = stack_trace.replace(user_home_escaped, "<USER_HOME>")
        ram_gb = get_system_ram_gb()
        cpu_cores = os.cpu_count() or 1
        payload = {
            "uuid": get_local_uuid(),
            "nickname": get_local_nickname(),
            "app_version": "v5.9",
            "error_code": error_code,
            "message": message,
            "stack_trace": stack_trace,
            "system_metadata": {
                "os_family": platform.system(),
                "cpu_cores": cpu_cores,
                "ram_gb": ram_gb
            }
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://alenia-porter.onrender.com/telemetry/crash",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read()
    except Exception as e:
        log_error_to_file(f"Crash report telemetry error: {str(e)}")


@contextmanager
def resource_path(relative_path):
    relative_path = os.path.normpath(relative_path)
    resolved_path = None
    try:
        parts = relative_path.split(os.sep)
        resource = files('alenia_porter')
        for part in parts:
            resource = resource / part

        from importlib.resources import as_file
        with as_file(resource) as path:
            path_str = str(path)
            if os.path.exists(path_str):
                yield path_str
                return
    except Exception:
        pass

    if not resolved_path:
        if hasattr(sys, "frozen") or getattr(sys, "readlink", None) is None:
            exe_dir = os.path.dirname(sys.executable)
            candidate = os.path.join(exe_dir, "alenia_porter", relative_path)
            if os.path.exists(candidate):
                resolved_path = candidate
            else:
                candidate_direct = os.path.join(exe_dir, relative_path)
                if os.path.exists(candidate_direct):
                    resolved_path = candidate_direct

    if not resolved_path:
        base_path = os.path.dirname(os.path.abspath(__file__))
        candidate = os.path.join(base_path, relative_path)
        if os.path.exists(candidate):
            resolved_path = candidate
        else:
            resolved_path = candidate

    yield resolved_path

_locales_error_shown = False

def load_locales():
    global _locales_error_shown
    data = None
    with resource_path(os.path.join("assets", "locales", "locales.json")) as locales_file_path:
        if os.path.exists(locales_file_path):
            try:
                with open(locales_file_path, "r", encoding="utf-8") as file_handle:
                    data = json.load(file_handle)
            except Exception:
                pass
    if data:
        return data

    if not _locales_error_shown:
        _locales_error_shown = True
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            title = "Alenia Porter - Error"
            message = (
                "Error de inicializacion de Alenia Porter:\n"
                "No se encontraron los recursos necesarios (locales.json).\n\n"
                "Esto ocurre si la instalacion esta corrupta o si quedan archivos de versiones anteriores (v5.7) en esta carpeta.\n\n"
                "Solucion:\n"
                "1. Cierre el programa.\n"
                "2. Borre los archivos de esta carpeta.\n"
                "3. Descargue e instale una copia limpia de la v5.9 desde GitHub o Itch.io.\n\n"
                "--------------------------------------------------\n\n"
                "Initialization Error:\n"
                "Required resources (locales.json) were not found.\n\n"
                "This occurs if the installation is corrupt or older v5.7 files remain in this folder.\n\n"
                "Solution:\n"
                "1. Close the program.\n"
                "2. Delete all files in this folder.\n"
                "3. Download and install a clean copy of v5.9 from GitHub or Itch.io."
            )
            messagebox.showerror(title, message)
            root.destroy()
        except Exception:
            sys.stderr.write("Error: Could not load locales.json. Please clean the directory and download the latest version from GitHub/Itch.io.\n")

    fallback = {
        "en": {
            "title": "Alenia Porter v5.9",
            "header": "Alenia Studios - Media Optimizer",
            "select_format": "Export to:",
            "format_ogg": "OGG",
            "format_opus": "OPUS",
            "btn_select": "Select Folder to Convert",
            "info_wait": "Processing files... Please wait.",
            "info_desc": "Ready.",
            "msg_done": "Done! {} files processed.",
            "msg_err": "Error in conversion.",
            "msg_success_t": "Success",
            "msg_success_m": "Optimized {} files!\n\nPath: {}",
            "btn_lang": "ES",
            "btn_patreon": "☕ Support Alenia",
            "formats_title": "Supported Formats",
            "formats_info": "🖼️ IMAGES:\n.png, .jpg, .jpeg, .bmp, .tga, .webp\n\n🎬 VIDEO:\n.mp4, .mkv, .webm, .avi, .mov, .wmv, .flv, .m4v, .mpg, .mpeg, .m2v, .3gp, .3g2, .ts, .m2ts, .vob, .ogv, .asf, .divx\n\n🎵 AUDIO:\n.wav, .mp3, .flac, .m4a, .ogg, .opus, .aac, .wma, .aiff, .aif, .alac, .amr, .mid, .midi, .mp2, .mpga, .au, .snd, .ra, .rm",
            "update_available_title": "Update Available",
            "update_available_desc": "Version {} is available. Do you want to update now?",
            "update_downloading": "Downloading update...",
            "support_title": "Support Alenia Studios",
            "support_label": "Support us on:",
            "formats_images": "🖼️ IMAGES:",
            "formats_videos": "🎬 VIDEO:",
            "formats_audio": "🎵 AUDIO:",
            "btn_select_folder": "Select Folder",
            "btn_files": "Select Files",
            "btn_cancel": "Cancel",
            "info_cancelling": "Cancelling..."
        },
        "es": {
            "title": "Alenia Porter v5.9",
            "header": "Alenia Studios - Optimizador de Medios",
            "select_format": "Exportar a:",
            "format_ogg": "OGG",
            "format_opus": "OPUS",
            "btn_select": "Seleccionar Directorio a Convertir",
            "info_wait": "Procesando archivos... Por favor espera.",
            "info_desc": "Listo.",
            "msg_done": "¡Listo! {} archivos procesados.",
            "msg_err": "Error en la conversión.",
            "msg_success_t": "¡Éxito!",
            "msg_success_m": "¡{} archivos optimizados!\n\nRuta: {}",
            "btn_lang": "FR",
            "btn_patreon": "☕ Apoyar a Alenia",
            "formats_title": "Formatos Soportados",
            "formats_info": "🖼️ IMÁGENES:\n.png, .jpg, .jpeg, .bmp, .tga, .webp\n\n🎬 VIDEO:\n.mp4, .mkv, .webm, .avi, .mov, .wmv, .flv, .m4v, .mpg, .mpeg, .m2v, .3gp, .3g2, .ts, .m2ts, .vob, .ogv, .asf, .divx\n\n🎵 AUDIO:\n.wav, .mp3, .flac, .m4a, .ogg, .opus, .aac, .wma, .aiff, .aif, .alac, .amr, .mid, .midi, .mp2, .mpga, .au, .snd, .ra, .rm",
            "update_available_title": "Actualización Disponible",
            "update_available_desc": "La versión {} está disponible. ¿Deseas actualizar ahora?",
            "update_downloading": "Descargando actualización...",
            "support_title": "Apoyar a Alenia Studios",
            "support_label": "Apóyanos en:",
            "formats_images": "🖼️ IMÁGENES:",
            "formats_videos": "🎬 VIDEO:",
            "formats_audio": "🎵 AUDIO:",
            "btn_select_folder": "Seleccionar Carpeta",
            "btn_files": "Seleccionar Archivos",
            "btn_cancel": "Cancelar",
            "info_cancelling": "Cancelando..."
        }
    }
    return fallback

def get_ffmpeg_path():
    if os.name == "nt":
        with resource_path(os.path.join("bin", "ffmpeg.exe")) as exe_path:
            if os.path.exists(exe_path):
                return exe_path
        with resource_path(os.path.join("bin", "ffmpeg.EXE")) as exe_path_upper:
            if os.path.exists(exe_path_upper):
                return exe_path_upper
        return "ffmpeg.exe"
    else:
        with resource_path(os.path.join("bin", "ffmpeg")) as exe_path:
            if os.path.exists(exe_path):
                return exe_path
        return "ffmpeg"

def setup_logger():
    log_dir = os.path.dirname(get_config_file_path())
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "porter.log")
    
    logger = logging.getLogger("AleniaPorter")
    logger.setLevel(logging.ERROR)
    if not logger.handlers:
        handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def log_error_to_file(error_message):
    try:
        logger = setup_logger()
        logger.error(error_message)
    except Exception:
        pass
