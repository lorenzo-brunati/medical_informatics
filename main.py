import sqlite3 as sql
import customtkinter as ctk
import PIL.Image

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
    "sottotitolo": ("Montserrat", 17, "italic"),
    "testo_normale": ("Montserrat", 14),
    "testo_bold": ("Montserrat", 14, "bold"),
    "micro_bold": ("Montserrat", 8, "bold")
}


class LoginApp():
    def __init__(self): # Runs only ONCE
        
        # Both CONN and CURSOR are created as ATTRIBUTES of the CLASS
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()

        self.root = ctk.CTk() # ROOT (Main Window) in the Hierarchical Structure
        self.root.title("LoginApp") # Window NAME
        self.root.geometry("300x300") # Window SIZE (HxV)[Pixel]

        self.setup_gui() # Call the METHOD when OBJ is built

        self.root.mainloop() # Method to RUN Window


    def setup_gui(self): # Method of the CLASS
        # by passing the SELF everything initialized can be retrieved
        
        # TEXT LABEL
        self.login_label = ctk.CTkLabel(self.root, text="Insert Username and Password",
                                        font=('Arial', 14), width=300, height=30)
        self.login_label.place(x=0, y=30) # TOP-LEFT coordinate system

        #PASSWORD ENTRY
        self.pass_entry = ctk.CTkEntry(self.root, placeholder_text="Password",
                                       font=('Arial', 12), width=200, height=30, show="*")
        self.pass_entry.place(x=50, y=135)

        # USERNAME ENTRY
        self.user_entry = ctk.CTkEntry(self.root, placeholder_text="Username",
                                       font=('Arial', 12), width=200, height=30)
        self.user_entry.place(x=50, y=90)

        # LOGIN BUTTON
        self.login_button = ctk.CTkButton(self.root, text="Login",
                                          font=('Arial', 12), width=100, height=30,
                                          hover=True, command=self.login_callback)
        self.login_button.place(x=100, y=180)

        # OUTCOME LABEL
        self.outcome_label = ctk.CTkLabel(self.root, text="",
                                          font=('Arial', 12), width=300, height=30)
        self.outcome_label.place(x=0, y=240)

        self.user_type = None
        self.tax_code = None

    def login_callback(self):
        
        # Retrieve ENTRY Information
        user = (self.user_entry.get(), )
        pw = self.pass_entry.get()

        # Execute SQL Query
        self.cursor.execute("SELECT username FROM user WHERE username = ?", user)
        result = self.cursor.fetchone()
        
        if result is not None: # Existing USERNAME?
            self.cursor.execute("SELECT password FROM user WHERE username = ?", user)
            password = self.cursor.fetchone()[0]

            if pw == password:
                self.outcome_label.configure(text=f"Welcome back {user[0]}!")
                self.outcome_label.configure(text_color="green")

                self.cursor.execute("SELECT UserType FROM user WHERE username = ?", user)
                user_type = self.cursor.fetchone()[0]

                if user_type == "Patient":
                    PatientApp(user)
                elif user_type == "Doctor":
                    DoctorApp(user)
                else:
                    AdminApp(user)

            else:
                self.outcome_label.configure(text=f"Wrong Password")
                self.outcome_label.configure(text_color="red")

        else:
            self.outcome_label.configure(text="Username doesn't exist.") # UPDATE Label Text
            self.outcome_label.configure(text_color="red")

