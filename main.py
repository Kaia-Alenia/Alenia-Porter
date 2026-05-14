import sys
import os
import threading
import webbrowser
import json
import subprocess
import traceback
import ctypes
import glob
import tkinter as tk
from tkinter import filedialog, ttk
import porter_logic
import updater

CURRENT_VERSION = "v4.2"

try:
    myappid = "alenia.porter.v4.2"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

with open("ALENIA_ERROR.txt", "w", encoding="utf-8") as startup_log_file:
    startup_log_file.write("Starting Alenia Porter v4.2...\n")

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
        return {"lang": "es", "theme": "Default Dark"}

    def save_user_configuration(config_to_save):
        if not os.path.exists(config_folder_path):
            os.makedirs(config_folder_path)
        try:
            with open(config_file_path, "w", encoding="utf-8") as config_file:
                json.dump(config_to_save, config_file)
        except Exception:
            pass

    def load_themes():
        themes_dict = {}
        if os.path.exists("themes"):
            for file in glob.glob("themes/*.json"):
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        name = data.get("name", os.path.basename(file))
                        themes_dict[name] = data
                except Exception:
                    pass
        if not themes_dict:
            themes_dict["Default Dark"] = {
                "name": "Default Dark",
                "bg_main": "#1e1e1e",
                "fg_main": "#ffffff",
                "fg_dim": "#a3a3a3",
                "accent": "#8b5cf6",
                "accent_hover": "#a78bfa",
                "link": "#F96854",
                "success": "#4ade80",
                "error": "#f87171",
                "warning": "#fbbf24",
                "progressbar_trough": "#2d2d2d"
            }
        return themes_dict

    available_themes = load_themes()
    theme_names = list(available_themes.keys())
    
    configuration_data = load_user_configuration()
    current_language_code = configuration_data.get("lang", "es")
    current_theme_name = configuration_data.get("theme", theme_names[0])
    
    if current_theme_name not in available_themes:
        current_theme_name = theme_names[0]
    
    current_theme = available_themes[current_theme_name]
    languages_dictionary = porter_logic.load_locales()

    def update_progressbar_style():
        progressbar_style = ttk.Style()
        progressbar_style.theme_use("default")
        progressbar_style.configure(
            "Purple.Horizontal.TProgressbar",
            troughcolor=current_theme.get("progressbar_trough", "#2d2d2d"),
            background=current_theme.get("accent", "#8b5cf6"),
            thickness=8,
            borderwidth=0
        )

    def apply_theme_to_ui():
        bg = current_theme.get("bg_main", "#1e1e1e")
        fg = current_theme.get("fg_main", "#ffffff")
        fg_dim = current_theme.get("fg_dim", "#a3a3a3")
        accent = current_theme.get("accent", "#8b5cf6")
        link = current_theme.get("link", "#F96854")
        
        root_window.configure(bg=bg)
        top_navigation_bar.configure(bg=bg)
        patreon_link_button.configure(bg=bg, activebackground=bg, fg=link)
        language_toggle_button.configure(bg=bg, activebackground=bg, fg=fg_dim)
        hamburger_button.configure(bg=bg, activebackground=bg, fg=fg)
        theme_toggle_button.configure(bg=bg, activebackground=bg, fg=fg)
        
        header_label.configure(bg=bg, fg=fg)
        format_selection_frame.configure(bg=bg)
        format_label.configure(bg=bg, fg=fg_dim)
        
        ogg_radiobutton.configure(bg=bg, fg=fg, selectcolor=accent, activebackground=bg)
        opus_radiobutton.configure(bg=bg, fg=fg, selectcolor=accent, activebackground=bg)
        
        engine_selection_frame.configure(bg=bg)
        engine_label.configure(bg=bg, fg=fg_dim)
        
        renpy_radiobutton.configure(bg=bg, fg=fg, selectcolor=accent, activebackground=bg)
        godot_radiobutton.configure(bg=bg, fg=fg, selectcolor=accent, activebackground=bg)
        
        select_folder_button.configure(bg=accent, fg="white")
        info_status_label.configure(bg=bg, fg=fg_dim)
        
        update_progressbar_style()

    def cycle_theme():
        global current_theme_name, current_theme
        idx = theme_names.index(current_theme_name)
        next_idx = (idx + 1) % len(theme_names)
        current_theme_name = theme_names[next_idx]
        current_theme = available_themes[current_theme_name]
        
        configuration_data["theme"] = current_theme_name
        save_user_configuration(configuration_data)
        apply_theme_to_ui()

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
        engine_label.config(text=active_translation["select_engine"])
        select_folder_button.config(text=active_translation["btn_select"])
        info_status_label.config(text=active_translation["info_desc"])
        language_toggle_button.config(text=active_translation["btn_lang"])
        patreon_link_button.config(text=active_translation["btn_patreon"])
        adjust_opus_button_state()

    def show_custom_popup(title, message, is_accordion=False):
        bg = current_theme.get("bg_main", "#1e1e1e")
        fg = current_theme.get("fg_main", "#ffffff")
        fg_dim = current_theme.get("fg_dim", "#a3a3a3")
        accent = current_theme.get("accent", "#8b5cf6")
        accent_hover = current_theme.get("accent_hover", "#a78bfa")
        
        popup = tk.Toplevel(root_window)
        popup.title(title)
        popup.configure(bg=bg)
        popup.transient(root_window)
        popup.grab_set()
        
        content_frame = tk.Frame(popup, bg=bg)
        content_frame.pack(expand=True, fill="both", padx=25, pady=20)
        
        if is_accordion:
            sections = message.split("\n\n")
            for section in sections:
                lines = section.split("\n")
                if len(lines) >= 2:
                    section_title = lines[0]
                    section_content = "\n".join(lines[1:])
                    
                    def make_accordion(parent, s_title, s_content):
                        container = tk.Frame(parent, bg=bg)
                        container.pack(fill="x", pady=2)
                        
                        content_label = tk.Label(
                            container, 
                            text=s_content, 
                            bg=bg, 
                            fg=fg_dim,
                            font=("Arial", 9),
                            justify="left",
                            wraplength=350
                        )
                        
                        is_open = [False]
                        
                        def toggle(lbl=content_label, state=is_open, btn=None):
                            if state[0]:
                                lbl.pack_forget()
                                if btn: btn.config(text="▶ " + s_title)
                            else:
                                lbl.pack(fill="x", padx=15, pady=(2, 10))
                                if btn: btn.config(text="▼ " + s_title)
                            state[0] = not state[0]
                            popup.update_idletasks()
                        
                        toggle_btn = tk.Button(
                            container,
                            text="▶ " + s_title,
                            bg=bg,
                            fg=fg,
                            relief="flat",
                            cursor="hand2",
                            borderwidth=0,
                            highlightthickness=0,
                            activebackground=bg,
                            font=("Arial", 10, "bold"),
                            anchor="w",
                            command=lambda: toggle(btn=toggle_btn)
                        )
                        toggle_btn.pack(fill="x")
                        
                    make_accordion(content_frame, section_title, section_content)
        else:
            msg_label = tk.Label(
                content_frame,
                text=message,
                bg=bg,
                fg=fg,
                font=("Arial", 10),
                justify="left"
            )
            msg_label.pack(expand=True, fill="both")
        
        btn_frame = tk.Frame(popup, bg=bg)
        btn_frame.pack(fill="x", pady=(0, 20))
        
        ok_btn = tk.Button(
            btn_frame,
            text="OK",
            command=popup.destroy,
            bg=accent,
            fg="white",
            padx=30,
            pady=8,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            font=("Arial", 9, "bold")
        )
        ok_btn.pack()
        
        ok_btn.bind("<Enter>", lambda e: ok_btn.config(bg=accent_hover))
        ok_btn.bind("<Leave>", lambda e: ok_btn.config(bg=accent))
        
        popup.update_idletasks()
        req_width = max(400, popup.winfo_reqwidth())
        req_height = popup.winfo_reqheight()
        x = root_window.winfo_x() + (root_window.winfo_width() // 2) - (req_width // 2)
        y = root_window.winfo_y() + (root_window.winfo_height() // 2) - (req_height // 2)
        popup.geometry(f"{req_width}x{req_height}+{x}+{y}")

    def on_progressbar_increment(current_value, total_value):
        root_window.after(0, lambda: progressbar_widget.config(maximum=total_value, value=current_value))

    def on_conversion_success(processed_count, output_path):
        active_translation = languages_dictionary[current_language_code]
        success_color = current_theme.get("success", "#4ade80")
        root_window.after(0, lambda: info_status_label.config(text=active_translation["msg_done"].format(processed_count), fg=success_color))
        root_window.after(0, lambda: progressbar_widget.config(value=progressbar_widget["maximum"]))
        root_window.after(0, lambda: select_folder_button.config(state=tk.NORMAL))
        
        if os.name == "nt":
            os.startfile(output_path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", output_path])
        else:
            subprocess.Popen(["xdg-open", output_path])
            
        root_window.after(0, lambda: show_custom_popup(
            active_translation["msg_success_t"],
            active_translation["msg_success_m"].format(processed_count, engine_variable.get().upper(), output_path),
            is_accordion=False
        ))

    def on_conversion_failure(error_details):
        active_translation = languages_dictionary[current_language_code]
        error_color = current_theme.get("error", "#f87171")
        root_window.after(0, lambda: info_status_label.config(text=active_translation["msg_err"], fg=error_color))
        root_window.after(0, lambda: select_folder_button.config(state=tk.NORMAL))

    def trigger_media_conversion():
        active_translation = languages_dictionary[current_language_code]
        warning_color = current_theme.get("warning", "#fbbf24")
        selected_directory = filedialog.askdirectory(title=active_translation["btn_select"])
        if not selected_directory:
            return
        
        select_folder_button.config(state=tk.DISABLED)
        info_status_label.config(text=active_translation["info_wait"], fg=warning_color)
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
        active_translation = languages_dictionary[current_language_code]
        base_ogg = active_translation["format_ogg"]
        base_opus = active_translation["format_opus"]
        if engine_variable.get() == "godot":
            format_variable.set("ogg")
            opus_radiobutton.config(state=tk.DISABLED)
            ogg_radiobutton.config(text=f"{base_ogg} / OGV / WebP")
            opus_radiobutton.config(text=f"{base_opus} / OGV / WebP")
        else:
            opus_radiobutton.config(state=tk.NORMAL)
            ogg_radiobutton.config(text=f"{base_ogg} / WebM / WebP")
            opus_radiobutton.config(text=f"{base_opus} / WebM / WebP")

    def show_formats_info():
        active_translation = languages_dictionary[current_language_code]
        show_custom_popup(
            active_translation["formats_title"],
            active_translation["formats_info"],
            is_accordion=True
        )

    def on_button_hover_enter(event_args):
        select_folder_button.config(bg=current_theme.get("accent_hover", "#a78bfa"))

    def on_button_hover_leave(event_args):
        select_folder_button.config(bg=current_theme.get("accent", "#8b5cf6"))

    root_window = tk.Tk()
    try:
        root_window.iconbitmap(porter_logic.resource_path("logo.ico"))
    except Exception:
        pass

    initial_translation = languages_dictionary[current_language_code]
    root_window.title(initial_translation["title"])
    root_window.geometry("400x420")
    
    bg_main = current_theme.get("bg_main", "#1e1e1e")
    fg_main = current_theme.get("fg_main", "#ffffff")
    fg_dim = current_theme.get("fg_dim", "#a3a3a3")
    accent_color = current_theme.get("accent", "#8b5cf6")
    link_color = current_theme.get("link", "#F96854")

    root_window.configure(bg=bg_main)

    update_progressbar_style()

    top_navigation_bar = tk.Frame(root_window, bg=bg_main)
    top_navigation_bar.pack(fill="x", padx=10, pady=5)

    patreon_link_button = tk.Button(
        top_navigation_bar,
        text=initial_translation["btn_patreon"],
        bg=bg_main,
        fg=link_color,
        relief="flat",
        cursor="hand2",
        borderwidth=0,
        highlightthickness=0,
        activebackground=bg_main,
        command=lambda: webbrowser.open("https://www.patreon.com/cw/alenia_studios"),
        font=("Arial", 9, "bold", "underline")
    )
    patreon_link_button.pack(side="left")

    hamburger_button = tk.Button(
        top_navigation_bar,
        text="≡",
        bg=bg_main,
        fg=fg_main,
        relief="flat",
        cursor="hand2",
        borderwidth=0,
        highlightthickness=0,
        activebackground=bg_main,
        command=show_formats_info,
        font=("Arial", 14, "bold")
    )
    hamburger_button.pack(side="right")
    
    theme_toggle_button = tk.Button(
        top_navigation_bar,
        text="🎨",
        bg=bg_main,
        fg=fg_main,
        relief="flat",
        cursor="hand2",
        borderwidth=0,
        highlightthickness=0,
        activebackground=bg_main,
        command=cycle_theme,
        font=("Segoe UI Emoji", 12)
    )
    theme_toggle_button.pack(side="right", padx=(0, 10))

    language_toggle_button = tk.Button(
        top_navigation_bar,
        text=initial_translation["btn_lang"],
        bg=bg_main,
        fg=fg_dim,
        relief="flat",
        cursor="hand2",
        borderwidth=0,
        highlightthickness=0,
        activebackground=bg_main,
        command=change_application_language,
        font=("Arial", 9, "bold")
    )
    language_toggle_button.pack(side="right", padx=(0, 10))

    header_label = tk.Label(
        root_window,
        text=initial_translation["header"],
        font=("Arial", 14, "bold"),
        bg=bg_main,
        fg=fg_main
    )
    header_label.pack(pady=(5, 15))

    format_selection_frame = tk.Frame(root_window, bg=bg_main)
    format_selection_frame.pack(pady=5)

    format_label = tk.Label(
        format_selection_frame,
        text=initial_translation["select_format"],
        bg=bg_main,
        fg=fg_dim,
        font=("Arial", 9)
    )
    format_label.pack()

    format_variable = tk.StringVar(value="ogg")
    
    ogg_radiobutton = tk.Radiobutton(
        format_selection_frame,
        text=initial_translation["format_ogg"],
        variable=format_variable,
        value="ogg",
        bg=bg_main,
        fg=fg_main,
        selectcolor=accent_color,
        activebackground=bg_main,
        borderwidth=0,
        highlightthickness=0
    )
    ogg_radiobutton.pack(side=tk.LEFT, padx=10)

    opus_radiobutton = tk.Radiobutton(
        format_selection_frame,
        text=initial_translation["format_opus"],
        variable=format_variable,
        value="opus",
        bg=bg_main,
        fg=fg_main,
        selectcolor=accent_color,
        activebackground=bg_main,
        borderwidth=0,
        highlightthickness=0
    )
    opus_radiobutton.pack(side=tk.LEFT, padx=10)

    engine_selection_frame = tk.Frame(root_window, bg=bg_main)
    engine_selection_frame.pack(pady=5)

    engine_label = tk.Label(
        engine_selection_frame,
        text=initial_translation["select_engine"],
        bg=bg_main,
        fg=fg_dim,
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
        bg=bg_main,
        fg=fg_main,
        selectcolor=accent_color,
        activebackground=bg_main,
        borderwidth=0,
        highlightthickness=0
    )
    renpy_radiobutton.pack(side=tk.LEFT, padx=10)

    godot_radiobutton = tk.Radiobutton(
        engine_selection_frame,
        text="Godot (.gd)",
        variable=engine_variable,
        value="godot",
        bg=bg_main,
        fg=fg_main,
        selectcolor=accent_color,
        activebackground=bg_main,
        borderwidth=0,
        highlightthickness=0
    )
    godot_radiobutton.pack(side=tk.LEFT, padx=10)

    select_folder_button = tk.Button(
        root_window,
        text=initial_translation["btn_select"],
        command=trigger_media_conversion,
        bg=accent_color,
        fg="white",
        padx=20,
        pady=10,
        borderwidth=0,
        highlightthickness=0,
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
        bg=bg_main,
        fg=fg_dim
    )
    info_status_label.pack()

    adjust_opus_button_state()

    def perform_update_check():
        has_update, new_ver, dl_url = updater.check_for_updates(CURRENT_VERSION)
        if has_update:
            root_window.after(1000, lambda: prompt_update(new_ver, dl_url))

    def prompt_update(new_ver, dl_url):
        trans = languages_dictionary[current_language_code]
        title = trans.get("update_available_title", "Update Available")
        desc = trans.get("update_available_desc", "Version {} is available. Update now?").format(new_ver)
        
        bg = current_theme.get("bg_main", "#1e1e1e")
        fg = current_theme.get("fg_main", "#ffffff")
        accent = current_theme.get("accent", "#8b5cf6")
        
        upd_win = tk.Toplevel(root_window)
        upd_win.title(title)
        upd_win.configure(bg=bg)
        upd_win.geometry("350x150")
        upd_win.transient(root_window)
        upd_win.grab_set()
        
        lbl = tk.Label(upd_win, text=desc, bg=bg, fg=fg, wraplength=300)
        lbl.pack(pady=20)
        
        btn_frame = tk.Frame(upd_win, bg=bg)
        btn_frame.pack()
        
        def do_update():
            lbl.config(text=trans.get("update_downloading", "Downloading update..."))
            for widget in btn_frame.winfo_children():
                widget.destroy()
                
            prog = ttk.Progressbar(upd_win, style="Purple.Horizontal.TProgressbar", orient="horizontal", length=250, mode="determinate")
            prog.pack(pady=10)
            
            def on_progress(p):
                prog["value"] = p
                upd_win.update_idletasks()
                
            def on_ready():
                upd_win.destroy()
                root_window.destroy()
                sys.exit(0)
                
            threading.Thread(target=updater.download_and_apply_update, args=(dl_url, on_progress, on_ready), daemon=True).start()
            
        tk.Button(btn_frame, text="Yes", bg=accent, fg="white", command=do_update, width=8).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="No", bg="#555555", fg="white", command=upd_win.destroy, width=8).pack(side=tk.LEFT, padx=10)

    threading.Thread(target=perform_update_check, daemon=True).start()

    root_window.mainloop()

except Exception as fatal_exception:
    fatal_error_details = traceback.format_exc()
    with open("ALENIA_ERROR.txt", "a", encoding="utf-8") as error_file:
        error_file.write(f"\n--- FATAL ERROR ---\n{fatal_error_details}\n")
    sys.exit(1)