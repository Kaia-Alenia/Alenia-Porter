__license__ = """
ALENIA STUDIOS TOOL LICENSE Version 1.0 Copyright (c) 2026 Alenia Studios This tool is designed to be free and accessible for the indie developer community. By using this software, you agree to the following terms: 1. OUTPUT OWNERSHIP & USE: The audio, video, or data files processed by this Software remain 100% your property. No attribution to Alenia Studios is required in your final project for simply using this tool to process your files. 2. ALWAYS FREE & SPREAD THE WORD: This Software is completely free for commercial and non-commercial projects. If you find it useful, we strongly encourage you to recommend it to other developers. 3. CODE ATTRIBUTION: If you modify, fork, or distribute the source code of this Software, you must provide appropriate credit to Alenia Studios and the respective community translators. 4. NO RESALE: Standalone redistribution, sublicensing, or resale of this Software or its source code for profit is strictly prohibited. It must remain free. 5. NO AI TRAINING: The source code, documentation, and logic of this Software may not be used, scraped, or included in datasets for the training of Artificial Intelligence models or machine learning algorithms. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
"""
import concurrent.futures

from alenia_porter import zenith

import sys
import os
import json
import subprocess
import traceback

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def load_locales():
    locales_file_path = resource_path(os.path.join("assets", "locales", "locales.json"))
    if os.path.exists(locales_file_path):
        try:
            with open(locales_file_path, "r", encoding="utf-8") as file_handle:
                data = json.load(file_handle)
                if data: return data
        except Exception:
            pass
    return {
        "en": {"title": "Alenia Porter v5.7", "header": "Alenia Studios - Media Optimizer", "btn_lang": "ES"},
        "es": {"title": "Alenia Porter v5.7", "header": "Alenia Studios - Optimizador de Medios", "btn_lang": "EN"}
    }

def get_ffmpeg_path():
    if os.name == "nt":
        exe_path = resource_path(os.path.join("bin", "ffmpeg.exe"))
        if os.path.exists(exe_path):
            return exe_path
        exe_path_upper = resource_path(os.path.join("bin", "ffmpeg.EXE"))
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

