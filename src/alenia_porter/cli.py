import sys
import os
import traceback

def global_exception_handler(exctype, value, tb):
    tb_text = "".join(traceback.format_exception(exctype, value, tb))
    try:
        from alenia_porter import porter
        porter.log_error_to_file(tb_text)
        try:
            porter.send_crash_report("UNHANDLED_EXCEPTION", f"{exctype.__name__}: {str(value)}", tb_text)
        except:
            pass
    except Exception:
        pass
    with open("ALENIA_ERROR.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- FATAL ---\n{tb_text}\n")
    sys.exit(1)

sys.excepthook = global_exception_handler

try:
    import zenith
    zenith.ignite(file=__file__, show_banner=False)

    import threading
    import webbrowser
    import json
    import subprocess
    import ctypes
    import glob
    import argparse
    from alenia_porter import updater
    from alenia_porter import porter

    def thread_exception_handler(args):
        tb_text = "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback))
        porter.log_error_to_file(tb_text)
        try:
            porter.send_crash_report("THREAD_EXCEPTION", f"{args.exc_type.__name__}: {str(args.exc_value)}", tb_text)
        except:
            pass
        with open("ALENIA_ERROR.txt", "a", encoding="utf-8") as f:
            f.write(f"\n--- THREAD FATAL ---\n{tb_text}\n")

    threading.excepthook = thread_exception_handler
except Exception as e:
    tb_text = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    with open("ALENIA_ERROR.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- IMPORT FATAL ---\n{tb_text}\n")
    sys.exit(1)

