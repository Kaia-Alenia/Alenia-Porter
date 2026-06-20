__license__ = """
ALENIA STUDIOS TOOL LICENSE Version 1.0 Copyright (c) 2026 Alenia Studios This tool is designed to be free and accessible for the indie developer community. By using this software, you agree to the following terms: 1. OUTPUT OWNERSHIP & USE: The audio, video, or data files processed by this Software remain 100% your property. No attribution to Alenia Studios is required in your final project for simply using this tool to process your files. 2. ALWAYS FREE & SPREAD THE WORD: This Software is completely free for commercial and non-commercial projects. If you find it useful, we strongly encourage you to recommend it to other developers. 3. CODE ATTRIBUTION: If you modify, fork, or distribute the source code of this Software, you must provide appropriate credit to Alenia Studios and the respective community translators. 4. NO RESALE: Standalone redistribution, sublicensing, or resale of this Software or its source code for profit is strictly prohibited. It must remain free. 5. NO AI TRAINING: The source code, documentation, and logic of this Software may not be used, scraped, or included in datasets for the training of Artificial Intelligence models or machine learning algorithms. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
"""
import concurrent.futures
import re
from importlib.resources import files
from contextlib import contextmanager

from alenia_porter import zenith

import sys
import os
import json
import traceback
import subprocess

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

