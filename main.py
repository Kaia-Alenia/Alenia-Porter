import sys
import os
import threading
import webbrowser
import json
import subprocess
import traceback
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import porter_logic

try:
    myappid = "alenia.porter.v3.0"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

with open("ALENIA_ERROR.txt", "w", encoding="utf-8") as startup_log_file:
    startup_log_file.write("Starting Alenia Porter v3.0...\n")

try:
    if os.name == "nt":
        local_app_data_path = os.getenv("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local")
        config_folder_path = os.path.join(local_app_data_path, "AleniaStudios", "AleniaPorter")
    else:
        config_folder_path = os.path.expanduser("~/.config/AleniaStudios/AleniaPorter")
    config_file_path = os.path.join(config_folder_path, "config.json")

    def load_user_configuration():
        if os.path.exists(config_file_path):
            try:
                with open(config_file_path, "r", encoding="utf-8") as config_file:
                    return json.load(config_file)
            except Exception:
                pass
        return {"lang": "es"}

    def save_user_configuration(config_to_save):
        if not os.path.exists(config_folder_path):
            os.makedirs(config_folder_path)
        try:
            with open(config_file_path, "w", encoding="utf-8") as config_file:
                json.dump(config_to_save, config_file)
        except Exception:
            pass

    configuration_data = load_user_configuration()
    current_language_code = configuration_data.get("lang", "es")
    languages_dictionary = porter_logic.load_locales()

    def update_progressbar_style():
        progressbar_style = ttk.Style()
        progressbar_style.theme_use("default")
        progressbar_style.configure(
            "Purple.Horizontal.TProgressbar",
            troughcolor="#2d2d2d",
            background="#8b5cf6",
            thickness=8,
            borderwidth=0
        )

    def change_application_language():
        global current_language_code
        available_languages = list(languages_dictionary.keys())
        current_index = available_languages.index(current_language_code)
        next_index = (current_index + 1) % len(available_languages)
        current_language_code = available_languages[next_index]
        configuration_data["lang"] = current_language_code
        save_user_configuration(configuration_data)
        refresh_interface_labels()

    def refresh_interface_labels():
        active_translation = languages_dictionary[current_language_code]
        root_window.title(active_translation["title"])
        header_label.config(text=active_translation["header"])
        format_label.config(text=active_translation["select_format"])
        ogg_radiobutton.config(text=active_translation["format_ogg"])
        opus_radiobutton.config(text=active_translation["format_opus"])
        engine_label.config(text=active_translation["select_engine"])
        select_folder_button.config(text=active_translation["btn_select"])
        info_status_label.config(text=active_translation["info_desc"])
        language_toggle_button.config(text=active_translation["btn_lang"])
        patreon_link_button.config(text=active_translation["btn_patreon"])

    def on_progressbar_increment(current_value, total_value):
        root_window.after(0, lambda: progressbar_widget.config(maximum=total_value, value=current_value))

    def on_conversion_success(processed_count, output_path):
        active_translation = languages_dictionary[current_language_code]
        root_window.after(0, lambda: info_status_label.config(text=active_translation["msg_done"].format(processed_count), fg="#4ade80"))
        root_window.after(0, lambda: progressbar_widget.config(value=progressbar_widget["maximum"]))
        root_window.after(0, lambda: select_folder_button.config(state=tk.NORMAL))
        
        if os.name == "nt":
            os.startfile(output_path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", output_path])
        else:
            subprocess.Popen(["xdg-open", output_path])
            
        root_window.after(0, lambda: messagebox.showinfo(
            active_translation["msg_success_t"],
            active_translation["msg_success_m"].format(processed_count, engine_variable.get().upper(), output_path)
        ))

    def on_conversion_failure(error_details):
        active_translation = languages_dictionary[current_language_code]
        root_window.after(0, lambda: info_status_label.config(text=active_translation["msg_err"], fg="#f87171"))
        root_window.after(0, lambda: select_folder_button.config(state=tk.NORMAL))

    def trigger_media_conversion():
        active_translation = languages_dictionary[current_language_code]
        selected_directory = filedialog.askdirectory(title=active_translation["btn_select"])
        if not selected_directory:
            return
        
        select_folder_button.config(state=tk.DISABLED)
        info_status_label.config(text=active_translation["info_wait"], fg="#fbbf24")
        progressbar_widget.config(value=0)
        
        conversion_worker_thread = threading.Thread(
            target=porter_logic.convert_media,
            args=(
                selected_directory,
                engine_variable.get(),
                format_variable.get(),
                on_progressbar_increment,
                None,
                on_conversion_success,
                on_conversion_failure
            ),
            daemon=True
        )
        conversion_worker_thread.start()

    def adjust_opus_button_state(*args):
        if engine_variable.get() == "godot":
            format_variable.set("ogg")
            opus_radiobutton.config(state=tk.DISABLED)
        else:
            opus_radiobutton.config(state=tk.NORMAL)

    def on_button_hover_enter(event_args):
        select_folder_button.config(bg="#a78bfa")

    def on_button_hover_leave(event_args):
        select_folder_button.config(bg="#8b5cf6")

    root_window = tk.Tk()
    try:
        root_window.iconbitmap(porter_logic.resource_path("logo.ico"))
    except Exception:
        pass

    initial_translation = languages_dictionary[current_language_code]
    root_window.title(initial_translation["title"])
    root_window.geometry("400x420")
    root_window.configure(bg="#1e1e1e")

    update_progressbar_style()

    top_navigation_bar = tk.Frame(root_window, bg="#1e1e1e")
    top_navigation_bar.pack(fill="x", padx=10, pady=5)

    patreon_link_button = tk.Button(
        top_navigation_bar,
        text=initial_translation["btn_patreon"],
        bg="#1e1e1e",
        fg="#F96854",
        relief="flat",
        cursor="hand2",
        command=lambda: webbrowser.open("https://www.patreon.com/cw/alenia_studios"),
        font=("Arial", 9, "bold", "underline")
    )
    patreon_link_button.pack(side="left")

    language_toggle_button = tk.Button(
        top_navigation_bar,
        text=initial_translation["btn_lang"],
        bg="#1e1e1e",
        fg="gray",
        relief="flat",
        cursor="hand2",
        command=change_application_language,
        font=("Arial", 9, "bold")
    )
    language_toggle_button.pack(side="right")

    header_label = tk.Label(
        root_window,
        text=initial_translation["header"],
        font=("Arial", 14, "bold"),
        bg="#1e1e1e",
        fg="#ffffff"
    )
    header_label.pack(pady=(5, 15))

    format_selection_frame = tk.Frame(root_window, bg="#1e1e1e")
    format_selection_frame.pack(pady=5)

    format_label = tk.Label(
        format_selection_frame,
        text=initial_translation["select_format"],
        bg="#1e1e1e",
        fg="#a3a3a3",
        font=("Arial", 9)
    )
    format_label.pack()

    format_variable = tk.StringVar(value="ogg")
    
    ogg_radiobutton = tk.Radiobutton(
        format_selection_frame,
        text=initial_translation["format_ogg"],
        variable=format_variable,
        value="ogg",
        bg="#1e1e1e",
        fg="white",
        selectcolor="#8b5cf6",
        activebackground="#1e1e1e"
    )
    ogg_radiobutton.pack(side=tk.LEFT, padx=10)

    opus_radiobutton = tk.Radiobutton(
        format_selection_frame,
        text=initial_translation["format_opus"],
        variable=format_variable,
        value="opus",
        bg="#1e1e1e",
        fg="white",
        selectcolor="#8b5cf6",
        activebackground="#1e1e1e"
    )
    opus_radiobutton.pack(side=tk.LEFT, padx=10)

    engine_selection_frame = tk.Frame(root_window, bg="#1e1e1e")
    engine_selection_frame.pack(pady=5)

    engine_label = tk.Label(
        engine_selection_frame,
        text=initial_translation["select_engine"],
        bg="#1e1e1e",
        fg="#a3a3a3",
        font=("Arial", 9)
    )
    engine_label.pack()

    engine_variable = tk.StringVar(value="renpy")
    engine_variable.trace_add("write", adjust_opus_button_state)

    renpy_radiobutton = tk.Radiobutton(
        engine_selection_frame,
        text="Ren'Py (.rpy)",
        variable=engine_variable,
        value="renpy",
        bg="#1e1e1e",
        fg="white",
        selectcolor="#8b5cf6",
        activebackground="#1e1e1e"
    )
    renpy_radiobutton.pack(side=tk.LEFT, padx=10)

    godot_radiobutton = tk.Radiobutton(
        engine_selection_frame,
        text="Godot (.gd)",
        variable=engine_variable,
        value="godot",
        bg="#1e1e1e",
        fg="white",
        selectcolor="#8b5cf6",
        activebackground="#1e1e1e"
    )
    godot_radiobutton.pack(side=tk.LEFT, padx=10)

    select_folder_button = tk.Button(
        root_window,
        text=initial_translation["btn_select"],
        command=trigger_media_conversion,
        bg="#8b5cf6",
        fg="white",
        padx=20,
        pady=10,
        borderwidth=0,
        cursor="hand2"
    )
    select_folder_button.pack(pady=15)
    select_folder_button.bind("<Enter>", on_button_hover_enter)
    select_folder_button.bind("<Leave>", on_button_hover_leave)

    progressbar_widget = ttk.Progressbar(
        root_window,
        style="Purple.Horizontal.TProgressbar",
        orient="horizontal",
        length=300,
        mode="determinate"
    )
    progressbar_widget.pack(pady=10)

    info_status_label = tk.Label(
        root_window,
        text=initial_translation["info_desc"],
        font=("Arial", 8),
        bg="#1e1e1e",
        fg="#a3a3a3"
    )
    info_status_label.pack()

    root_window.mainloop()

except Exception as fatal_exception:
    fatal_error_details = traceback.format_exc()
    with open("ALENIA_ERROR.txt", "a", encoding="utf-8") as error_file:
        error_file.write(f"\n--- FATAL ERROR ---\n{fatal_error_details}\n")
    sys.exit(1)