class DoctorApp():
    def __init__(self, username):

        self.user = username

        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()

        self.root = ctk.CTk()
        self.root.title("DoctorApp")
        self.root.geometry("1600x900")
        self.root.configure(fg_color="#F2F3F7")

        self.setup_gui()

        self.root.mainloop()
    
    def setup_gui(self):

        self.topbar = ctk.CTkFrame(self.root, width=1600, height=120, fg_color="#F2F3F7")
        self.topbar.place(x=0, y=0)

        self.cursor.execute("SELECT name FROM user WHERE username = ?", self.user)
        name = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT surname FROM user WHERE username = ?", self.user)
        surname = self.cursor.fetchone()[0]

        self.name = ctk.CTkLabel(self.topbar, text=f"Hey, Dr. {surname}!", font=('Roboto', 20), text_color="#8E9198")
        self.name.place(x=30, y=30)

        self.subtitle = ctk.CTkLabel(self.topbar, text="Let's get to work", font=('Roboto', 30),text_color="#282B3C")        
        self.subtitle.place(x=30, y=60)

        buttons_names = ["Dashboard", "Patients", "Schedule", "Reports"]
        self.menu_buttons = []

        self.button_menu = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.button_menu.place(x=475, y=20)

        for name in buttons_names:
            btn = ctk.CTkButton(
                self.button_menu,
                text=name,
                width=160,
                height=40,
                corner_radius=20,
                fg_color="transparent",
                text_color="#1A1A1A",
                font=("Roboto", 18, "bold")
            )

            btn.configure(command=lambda b=btn: self.handle_click(b))
            
            btn.pack(side="left", padx=5)
            self.menu_buttons.append(btn)
        
        if self.menu_buttons:
            self.handle_click(self.menu_buttons[0])

        
    def update_button_colors(self, clicked_button):
        for btn in self.menu_buttons:
            btn.configure(fg_color="transparent", text_color="#1A1A1A")
        
        clicked_button.configure(fg_color="#3366cc", text_color="white")

    def handle_click(self, button):
        self.update_button_colors(button)
        
        page = button.cget("text")
        if page == "Dashboard":
            print("Dashboard")
        elif page == "Patients":
            print("Patients")

