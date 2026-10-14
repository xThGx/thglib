import tkinter as tk
from tkinter import ttk, messagebox
import db_manager


class UserManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Userverwaltung - System")
        self.geometry("900x550")
        self.minsize(800, 450)

        # Datenbank initialisieren
        db_manager.db_init()

        # Aktuell eingelogger User
        self.current_user = None

        # Custom Styling für Dark Theme SideNav
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Dark colors
        self.dark_bg = "#2b2b2b"
        self.button_bg = "#3c3f41"
        self.text_fg = "#ffffff"
        
        self.style.configure("Sidebar.TFrame", background=self.dark_bg)
        self.style.configure(
            "Sidebar.TButton",
            background=self.button_bg,
            foreground=self.text_fg,
            borderwidth=0,
            focuscolor="none",
            font=("Helvetica", 10)
        )
        self.style.map("Sidebar.TButton", background=[("active", "#4e5254")])

        # Haupt-Grid Konfiguration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- SIDEBAR (LINKS) ----------------
        self.sidebar_expanded_width = 180
        self.sidebar_collapsed_width = 45
        self.is_sidebar_expanded = True

        self.nav_frame = ttk.Frame(self, style="Sidebar.TFrame", width=self.sidebar_expanded_width)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_propagate(False)

        # Top-Left Toggle Button (☰)
        self.btn_toggle = ttk.Button(
            self.nav_frame, text="☰", style="Sidebar.TButton", command=self.toggle_sidebar, width=3
        )
        self.btn_toggle.pack(anchor="nw", padx=8, pady=8)

        # Button Container Frame
        self.btn_container = ttk.Frame(self.nav_frame, style="Sidebar.TFrame")
        self.btn_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.btn_home = ttk.Button(self.btn_container, text="Home", style="Sidebar.TButton", command=lambda: self.show_frame("HomeFrame"))
        self.btn_home.pack(fill="x", pady=4)

        self.btn_login = ttk.Button(self.btn_container, text="Login", style="Sidebar.TButton", command=lambda: self.show_frame("LoginFrame"))
        self.btn_login.pack(fill="x", pady=4)

        self.btn_register = ttk.Button(self.btn_container, text="Registrieren", style="Sidebar.TButton", command=lambda: self.show_frame("RegisterFrame"))
        self.btn_register.pack(fill="x", pady=4)

        self.btn_dashboard = ttk.Button(self.btn_container, text="Dashboard", style="Sidebar.TButton", command=lambda: self.show_frame("DashboardFrame"))
        self.btn_dashboard.pack(fill="x", pady=4)

        self.btn_logout = ttk.Button(self.btn_container, text="Abmelden", style="Sidebar.TButton", command=self.handle_logout)
        self.btn_logout.pack(fill="x", pady=4)

        # ---------------- CONTENT CONTAINER (RECHTS) ----------------
        self.container = ttk.Frame(self, padding=20)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Wörterbuch zur Verwaltung aller Frames
        self.frames = {}

        # Initialisiere die Ansichten
        for FrameClass in (HomeFrame, LoginFrame, RegisterFrame, DashboardFrame):
            page_name = FrameClass.__name__
            frame = FrameClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # UI & Buttons initialisieren
        self.update_nav_buttons()
        self.show_frame("HomeFrame")

    def toggle_sidebar(self):
        """Animiert das Ein- und Ausklappen der Sidebar."""
        current_width = self.nav_frame.winfo_width()
        
        if self.is_sidebar_expanded:
            target_width = self.sidebar_collapsed_width
            self.btn_container.pack_forget()
        else:
            target_width = self.sidebar_expanded_width

        def animate(w):
            step = -10 if self.is_sidebar_expanded else 10
            new_w = w + step
            
            if (self.is_sidebar_expanded and new_w > target_width) or (not self.is_sidebar_expanded and new_w < target_width):
                self.nav_frame.configure(width=new_w)
                self.after(10, lambda: animate(new_w))
            else:
                self.nav_frame.configure(width=target_width)
                self.is_sidebar_expanded = not self.is_sidebar_expanded
                if self.is_sidebar_expanded:
                    self.btn_container.pack(fill="both", expand=True, padx=5, pady=5)

        animate(current_width)

    def update_nav_buttons(self):
        """Aktualisiert die Navigationsbuttons basierend auf dem Login-Status."""
        if self.current_user:
            self.btn_dashboard.state(["!disabled"])
            self.btn_logout.pack(fill="x", pady=4)
            self.btn_login.state(["disabled"])
            self.btn_register.state(["disabled"])
        else:
            self.btn_dashboard.state(["disabled"])
            self.btn_logout.pack_forget()
            self.btn_login.state(["!disabled"])
            self.btn_register.state(["!disabled"])

    def show_frame(self, page_name: str):
        """Wechselt zur angegebenen Frame-Klasse."""
        frame = self.frames[page_name]

        if page_name == "DashboardFrame":
            if not self.current_user:
                messagebox.showwarning("Zugriff verweigert", "Bitte melden Sie sich zuerst an.")
                return
            frame.refresh_data()

        frame.tkraise()

    def handle_logout(self):
        """Meldet den aktuellen Benutzer ab."""
        self.current_user = None
        self.update_nav_buttons()
        messagebox.showinfo("Abgemeldet", "Sie wurden erfolgreich abgemeldet.")
        self.show_frame("HomeFrame")


class HomeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl_title = ttk.Label(self, text="Willkommen zur Userverwaltung", font=("Helvetica", 18, "bold"))
        lbl_title.pack(pady=20)

        self.lbl_info = ttk.Label(self, text="Bitte wählen Sie eine Option aus dem linken Menü.", font=("Helvetica", 11))
        self.lbl_info.pack(pady=10)


class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl_title = ttk.Label(self, text="Anmeldung", font=("Helvetica", 18, "bold"))
        lbl_title.pack(pady=20)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="E-Mail:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.ent_email = ttk.Entry(form_frame, width=30)
        self.ent_email.grid(row=0, column=1, pady=5, padx=5)
        self.ent_email.bind("<Return>", lambda event: self.ent_password.focus())

        ttk.Label(form_frame, text="Passwort:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.ent_password = ttk.Entry(form_frame, width=30, show="*")
        self.ent_password.grid(row=1, column=1, pady=5, padx=5)
        self.ent_password.bind("<Return>", lambda event: self.handle_login())

        btn_login = ttk.Button(self, text="Einloggen", command=self.handle_login)
        btn_login.pack(pady=10)

    def handle_login(self):
        email = self.ent_email.get()
        password = self.ent_password.get()

        erfolg, nachricht, user_info = db_manager.user_password_check(email, password)

        if erfolg and user_info is not None:
            self.controller.current_user = user_info
            self.controller.update_nav_buttons()
            messagebox.showinfo("Erfolg", f"Willkommen zurück, {user_info['firstname']}!")
            
            self.ent_email.delete(0, tk.END)
            self.ent_password.delete(0, tk.END)
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Anmeldefehler", nachricht)


class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl_title = ttk.Label(self, text="Neuen User registrieren", font=("Helvetica", 18, "bold"))
        lbl_title.pack(pady=20)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Vorname:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.ent_firstname = ttk.Entry(form_frame, width=30)
        self.ent_firstname.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Nachname:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.ent_lastname = ttk.Entry(form_frame, width=30)
        self.ent_lastname.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="E-Mail:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.ent_email = ttk.Entry(form_frame, width=30)
        self.ent_email.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Passwort:").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.ent_password = ttk.Entry(form_frame, width=30, show="*")
        self.ent_password.grid(row=3, column=1, pady=5, padx=5)
        self.ent_password.bind("<Return>", lambda event: self.handle_register())

        btn_register = ttk.Button(self, text="Konto anlegen", command=self.handle_register)
        btn_register.pack(pady=10)

    def handle_register(self):
        firstname = self.ent_firstname.get()
        lastname = self.ent_lastname.get()
        email = self.ent_email.get()
        password = self.ent_password.get()

        erfolg, nachricht = db_manager.user_create(firstname, lastname, email, password)

        if erfolg:
            messagebox.showinfo("Erfolg", nachricht)
            self.ent_firstname.delete(0, tk.END)
            self.ent_lastname.delete(0, tk.END)
            self.ent_email.delete(0, tk.END)
            self.ent_password.delete(0, tk.END)
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Fehler", nachricht)


class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.lbl_welcome = ttk.Label(self, text="Benutzerverwaltung Dashboard", font=("Helvetica", 16, "bold"))
        self.lbl_welcome.pack(anchor="w", pady=(0, 10))

        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=5)

        # Admin-Buttons
        self.btn_toggle_status = ttk.Button(top_bar, text="Status umschalten", command=self.toggle_user_status)
        self.btn_toggle_admin = ttk.Button(top_bar, text="Admin-Status ändern", command=self.toggle_admin_status)
        self.btn_add_user = ttk.Button(top_bar, text="Neuen User anlegen", command=self.open_add_user_dialog)

        btn_refresh = ttk.Button(top_bar, text="Tabelle aktualisieren", command=self.refresh_data)
        btn_refresh.pack(side="left", padx=5)

        # Tabelle erweitern um die Spalte 'role'
        columns = ("id", "firstname", "lastname", "email", "role", "last_login", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("firstname", text="Vorname")
        self.tree.heading("lastname", text="Nachname")
        self.tree.heading("email", text="E-Mail")
        self.tree.heading("role", text="Rolle")
        self.tree.heading("last_login", text="Letzter Login")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=35, anchor="center")
        self.tree.column("firstname", width=110)
        self.tree.column("lastname", width=110)
        self.tree.column("email", width=160)
        self.tree.column("role", width=70, anchor="center")
        self.tree.column("last_login", width=130)
        self.tree.column("status", width=70, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

    def refresh_data(self):
        if self.controller.current_user:
            user_name = self.controller.current_user['firstname']
            is_admin = self.controller.current_user.get("is_admin", False)
            role_str = " (Admin)" if is_admin else ""
            self.lbl_welcome.config(text=f"Willkommen, {user_name}{role_str} (Dashboard)")

            # Admin-Aktionen nur einblenden, wenn der User Admin ist
            if is_admin:
                self.btn_toggle_status.pack(side="left", padx=5)
                self.btn_toggle_admin.pack(side="left", padx=5)
                self.btn_add_user.pack(side="left", padx=5)
            else:
                self.btn_toggle_status.pack_forget()
                self.btn_toggle_admin.pack_forget()
                self.btn_add_user.pack_forget()

        for row in self.tree.get_children():
            self.tree.delete(row)

        users = db_manager.user_get_all(active_only=False)

        for u in users:
            status_str = "Aktiv" if u["is_active"] else "Inaktiv"
            role_str = "Admin" if u.get("is_admin", False) else "User"
            self.tree.insert(
                "",
                "end",
                values=(u["id"], u["firstname"], u["lastname"], u["email"], role_str, u["last_login"], status_str)
            )

    def toggle_user_status(self):
        """Aktiviert oder deaktiviert den ausgewählten User (nur Admin)."""
        if not self.controller.current_user.get("is_admin", False):
            messagebox.showerror("Zugriff verweigert", "Nur Admins dürfen den Benutzer-Status ändern.")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Hinweis", "Bitte wählen Sie zuerst einen User aus der Tabelle aus.")
            return

        item_values = self.tree.item(selected_item[0], "values")
        email = item_values[3]
        current_status = item_values[6]

        if email == self.controller.current_user["email"]:
            messagebox.showerror("Aktion nicht möglich", "Sie können Ihren eigenen Account nicht deaktivieren.")
            return

        neuer_status = False if current_status == "Aktiv" else True
        erfolg, nachricht = db_manager.user_set_active_status(email, neuer_status)

        if erfolg:
            messagebox.showinfo("Status geändert", nachricht)
            self.refresh_data()
        else:
            messagebox.showerror("Fehler", nachricht)

    def toggle_admin_status(self):
        """Macht den ausgewählten User zum Admin oder entzieht Admin-Rechte."""
        if not self.controller.current_user.get("is_admin", False):
            messagebox.showerror("Zugriff verweigert", "Nur Admins dürfen Admin-Rechte vergeben.")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Hinweis", "Bitte wählen Sie zuerst einen User aus der Tabelle aus.")
            return

        item_values = self.tree.item(selected_item[0], "values")
        email = item_values[3]
        current_role = item_values[4]

        if email == self.controller.current_user["email"]:
            messagebox.showerror("Aktion nicht möglich", "Sie können Ihren eigenen Admin-Status nicht entziehen.")
            return

        neuer_admin_status = False if current_role == "Admin" else True

        try:
            erfolg, nachricht = db_manager.user_set_admin_status(email, neuer_admin_status)
        except AttributeError:
            messagebox.showerror("Fehler", "Die Funktion 'user_set_admin_status' fehlt in db_manager.py.")
            return

        if erfolg:
            messagebox.showinfo("Rolle geändert", nachricht)
            self.refresh_data()
        else:
            messagebox.showerror("Fehler", nachricht)

    def open_add_user_dialog(self):
        """Öffnet ein modales Fenster zum Anlegen eines neuen Benutzers durch Admins."""
        dialog = tk.Toplevel(self)
        dialog.title("Neuen Benutzer anlegen (Admin)")
        dialog.geometry("380x300")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        lbl_title = ttk.Label(dialog, text="Neuen Benutzer erstellen", font=("Helvetica", 14, "bold"))
        lbl_title.pack(pady=15)

        form_frame = ttk.Frame(dialog)
        form_frame.pack(pady=5, padx=20)

        ttk.Label(form_frame, text="Vorname:").grid(row=0, column=0, sticky="w", pady=5)
        ent_firstname = ttk.Entry(form_frame, width=25)
        ent_firstname.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Nachname:").grid(row=1, column=0, sticky="w", pady=5)
        ent_lastname = ttk.Entry(form_frame, width=25)
        ent_lastname.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="E-Mail:").grid(row=2, column=0, sticky="w", pady=5)
        ent_email = ttk.Entry(form_frame, width=25)
        ent_email.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Passwort:").grid(row=3, column=0, sticky="w", pady=5)
        ent_password = ttk.Entry(form_frame, width=25, show="*")
        ent_password.grid(row=3, column=1, pady=5, padx=5)

        var_is_admin = tk.BooleanVar(value=False)
        chk_admin = ttk.Checkbutton(form_frame, text="Als Admin anlegen", variable=var_is_admin)
        chk_admin.grid(row=4, column=1, sticky="w", pady=5)

        def save_user():
            fname = ent_firstname.get()
            lname = ent_lastname.get()
            email = ent_email.get()
            pwd = ent_password.get()
            is_adm = var_is_admin.get()

            if not fname or not lname or not email or not pwd:
                messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen.", parent=dialog)
                return

            try:
                erfolg, nachricht = db_manager.user_create(fname, lname, email, pwd, is_admin=is_adm)
            except TypeError:
                erfolg, nachricht = db_manager.user_create(fname, lname, email, pwd)

            if erfolg:
                messagebox.showinfo("Erfolg", nachricht, parent=dialog)
                dialog.destroy()
                self.refresh_data()
            else:
                messagebox.showerror("Fehler", nachricht, parent=dialog)

        btn_save = ttk.Button(dialog, text="Benutzer speichern", command=save_user)
        btn_save.pack(pady=15)


if __name__ == "__main__":
    app = UserManagementApp()
    app.mainloop()