class ToolTip(object):
    def __init__(self, widget, text_func):
        self.widget = widget
        self.text_func = text_func
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        import tkinter as tk
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text_func() if callable(self.text_func) else self.text_func, justify=tk.LEFT,
                         background="#2d2d2d", foreground="#ffffff", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", "9", "normal"))
        label.pack(ipadx=4, ipady=2)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def main():
    parser = argparse.ArgumentParser(description="Alenia Porter - Media Optimizer")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode (no GUI)")
    args = parser.parse_args()

    if args.headless:
        print("Alenia Porter v5.9 - Headless Mode")
        locales = porter.load_locales()
        if not locales:
            sys.exit(1)
        print("✓ Application initialized successfully")
        return

    import tkinter as tk
    from tkinter import filedialog, ttk

    CURRENT_VERSION = "v5.9"
    update_info = {"found": False, "ver": None, "url": None}
    try:
        has_update, new_ver, dl_url = updater.check_for_updates(CURRENT_VERSION)
        if has_update:
            update_info["found"] = True
            update_info["ver"] = new_ver
            update_info["url"] = dl_url
    except: pass

    try:
        myappid = "alenia.porter.v5.9"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

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
            with porter.resource_path(os.path.join("assets", "themes")) as themes_path:
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
                    "char_sprite": "assets/images/kaia_default.png",
                    "studio_logo_image": "assets/images/studio_logo_white.png"
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
        languages_dictionary = porter.load_locales()
        if current_language_code not in languages_dictionary: current_language_code = "en"

        image_cache = {"bg": None, "char": None, "progress": None, "studio": None, "success_kaia": None, "info_kaia": None, "support_kaia": None}

        def load_theme_image(path):
            if not path: return None
            with porter.resource_path(path) as full_path:
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
        
            char_path = current_theme.get("char_sprite", "assets/images/kaia_default.png")
            image_cache["char"] = load_theme_image(char_path)
            if image_cache["char"]:
                character_label.configure(image=image_cache["char"], bg=bg)
                character_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
            else:
                character_label.place_forget()

            prog_icon_path = current_theme.get("progress_icon", "")
            image_cache["progress"] = load_theme_image(prog_icon_path)

            studio_path = current_theme.get("studio_logo_image", "assets/images/studio_logo.png")
            image_cache["studio"] = load_theme_image(studio_path)
            if image_cache["studio"]:
                studio_logo_label.configure(image=image_cache["studio"], bg=bg)
                studio_logo_label.pack(pady=(2, 0))
            else:
                studio_logo_label.pack_forget()

            patreon_link_button.configure(bg=bg, activebackground=bg, fg=link)
            language_toggle_button.configure(bg=bg, activebackground=bg, fg=fg)
            hamburger_button.configure(bg=bg, activebackground=bg, fg=fg)
            theme_toggle_button.configure(bg=bg, activebackground=bg, fg=fg)
            try:
                nickname_toggle_button.configure(bg=bg, activebackground=bg, fg=fg)
            except NameError:
                pass
        
            header_label.configure(bg=bg, fg=fg)
            format_selection_frame.configure(bg=bg)
            format_label.configure(bg=bg, fg=fg_dim)
        
            # Apply theme to comboboxes and labels if present
            try:
                audio_combobox.configure(background=bg, foreground=fg)
                video_combobox.configure(background=bg, foreground=fg)
                image_combobox.configure(background=bg, foreground=fg)
            except Exception:
                pass
            try:
                # checkbuttons and labels adjust automatically via parent bg/fg
                pass
            except Exception:
                pass
        

        
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
            nonlocal current_theme_name, current_theme
            idx = theme_names.index(current_theme_name)
            next_idx = (idx + 1) % len(theme_names)
            current_theme_name = theme_names[next_idx]
            current_theme = available_themes[current_theme_name]
        
            configuration_data["theme"] = current_theme_name
            save_user_configuration(configuration_data)
            apply_theme_to_ui()

        def change_application_language():
            nonlocal current_language_code
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

            select_folder_button.config(text=active_translation["btn_select"])
            info_status_label.config(text=active_translation["info_desc"])
            language_toggle_button.config(text=active_translation["btn_lang"])
            patreon_link_button.config(text=active_translation["btn_patreon"])
        
            # Construir info de formatos traducida
            f_info = active_translation.get("formats_images", "IMAGES:") + "\n.png, .jpg, .jpeg, .bmp, .tga, .webp\n\n"
            f_info += active_translation.get("formats_videos", "VIDEO:") + "\n.mp4, .mkv, .webm, .avi, .mov, .wmv, .flv, .m4v, .mpg, .mpeg, .m2v, .3gp, .3g2, .ts, .m2ts, .vob, .ogv, .asf, .divx\n\n"
            f_info += active_translation.get("formats_audio", "AUDIO:") + "\n.wav, .mp3, .flac, .m4a, .ogg, .opus, .aac, .wma, .aiff, .aif, .alac, .amr, .mid, .midi, .mp2, .mpga, .au, .snd, .ra, .rm"
        
            hamburger_button.config(command=lambda: show_custom_popup(active_translation["formats_title"], f_info, is_accordion=True))
            refresh_format_labels()

        def show_custom_popup(title, message, is_error=False, is_accordion=False):
            bg = current_theme.get("bg_main", "#1e1e1e")
            fg = current_theme.get("fg_main", "#ffffff")
            fg_dim = current_theme.get("fg_dim", "#a3a3a3")
            accent = current_theme.get("accent", "#8b5cf6")
            accent_hover = current_theme.get("accent_hover", "#a78bfa")
        
            popup = tk.Toplevel(root_window)
            popup.title(title)
            popup.geometry("480x420") 
            popup.configure(bg=bg)
            popup.resizable(False, False)
            popup.transient(root_window)
            popup.wait_visibility()
            popup.grab_set()

            content_frame = tk.Frame(popup, bg=bg)
            content_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
            if not is_error and not is_accordion:
                success_path = current_theme.get("char_success", "assets/images/kaia_success.png")
                image_cache["success_kaia"] = load_theme_image(success_path)
                if image_cache["success_kaia"]:
                    tk.Label(content_frame, image=image_cache["success_kaia"], bg=bg).pack(pady=(5, 5))

            if is_accordion:
                popup.geometry("580x300")
                cols_f = tk.Frame(content_frame, bg=bg)
                cols_f.pack(fill="both", expand=True)
                scroll_f = tk.Frame(cols_f, bg=bg)
                scroll_f.pack(side="left", fill="both", expand=True)
                canvas = tk.Canvas(scroll_f, bg=bg, highlightthickness=0)
                inner_f = tk.Frame(canvas, bg=bg)
                inner_f.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                canvas.create_window((0, 0), window=inner_f, anchor="nw")
                canvas.pack(side="left", fill="both", expand=True)

                image_cache["info_kaia"] = load_theme_image("assets/images/kaia_info.png")
                if image_cache["info_kaia"]:
                    tk.Label(cols_f, image=image_cache["info_kaia"], bg=bg).pack(side="right", anchor="ne", padx=(10, 0))

                sections = message.split("\n\n")
                for sec in sections:
                    lines = sec.split("\n")
                    if lines:
                        tk.Label(inner_f, text=lines[0], bg=bg, fg=fg, font=("Arial", 10, "bold"), anchor="w").pack(fill="x", pady=(5, 0))
                        if len(lines) > 1:
                            tk.Label(inner_f, text="\n".join(lines[1:]), bg=bg, fg=fg_dim, font=("Arial", 9), justify="left", wraplength=350, anchor="w").pack(fill="x", padx=15)
            else:
                tk.Label(content_frame, text=message, bg=bg, fg=fg, font=("Arial", 10), justify="center", wraplength=400).pack(expand=True, fill="both")
        
            btn_frame = tk.Frame(popup, bg=bg)
            btn_frame.pack(fill="x", side="bottom", pady=20)
            ok_btn = tk.Button(btn_frame, text="OK", command=popup.destroy, bg=accent, fg="white", padx=40, pady=8, borderwidth=0, cursor="hand2", font=("Arial", 9, "bold"))
            ok_btn.pack()
            ok_btn.bind("<Enter>", lambda e: ok_btn.config(bg=accent_hover))
            ok_btn.bind("<Leave>", lambda e: ok_btn.config(bg=accent))

        def show_support_info():
            active_translation = languages_dictionary[current_language_code]
            bg = current_theme.get("bg_main", "#1e1e1e")
            fg = current_theme.get("fg_main", "#ffffff")
            accent = current_theme.get("accent", "#8b5cf6")
            popup = tk.Toplevel(root_window)
            popup.title(active_translation.get("support_title", "Support Alenia Studios"))
            popup.geometry("472x226")
            popup.configure(bg=bg)
            popup.transient(root_window)
            popup.wait_visibility()
            popup.grab_set()
            content_frame = tk.Frame(popup, bg=bg)
            content_frame.pack(expand=True, fill="both", padx=25, pady=20)
            columns_frame = tk.Frame(content_frame, bg=bg)
            columns_frame.pack(fill="both", expand=True)
            left_column = tk.Frame(columns_frame, bg=bg)
            left_column.pack(side="left", fill="both", expand=True)
            tk.Label(left_column, text=active_translation.get("support_label", "Support us on:"), bg=bg, fg=fg, font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
            links = [("Patreon", "https://patreon.com/alenia_studios"), ("Ko-fi", "https://ko-fi.com/alenia_studios"), ("GitHub", "https://github.com/Kaia-Alenia"), ("Itch.io", "https://alenia-studios.itch.io/"), ("PayPal", "https://www.paypal.com/ncp/payment/TCCYMCFSVMV8E")]
            btn_f = tk.Frame(left_column, bg=bg)
            btn_f.pack(anchor="w")
            for i, (name, url) in enumerate(links):
                tk.Button(btn_f, text=name, command=lambda u=url: webbrowser.open(u), bg=bg, fg=accent, relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2", font=("Arial", 10, "underline", "bold"), padx=5).grid(row=i//3, column=i%3, sticky="w", padx=2, pady=2)
            image_cache["support_kaia"] = load_theme_image("assets/images/kaia_support.png")
            if image_cache["support_kaia"]:
                tk.Label(columns_frame, image=image_cache["support_kaia"], bg=bg).pack(side="right", anchor="ne", padx=(15, 0))
            tk.Button(popup, text="OK", command=popup.destroy, bg=accent, fg="white", padx=30, pady=8, borderwidth=0, cursor="hand2", font=("Arial", 9, "bold")).pack(pady=(0, 20))

        def show_feedback_popup():
            bg = current_theme.get("bg_main", "#1e1e1e")
            fg = current_theme.get("fg_main", "#ffffff")
            accent = current_theme.get("accent", "#8b5cf6")
            accent_hover = current_theme.get("accent_hover", "#a78bfa")
            
            trans_dict = {
                "es": {
                    "title": "Comentarios",
                    "question": "¿Qué tal tu experiencia con Alenia Porter?",
                    "rating": "Calificación (1-5):",
                    "comments": "Comentarios o sugerencias:",
                    "send": "Enviar"
                },
                "en": {
                    "title": "Feedback",
                    "question": "How is your experience with Alenia Porter?",
                    "rating": "Rating (1-5):",
                    "comments": "Comments or suggestions:",
                    "send": "Send"
                },
                "fr": {
                    "title": "Commentaires",
                    "question": "Comment est votre expérience avec Alenia Porter ?",
                    "rating": "Évaluation (1-5) :",
                    "comments": "Commentaires ou suggestions :",
                    "send": "Envoyer"
                },
                "ja": {
                    "title": "フィードバック",
                    "question": "Alenia Porterの使い心地はいかがですか？",
                    "rating": "評価 (1-5):",
                    "comments": "コメントまたは提案:",
                    "send": "送信"
                },
                "zh": {
                    "title": "反馈",
                    "question": "您对 Alenia Porter 的体验如何？",
                    "rating": "评分 (1-5):",
                    "comments": "意见或建议:",
                    "send": "发送"
                },
                "ru": {
                    "title": "Отзыв",
                    "question": "Как вам опыт использования Alenia Porter?",
                    "rating": "Оценка (1-5):",
                    "comments": "Комментарии или предложения:",
                    "send": "Отправить"
                },
                "de": {
                    "title": "Feedback",
                    "question": "Wie ist Ihre Erfahrung mit Alenia Porter?",
                    "rating": "Bewertung (1-5):",
                    "comments": "Kommentare oder Vorschläge:",
                    "send": "Senden"
                },
                "pt": {
                    "title": "Feedback",
                    "question": "Como está sendo sua experiência com o Alenia Porter?",
                    "rating": "Avaliação (1-5):",
                    "comments": "Comentários ou sugestões:",
                    "send": "Enviar"
                }
            }
            lang = current_language_code if current_language_code in trans_dict else "en"
            t = trans_dict[lang]

            popup = tk.Toplevel(root_window)
            popup.title(t["title"])
            popup.geometry("450x300")
            popup.configure(bg=bg)
            popup.transient(root_window)
            popup.wait_visibility()
            popup.grab_set()
            
            content_frame = tk.Frame(popup, bg=bg)
            content_frame.pack(expand=True, fill="both", padx=20, pady=15)
            
            tk.Label(content_frame, text=t["question"], bg=bg, fg=fg, font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
            
            rating_frame = tk.Frame(content_frame, bg=bg)
            rating_frame.pack(anchor="w", pady=(0, 15))
            tk.Label(rating_frame, text=t["rating"], bg=bg, fg=fg).pack(side="left", padx=(0, 10))
            rating_var = tk.IntVar(value=5)
            for i in range(1, 6):
                tk.Radiobutton(rating_frame, text=str(i), variable=rating_var, value=i, bg=bg, fg=fg, selectcolor=accent, activebackground=bg).pack(side="left", padx=5)
                
            tk.Label(content_frame, text=t["comments"], bg=bg, fg=fg).pack(anchor="w", pady=(0, 5))
            comments_text = tk.Text(content_frame, height=5, width=45, bg="#2d2d2d", fg=fg, insertbackground=fg, borderwidth=1)
            comments_text.pack(fill="x", pady=(0, 15))
            
            def submit_feedback():
                rating = rating_var.get()
                comments = comments_text.get("1.0", "end").strip()
                threading.Thread(target=porter.send_feedback_stats, args=(rating, comments), daemon=True).start()
                configuration_data["feedback_shown"] = True
                save_user_configuration(configuration_data)
                popup.destroy()
                
            submit_btn = tk.Button(content_frame, text=t["send"], command=submit_feedback, bg=accent, fg="white", padx=30, pady=8, borderwidth=0, cursor="hand2", font=("Arial", 9, "bold"))
            submit_btn.pack(anchor="center")
            submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg=accent_hover))
            submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg=accent))


        def on_progressbar_increment(current_value, total_value):
            percent = int((current_value / total_value) * 100) if total_value > 0 else 0
            draw_progress(percent)
            root_window.update_idletasks()

        def on_conversion_success(processed_count, output_path, original_size, final_size):
            configuration_data["total_optimized"] = configuration_data.get("total_optimized", 0) + processed_count
            save_user_configuration(configuration_data)
            active_translation = languages_dictionary[current_language_code]
            success_color = current_theme.get("success", "#4ade80")
        
            saved_bytes = max(0, original_size - final_size)
            saved_percent = (saved_bytes / original_size * 100) if original_size > 0 else 0
            saved_mb = saved_bytes / (1024 * 1024)
        
            saving_report = f"\n\n📊 Total Savings: {saved_mb:.2f} MB ({saved_percent:.1f}%)"
        
            root_window.after(0, lambda: info_status_label.config(text=active_translation["msg_done"].format(processed_count), fg=success_color))
            draw_progress(100)
            root_window.after(0, lambda: select_folder_button.config(state=tk.NORMAL))
        
            if os.name == "nt": 
                try: os.startfile(output_path)
                except: pass
            else: 
                try: subprocess.Popen(["xdg-open" if sys.platform.startswith("linux") else "open", output_path])
                except: pass
            
            msg = active_translation["msg_success_m"].format(processed_count, output_path) + saving_report
            root_window.after(0, lambda: show_custom_popup(active_translation["msg_success_t"], msg))
            if not configuration_data.get("feedback_shown", False):
                root_window.after(2000, show_feedback_popup)

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
            # collect targets and start conversion with per-type options
            a_code, v_code, i_code, rec_flag, a_enabled, v_enabled, i_enabled = collect_targets()
            # If a type is disabled, pass placeholder values and porter will simply not find files for that type
            threading.Thread(target=porter.convert_media, args=(selected_directory, a_code, v_code, i_code, rec_flag, on_progressbar_increment, None, on_conversion_success, on_conversion_failure, current_language_code, False), daemon=True).start()

        def refresh_format_labels(*args):
            active_translation = languages_dictionary[current_language_code]
            # audio translations
            a0 = active_translation.get('format_ogg', 'OGG')
            a1 = active_translation.get('format_opus', 'OPUS')
            audio_vals = [a0, a1, 'MP3', 'FLAC', 'WAV', 'AAC']
            try:
                audio_combobox['values'] = audio_vals
                audio_display_var.set(audio_vals[0])
            except Exception:
                pass
            # video
            video_vals = ['WEBM', 'MP4']
            try:
                video_combobox['values'] = video_vals
                video_display_var.set(video_vals[0])
            except Exception:
                pass
            # images
            image_vals = ['WEBP', 'JPG', 'PNG']
            try:
                image_combobox['values'] = image_vals
                image_display_var.set(image_vals[0])
            except Exception:
                pass

        root_window = tk.Tk()
        def report_callback_exception(exc, val, tb):
            tb_text = "".join(traceback.format_exception(exc, val, tb))
            porter.log_error_to_file(tb_text)
            try:
                porter.send_crash_report("GUI_CALLBACK_EXCEPTION", f"{exc.__name__}: {str(val)}", tb_text)
            except:
                pass
            with open("ALENIA_ERROR.txt", "a", encoding="utf-8") as f:
                f.write(f"\n--- GUI FATAL ---\n{tb_text}\n")
            try:
                show_custom_popup("Error", f"Error: {str(val)}", is_error=True)
            except:
                pass
        root_window.report_callback_exception = report_callback_exception
        try:
            with porter.resource_path(os.path.join("assets", "images", "logo.ico")) as icon_path:
                root_window.iconbitmap(icon_path)
        except: pass
        initial_translation = languages_dictionary[current_language_code]
        root_window.title(initial_translation["title"])
        root_window.geometry("480x550")
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
        ToolTip(hamburger_button, lambda: languages_dictionary[current_language_code]["formats_title"])
        theme_toggle_button = tk.Button(top_navigation_bar, text="Theme", bg=bg_main, fg=fg_main, relief="flat", cursor="hand2", borderwidth=0, highlightthickness=0, activebackground=bg_main, command=cycle_theme, font=("Arial", 9, "bold"))
        theme_toggle_button.pack(side="right", padx=(0, 10))
        ToolTip(theme_toggle_button, "Theme")
        language_toggle_button = tk.Button(top_navigation_bar, text=initial_translation["btn_lang"], bg=bg_main, fg=fg_main, relief="flat", cursor="hand2", borderwidth=0, highlightthickness=0, activebackground=bg_main, command=change_application_language, font=("Arial", 9, "bold"))
        language_toggle_button.pack(side="right", padx=(0, 10))

        def on_nickname_button_click():
            show_profile_info()

        nickname_toggle_button = tk.Button(top_navigation_bar, text=f"({porter.get_local_nickname()})", bg=bg_main, fg=fg_main, relief="flat", cursor="hand2", borderwidth=0, highlightthickness=0, activebackground=bg_main, command=on_nickname_button_click, font=("Arial", 9, "bold"))
        nickname_toggle_button.pack(side="right", padx=(0, 10))

        header_label = tk.Label(root_window, text=initial_translation["header"], font=("Arial", 14, "bold"), bg=bg_main, fg=fg_main)
        header_label.pack(pady=(5, 15))
        format_selection_frame = tk.Frame(root_window, bg=bg_main)
        format_selection_frame.pack(pady=5)
        format_label = tk.Label(format_selection_frame, text=initial_translation["select_format"], bg=bg_main, fg=fg_dim, font=("Arial", 9))
        format_label.pack()
        # Per-type format selectors and options
        audio_enabled_var = tk.BooleanVar(value=True)
        video_enabled_var = tk.BooleanVar(value=True)
        image_enabled_var = tk.BooleanVar(value=True)
        recursive_var = tk.BooleanVar(value=True)

        # Display mappings
        audio_options_display = [initial_translation.get("format_ogg", "OGG"), initial_translation.get("format_opus", "OPUS"), "MP3", "FLAC", "WAV", "AAC"]
        audio_display_var = tk.StringVar(value=audio_options_display[0])
        audio_combobox = ttk.Combobox(format_selection_frame, textvariable=audio_display_var, values=audio_options_display, state="readonly", width=12)

        video_options_display = ["WEBM", "MP4"]
        video_display_var = tk.StringVar(value=video_options_display[0])
        video_combobox = ttk.Combobox(format_selection_frame, textvariable=video_display_var, values=video_options_display, state="readonly", width=8)

        image_options_display = ["WEBP", "JPG", "PNG"]
        image_display_var = tk.StringVar(value=image_options_display[0])
        image_combobox = ttk.Combobox(format_selection_frame, textvariable=image_display_var, values=image_options_display, state="readonly", width=8)

        # Layout in a compact row
        row_frame = tk.Frame(format_selection_frame, bg=bg_main)
        row_frame.pack(pady=6)

        # Audio column
        audio_col = tk.Frame(row_frame, bg=bg_main)
        audio_col.pack(side=tk.LEFT, padx=8)
        tk.Checkbutton(audio_col, text="Audio", variable=audio_enabled_var, bg=bg_main, fg=fg_main, selectcolor=accent_color, activebackground=bg_main, borderwidth=0).pack()
        audio_combobox.pack(in_=audio_col)

        # Video column
        video_col = tk.Frame(row_frame, bg=bg_main)
        video_col.pack(side=tk.LEFT, padx=8)
        tk.Checkbutton(video_col, text="Video", variable=video_enabled_var, bg=bg_main, fg=fg_main, selectcolor=accent_color, activebackground=bg_main, borderwidth=0).pack()
        video_combobox.pack(in_=video_col)

        # Image column
        image_col = tk.Frame(row_frame, bg=bg_main)
        image_col.pack(side=tk.LEFT, padx=8)
        tk.Checkbutton(image_col, text="Images", variable=image_enabled_var, bg=bg_main, fg=fg_main, selectcolor=accent_color, activebackground=bg_main, borderwidth=0).pack()
        image_combobox.pack(in_=image_col)

        # Recursive option
        tk.Checkbutton(format_selection_frame, text="Recursive (include subfolders)", variable=recursive_var, bg=bg_main, fg=fg_dim, borderwidth=0, activebackground=bg_main).pack(pady=(6,0))

        # helper to map display to internal codes
        def _map_audio_display_to_code(d):
            m = {
                initial_translation.get("format_ogg", "OGG"): "ogg",
                initial_translation.get("format_opus", "OPUS"): "opus",
                "MP3": "mp3",
                "FLAC": "flac",
                "WAV": "wav",
                "AAC": "aac"
            }
            return m.get(d, "opus")

        def _map_video_display_to_code(d):
            return "mp4" if d.lower() == "mp4" else "webm"

        def _map_image_display_to_code(d):
            if d.lower() in ("jpg", "jpeg"):
                return "jpg"
            if d.lower() == "png":
                return "png"
            return "webp"

        def collect_targets():
            return (_map_audio_display_to_code(audio_display_var.get()), _map_video_display_to_code(video_display_var.get()), _map_image_display_to_code(image_display_var.get()), recursive_var.get(), audio_enabled_var.get(), video_enabled_var.get(), image_enabled_var.get())

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

        def show_profile_info():
            bg = current_theme.get("bg_main", "#1e1e1e")
            fg = current_theme.get("fg_main", "#ffffff")
            accent = current_theme.get("accent", "#8b5cf6")
            popup = tk.Toplevel(root_window)
            popup.title("Profile")
            popup.geometry("380x280")
            popup.configure(bg=bg)
            popup.transient(root_window)
            popup.wait_visibility()
            popup.grab_set()
            content_frame = tk.Frame(popup, bg=bg)
            content_frame.pack(expand=True, fill="both", padx=20, pady=15)
            tk.Label(content_frame, text="User Profile", bg=bg, fg=fg, font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
            
            nick_frame = tk.Frame(content_frame, bg=bg)
            nick_frame.pack(fill="x", pady=2)
            tk.Label(nick_frame, text="Nickname:", bg=bg, fg=fg, font=("Arial", 10)).pack(side="left")
            nick_entry = tk.Entry(nick_frame, bg="#2d2d2d", fg=fg, insertbackground=fg, borderwidth=1)
            nick_entry.insert(0, porter.get_local_nickname())
            nick_entry.pack(side="left", padx=10, fill="x", expand=True)

            def save_nickname():
                new_nick = nick_entry.get().strip()
                if new_nick:
                    porter.set_local_nickname(new_nick)
                    nickname_toggle_button.configure(text=f"({new_nick})")
                    status_lbl.configure(text="Guardado", fg=current_theme.get("success", "#4ade80"))
                else:
                    status_lbl.configure(text="Invalido", fg=current_theme.get("error", "#f87171"))

            save_btn = tk.Button(nick_frame, text="OK", command=save_nickname, bg=accent, fg="white", borderwidth=0, cursor="hand2", padx=5)
            save_btn.pack(side="left")

            status_lbl = tk.Label(content_frame, text="", bg=bg, font=("Arial", 8))
            status_lbl.pack(anchor="w", pady=(0, 5))

            tk.Label(content_frame, text=f"UUID: {porter.get_local_uuid()}", bg=bg, fg=fg, font=("Arial", 9)).pack(anchor="w", pady=2)
            total_opt = configuration_data.get("total_optimized", 0)
            tk.Label(content_frame, text=f"Total Optimized Files: {total_opt}", bg=bg, fg=fg, font=("Arial", 10, "bold")).pack(anchor="w", pady=(8, 10))
            btn_frame = tk.Frame(content_frame, bg=bg)
            btn_frame.pack()
            close_btn = tk.Button(btn_frame, text="Close", command=popup.destroy, bg=accent, fg="white", padx=20, pady=5, borderwidth=0, cursor="hand2", font=("Arial", 9, "bold"))
            close_btn.pack()

        def prompt_update(new_ver, dl_url):
            trans = languages_dictionary[current_language_code]
            bg, fg, accent = current_theme["bg_main"], current_theme["fg_main"], current_theme["accent"]
            upd_win = tk.Toplevel(root_window)
            upd_win.title(trans.get("update_available_title", "Update"))
            upd_win.configure(bg=bg)
            upd_win.geometry("350x150")
            upd_win.transient(root_window)
            upd_win.wait_visibility()
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

        def check_startup_prompts():
            if not os.path.exists(config_file_path):
                show_profile_info()
            elif update_info["found"]:
                prompt_update(update_info["ver"], update_info["url"])

        apply_theme_to_ui()
        root_window.after(1500, check_startup_prompts)
        root_window.mainloop()

    except Exception as e:
        tb_text = traceback.format_exc()
        try:
            porter.send_crash_report("FATAL_MAIN_LOOP", str(e), tb_text)
        except:
            pass
        with open("ALENIA_ERROR.txt", "a", encoding="utf-8") as f: f.write(f"\n--- FATAL ---\n{tb_text}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()