class PatientApp():
    def __init__(self, username):
        self.user = username
        
        # Database e finestra principale
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()
        self.root = ctk.CTk()
        self.root.title("PatientApp")
        self.root.geometry("1600x900")
        
        # Questa mi serve per distruggere la pagina vecchia quando cambio sezione
        self.current_page_frame = None

        # Carico le icone e poi costruisco la grafica
        self.carica_icone()
        self.setup_gui()
        
        self.root.mainloop()

    def carica_icone(self):
        # Le carico una volta sola all'inizio così l'app è più veloce
        # light_image è quella che si vede sullo sfondo chiaro dell'app
        self.icon_notif = ctk.CTkImage(light_image=PIL.Image.open("icons/dark_bell.png"), size=(24, 24))
        self.icon_profile = ctk.CTkImage(light_image=PIL.Image.open("icons/dark_user.png"), size=(20, 20))
        # Versione chiara per quando il tasto diventa blu/scuro
        self.icon_notif_light = ctk.CTkImage(light_image=PIL.Image.open("icons/light_bell.png"), size=(24, 24))
        self.icon_profile_light = ctk.CTkImage(light_image=PIL.Image.open("icons/light_user.png"), size=(20, 20))

    # --- FUNZIONE PER PESCARE I DATI DAL DB ---
    def recupera_info_db(self):
        # Prendo l'ID del paziente
        self.cursor.execute("SELECT Id FROM USER WHERE Username = ?", self.user)
        user_row = self.cursor.fetchone()
        if not user_row: return None
        p_id = user_row[0]

        # Funzioncina interna per non ripetere la query chilometrica dei dati numerici
        def get_latest(metrica):
            self.cursor.execute("""
                SELECT N.Mean FROM DATA D 
                JOIN NUMERICAL_DATA N ON D.IdData = N.IdNumData 
                WHERE D.IdPatient = ? AND D.NameData = ? 
                ORDER BY D.Date DESC LIMIT 1
            """, (p_id, metrica))
            res = self.cursor.fetchone()
            return f"{res[0]:.1f}" if res else "--"

        # Recupero la terapia
        self.cursor.execute("SELECT Description FROM THERAPY WHERE IdPatient = ? ORDER BY Date DESC LIMIT 1", (p_id,))
        terapia = (self.cursor.fetchone() or ["No active therapy."])[0]

        # Recupero l'appuntamento
        self.cursor.execute("SELECT Date, Time FROM APPOINTMENT WHERE IdPatient = ? ORDER BY Date ASC LIMIT 1", (p_id,))
        app_res = self.cursor.fetchone()
        appuntamento = f"{app_res[0]} at {app_res[1]}" if app_res else "No upcoming appointments."

        # Impacchetto tutto e lo spedisco alla dashboard
        return {
            "vitals": f"SBP: {get_latest('SBP')} mmHg\n\nDBP: {get_latest('DBP')} mmHg\n\nHR: {get_latest('HR')} bpm",
            "fitness": f"VO2 Max: {get_latest('VO2Max')}\n\nSpO2: {get_latest('SPO2')} %",
            "activity": f"Sleep: {get_latest('SleepHours')} h\n\nSteps: {get_latest('StepCount')}",
            "therapy": terapia,
            "appointment": appuntamento
        }

    def setup_gui(self):
        # La barra in alto grigia
        self.topbar = ctk.CTkFrame(self.root, width=1600, height=100, fg_color=COLORS["sfondo_grigino"])
        self.topbar.place(x=0, y=0)

        # Prendo il nome dal database
        self.cursor.execute("SELECT name FROM user WHERE username = ?", self.user)
        res = self.cursor.fetchone()
        nome_utente = res[0] if res else "User"

        # Benvenuto in alto a sinistra
        ctk.CTkLabel(self.topbar, text=f"Hello, {nome_utente}", font=FONTS["sottotitolo"], 
                     text_color=COLORS["testo_chiaro"]).place(x=60, y=12)
        ctk.CTkLabel(self.topbar, text="Welcome back!", font=FONTS["titolo"], 
                     text_color=COLORS["testo_scuro"]).place(x=60, y=35)

        # Contenitore per i bottoni centrali
        self.menu_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.menu_frame.place(x=300, y=30)

        self.menu_buttons = {} # Uso un dizionario per trovarli subito per nome
        pagine = ["Dashboard", "Data", "Appointments", "Support"]

        for nome in pagine:
            btn = ctk.CTkButton(self.menu_frame, text=nome, width=140, height=35, corner_radius=20,
                                fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"],
                                font=FONTS["testo_normale"], border_width=1, border_color=COLORS["bordi"],
                                hover_color=COLORS["bordi"], 
                                command=lambda n=nome: self.cambia_pagina(n))
            btn.pack(side="left", padx=5)
            self.menu_buttons[nome] = btn

        # Bottoni a destra (Notifiche e Profilo)
        self.side_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.side_frame.place(x=1064, y=26)
        
        self.btn_notif = self.crea_tasto_icona(self.icon_notif, "Notifications")
        self.btn_profile = self.crea_tasto_icona(self.icon_profile, "Profile")

        # Menu a tendina che compare sotto il profilo
        self.profile_dropdown = ctk.CTkOptionMenu(self.root, values=["Personal Info", "Settings", "Logout"],
                                                command=self.gestisci_dropdown, width=150,
                                                dynamic_resizing=False,
                                                dropdown_fg_color=COLORS["testo_scuro"],
                                                dropdown_hover_color=COLORS["bordi"],
                                                dropdown_text_color=COLORS["sfondo_grigino"], 
                                                dropdown_font=FONTS["micro_bold"])

        # Partiamo dalla Dashboard
        self.cambia_pagina("Dashboard")

    def crea_tasto_icona(self, icona, nome):
        btn = ctk.CTkButton(self.side_frame, text="", image=icona, width=38, height=38, corner_radius=19,
                            fg_color=COLORS["bottone_grigio"], border_width=2, border_color=COLORS["bordi"],
                            hover_color=COLORS["bordi"], command=lambda: self.cambia_pagina(nome))
        btn.pack(side="left", padx=5)
        return btn
    
    def cambia_pagina(self, nome):
        # 1. Pulisco la pagina attuale
        if self.current_page_frame: 
            self.current_page_frame.destroy()
        
        # 2. RESET TOTALE: Riporto tutti i bottoni (testo e icone) allo stato grigio/scuro
        # Bottoni principali
        for b in self.menu_buttons.values():
            b.configure(fg_color=COLORS["bottone_grigio"], border_color=COLORS["bordi"], hover_color=COLORS["bordi"], text_color=COLORS["testo_scuro"], font=FONTS["testo_normale"])
        
        # Bottoni laterali (li rimettiamo scuri con sfondo grigio)
        self.btn_notif.configure(fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], image=self.icon_notif)
        self.btn_profile.configure(fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], image=self.icon_profile)

        # 3. ATTIVAZIONE: Chi è stato cliccato?
        if nome in self.menu_buttons:
            # Se è un bottone del menu principale: diventa blu con testo bianco
            self.menu_buttons[nome].configure(fg_color=COLORS["blu_acceso"], hover_color=COLORS["blu_acceso"], border_color=COLORS["blu_acceso"], text_color="white", font=FONTS["testo_bold"])
            self.mostra_dashboard() if nome == "Dashboard" else self.mostra_placeholder(nome)

        elif nome == "Notifications":
            # Inversione: sfondo scuro e icona chiara
            self.btn_notif.configure(fg_color=COLORS["testo_scuro"], hover_color=COLORS["testo_scuro"], border_color=COLORS["testo_scuro"], image=self.icon_notif_light)
            self.mostra_placeholder(nome)

        elif nome == "Profile":
            # Inversione: sfondo scuro e icona chiara
            self.btn_profile.configure(fg_color=COLORS["testo_scuro"], hover_color=COLORS["testo_scuro"], border_color=COLORS["testo_scuro"], image=self.icon_profile_light)
            self.apri_menu_profilo()

    def mostra_dashboard(self):
        dati = self.recupera_info_db()

        # Frame principale della dashboard
        self.current_page_frame = ctk.CTkFrame(self.root, fg_color=COLORS["sfondo_grigino"])
        self.current_page_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

        # Funzione helper interna per non ripetere 100 volte i parametri dei pannelli bianchi
        def aggiungi_pannello(x, y, w, h, titolo, info):
            p = ctk.CTkFrame(self.current_page_frame, fg_color="white", corner_radius=15, 
                             border_width=2, border_color=COLORS["bordi"])
            p.place(relx=x, rely=y, relwidth=w, relheight=h)
            
            ctk.CTkLabel(p, text=titolo, font=FONTS["testo_bold"], text_color=COLORS["testo_scuro"]).place(relx=0.05, rely=0.05)
            ctk.CTkLabel(p, text=info, font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"] if titolo == "ECG:" else COLORS["blu_acceso"], justify="left").place(relx=0.05, rely=0.25)

        # Colonna 1
        aggiungi_pannello(0.04, 0.05, 0.28, 0.42, "Vitals (Mean)", dati["vitals"])
        aggiungi_pannello(0.04, 0.52, 0.28, 0.42, "Oxygen & Fitness", dati["fitness"])

        # Colonna 2
        aggiungi_pannello(0.34, 0.05, 0.28, 0.42, "Daily Activity", dati["activity"])
        aggiungi_pannello(0.34, 0.52, 0.28, 0.42, "ECG:", "Signal data recorded.")

        # Colonna 3
        aggiungi_pannello(0.66, 0.05, 0.30, 0.58, "Therapy", dati["therapy"])
        aggiungi_pannello(0.66, 0.68, 0.30, 0.26, "Next Appointment", dati["appointment"])

    def apri_menu_profilo(self):
        # Calcolo dove si trova il tasto profilo per schiaffarci sotto il menu
        x = self.btn_profile.winfo_rootx() - self.root.winfo_rootx() -30
        y = self.btn_profile.winfo_rooty() - self.root.winfo_rooty()
        self.profile_dropdown.place(x=x - 110, y=y) # -110 per allinearlo un po' meglio
        self.root.update_idletasks()
        self.profile_dropdown._open_dropdown_menu()

    def gestisci_dropdown(self, scelta):
        if scelta == "Logout":
            self.root.destroy()
        else:
            print(f"Hai cliccato: {scelta}")

    def mostra_placeholder(self, nome):
        self.current_page_frame = ctk.CTkFrame(self.root, fg_color=COLORS["sfondo_grigino"])
        self.current_page_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        ctk.CTkLabel(self.current_page_frame, text=f"Section: {nome}", font=FONTS["titolo"]).pack(expand=True)


class AdminApp():
    def __init__(self):
        
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()

        self.root = ctk.CTk()
        self.root.title("AdminApp")
        self.root.geometry("400x400")

        self.setup_gui()

        self.root.mainloop()
    
    def setup_gui(self):
        self.temp = ctk.CTkLabel(self.root, text="Admin App",
                                        font=('Roboto', 14), width=300, height=30)
        self.temp.place(x=0, y=30)

#LoginApp()
user = ("mrossi",)
PatientApp(user)