def update_telemetry_stats(file_type, file_count, headless=False):
    if not file_type or file_count <= 0:
        return
    try:
        import urllib.request
        import json
        import platform
        payload = {
            "uuid": get_local_uuid(),
            "os_family": platform.system(),
            "interface_type": "CLI" if headless else "IDE",
            "file_type": file_type,
            "file_count": file_count
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://alenia-porter-telemetry.onrender.com/telemetry/event",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read()
    except Exception as e:
        log_error_to_file(f"Telemetry error: {str(e)}")

@contextmanager
def resource_path(relative_path):
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
                resolved_path = path_str
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
                "3. Descargue e instale una copia limpia de la v5.8 desde GitHub o Itch.io.\n\n"
                "--------------------------------------------------\n\n"
                "Initialization Error:\n"
                "Required resources (locales.json) were not found.\n\n"
                "This occurs if the installation is corrupt or older v5.7 files remain in this folder.\n\n"
                "Solution:\n"
                "1. Close the program.\n"
                "2. Delete all files in this folder.\n"
                "3. Download and install a clean copy of v5.8 from GitHub or Itch.io."
            )
            messagebox.showerror(title, message)
            root.destroy()
        except Exception:
            sys.stderr.write("Error: Could not load locales.json. Please clean the directory and download the latest version from GitHub/Itch.io.\n")

    fallback = {
        "en": {
            "title": "Alenia Porter v5.8",
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
            "formats_audio": "🎵 AUDIO:"
        },
        "es": {
            "title": "Alenia Porter v5.8",
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
            "formats_audio": "🎵 AUDIO:"
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
    return "ffmpeg"

def log_error_to_file(error_message):
    try:
        with open("ALENIA_ERROR.txt", "a", encoding="utf-8") as file_handle:
            file_handle.write(f"\n--- ERROR ---\n{error_message}\n")
    except Exception:
        pass

def stream_files(directory, base_directory, audio_exts, video_exts, image_exts):
    try:
        for entry in os.scandir(directory):
            if entry.is_dir():
                if entry.name != "Alenia_Optimized":
                    yield from stream_files(entry.path, base_directory, audio_exts, video_exts, image_exts)
            elif entry.is_file():
                name_lower = entry.name.lower()
                if name_lower.endswith(audio_exts):
                    rel = os.path.relpath(entry.path, base_directory)
                    yield (entry.path, rel, "audio")
                elif name_lower.endswith(video_exts):
                    rel = os.path.relpath(entry.path, base_directory)
                    yield (entry.path, rel, "video")
                elif name_lower.endswith(image_exts):
                    rel = os.path.relpath(entry.path, base_directory)
                    yield (entry.path, rel, "image")
    except Exception:
        pass

def process_single_file_top_level(file_info, target_audio_format, audio_output_directory, video_output_directory, image_output_directory, ffmpeg_executable_path, subprocess_creation_flags):
    absolute_path, relative_path, media_type = file_info
    cleaned_base_name = os.path.splitext(relative_path)[0].replace(os.sep, "_")
    cleaned_base_name = re.sub(r'[^a-zA-Z0-9_]', '_', cleaned_base_name).lower()
    
    orig_size = os.path.getsize(absolute_path)
    ffmpeg_command = []
    output_file_path = ""
    output_file_name = ""

    if media_type == "video":
        if not os.path.exists(video_output_directory):
            os.makedirs(video_output_directory, exist_ok=True)
        output_file_name = f"{cleaned_base_name}.webm"
        output_file_path = os.path.join(video_output_directory, output_file_name)
        ffmpeg_command = [
            ffmpeg_executable_path, "-y", "-i", absolute_path,
            "-map_metadata", "-1", "-metadata", "software=Optimized in Alenia Porter",
            "-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0",
            "-cpu-used", "4", "-row-mt", "1",
            "-c:a", "libopus", "-b:a", "128k",
            "-threads", "1",
            output_file_path
        ]
    elif media_type == "image":
        if not os.path.exists(image_output_directory):
            os.makedirs(image_output_directory, exist_ok=True)
        output_file_name = f"{cleaned_base_name}.webp"
        output_file_path = os.path.join(image_output_directory, output_file_name)
        ffmpeg_command = [
            ffmpeg_executable_path, "-y", "-i", absolute_path,
            "-map_metadata", "-1", "-metadata", "software=Optimized in Alenia Porter",
            "-c:v", "libwebp", "-quality", "80",
            output_file_path
        ]
    else:
        if not os.path.exists(audio_output_directory):
            os.makedirs(audio_output_directory, exist_ok=True)
        output_file_name = f"{cleaned_base_name}.{target_audio_format}"
        output_file_path = os.path.join(audio_output_directory, output_file_name)
        if target_audio_format == "ogg":
            ffmpeg_command = [
                ffmpeg_executable_path, "-y", "-i", absolute_path,
                "-map_metadata", "-1", "-metadata", "software=Optimized in Alenia Porter",
                "-c:a", "libvorbis", "-b:a", "192k",
                "-threads", "1",
                output_file_path
            ]
        else:
            ffmpeg_command = [
                ffmpeg_executable_path, "-y", "-i", absolute_path,
                "-map_metadata", "-1", "-metadata", "software=Optimized in Alenia Porter",
                "-c:a", "libopus", "-b:a", "128k",
                "-threads", "1",
                output_file_path
            ]

    try:
        process_handle = subprocess.Popen(
            ffmpeg_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess_creation_flags
        )
        process_handle.communicate()
        final_size = os.path.getsize(output_file_path)
        return (media_type, cleaned_base_name, output_file_name, orig_size, final_size, True, None)
    except Exception as e:
        return (media_type, cleaned_base_name, output_file_name, orig_size, 0, False, str(e))

def convert_media(input_directory, target_audio_format, progress_update_callback, status_update_callback, completion_callback, error_callback, lang_code="es", headless=False):
    try:
        audio_extensions = (".wav", ".mp3", ".flac", ".m4a", ".ogg", ".opus", ".aac", ".wma", ".aiff", ".aif", ".alac", ".amr", ".mid", ".midi", ".mp2", ".mpga", ".au", ".snd", ".ra", ".rm")
        video_extensions = (".mp4", ".mkv", ".webm", ".avi", ".mov", ".wmv", ".flv", ".m4v", ".mpg", ".mpeg", ".m2v", ".3gp", ".3g2", ".ts", ".m2ts", ".vob", ".ogv", ".asf", ".divx")
        image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".tga", ".webp")
        
        total_files_count = 0
        file_generator = stream_files(input_directory, input_directory, audio_extensions, video_extensions, image_extensions)
        for _ in file_generator:
            total_files_count += 1

        if total_files_count == 0:
            completion_callback(0, input_directory, 0, 0)
            return

        target_folder_name = "Alenia_Optimized"
        output_directory_path = os.path.join(input_directory, target_folder_name)
        audio_output_directory = os.path.join(output_directory_path, "audio")
        video_output_directory = os.path.join(output_directory_path, "video")
        image_output_directory = os.path.join(output_directory_path, "images")

        ffmpeg_executable_path = get_ffmpeg_path()
        subprocess_creation_flags = 0
        if os.name == "nt":
            subprocess_creation_flags = 0x08000000

        godot_audio_defines = []
        godot_video_defines = []
        godot_image_defines = []

        total_original_size = 0
        total_final_size = 0
        processed_files_count = 0

        file_generator = stream_files(input_directory, input_directory, audio_extensions, video_extensions, image_extensions)
        max_workers = max(1, os.cpu_count() - 1)
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    process_single_file_top_level,
                    file_info,
                    target_audio_format,
                    audio_output_directory,
                    video_output_directory,
                    image_output_directory,
                    ffmpeg_executable_path,
                    subprocess_creation_flags
                ): file_info for file_info in file_generator
            }

            for future in concurrent.futures.as_completed(futures):
                media_type, cleaned_base_name, output_file_name, orig_size, final_size, success, error_msg = future.result()
                if success:
                    total_original_size += orig_size
                    total_final_size += final_size
                    if media_type == "video":
                        godot_video_defines.append(f"    \"{cleaned_base_name}\": preload(\"res://video/{output_file_name}\"),")
                    elif media_type == "image":
                        godot_image_defines.append(f"    \"{cleaned_base_name}\": preload(\"res://images/{output_file_name}\"),")
                    else:
                        godot_audio_defines.append(f"    \"{cleaned_base_name}\": preload(\"res://audio/{output_file_name}\"),")
                else:
                    if error_msg:
                        log_error_to_file(error_msg)

                processed_files_count += 1
                progress_update_callback(processed_files_count, total_files_count)

        godot_registry_lines = []
        godot_registry_lines.append("extends Node\n")
        godot_registry_lines.append("const TRACKS: Dictionary = {")
        godot_registry_lines.extend(godot_audio_defines)
        godot_registry_lines.append("}\n")
        godot_registry_lines.append("const VIDEOS: Dictionary = {")
        godot_registry_lines.extend(godot_video_defines)
        godot_registry_lines.append("}\n")
        godot_registry_lines.append("const IMAGES: Dictionary = {")
        godot_registry_lines.extend(godot_image_defines)
        godot_registry_lines.append("}\n")
        godot_registry_lines.append("func play_track(player: AudioStreamPlayer, track_name: String) -> void:")
        godot_registry_lines.append("    if TRACKS.has(track_name):")
        godot_registry_lines.append("        player.stream = TRACKS[track_name]")
        godot_registry_lines.append("        player.play()")
        godot_registry_lines.append("    else:")
        godot_registry_lines.append("        push_error('Alenia Error: Track ' + track_name + ' not found')\n")
        godot_registry_lines.append("func play_video(player: VideoStreamPlayer, video_name: String) -> void:")
        godot_registry_lines.append("    if VIDEOS.has(video_name):")
        godot_registry_lines.append("        player.stream = VIDEOS[video_name]")
        godot_registry_lines.append("        player.play()")
        godot_registry_lines.append("    else:")
        godot_registry_lines.append("        push_error('Alenia Error: Video ' + video_name + ' not found')\n")
        godot_registry_lines.append("func get_image(image_name: String) -> Texture2D:")
        godot_registry_lines.append("    if IMAGES.has(image_name):")
        godot_registry_lines.append("        return IMAGES[image_name]")
        godot_registry_lines.append("    else:")
        godot_registry_lines.append("        push_error('Alenia Error: Image ' + image_name + ' not found')")
        godot_registry_lines.append("        return null")
        
        with open(os.path.join(output_directory_path, "MediaRegistry.gd"), "w", encoding="utf-8") as file_handle:
            file_handle.write("\n".join(godot_registry_lines))

        if len(godot_audio_defines) > 0:
            update_telemetry_stats("audio", len(godot_audio_defines), headless)
        if len(godot_video_defines) > 0:
            update_telemetry_stats("video", len(godot_video_defines), headless)
        if len(godot_image_defines) > 0:
            update_telemetry_stats("image", len(godot_image_defines), headless)

        completion_callback(processed_files_count, output_directory_path, total_original_size, total_final_size)

    except Exception as conversion_exception:
        exception_traceback = traceback.format_exc()
        log_error_to_file(exception_traceback)
        error_callback(str(conversion_exception))
