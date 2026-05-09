import sys
import os
import json
import subprocess
import traceback

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_locales():
    locales_file_path = resource_path(os.path.join("locales", "locales.json"))
    if os.path.exists(locales_file_path):
        try:
            with open(locales_file_path, "r", encoding="utf-8") as file_handle:
                return json.load(file_handle)
        except Exception:
            pass
    return {
        "en": {
            "title": "Alenia Porter v3.0",
            "header": "Alenia Studios - Media Optimizer",
            "select_format": "Export audio to:",
            "format_ogg": "OGG (Standard)",
            "format_opus": "OPUS (High Comp)",
            "select_engine": "Target Engine:",
            "btn_select": "Select Folder to Convert",
            "info_wait": "Processing files... Please wait.",
            "info_desc": "Supports audio and video (MP4, MKV, WebM, AVI, MOV)",
            "msg_done": "Done! {} files processed.",
            "msg_err": "Error in conversion.",
            "msg_success_t": "Success",
            "msg_success_m": "Optimized {} files for {}!\n\nPath: {}\n\nInstructions opened.",
            "btn_lang": "ES",
            "btn_patreon": "☕ Support Alenia"
        },
        "es": {
            "title": "Alenia Porter v3.0",
            "header": "Alenia Studios - Optimizador de Medios",
            "select_format": "Exportar audio en:",
            "format_ogg": "OGG (Estándar)",
            "format_opus": "OPUS (Alta Compresión)",
            "select_engine": "Motor de Destino:",
            "btn_select": "Seleccionar Directorio a Convertir",
            "info_wait": "Procesando archivos... Por favor espera.",
            "info_desc": "Soporta audio y video (MP4, MKV, WebM, AVI, MOV)",
            "msg_done": "¡Listo! {} archivos procesados.",
            "msg_err": "Error en la conversión.",
            "msg_success_t": "¡Éxito!",
            "msg_success_m": "¡{} archivos optimizados para {}!\n\nRuta: {}\n\nInstrucciones abiertas.",
            "btn_lang": "FR",
            "btn_patreon": "☕ Apoyar a Alenia"
        },
        "fr": {
            "title": "Alenia Porter v3.0",
            "header": "Alenia Studios - Optimiseur de Médias",
            "select_format": "Exporter l'audio en :",
            "format_ogg": "OGG (Standard)",
            "format_opus": "OPUS (Haute Comp.)",
            "select_engine": "Moteur de Destination :",
            "btn_select": "Sélectionner le Dossier à Convertir",
            "info_wait": "Traitement des fichiers... Veuillez patienter.",
            "info_desc": "Prend en charge l'audio et la vidéo (MP4, MKV, WebM, AVI, MOV)",
            "msg_done": "Terminé ! {} fichiers traités.",
            "msg_err": "Erreur lors de la conversion.",
            "msg_success_t": "Succès",
            "msg_success_m": "Optimisation de {} fichiers pour {} réussie !\n\nChemin : {}\n\nInstructions ouvertes.",
            "btn_lang": "JA",
            "btn_patreon": "☕ Soutenir Alenia"
        },
        "ja": {
            "title": "Alenia Porter v3.0",
            "header": "Alenia Studios - メディアオプティマイザー",
            "select_format": "オーディオ書き出し形式:",
            "format_ogg": "OGG (標準)",
            "format_opus": "OPUS (高圧縮)",
            "select_engine": "対象エンジン:",
            "btn_select": "変換するフォルダを選択",
            "info_wait": "ファイルを処理中... しばらくお待ちください。",
            "info_desc": "オーディオおよびビデオをサポート (MP4, MKV, WebM, AVI, MOV)",
            "msg_done": "完了しました！{} 個のファイルを処理しました。",
            "msg_err": "変換エラー。",
            "msg_success_t": "成功",
            "msg_success_m": "{} 個のファイルを {} 向けに最適化しました！\n\nパス: {}\n\n説明書を開きました。",
            "btn_lang": "ZH",
            "btn_patreon": "☕ Alenia を支援する"
        },
        "zh": {
            "title": "Alenia Porter v3.0",
            "header": "Alenia Studios - 媒体优化器",
            "select_format": "音频导出格式:",
            "format_ogg": "OGG (标准)",
            "format_opus": "OPUS (高压缩)",
            "select_engine": "目标引擎:",
            "btn_select": "选择要转换的文件夹",
            "info_wait": "正在处理文件... 请稍候。",
            "info_desc": "支持音频与视频 (MP4, MKV, WebM, AVI, MOV)",
            "msg_done": "完成！已处理 {} 个文件。",
            "msg_err": "转换出错。",
            "msg_success_t": "成功",
            "msg_success_m": "已为 {} 优化了 {} 个文件！\n\n路径: {}\n\n已打开说明文档。",
            "btn_lang": "EN",
            "btn_patreon": "☕ 支持 Alenia"
        }
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

def convert_media(input_directory, target_engine, target_audio_format, progress_update_callback, status_update_callback, completion_callback, error_callback):
    try:
        audio_extensions = (".wav", ".mp3", ".flac", ".m4a", ".ogg", ".opus", ".aac", ".wma")
        video_extensions = (".mp4", ".mkv", ".webm", ".avi", ".mov")
        
        media_files_list = []
        for root_path, sub_directories, files_list in os.walk(input_directory):
            sub_directories[:] = [dir_name for dir_name in sub_directories if dir_name not in ["Alenia_RenPy_Ready", "Alenia_Godot_Ready"]]
            for file_name in files_list:
                file_name_lower = file_name.lower()
                if file_name_lower.endswith(audio_extensions) or file_name_lower.endswith(video_extensions):
                    absolute_file_path = os.path.join(root_path, file_name)
                    relative_file_path = os.path.relpath(absolute_file_path, input_directory)
                    is_video_file = file_name_lower.endswith(video_extensions)
                    media_files_list.append((absolute_file_path, relative_file_path, is_video_file))
        
        total_files_count = len(media_files_list)
        if total_files_count == 0:
            completion_callback(0, input_directory)
            return

        target_folder_name = "Alenia_RenPy_Ready" if target_engine == "renpy" else "Alenia_Godot_Ready"
        output_directory_path = os.path.join(input_directory, target_folder_name)
        audio_output_directory = os.path.join(output_directory_path, "audio")
        video_output_directory = os.path.join(output_directory_path, "video")

        ffmpeg_executable_path = get_ffmpeg_path()
        subprocess_creation_flags = 0
        if os.name == "nt":
            subprocess_creation_flags = 0x08000000

        renpy_audio_defines = []
        renpy_video_defines = []
        godot_audio_defines = []
        godot_video_defines = []

        processed_files_count = 0
        for absolute_path, relative_path, is_video in media_files_list:
            cleaned_base_name = os.path.splitext(relative_path)[0].replace(os.sep, "_").replace(" ", "_").lower()
            
            if is_video:
                if not os.path.exists(video_output_directory):
                    os.makedirs(video_output_directory)
                output_file_name = f"{cleaned_base_name}.webm"
                output_file_path = os.path.join(video_output_directory, output_file_name)
                ffmpeg_command = [
                    ffmpeg_executable_path, "-y", "-i", absolute_path,
                    "-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0",
                    "-cpu-used", "4", "-row-mt", "1",
                    "-c:a", "libopus", "-b:a", "128k",
                    output_file_path
                ]
                
                if target_engine == "renpy":
                    renpy_video_defines.append(f'image {cleaned_base_name} = Movie(play="video/{output_file_name}")')
                else:
                    godot_video_defines.append(f'    "{cleaned_base_name}": preload("res://video/{output_file_name}"),')
            else:
                if not os.path.exists(audio_output_directory):
                    os.makedirs(audio_output_directory)
                output_file_name = f"{cleaned_base_name}.{target_audio_format}"
                output_file_path = os.path.join(audio_output_directory, output_file_name)
                if target_audio_format == "ogg":
                    ffmpeg_command = [
                        ffmpeg_executable_path, "-y", "-i", absolute_path,
                        "-c:a", "libvorbis", "-b:a", "192k",
                        output_file_path
                    ]
                else:
                    ffmpeg_command = [
                        ffmpeg_executable_path, "-y", "-i", absolute_path,
                        "-c:a", "libopus", "-b:a", "128k",
                        output_file_path
                    ]
                
                if target_engine == "renpy":
                    renpy_audio_defines.append(f'define audio.{cleaned_base_name} = "audio/{output_file_name}"')
                else:
                    godot_audio_defines.append(f'    "{cleaned_base_name}": preload("res://audio/{output_file_name}"),')

            process_handle = subprocess.Popen(
                ffmpeg_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess_creation_flags
            )
            process_handle.communicate()

            processed_files_count += 1
            progress_update_callback(processed_files_count, total_files_count)

        instructions_file_path = os.path.join(output_directory_path, "INSTRUCCIONES_ALENIA.txt")
        with open(instructions_file_path, "w", encoding="utf-8") as instructions_file:
            instructions_file.write(f"ALENIA PORTER - QUICK GUIDE / GUÍA RÁPIDA ({target_engine.upper()})\n")
            instructions_file.write("=" * 70 + "\n\n")
            if target_engine == "godot":
                instructions_file.write("[ENGLISH]\n1. Setup: Project -> Project Settings -> Globals (Autoload).\n")
                instructions_file.write("2. Add 'AudioRegistry.gd' as 'Audio'.\n")
                instructions_file.write("3. CODE EXAMPLE:\n")
                instructions_file.write("   func _ready():\n")
                instructions_file.write("       Audio.play_track($AudioStreamPlayer, 'track_name')\n")
                instructions_file.write("       Audio.play_video($VideoStreamPlayer, 'video_name')\n\n")
                instructions_file.write("[ESPAÑOL]\n1. Configuración: Proyecto -> Ajustes del Proyecto -> Globales (Autoload).\n")
                instructions_file.write("2. Añade 'AudioRegistry.gd' con el nombre 'Audio'.\n")
                instructions_file.write("3. EJEMPLO DE CÓDIGO:\n")
                instructions_file.write("   func _ready():\n")
                instructions_file.write("       Audio.play_track($AudioStreamPlayer, 'nombre_pista')\n")
                instructions_file.write("       Audio.play_video($VideoStreamPlayer, 'nombre_video')\n")
            else:
                instructions_file.write("[ENGLISH]\n1. Copy files to your /game folder.\n")
                instructions_file.write("2. CODE EXAMPLE:\n   label start:\n       play audio track_name\n")
                instructions_file.write("       show movie_name\n\n")
                instructions_file.write("[ESPAÑOL]\n1. Copia los archivos a tu carpeta /game.\n")
                instructions_file.write("2. EJEMPLO DE CÓDIGO:\n   label start:\n       play audio nombre_pista\n")
                instructions_file.write("       show nombre_video\n")

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
            godot_registry_lines.append("const TRACKS = {")
            godot_registry_lines.extend(godot_audio_defines)
            godot_registry_lines.append("}\n")
            godot_registry_lines.append("const VIDEOS = {")
            godot_registry_lines.extend(godot_video_defines)
            godot_registry_lines.append("}\n")
            godot_registry_lines.append("func play_track(player, track_name: String):")
            godot_registry_lines.append("    if TRACKS.has(track_name):")
            godot_registry_lines.append("        player.stream = TRACKS[track_name]")
            godot_registry_lines.append("        player.play()")
            godot_registry_lines.append("    else:")
            godot_registry_lines.append("        print('Alenia Error: Track ', track_name, ' not found')\n")
            godot_registry_lines.append("func play_video(player, video_name: String):")
            godot_registry_lines.append("    if VIDEOS.has(video_name):")
            godot_registry_lines.append("        player.stream = VIDEOS[video_name]")
            godot_registry_lines.append("        player.play()")
            godot_registry_lines.append("    else:")
            godot_registry_lines.append("        print('Alenia Error: Video ', video_name, ' not found')")
            
            with open(os.path.join(output_directory_path, "AudioRegistry.gd"), "w", encoding="utf-8") as file_handle:
                file_handle.write("\n".join(godot_registry_lines))

        completion_callback(processed_files_count, output_directory_path)

    except Exception as conversion_exception:
        exception_traceback = traceback.format_exc()
        log_error_to_file(exception_traceback)
        error_callback(str(conversion_exception))