def convert_media(input_directory, target_engine, target_audio_format, progress_update_callback, status_update_callback, completion_callback, error_callback, lang_code="es"):
    try:
        audio_extensions = (".wav", ".mp3", ".flac", ".m4a", ".ogg", ".opus", ".aac", ".wma", ".aiff", ".aif", ".alac", ".amr", ".mid", ".midi", ".mp2", ".mpga", ".au", ".snd", ".ra", ".rm")
        video_extensions = (".mp4", ".mkv", ".webm", ".avi", ".mov", ".wmv", ".flv", ".m4v", ".mpg", ".mpeg", ".m2v", ".3gp", ".3g2", ".ts", ".m2ts", ".vob", ".ogv", ".asf", ".divx")
        image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".tga", ".webp")
        
        media_files_list = []
        for root_path, sub_directories, files_list in os.walk(input_directory):
            sub_directories[:] = [dir_name for dir_name in sub_directories if dir_name not in ["Alenia_RenPy_Ready", "Alenia_Godot_Ready"]]
            for file_name in files_list:
                file_name_lower = file_name.lower()
                if file_name_lower.endswith(audio_extensions):
                    absolute_file_path = os.path.join(root_path, file_name)
                    relative_file_path = os.path.relpath(absolute_file_path, input_directory)
                    media_files_list.append((absolute_file_path, relative_file_path, "audio"))
                elif file_name_lower.endswith(video_extensions):
                    absolute_file_path = os.path.join(root_path, file_name)
                    relative_file_path = os.path.relpath(absolute_file_path, input_directory)
                    media_files_list.append((absolute_file_path, relative_file_path, "video"))
                elif file_name_lower.endswith(image_extensions):
                    absolute_file_path = os.path.join(root_path, file_name)
                    relative_file_path = os.path.relpath(absolute_file_path, input_directory)
                    media_files_list.append((absolute_file_path, relative_file_path, "image"))
        
        total_files_count = len(media_files_list)
        if total_files_count == 0:
            completion_callback(0, input_directory)
            return

        target_folder_name = "Alenia_RenPy_Ready" if target_engine == "renpy" else "Alenia_Godot_Ready"
        output_directory_path = os.path.join(input_directory, target_folder_name)
        audio_output_directory = os.path.join(output_directory_path, "audio")
        video_output_directory = os.path.join(output_directory_path, "video")
        image_output_directory = os.path.join(output_directory_path, "images")

        ffmpeg_executable_path = get_ffmpeg_path()
        subprocess_creation_flags = 0
        if os.name == "nt":
            subprocess_creation_flags = 0x08000000

        renpy_audio_defines = []
        renpy_video_defines = []
        godot_audio_defines = []
        godot_video_defines = []
        godot_image_defines = []


        import threading
        import concurrent.futures
        
        lock = threading.Lock()
        total_original_size = 0
        total_final_size = 0
        processed_files_count = 0

        def process_single_file(file_info):
            nonlocal processed_files_count, total_original_size, total_final_size
            absolute_path, relative_path, media_type = file_info
            cleaned_base_name = os.path.splitext(relative_path)[0].replace(os.sep, "_").replace(" ", "_").lower()
            
            orig_size = os.path.getsize(absolute_path)
            ffmpeg_command = []
            output_file_path = ""

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
                    output_file_path
                ]
                with lock:
                    if target_engine == "renpy":
                        renpy_video_defines.append(f"image {cleaned_base_name} = Movie(play=\"video/{output_file_name}\")")
                    else:
                        godot_video_defines.append(f"    \"{cleaned_base_name}\": preload(\"res://video/{output_file_name}\"),")
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
                with lock:
                    if target_engine != "renpy":
                        godot_image_defines.append(f"    \"{cleaned_base_name}\": preload(\"res://images/{output_file_name}\"),")
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
                        output_file_path
                    ]
                else:
                    ffmpeg_command = [
                        ffmpeg_executable_path, "-y", "-i", absolute_path,
                        "-map_metadata", "-1", "-metadata", "software=Optimized in Alenia Porter",
                        "-c:a", "libopus", "-b:a", "128k",
                        output_file_path
                    ]
                with lock:
                    if target_engine == "renpy":
                        renpy_audio_defines.append(f"define audio.{cleaned_base_name} = \"audio/{output_file_name}\"")
                    else:
                        godot_audio_defines.append(f"    \"{cleaned_base_name}\": preload(\"res://audio/{output_file_name}\"),")

            try:
                process_handle = subprocess.Popen(
                    ffmpeg_command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess_creation_flags
                )
                process_handle.communicate()
                
                final_size = os.path.getsize(output_file_path)
                with lock:
                    total_original_size += orig_size
                    total_final_size += final_size
                    processed_files_count += 1
                    progress_update_callback(processed_files_count, total_files_count)
            except Exception as e:
                log_error_to_file(f"Error processing {absolute_path}: {str(e)}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            list(executor.map(process_single_file, media_files_list))

        locales_dict = load_locales()
        current_locale = locales_dict.get(lang_code, locales_dict.get("es", {}))
        filename = current_locale.get("instructions_filename", "ALENIA_INSTRUCTIONS.txt")

        instructions_file_path = os.path.join(output_directory_path, filename)
        with open(instructions_file_path, "w", encoding="utf-8") as instructions_file:
            instructions_title = current_locale.get("instructions_title", "ALENIA PORTER - QUICK GUIDE")
            instructions_file.write(f"{instructions_title} ({target_engine.upper()})\n")
            instructions_file.write("=" * 70 + "\n\n")
            if target_engine == "godot":
                instructions_content = current_locale.get("instructions_godot", "")
            else:
                instructions_content = current_locale.get("instructions_renpy", "")
            instructions_file.write(instructions_content + "\n")

        if target_engine == "renpy":
            if renpy_audio_defines:
                with open(os.path.join(output_directory_path, "audio_defines.rpy"), "w", encoding="utf-8") as file_handle:
                    file_handle.write("\n".join(renpy_audio_defines))
            if renpy_video_defines:
                with open(os.path.join(output_directory_path, "video_defines.rpy"), "w", encoding="utf-8") as file_handle:
                    file_handle.write("\n".join(renpy_video_defines))
        else:
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

        completion_callback(processed_files_count, output_directory_path, total_original_size, total_final_size)

    except Exception as conversion_exception:
        exception_traceback = traceback.format_exc()
        log_error_to_file(exception_traceback)
        error_callback(str(conversion_exception))
