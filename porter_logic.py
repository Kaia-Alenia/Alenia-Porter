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
            "btn_patreon": "☕ Support Alenia",
            "instructions_filename": "ALENIA_INSTRUCTIONS.txt",
            "instructions_title": "ALENIA PORTER - QUICK GUIDE",
            "instructions_renpy": "1. Copy files to your /game folder.\n2. CODE EXAMPLE:\n   label start:\n       play audio track_name\n       show movie_name",
            "instructions_godot": "1. Setup: Project -> Project Settings -> Globals (Autoload).\n2. Add 'AudioRegistry.gd' as 'Audio'.\n3. CODE EXAMPLE:\n   func _ready():\n       Audio.play_track($AudioStreamPlayer, 'track_name')\n       Audio.play_video($VideoStreamPlayer, 'video_name')"
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
            "btn_patreon": "☕ Apoyar a Alenia",
            "instructions_filename": "INSTRUCCIONES_ALENIA.txt",
            "instructions_title": "ALENIA PORTER - GUÍA RÁPIDA",
            "instructions_renpy": "1. Copia los archivos a tu carpeta /game.\n2. EJEMPLO DE CÓDIGO:\n   label start:\n       play audio nombre_pista\n       show nombre_video",
            "instructions_godot": "1. Configuración: Proyecto -> Ajustes del Proyecto -> Globales (Autoload).\n2. Añade 'AudioRegistry.gd' con el nombre 'Audio'.\n3. EJEMPLO DE CÓDIGO:\n   func _ready():\n       Audio.play_track($AudioStreamPlayer, 'nombre_pista')\n       Audio.play_video($VideoStreamPlayer, 'nombre_video')"
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
            "btn_patreon": "☕ Soutenir Alenia",
            "instructions_filename": "INSTRUCTIONS_ALENIA.txt",
            "instructions_title": "ALENIA PORTER - GUIDE RAPIDE",
            "instructions_renpy": "1. Copiez les fichiers dans votre dossier /game.\n2. EXEMPLE DE CODE :\n   label start:\n       play audio nom_piste\n       show nom_video",
            "instructions_godot": "1. Configuration : Projet -> Paramètres du Projet -> Globaux (Autoload).\n2. Ajoutez 'AudioRegistry.gd' sous le nom 'Audio'.\n3. EXEMPLE DE CODE :\n   func _ready():\n       Audio.play_track($AudioStreamPlayer, 'nom_piste')\n       Audio.play_video($VideoStreamPlayer, 'nom_video')"
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
            "btn_patreon": "☕ Alenia を支援する",
            "instructions_filename": "ALENIA_指示.txt",
            "instructions_title": "ALENIA PORTER - クイックガイド",
            "instructions_renpy": "1. ファイルを /game フォルダにコピーします。\n2. コード例:\n   label start:\n       play audio track_name\n       show movie_name",
            "instructions_godot": "1. 設定: プロジェクト -> プロジェクト設定 -> グローバル (Autoload)。\n2. 'AudioRegistry.gd' を 'Audio' として追加します。\n3. コード例:\n   func _ready():\n       Audio.play_track($AudioStreamPlayer, 'track_name')\n       Audio.play_video($VideoStreamPlayer, 'video_name')"
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
            "btn_lang": "RU",
            "btn_patreon": "☕ 支持 Alenia",
            "instructions_filename": "ALENIA_说明.txt",
            "instructions_title": "ALENIA PORTER - 快速指南",
            "instructions_renpy": "1. 将文件复制到您的 /game 文件夹中。\n2. 代码示例:\n   label start:\n       play audio track_name\n       show movie_name",
            "instructions_godot": "1. 设置: 项目 -> 项目设置 -> 全局 (Autoload)。\n2. 将 'AudioRegistry.gd' 添加为 'Audio'。\n3. 代码示例:\n   func _ready():\n       Audio.play_track($AudioStreamPlayer, 'track_name')\n       Audio.play_video($VideoStreamPlayer, 'video_name')"
        },
        "ru": {
            "title": "Alenia Porter v3.0",
            "header": "Alenia Studios - Оптимизатор медиа",
            "select_format": "Экспортировать аудио в:",
            "format_ogg": "OGG (Стандарт)",
            "format_opus": "OPUS (Высокое сжатие)",
            "select_engine": "Целевой движок:",
            "btn_select": "Выбрать папку для конвертации",
            "info_wait": "Обработка файлов... Пожалуйста, подождите.",
            "info_desc": "Поддерживает аудио и видео (MP4, MKV, WebM, AVI, MOV)",
            "msg_done": "Готово! Обработано {} файлов.",
            "msg_err": "Ошибка при конвертации.",
            "msg_success_t": "Успех",
            "msg_success_m": "Оптимизировано {} файлов для {}!\n\nПуть: {}\n\nИнструкции открыты.",
            "btn_lang": "EN",
            "btn_patreon": "☕ Поддержать Alenia",
            "instructions_filename": "ALENIA_ИНСТРУКЦИИ.txt",
            "instructions_title": "ALENIA PORTER - КРАТКОЕ РУКОВОДСТВО",
            "instructions_renpy": "1. Скопируйте файлы в папку /game.\n2. ПРИМЕР КОДА:\n   label start:\n       play audio track_name\n       show movie_name",
            "instructions_godot": "1. Настройка: Проект -> Настройки проекта -> Глобальные переменные (Autoload).\n2. Добавьте 'AudioRegistry.gd' как 'Audio'.\n3. ПРИМЕР КОДА:\n   func _ready():\n       Audio.play_track($AudioStreamPlayer, 'track_name')\n       Audio.play_video($VideoStreamPlayer, 'video_name')"
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

        # Obtener el nombre del archivo de instrucciones de acuerdo al idioma configurado
        try:
            if os.name == "nt":
                local_app_data_path = os.getenv("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local")
                config_folder_path = os.path.join(local_app_data_path, "AleniaStudios", "AleniaPorter")
            else:
                config_folder_path = os.path.expanduser("~/.config/AleniaStudios/AleniaPorter")
            config_file_path = os.path.join(config_folder_path, "config.json")
            
            lang_code = "es"
            if os.path.exists(config_file_path):
                with open(config_file_path, "r", encoding="utf-8") as config_file:
                    user_config = json.load(config_file)
                    lang_code = user_config.get("lang", "es")
        except Exception:
            lang_code = "es"

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
