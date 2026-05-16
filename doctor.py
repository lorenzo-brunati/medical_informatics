import customtkinter as ctk
import sqlite3 as sql

# --- I MIEI COLORI ---
# Li tengo qui così se mi stufo del blu cambio solo una riga
COLORS = {
    "sfondo_grigino": "#E8EBF2",
    "bianco_puro": "#FFFFFF",
    "blu_acceso": "#3366cc",
    "testo_scuro": "#475569",
    "testo_chiaro": "#9DA1A7",
    "bordi": "#BFC6D1",
    "bottone_grigio": "#DCE1E9"
}

# --- I MIEI FONT ---
# Montserrat è ovunque, qui decido solo le grandezze
FONTS = {
    "titolo": ("Montserrat", 22, "bold"),
    "sottotitolo": ("Montserrat", 16, "italic"),
    "testo_normale": ("Montserrat", 14),
    "testo_bold": ("Montserrat", 14, "bold"),
    "micro_bold": ("Montserrat", 8, "bold")
}

class DoctorApp():
    def __init__(self, ID):
        
        self.ID = ID
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()

        self.root = ctk.CTk()
        self.root.title("DoctorApp")

        self.root.geometry("1600x900")
        
        self.setup_gui()
        self.root.mainloop()

    def setup_gui(self):

        self.topbar = ctk.CTkFrame(self.root, fg_color=COLORS["sfondo_grigino"])
        self.topbar.place(relx=0, rely=0, relheight=0.1, relwidth=1)

        self.main = ctk.CTkFrame(self.root, fg_color="#000000")
        self.main.place(relx=0, rely=0.1, relheight=0.9, relwidth=1)

        self.welcome()
        self.nav_buttons()

    def welcome(self):

        self.cursor.execute("SELECT surname FROM user WHERE ID = ?", self.ID)
        surname = self.cursor.fetchall()[0][0] 

        self.surname_label = ctk.CTkLabel(self.topbar, text=f"Hello Mr. {surname}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
        self.surname_label.place(x=30, y=30)

        self.welcome_label = ctk.CTkLabel(self.topbar, text="Welcome Back!", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.welcome_label.place(x=30, y=50)

    def nav_buttons(self):

        self.container = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.container.place(relx=0.3, rely=0, relheight=1, relwidth=0.5)

        self.buttons_dict = {}
        buttons = ["Dashboard", "Patients", "Appointments", "Support"]
        for b in buttons:
            btn = ctk.CTkButton(self.container, text=b, text_color=COLORS["testo_scuro"], font=FONTS["testo_normale"],
                                command = lambda b=b: self.switch_tab(b), width=150, height=40, corner_radius=20,
                                fg_color=COLORS["bottone_grigio"], border_color=COLORS["bordi"], hover_color=COLORS["blu_acceso"])
            btn.pack(side="left", padx=10)
            self.buttons_dict[b] = btn
        
        self.update_buttons("Dashboard")

    def switch_tab(self, tab):
        self.update_buttons(tab)

    def update_buttons(self, current_tab):
        for tab, btn in self.buttons_dict.items():
            if tab == current_tab:
                btn.configure(fg_color=COLORS["blu_acceso"], text_color=COLORS["bianco_puro"])
            else:
                btn.configure(fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"])





ID = (11,)
DoctorApp(ID)