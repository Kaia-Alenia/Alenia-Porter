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
import updater

import zenith
zenith.ignite()

import porter_logic

CURRENT_VERSION = "v5.3"
update_info = {"found": False, "ver": None, "url": None}
try:
    has_update, new_ver, dl_url = updater.check_for_updates(CURRENT_VERSION)
    if has_update:
        update_info["found"] = True
        update_info["ver"] = new_ver
        update_info["url"] = dl_url
except: pass

try:
    myappid = "alenia.porter.v5.3"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

with open("ALENIA_ERROR.txt", "w", encoding="utf-8") as startup_log_file:
    startup_log_file.write("Starting Alenia Porter v5.3...\n")

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
        return {"lang": "es", "theme": "Default Theme"}

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
        themes_path = porter_logic.resource_path("themes")
        if os.path.exists(themes_path):
            for file in glob.glob(os.path.join(themes_path, "*.json")):
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        name = data.get("name", os.path.basename(file))
                        themes_dict[name] = data
                except Exception:
                    pass
        if not themes_dict:
            themes_dict["Default Theme"] = {
                "name": "Default Theme",
                "bg_main": "#1e1e1e",
                "fg_main": "#ffffff",
                "fg_dim": "#a3a3a3",
                "accent": "#8b5cf6",
                "accent_hover": "#a78bfa",
                "link": "#F96854",
                "success": "#4ade80",
                "error": "#f87171",
                "warning": "#fbbf24",
                "progressbar_trough": "#2d2d2d",
                "char_sprite": "assets/kaia_default.png",
                "studio_logo_image": "assets/studio_logo_white.png"
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

    image_cache = {"bg": None, "char": None, "progress": None, "studio": None, "success_kaia": None, "info_kaia": None, "support_kaia": None}

    def load_theme_image(path):
        if not path: return None
        full_path = porter_logic.resource_path(path)
        if not os.path.exists(full_path):
            return None
        try:
            return tk.PhotoImage(file=full_path)
        except Exception:
            return None

    def apply_theme_to_ui():
        bg = current_theme.get("bg_main", "#1e1e1e")
        fg = current_theme.get("fg_main", "#ffffff")
        fg_dim = current_theme.get("fg_dim", "#a3a3a3")
        accent = current_theme.get("accent", "#8b5cf6")
        link = current_theme.get("link", "#F96854")
        
        root_window.configure(bg=bg)
        top_navigation_bar.configure(bg=bg)
        
        char_path = current_theme.get("char_sprite", "assets/kaia_default.png")
        image_cache["char"] = load_theme_image(char_path)
        if image_cache["char"]:
            character_label.configure(image=image_cache["char"], bg=bg)
            character_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        else:
            character_label.place_forget()

        prog_icon_path = current_theme.get("progress_icon", "")
        image_cache["progress"] = load_theme_image(prog_icon_path)

        studio_path = current_theme.get("studio_logo_image", "assets/studio_logo.png")
        image_cache["studio"] = load_theme_image(studio_path)
        if image_cache["studio"]:
            studio_logo_label.configure(image=image_cache["studio"], bg=bg)
            studio_logo_label.pack(pady=(2, 0))
        else:
            studio_logo_label.pack_forget()

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
        
        progress_canvas.configure(bg=bg)
        draw_progress(0)

    def draw_progress(percent):
        bg = current_theme.get("bg_main", "#1e1e1e")
        accent = current_theme.get("accent", "#8b5cf6")
        trough = current_theme.get("progressbar_trough", "#2d2d2d")
        
        progress_canvas.delete("all")
        progress_canvas.create_round_rect(5, 20, 295, 30, radius=5, fill=trough, outline="")
        
        width = (percent / 100) * 290
        if width > 0:
            progress_canvas.create_round_rect(5, 20, 5 + width, 30, radius=5, fill=accent, outline="")
        
        if image_cache["progress"]:
            pos_x = 5 + width
            progress_canvas.create_image(pos_x, 25, image=image_cache["progress"])

    def create_round_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)
    
    tk.Canvas.create_round_rect = create_round_rect

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
        hamburger_button.config(command=lambda: show_custom_popup(active_translation["formats_title"], active_translation["formats_info"], is_accordion=True))
        adjust_opus_button_state()

    def show_custom_popup(title, message, is_error=False, is_accordion=False):
        accent_color = current_theme.get("error" if is_error else "success", "#4ade80")
        popup = tk.Toplevel(root_window)
        popup.title(title)
        popup.geometry("450x380") 
        popup.configure(bg=current_theme["bg_main"])
        popup.resizable(False, False)
        popup.transient(root_window)
        popup.grab_set()
        
        bg = current_theme.get("bg_main", "#1e1e1e")
        fg = current_theme.get("fg_main", "#ffffff")
        fg_dim = current_theme.get("fg_dim", "#a3a3a3")
        accent = current_theme.get("accent", "#8b5cf6")
        accent_hover = current_theme.get("accent_hover", "#a78bfa")

        content_frame = tk.Frame(popup, bg=bg)
        content_frame.pack(expand=True, fill="both", padx=25, pady=20)
        
        if not is_error and not is_accordion:
            success_path = current_theme.get("char_success", "assets/kaia_success.png")
            image_cache["success_kaia"] = load_theme_image(success_path)
            if image_cache["success_kaia"]:
                tk.Label(content_frame, image=image_cache["success_kaia"], bg=bg).pack(pady=(0, 10))

        if is_accordion:
            popup.geometry("552x236")
            columns_frame = tk.Frame(content_frame, bg=bg)
            columns_frame.pack(fill="both", expand=True)
            scroll_container = tk.Frame(columns_frame, bg=bg)
            scroll_container.pack(side="left", fill="both", expand=True)
            canvas = tk.Canvas(scroll_container, bg=bg, highlightthickness=0)
            scrollable_frame = tk.Frame(canvas, bg=bg)
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.pack(side="left", fill="both", expand=True)

            image_cache["info_kaia"] = load_theme_image("assets/kaia_info.png")
            if image_cache["info_kaia"]:
                tk.Label(columns_frame, image=image_cache["info_kaia"], bg=bg).pack(side="right", anchor="ne", padx=(15, 0), pady=(10, 0))

            sections = message.split("\n\n")
            for section in sections:
                lines = section.split("\n")
                if len(lines) >= 1:
                    tk.Label(scrollable_frame, text=lines[0], bg=bg, fg=fg, font=("Arial", 10, "bold"), anchor="w").pack(fill="x", pady=(5, 0))
                    if len(lines) > 1:
                        tk.Label(scrollable_frame, text="\n".join(lines[1:]), bg=bg, fg=fg_dim, font=("Arial", 9), justify="left", wraplength=320, anchor="w").pack(fill="x", padx=15)
        else:
            tk.Label(content_frame, text=message, bg=bg, fg=fg, font=("Arial", 10), justify="left").pack(expand=True, fill="both")
        
        ok_btn = tk.Button(popup, text="OK", command=popup.destroy, bg=accent, fg="white", padx=30, pady=8, borderwidth=0, highlightthickness=0, cursor="hand2", font=("Arial", 9, "bold"))
        ok_btn.pack(pady=(0, 20))
        ok_btn.bind("<Enter>", lambda e: ok_btn.config(bg=accent_hover))
        ok_btn.bind("<Leave>", lambda e: ok_btn.config(bg=accent))

    def show_support_info():
        bg = current_theme.get("bg_main", "#1e1e1e")
        fg = current_theme.get("fg_main", "#ffffff")
        accent = current_theme.get("accent", "#8b5cf6")
        popup = tk.Toplevel(root_window)
        popup.title("Support Alenia Studios")
        popup.geometry("472x226")
        popup.configure(bg=bg)
        popup.transient(root_window)
        popup.grab_set()
        content_frame = tk.Frame(popup, bg=bg)
        content_frame.pack(expand=True, fill="both", padx=25, pady=20)
        columns_frame = tk.Frame(content_frame, bg=bg)
        columns_frame.pack(fill="both", expand=True)
        left_column = tk.Frame(columns_frame, bg=bg)
        left_column.pack(side="left", fill="both", expand=True)
        tk.Label(left_column, text="Support us on:", bg=bg, fg=fg, font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        links = [("Patreon", "https://patreon.com/alenia_studios"), ("Ko-fi", "https://ko-fi.com/alenia_studios"), ("GitHub", "https://github.com/Kaia-Alenia"), ("Itch.io", "https://alenia-studios.itch.io/"), ("PayPal", "https://www.paypal.com/ncp/payment/TCCYMCFSVMV8E")]
        btn_f = tk.Frame(left_column, bg=bg)
        btn_f.pack(anchor="w")
        for i, (name, url) in enumerate(links):
            tk.Button(btn_f, text=name, command=lambda u=url: webbrowser.open(u), bg=bg, fg=accent, relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2", font=("Arial", 10, "underline", "bold"), padx=5).grid(row=i//3, column=i%3, sticky="w", padx=2, pady=2)
        image_cache["support_kaia"] = load_theme_image("assets/kaia_support.png")
        if image_cache["support_kaia"]:
            tk.Label(columns_frame, image=image_cache["support_kaia"], bg=bg).pack(side="right", anchor="ne", padx=(15, 0))
        tk.Button(popup, text="OK", command=popup.destroy, bg=accent, fg="white", padx=30, pady=8, borderwidth=0, cursor="hand2", font=("Arial", 9, "bold")).pack(pady=(0, 20))

    def on_progressbar_increment(current_value, total_value):
        percent = int((current_value / total_value) * 100) if total_value > 0 else 0
        draw_progress(percent)
        root_window.update_idletasks()

    def on_conversion_success(processed_count, output_path):
        active_translation = languages_dictionary[current_language_code]
        success_color = current_theme.get("success", "#4ade80")
        root_window.after(0, lambda: info_status_label.config(text=active_translation["msg_done"].format(processed_count), fg=success_color))
        draw_progress(100)
        root_window.after(0, lambda: select_folder_button.config(state=tk.NORMAL))
        if os.name == "nt": os.startfile(output_path)
        else: subprocess.Popen(["xdg-open" if sys.platform.startswith("linux") else "open", output_path])
        root_window.after(0, lambda: show_custom_popup(active_translation["msg_success_t"], active_translation["msg_success_m"].format(processed_count, engine_variable.get().upper(), output_path)))

    def on_conversion_failure(error_details):
        active_translation = languages_dictionary[current_language_code]
        error_color = current_theme.get("error", "#f87171")
        root_window.after(0, lambda: info_status_label.config(text=active_translation["msg_err"], fg=error_color))
        root_window.after(0, lambda: select_folder_button.config(state=tk.NORMAL))

    def trigger_media_conversion():
        active_translation = languages_dictionary[current_language_code]
        warning_color = current_theme.get("warning", "#fbbf24")
        selected_directory = filedialog.askdirectory(title=active_translation["btn_select"])
        if not selected_directory: return
        select_folder_button.config(state=tk.DISABLED)
        info_status_label.config(text=active_translation["info_wait"], fg=warning_color)
        draw_progress(0)
        threading.Thread(target=porter_logic.convert_media, args=(selected_directory, engine_variable.get(), format_variable.get(), on_progressbar_increment, None, on_conversion_success, on_conversion_failure), daemon=True).start()

    def adjust_opus_button_state(*args):
        active_translation = languages_dictionary[current_language_code]
        if engine_variable.get() == "godot":
            format_variable.set("ogg")
            opus_radiobutton.config(state=tk.DISABLED)
            ogg_radiobutton.config(text=f"{active_translation['format_ogg']} / OGV / WebP")
            opus_radiobutton.config(text=f"{active_translation['format_opus']} / OGV / WebP")
        else:
            opus_radiobutton.config(state=tk.NORMAL)
            ogg_radiobutton.config(text=f"{active_translation['format_ogg']} / WebM / WebP")
            opus_radiobutton.config(text=f"{active_translation['format_opus']} / WebM / WebP")

    root_window = tk.Tk()
    try: root_window.iconbitmap(porter_logic.resource_path("logo.ico"))
    except: pass
    initial_translation = languages_dictionary[current_language_code]
    root_window.title(initial_translation["title"])
    root_window.geometry("450x550")
    bg_main = current_theme.get("bg_main", "#1e1e1e")
    fg_main = current_theme.get("fg_main", "#ffffff")
    fg_dim = current_theme.get("fg_dim", "#a3a3a3")
    accent_color = current_theme.get("accent", "#8b5cf6")
    link_color = current_theme.get("link", "#F96854")
    root_window.configure(bg=bg_main)
    top_navigation_bar = tk.Frame(root_window, bg=bg_main)
    top_navigation_bar.pack(fill="x", padx=10, pady=5)
    patreon_link_button = tk.Button(top_navigation_bar, text=initial_translation["btn_patreon"], bg=bg_main, fg=link_color, relief="flat", cursor="hand2", borderwidth=0, highlightthickness=0, activebackground=bg_main, command=show_support_info, font=("Arial", 9, "bold", "underline"))
    patreon_link_button.pack(side="left")
    hamburger_button = tk.Button(top_navigation_bar, text="≡", bg=bg_main, fg=fg_main, relief="flat", cursor="hand2", borderwidth=0, highlightthickness=0, activebackground=bg_main, command=lambda: show_custom_popup(initial_translation["formats_title"], initial_translation["formats_info"], is_accordion=True), font=("Arial", 14, "bold"))
    hamburger_button.pack(side="right")
    theme_toggle_button = tk.Button(top_navigation_bar, text="🎨", bg=bg_main, fg=fg_main, relief="flat", cursor="hand2", borderwidth=0, highlightthickness=0, activebackground=bg_main, command=cycle_theme, font=("Segoe UI Emoji", 12))
    theme_toggle_button.pack(side="right", padx=(0, 10))
    language_toggle_button = tk.Button(top_navigation_bar, text=initial_translation["btn_lang"], bg=bg_main, fg=fg_dim, relief="flat", cursor="hand2", borderwidth=0, highlightthickness=0, activebackground=bg_main, command=change_application_language, font=("Arial", 9, "bold"))
    language_toggle_button.pack(side="right", padx=(0, 10))
    header_label = tk.Label(root_window, text=initial_translation["header"], font=("Arial", 14, "bold"), bg=bg_main, fg=fg_main)
    header_label.pack(pady=(5, 15))
    format_selection_frame = tk.Frame(root_window, bg=bg_main)
    format_selection_frame.pack(pady=5)
    format_label = tk.Label(format_selection_frame, text=initial_translation["select_format"], bg=bg_main, fg=fg_dim, font=("Arial", 9))
    format_label.pack()
    format_variable = tk.StringVar(value="ogg")
    ogg_radiobutton = tk.Radiobutton(format_selection_frame, text=initial_translation["format_ogg"], variable=format_variable, value="ogg", bg=bg_main, fg=fg_main, selectcolor=accent_color, activebackground=bg_main, borderwidth=0, highlightthickness=0)
    ogg_radiobutton.pack(side=tk.LEFT, padx=10)
    opus_radiobutton = tk.Radiobutton(format_selection_frame, text=initial_translation["format_opus"], variable=format_variable, value="opus", bg=bg_main, fg=fg_main, selectcolor=accent_color, activebackground=bg_main, borderwidth=0, highlightthickness=0)
    opus_radiobutton.pack(side=tk.LEFT, padx=10)
    engine_selection_frame = tk.Frame(root_window, bg=bg_main)
    engine_selection_frame.pack(pady=5)
    engine_label = tk.Label(engine_selection_frame, text=initial_translation["select_engine"], bg=bg_main, fg=fg_dim, font=("Arial", 9))
    engine_label.pack()
    engine_variable = tk.StringVar(value="renpy")
    engine_variable.trace_add("write", adjust_opus_button_state)
    renpy_radiobutton = tk.Radiobutton(engine_selection_frame, text="Ren'Py (.rpy)", variable=engine_variable, value="renpy", bg=bg_main, fg=fg_main, selectcolor=accent_color, activebackground=bg_main, borderwidth=0, highlightthickness=0)
    renpy_radiobutton.pack(side=tk.LEFT, padx=10)
    godot_radiobutton = tk.Radiobutton(engine_selection_frame, text="Godot (.gd)", variable=engine_variable, value="godot", bg=bg_main, fg=fg_main, selectcolor=accent_color, activebackground=bg_main, borderwidth=0, highlightthickness=0)
    godot_radiobutton.pack(side=tk.LEFT, padx=10)
    select_folder_button = tk.Button(root_window, text=initial_translation["btn_select"], command=trigger_media_conversion, bg=accent_color, fg="white", padx=20, pady=10, borderwidth=0, highlightthickness=0, cursor="hand2")
    select_folder_button.pack(pady=15)
    select_folder_button.bind("<Enter>", lambda e: select_folder_button.config(bg=current_theme.get("accent_hover", "#a78bfa")))
    select_folder_button.bind("<Leave>", lambda e: select_folder_button.config(bg=current_theme.get("accent", "#8b5cf6")))
    progress_canvas = tk.Canvas(root_window, width=300, height=50, bg=bg_main, highlightthickness=0)
    progress_canvas.pack(pady=5)
    character_label = tk.Label(root_window, bg=bg_main)
    info_status_label = tk.Label(root_window, text=initial_translation["info_desc"], font=("Arial", 8), bg=bg_main, fg=fg_dim)
    info_status_label.pack(pady=(0, 15)) 
    studio_logo_label = tk.Label(root_window, bg=bg_main)
    studio_logo_label.pack(pady=(0, 5)) 

    def prompt_update(new_ver, dl_url):
        trans = languages_dictionary[current_language_code]
        bg, fg, accent = current_theme["bg_main"], current_theme["fg_main"], current_theme["accent"]
        upd_win = tk.Toplevel(root_window)
        upd_win.title(trans.get("update_available_title", "Update"))
        upd_win.configure(bg=bg)
        upd_win.geometry("350x150")
        upd_win.transient(root_window)
        upd_win.grab_set()
        tk.Label(upd_win, text=trans.get("update_available_desc", "Version {} is available.").format(new_ver), bg=bg, fg=fg, wraplength=300).pack(pady=20)
        btn_f = tk.Frame(upd_win, bg=bg)
        btn_f.pack()
        def do_upd():
            for w in btn_f.winfo_children(): w.destroy()
            p = ttk.Progressbar(upd_win, orient="horizontal", length=250, mode="determinate")
            p.pack(pady=10)
            def on_p(pct): p["value"] = pct; upd_win.update_idletasks()
            def on_r(): upd_win.destroy(); root_window.destroy(); sys.exit(0)
            threading.Thread(target=updater.download_and_apply_update, args=(dl_url, on_p, on_r), daemon=True).start()
        tk.Button(btn_f, text="Yes", bg=accent, fg="white", command=do_upd, width=8).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_f, text="No", bg="#555555", fg="white", command=upd_win.destroy, width=8).pack(side=tk.LEFT, padx=10)

    apply_theme_to_ui()
    root_window.after(1500, lambda: prompt_update(update_info["ver"], update_info["url"]) if update_info["found"] else None)
    root_window.mainloop()

except Exception:
    with open("ALENIA_ERROR.txt", "a", encoding="utf-8") as f: f.write(f"\n--- FATAL ---\n{traceback.format_exc()}\n")
    sys.exit(1)