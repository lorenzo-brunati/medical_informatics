import customtkinter as ctk
import sqlite3 as sql

from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
import PIL
import struct
import bcrypt

from tkinter import filedialog
from tkinter import messagebox
import shutil

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
        
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
    "sottotitolo": ("Montserrat", 17),
    "testo_normale": ("Montserrat", 14),
    "titolo_menu": ("Montserrat", 18),
    "testo_bold": ("Montserrat", 14, "bold"),
    "micro_bold": ("Montserrat", 8, "bold")
}

# --- UNITA DI MISURA PER I DATI NUMERICI ---
UNITS = {
    "Systolic BP": "mmHg",       # Millimetri di mercurio
    "Diastolic BP": "mmHg",      # Millimetri di mercurio
    "Heart Rate": "bpm",         # Battiti al minuto
    "Step Count": "steps",       # Conteggio passi
    "Sleep Hours": "hours",        # Ore di sonno
    "SPO2": "%",                 # Percentuale di ossigeno nel sangue
    "VO2max": "mL/kg/min"        # Millilitri di ossigeno per chilogrammo al minuto
}

# Setto Montserrat come font di default per tutto il programma
ctk.ThemeManager.theme["CTkFont"]["family"] = "Montserrat"

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
                                        font=('Montserrat', 14), width=300, height=30)
        self.login_label.place(x=0, y=30) # TOP-LEFT coordinate system

        #PASSWORD ENTRY
        self.pass_entry = ctk.CTkEntry(self.root, placeholder_text="Password",
                                       font=('Montserrat', 12), width=200, height=30, show="*")
        self.pass_entry.place(x=50, y=135)

        # USERNAME ENTRY
        self.user_entry = ctk.CTkEntry(self.root, placeholder_text="Username",
                                       font=('Montserrat', 12), width=200, height=30)
        self.user_entry.place(x=50, y=90)

        # LOGIN BUTTON
        self.login_button = ctk.CTkButton(self.root, text="Login",
                                          font=('Montserrat', 12, 'bold'), width=100, height=30, fg_color=COLORS["blu_acceso"], text_color=COLORS["bianco_puro"],
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
            hash_password = self.cursor.fetchone()[0]

            hash_password_bytes = hash_password.encode("utf-8")
            pw_bytes = pw.encode("utf-8")

            if bcrypt.checkpw(pw_bytes, hash_password_bytes):
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
        
        # Questa mi serve per distruggere le pagine vecchie quando cambio sezione
        self.current_page_frame = None
        self.profile_page_frame = None

        # Recupero le informazioni personali dal database
        self.cursor.execute("SELECT Id, Name, Surname, BirthDate, Address, PhoneNumber, Email, Username, Password, FiscalCode FROM user WHERE username = ?", (self.user[0],))
        self.user_data = self.cursor.fetchone()

        self.p_id = self.user_data[0]
        self.patient_name = self.user_data[1]
        self.patient_surname = self.user_data[2]
        self.patient_birthdate = self.user_data[3]
        self.patient_fiscal_code = self.user_data[9]
        self.patient_age = self.get_age()[0]

        self.doctor = self.get_doctor()
        self.doctor_name = self.doctor[0]
        self.doctor_surname = self.doctor[1]
        self.doctor_id = self.doctor[2]

        # Recupero peso e altezza del paziente
        query = """
                    SELECT Height, Weight
                    FROM PATIENT_CLINICALDATA
                    WHERE IdPatient = ?
                """
        
        self.cursor.execute(query, (self.p_id,))
        clinical = self.cursor.fetchall()[0]
        self.patient_height = clinical[0]
        self.patient_weight = clinical[1]

        # Carico le icone e poi costruisco la grafica
        self.carica_icone()
        self.setup_gui()
        
        self.root.mainloop()

    def carica_icone(self):
        # Le carico una volta sola all'inizio così l'app è più veloce
        # light_image è quella che si vede sullo sfondo chiaro dell'app
        self.icon_notif = ctk.CTkImage(light_image=PIL.Image.open("icons/dark_support.png"), size=(20, 20))
        self.icon_profile = ctk.CTkImage(light_image=PIL.Image.open("icons/dark_user.png"), size=(20, 20))
        # Versione chiara per quando il tasto diventa blu/scuro
        self.icon_notif_light = ctk.CTkImage(light_image=PIL.Image.open("icons/light_support.png"), size=(24, 24))
        self.icon_profile_light = ctk.CTkImage(light_image=PIL.Image.open("icons/light_user.png"), size=(20, 20))

    def setup_gui(self):
        # La barra in alto grigia
        self.topbar = ctk.CTkFrame(self.root, width=1600, height=100, fg_color=COLORS["sfondo_grigino"])
        self.topbar.place(x=0, y=0)

        # Prendo il nome dal database
        self.cursor.execute("SELECT name FROM user WHERE username = ?", self.user)
        res = self.cursor.fetchone()
        nome_utente = res[0] if res else "User"

        # Benvenuto in alto a sinistra
        ctk.CTkLabel(self.topbar, height=0, fg_color='transparent', text=f"Hello, {nome_utente}", font=FONTS["sottotitolo"], 
                     text_color=COLORS["testo_chiaro"]).place(x=45, y=18)
        ctk.CTkLabel(self.topbar, height=0, fg_color='transparent', text="Welcome back!", font=FONTS["titolo"], 
                     text_color=COLORS["testo_scuro"]).place(x=45, y=39)

        # Contenitore per i bottoni centrali
        self.menu_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.menu_frame.place(x=300, y=30)

        self.menu_buttons = {} # Uso un dizionario per trovarli subito per nome
        pagine = ["Dashboard", "Data", "Appointments", "Messages"]

        for nome in pagine:
            btn = ctk.CTkButton(self.menu_frame, text=nome, width=140, height=35, corner_radius=20,
                                fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"],
                                font=FONTS["testo_normale"],  border_color=COLORS["bordi"],
                                hover_color=COLORS["bordi"], 
                                command=lambda n=nome: self.cambia_pagina(n))
            btn.pack(side="left", padx=5)
            self.menu_buttons[nome] = btn

        # Bottoni a destra (Notifiche e Profilo)
        self.side_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.side_frame.place(x=1064, y=26)
        
        self.btn_supp = self.crea_tasto_icona(self.icon_notif, "Support")
        self.btn_profile = self.crea_tasto_icona(self.icon_profile, "Profile")

        # Partiamo dalla Dashboard
        self.cambia_pagina("Dashboard")

    def crea_tasto_icona(self, icona, nome):
        btn = ctk.CTkButton(self.side_frame, text="", image=icona, width=38, height=38, corner_radius=19,
                            fg_color=COLORS["bottone_grigio"],  border_color=COLORS["bordi"], border_width=1,
                            hover_color=COLORS["bordi"], command=lambda: self.cambia_pagina(nome))
        btn.pack(side="left", padx=5)
        return btn
    
    def cambia_pagina(self, nome):
        # Verifica che il frame esista
        if hasattr(self, 'current_page_frame') and self.current_page_frame:
            try:
                self.current_page_frame.destroy()
            except Exception as e:
                print(f"Errore durante la distruzione: {e}")

        self.current_page_frame = ctk.CTkFrame(self.root, fg_color=COLORS["sfondo_grigino"])
        self.current_page_frame.place(relx=0, rely=0.12, relwidth=1, relheight=0.88)
        
        # Riporto tutti i bottoni (testo e icone) allo stato grigio/scuro tranne quelli che sono stati cliccati, quelli diventano blu con testo bianco o icona chiara a seconda del caso
        for chiave,b in self.menu_buttons.items():
            self.root.update_idletasks()
            if chiave != nome:
                b.configure(fg_color=COLORS["bottone_grigio"], border_color=COLORS["bordi"], hover_color=COLORS["bordi"], text_color=COLORS["testo_scuro"], font=FONTS["testo_normale"])
            else:
                b.configure(fg_color=COLORS["blu_acceso"], hover_color=COLORS["blu_acceso"], border_color=COLORS["blu_acceso"], text_color=COLORS["sfondo_grigino"], font=FONTS["testo_bold"])
    
        # Bottoni laterali
        self.root.update_idletasks()
        if nome == "Support":
                    # Inversione: sfondo scuro e icona chiara
                    self.btn_supp.configure(fg_color=COLORS["testo_scuro"], hover_color=COLORS["testo_scuro"], border_color=COLORS["testo_scuro"], image=self.icon_notif_light)
                    self.mostra_support()
        elif nome == "Profile":
                    # Inversione: sfondo scuro e icona chiara
                    self.btn_profile.configure(fg_color=COLORS["testo_scuro"], hover_color=COLORS["testo_scuro"], border_color=COLORS["testo_scuro"], image=self.icon_profile_light)
                    self.mostra_profilo()

        self.btn_supp.configure(fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], image=self.icon_notif) if nome != "Support" else None
        self.btn_profile.configure(fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], image=self.icon_profile) if nome != "Profile" else None

        # Funzioni che mostrano i contenuti 
        if nome == "Dashboard":
            self.mostra_dashboard()

        elif nome == "Data":
            self.mostra_dati()

        elif nome == "Appointments":
            self.mostra_appuntamenti()
        
        elif nome == "Messages":
            self.mostra_messaggi()

   # DASHBOARD
    def mostra_dashboard(self):
        # Svuota il frame principale per evitare sovrapposizioni
        for widget in self.current_page_frame.winfo_children():
            widget.destroy()

        dati = self.recupera_latest_data_db()

        # Funzione interna per supportare il posizionamento flessibile dei contenuti
        def aggiungi_pannello(x, y, w, h, titolo):
            p = ctk.CTkFrame(self.current_page_frame, fg_color="white", corner_radius=15, 
                             border_width=2, border_color=COLORS["bordi"])
            p.place(relx=x, rely=y, relwidth=w, relheight=h)
            
            # Titolo del Pannello ben visibile
            ctk.CTkLabel(p, text=titolo, font=("Montserrat", 20, "bold"), text_color=COLORS["blu_acceso"]).place(relx=0.06, rely=0.06)
            return p

        # Parametri fisiologici
        p_vitals = aggiungi_pannello(0.03, 0.05, 0.30, 0.42, "Vitals")
        p_fitness = aggiungi_pannello(0.03, 0.53, 0.30, 0.42, "Oxygen & Fitness")
        
        # Recuperiamo i singoli valori numerici per non avere un,.a stringa unica
        sbp_val = dati["vitals_raw"]["SBP"]
        dbp_val = dati["vitals_raw"]["DBP"]
        hr_val  = dati["vitals_raw"]["HR"]
        spo2_val = dati["vitals_raw"]["SPO2"]
        vo2_val  = dati["vitals_raw"]["VO2Max"]

        # Attività e segnali
        p_activity = aggiungi_pannello(0.36, 0.05, 0.30, 0.42, "Daily Activity")
        p_ecg = aggiungi_pannello(0.36, 0.53, 0.30, 0.42, "ECG Status")
    
        sleep_val = dati["activity"]["Sleep"]
        steps_val = dati["activity"]["Steps"]

        # --- LABELS PANNELLO 1: VITALS ---
        ctk.CTkLabel(p_vitals, text="SYS PRESSURE ", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.08, rely=0.24)
        ctk.CTkLabel(p_vitals, text=sbp_val, font=("Montserrat", 34, "bold"), text_color=COLORS["testo_scuro"], height=0).place(relx=0.08, rely=0.31)
        ctk.CTkLabel(p_vitals, text="mmHg", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.08, rely=0.49)

        ctk.CTkLabel(p_vitals, text="DIA PRESSURE ", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.55, rely=0.24)
        ctk.CTkLabel(p_vitals, text=dbp_val, font=("Montserrat", 34, "bold"), text_color=COLORS["testo_scuro"], height=0).place(relx=0.55, rely=0.31)
        ctk.CTkLabel(p_vitals, text="mmHg", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.55, rely=0.49)

        ctk.CTkLabel(p_vitals, text="HEART RATE ", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.08, rely=0.63)
        ctk.CTkLabel(p_vitals, text=hr_val, font=("Montserrat", 34, "bold"), text_color=COLORS["testo_scuro"], height=0).place(relx=0.08, rely=0.70)
        ctk.CTkLabel(p_vitals, text="bpm", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.08, rely=0.88)


        # --- LABELS PANNELLO 2: OXYGEN & FITNESS ---
        ctk.CTkLabel(p_fitness, text="BLOOD OXYGEN ", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.08, rely=0.28)
        ctk.CTkLabel(p_fitness, text=spo2_val, font=("Montserrat", 34, "bold"), text_color=COLORS["testo_scuro"], height=0).place(relx=0.08, rely=0.35)
        ctk.CTkLabel(p_fitness, text="%", font=("Montserrat", 12, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.09, rely=0.53)

        ctk.CTkLabel(p_fitness, text="VO2 MAX ", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.55, rely=0.28)
        ctk.CTkLabel(p_fitness, text=vo2_val, font=("Montserrat", 34, "bold"), text_color=COLORS["testo_scuro"], height=0).place(relx=0.55, rely=0.35)
        ctk.CTkLabel(p_fitness, text="ml/kg/min", font=("Montserrat", 8, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.55, rely=0.53)


        # --- LABELS PANNELLO 3: DAILY ACTIVITY ---
        ctk.CTkLabel(p_activity, text="SLEEP ", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.08, rely=0.24)
        ctk.CTkLabel(p_activity, text=sleep_val, font=("Montserrat", 34, "bold"), text_color=COLORS["testo_scuro"], height=0).place(relx=0.08, rely=0.31)
        ctk.CTkLabel(p_activity, text="hours", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.08, rely=0.49)

        ctk.CTkLabel(p_activity, text="STEPS COUNT ", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.55, rely=0.24)
        ctk.CTkLabel(p_activity, text=steps_val, font=("Montserrat", 34, "bold"), text_color=COLORS["testo_scuro"], height=0).place(relx=0.55, rely=0.31)
        ctk.CTkLabel(p_activity, text="steps", font=("Montserrat", 10, "bold"), text_color=COLORS["testo_chiaro"], height=0).place(relx=0.55, rely=0.49)


        # --- LABELS PANNELLO 4: ECG STATUS ---
        self.draw_last_ecg(p_ecg)
        
        
        # Terapia e interazioni
        # Pannello therapy
        p_therapy = aggiungi_pannello(0.69, 0.05, 0.28, 0.28, "Active Therapy")
        ctk.CTkLabel(p_therapy, text=dati["active therapy_short"], font=FONTS["testo_bold"], text_color=COLORS["testo_chiaro"], justify="left", wraplength=300).place(relx=0.08, rely=0.28)
        
        # Bottone "Details" per la Terapia (apre il popup dedicato)
        if dati["has_therapy"]:
            btn_th = ctk.CTkButton(p_therapy, text="Details", width=85, height=26, corner_radius=12,
                                fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], border_color=COLORS['bordi'],
                                command=self.show_therapy)
            btn_th.place(relx=0.08, rely=0.76)

        # Pannello last message
        p_msg = aggiungi_pannello(0.69, 0.37, 0.28, 0.28, "Last Message")
        ctk.CTkLabel(p_msg, text=f"{dati["last_msg_text"][:60]}...", font=FONTS["testo_bold"], text_color=COLORS["testo_chiaro"], justify="left", wraplength=300).place(relx=0.08, rely=0.28)
        
        # Bottoni del Messaggio
        if dati["last_msg_details"] is not None:
            btn_msg_view = ctk.CTkButton(p_msg, text="Details", width=85, height=26, corner_radius=12,
                                         fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], border_color=COLORS['bordi'], 
                                         command=lambda: self.view_message(dati["last_msg_details"][0], dati["last_msg_details"][1], dati["last_msg_details"][2], dati["last_msg_text"], dati["last_msg_details"][3], dati["last_msg_details"][4]))
            btn_msg_view.place(relx=0.35, rely=0.76)
        
        btn_msg_all = ctk.CTkButton(p_msg, text="Show All", width=85, height=26, corner_radius=12,
                                     fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], border_color=COLORS['bordi'], 
                                     command=lambda: self.cambia_pagina("Messages"))
        btn_msg_all.place(relx=0.08, rely=0.76)

        # Pannello next appointment
        p_app = aggiungi_pannello(0.69, 0.69, 0.28, 0.26, "Next Appointment")
        ctk.CTkLabel(p_app, text=dati["upcoming appointment"], font=FONTS["testo_bold"], text_color=COLORS["testo_chiaro"], justify="left").place(relx=0.08, rely=0.30)
        
        # Bottoni dell'Appuntamento
        if dati["has_appointment"]:
            btn_app_det = ctk.CTkButton(p_app, text="Details", width=85, height=26, corner_radius=12,
                                         fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], border_color=COLORS['bordi'], 
                                         command=lambda: self.open_appointment(dati["app_raw_data"]))
            btn_app_det.place(relx=0.35, rely=0.68)
            
        btn_app_all = ctk.CTkButton(p_app, text="Show All", width=85, height=26, corner_radius=12,
                                     fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], border_color=COLORS['bordi'], 
                                     command=lambda: self.cambia_pagina("Appointments"))
        btn_app_all.place(relx=0.08, rely=0.68)


    # Recupero dati dal DB 
    def recupera_latest_data_db(self):
        def get_latest(metrica):
            self.cursor.execute("""
                SELECT N.Mean FROM DATA D 
                JOIN NUMERICAL_DATA N ON D.IdData = N.IdNumData 
                WHERE D.IdPatient = ? AND D.NameData = ? 
                ORDER BY D.Date DESC, D.IdData DESC LIMIT 1
            """, (self.p_id, metrica))
            res = self.cursor.fetchone()
            return f"{res[0]:.1f}" if res else "--"

        # Recupero la terapia
        self.cursor.execute("SELECT Date, Description FROM THERAPY WHERE IdPatient = ? ORDER BY Date DESC LIMIT 1", (self.p_id,))
        self.current_therapy = self.cursor.fetchone()
        has_therapy = self.current_therapy is not None
        therapy_short = f"{self.current_therapy[0]}:\n{self.current_therapy[1][:60]}..." if has_therapy else "No active therapy."

        # Cerchiamo l'ultimo messaggio non letto non inviato dal paziente stesso (IdSender != self.p_id o simile a seconda della tua logica)
        self.cursor.execute("""
            SELECT IDNotification, IdSender, IdReceiver, Date, Time, Message
            FROM Notification 
            WHERE IdReceiver = ? AND IsRead = FALSE
            ORDER BY Date DESC, Time DESC LIMIT 1
        """, (self.p_id,))
        last_msg = self.cursor.fetchone()
        
        if last_msg:
            last_msg_details = [last_msg[0], last_msg[1], last_msg [2], last_msg [3], last_msg [4]]

            # Accorcia il testo se è troppo lungo per il box della dashboard
            testo_msg = last_msg[5]
            last_msg_text = f"{last_msg[3]} {last_msg[4]}:\n\"{testo_msg}\""
        else:
            last_msg_details = None
            last_msg_text = "No unread messages."

        # Recupero l'appuntamento futuro più vicino
        self.cursor.execute("""
            SELECT IdAppointment, Date, Time, Notes 
            FROM APPOINTMENT 
            WHERE IdPatient = ? AND Date >= DATE('now', 'localtime')
            ORDER BY Date ASC, Time ASC LIMIT 1
        """, (self.p_id,))
        self.next_app_info = self.cursor.fetchone()
        has_appointment = self.next_app_info is not None
        next_appointment = f"{self.next_app_info[1]} at {self.next_app_info[2]}" if has_appointment else "No upcoming appointments."

        vitals_raw = {
            "SBP": get_latest('SBP'),
            "DBP": get_latest('DBP'),
            "HR": get_latest('HR'),
            "SPO2": get_latest('SPO2'),
            "VO2Max": get_latest('VO2Max')
        }

        activity_raw = {
            "Sleep": get_latest('SleepHours'), 
            "Steps": get_latest('StepCount')
        }

        return {
            "vitals_raw": vitals_raw,
            "fitness": f"...",
            "activity" : activity_raw,
            "has_therapy": has_therapy,
            "active therapy_short": therapy_short,
            "last_msg_details": last_msg_details,
            "last_msg_text": last_msg_text,
            "has_appointment": has_appointment,
            "upcoming appointment": next_appointment,
            "app_raw_data": self.next_app_info
        }
   



    def draw_last_ecg(self, panel):
        # Query per recuperare data/ora e la stringa del tracciato dell'ultimo ECG
        query = """
            SELECT S.Value, S.Sampling_Freq, D.Date, S.Time
            FROM SIGNALS S
            JOIN DATA as D ON S.IdSignals = D.IdData 
            WHERE D.IdPatient = ? 
            AND D.NameData = 'ECG'  
            ORDER BY D.Date DESC, S.Time DESC     
            LIMIT 1
            """
        try:
            self.cursor.execute(query, (self.p_id,))
            record = self.cursor.fetchone()
            
            # Se l'utente non ha ancora nessun tracciato nel DB
            if not record:
                lbl_no_data = ctk.CTkLabel(panel, text="No ECG records found.", 
                                        font=FONTS["testo_bold"], text_color=COLORS["testo_chiaro"])
                lbl_no_data.place(relx=0.5, rely=0.5, anchor="center")
                return
            
            signal_raw = record[0]
            date = record[2]
            time = record[3]

            # Converto la stringa di testo del DB in una lista di numeri float
            ecg_points = [float(val) for val in signal_raw.split(",") if val.strip()]

            # Estraggo ESATTAMENTE UN SESTO del tracciato per l'anteprima
            sixth = len(ecg_points) // 12
            overview_points = ecg_points[:sixth] # Prende la prima porzione (1/6)
            
            fig = Figure(figsize=(3, 1.5), dpi=100, facecolor=COLORS["bianco_puro"])
            ax = fig.add_subplot(111)
            ax.set_facecolor(COLORS["bianco_puro"])
            
            # Disegno la linea dell'ECG
            ax.plot(overview_points, color="#ff4d4d", linewidth=1.5)
            
            # Imposto il titolo con Data e Ora recuperati dal database
            ax.set_title(f"Last ECG: {date} - {time}", color=COLORS["testo_chiaro"], fontproperties={'weight': 'bold'}, fontsize=10, pad=10)
            
            # Rimuovo gli assi X e Y 
            ax.axis('off')
            fig.tight_layout()

            # Trasformo il grafico in un widget Tkinter e lo inserisco nel pannello
            canvas = FigureCanvasTkAgg(fig, master=panel)
            canvas_widget = canvas.get_tk_widget()
            
            canvas_widget.place(relx=0.05, rely=0.17, relwidth=0.9, relheight=0.80)
            canvas.draw()

        except Exception as e:
            print(f"Errore durante il rendering del grafico ECG: {e}")
            lbl_error = ctk.CTkLabel(panel, text="Error loading ECG plot.", text_color="red", font=FONTS["testo_normale"])
            lbl_error.place(relx=0.5, rely=0.5, anchor="center")

    def show_therapy(self):
        therapy_data = self.current_therapy

        therapy_date, therapy_desc = therapy_data
        doctor_full_name = f"Dr. {self.doctor_name} {self.doctor_surname}"

        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x520")
        self.edit_window.configure(fg_color=COLORS["sfondo_grigino"])
        self.edit_window.title("Active Therapy Details")

        title = ctk.CTkLabel(self.edit_window, text="Active Therapy Details", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        lbl_name = ctk.CTkLabel(self.edit_window,text="Prescribed by",font=FONTS["titolo_menu"], text_color=COLORS["testo_chiaro"])
        lbl_name.place(x=30, y=90, anchor="w")

        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=doctor_full_name, anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], width=340, height=35)
        entry_name.place(x=30, y=105)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Updated on", font=FONTS["titolo_menu"], text_color=COLORS["testo_chiaro"])
        lbl_date.place(x=30, y=170, anchor="w")

        # Mostriamo la data di caricamento
        entry_date = ctk.CTkLabel(self.edit_window, corner_radius=5, width=340, height=35, font=FONTS["testo_normale"], anchor="w", text=therapy_date, text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_date.place(x=30, y=185)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Description", font=FONTS["titolo_menu"], text_color=COLORS["testo_chiaro"])
        lbl_notes.place(x=30, y=250, anchor="w")

        # Textbox per mostrare il contenuto della terapia
        entry_textbox = ctk.CTkTextbox(
            self.edit_window,
            width=340,
            height=180,
            corner_radius=5,
            font=FONTS["testo_normale"],
            text_color=COLORS["testo_scuro"],
            fg_color=COLORS["bianco_puro"],
            wrap="word",
        )
        entry_textbox.place(x=30, y=265)

        # Inserisco la descrizione e blocco la textbox (state="disabled") in modo che l'utente possa solo leggere e non scriverci dentro
        entry_textbox.insert("1.0", therapy_desc)
        entry_textbox.configure(state="disabled")

        # Pulsante di chiusura
        btn_close = ctk.CTkButton(self.edit_window, text="Close", width=100, height=32, corner_radius=10,
                                  fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"], 
                                  hover_color=COLORS["bordi"], font=FONTS["testo_bold"],
                                  command=self.edit_window.destroy)
        btn_close.place(x=150, y=470)
    
        




    #PROFILE
    def mostra_profilo(self):
        #creo un frame a sinistra che conterrà le opzioni del profilo (Personal Info, Settings, Logout)
        self.side_frame = ctk.CTkFrame(self.current_page_frame, fg_color=COLORS["bianco_puro"], corner_radius=20, border_color=COLORS["bordi"], border_width=2)
        self.side_frame.place(x=42, y=20, relheight=0.88, relwidth=0.16)
        
        #opzioni del menu del profilo
        self.profile_buttons = {}
        opzioni = ["Personal Info", "Settings", "Privacy", "Logout"]

        #creo un bottone per ogni opzione del menu del profilo, invsibile per non alterare il layout
        for i, opzione in enumerate(opzioni):
            btn = ctk.CTkButton(self.side_frame, text=f"   {opzione}", font=FONTS["testo_normale"], height=40, width=180, corner_radius=0, anchor="w", fg_color="transparent", text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], command=lambda o=opzione: self.cambia_pagina_profilo(o))
            self.profile_buttons[opzione] = btn
            btn.pack(padx=(2,2),pady=(24,0), anchor="center") if i ==0 else  btn.pack(padx=(2,2),pady=0, anchor="center")
    
    def cambia_pagina_profilo(self, nome):
        # Questa funzione è chiamata quando clicco su una voce del menu del profilo
        if self.profile_page_frame:
            self.profile_page_frame.destroy()

        self.profile_page_frame = ctk.CTkFrame(self.current_page_frame, fg_color=COLORS["sfondo_grigino"])
        self.profile_page_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
        
        #dinaimica simile a quella dei bottoni principali, ma con colori invertiti 
        for chiave,opt in self.profile_buttons.items():
            if chiave == nome:
                opt.configure(fg_color=COLORS["bordi"])
            else:
                opt.configure(fg_color="transparent")

        if nome == "Personal Info":
            self.mostra_profile_personal_info()
        elif nome == "Settings":
            self.mostra_placeholder(nome)
        elif nome == "Privacy":
            self.mostra_placeholder(nome)
        elif nome == "Logout":
            risposta = messagebox.askyesno("Log-out", "Are you sure you want to log out?")
            if risposta:
                self.root.destroy()
                LoginApp()

    def mostra_profile_personal_info(self):

        #Frame principale di contenimento scorrevole (allineato a destra del menu profilo)
        self.content_scroll = ctk.CTkScrollableFrame(self.profile_page_frame, fg_color="transparent", height=600)
        self.content_scroll.pack(fill="both", expand=True, padx=0, pady=(10,0))

        # Sfrutto una griglia all'interno del frame per dividere lo spazio in 2 colonne
        self.content_scroll.grid_columnconfigure(0, weight=1, pad=30)
        self.content_scroll.grid_columnconfigure(1, weight=1, pad=30)

        # Ogni elemento definisce: label, valore dal DB, colonna, e se è modificabile
        campi = [
            {"lbl": "First Name",    "val": self.user_data[1], "col": 1, "modificabile": False},
            {"lbl": "Last Name",     "val": self.user_data[2], "col": 0, "modificabile": False},
            {"lbl": "Birth Date",    "val": self.user_data[3], "col": 1, "modificabile": False},
            {"lbl": "Address",       "val": self.user_data[4], "col": 0, "modificabile": True},
            {"lbl": "Phone Number",  "val": self.user_data[5], "col": 1, "modificabile": True},
            {"lbl": "Email",         "val": self.user_data[6], "col": 0, "modificabile": True},
            {"lbl": "Username",      "val": self.user_data[7], "col": 0, "modificabile": False},
            {"lbl": "Password",      "val": self.user_data[8], "col": 1, "modificabile": True},
            {"lbl": "Fiscal Code",   "val": self.user_data[9], "col": 0, "modificabile": False}
        ]


        # Titolo Sezione
        ctk.CTkLabel(self.content_scroll, text="Personal Information", font=FONTS["testo_bold"], text_color=COLORS["testo_scuro"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20), padx= 12)

        # Ciclo per generare le label e i campi di testo
        for i, campo in enumerate(campi):
            riga = (i//2)+1 # La riga dipende dall'indice, ogni 2 campi cambio riga

            #creo e posiziono il container per ogni campo
            field_frame = ctk.CTkFrame(self.content_scroll, fg_color="transparent")
            field_frame.grid(row=riga, column=campo["col"], sticky="ew", pady=10, padx=10)
            field_frame.grid_columnconfigure(0, weight=1)
            
            # Label del campo
            ctk.CTkLabel(field_frame, text=campo["lbl"], font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"]).grid(row=0, column=0, sticky="w", padx=5, pady=0)

            # Se il campo è modificabile, mettiamo un'Entry normale, altrimenti la blocchiamo, mostro gli asterischi per la password    
            entry = ctk.CTkEntry(
                field_frame, font=FONTS["testo_normale"], height=45, fg_color="white",
                 border_color=COLORS["bordi"], corner_radius=8,
                text_color=COLORS["testo_chiaro"] if campo["modificabile"] else COLORS["bordi"],
                show="*" if campo["lbl"] == "Password" else None
            )
            entry.insert(0, campo["val"])

            #Se non è modificabile, disattiviamo l'entry
            if not campo["modificabile"]:
                entry.configure(state="disabled")

           # Posizioniamo l'entry all'interno del suo frame     
            entry.grid(row=1, column=0, sticky="ew")

            # Se il campo è modificabile, aggiungiamo di fianco il pulsantino per il popup
            if campo["modificabile"]:
                entry.grid(row=1, column=0, sticky="ew") # Lascia spazio a destra per il bottoncino
                btn_profile_edit = ctk.CTkButton(
                    field_frame, text="Update", width=35, height=30, corner_radius=14,
                    fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"],
                    hover_color=COLORS["bordi"],  border_color=COLORS["bordi"], bg_color="white",
                    command=lambda campo_nome=campo["lbl"], campo_val=campo["val"]: self.apri_popup_modifica(campo_nome, campo_val)
                )
                btn_profile_edit.place(relx=0.98, rely=0.69, anchor="e")

    def apri_popup_modifica(self, nome_campo, valore_attuale):
        popup = ctk.CTkToplevel(self.root, fg_color=COLORS["sfondo_grigino"])
        popup.title(f"Edit {nome_campo}")
        popup.geometry("400x360")
        popup.grab_set() 
        
        ctk.CTkLabel(popup, text=f"Modify your {nome_campo}:", font=FONTS["titolo"], text_color=COLORS["testo_scuro"]).pack(pady=(30,30))
        
        # Se è la password, gestisco il popup in modo da mostrare gli asterischi, e richiedere di inserire la password attuale per confermare l'identità dell'utente (per sicurezza)
        if nome_campo == "Password":
            popup.geometry("400x440")
            ctk.CTkLabel(popup, text="Current Password:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"]).pack(pady=(0,0), padx=78, anchor="w")
            current_pw_entry = ctk.CTkEntry(popup, width=250, height=40,  corner_radius=8, border_color=COLORS["bordi"], text_color=COLORS["testo_chiaro"], show="*")
            current_pw_entry.pack(pady=(0,15))

            #chiedo di inserire la nuova password
            ctk.CTkLabel(popup, text="New Password:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"]).pack(pady=(0,0), padx=78, anchor="w")
            nuovo_input = ctk.CTkEntry(popup, width=250, height=40,  corner_radius=8, border_color=COLORS["bordi"], text_color=COLORS["testo_chiaro"], show="*")
            nuovo_input.pack(pady=(0,15))

            #chiedo conferma della nuova password
            ctk.CTkLabel(popup, text="Confirm New Password:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"]).pack(pady=(0,0), padx=78, anchor="w")
            confirm_input = ctk.CTkEntry(popup, width=250, height=40,  corner_radius=8, border_color=COLORS["bordi"], text_color=COLORS["testo_chiaro"], show="*")
            confirm_input.pack(pady=(0,0))

        else:
            ctk.CTkLabel(popup, text="Insert Current Password:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"]).pack(pady=(0,0), padx=78, anchor="w")
            current_pw_entry = ctk.CTkEntry(popup, width=250, height=40,  corner_radius=8, border_color=COLORS["bordi"], text_color=COLORS["testo_chiaro"], show="*")
            current_pw_entry.pack(pady=(0,15))

            ctk.CTkLabel(popup, text=f"Insert New {nome_campo}:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"]).pack(pady=(0,0), padx=78, anchor="w")
            nuovo_input = ctk.CTkEntry(popup, width=250, height=40,  corner_radius=8, border_color=COLORS["bordi"], text_color=COLORS["testo_chiaro"])
            nuovo_input.insert(0, valore_attuale)
            nuovo_input.pack(pady=(0,0))
            
        # Sottofunzione per salvare la modifica, aggiorna il database e rinfresca la pagina del profilo così si vede subito il nuovo dato
        def salva_modifica():
            nuovo_valore = nuovo_input.get().strip()
            password_inserita = current_pw_entry.get().strip()
            
            if not nuovo_valore:
                # Evita di salvare campi vuoti se sono obbligatori
                return 

            # Dizionario per mappare la Label dell'interfaccia con il nome reale della colonna nel Database
            from_labels_to_db = {
                "Address": "Address",
                "Phone Number": "PhoneNumber",
                "Email": "Email",
                "Password": "Password"
            }
            
            nome_colonna_db = from_labels_to_db.get(nome_campo)
            
            # Prepariamo l'hash del database assicurandoci che sia in formato bytes
            hash_db = self.user_data[8].encode('utf-8') if isinstance(self.user_data[8], str) else self.user_data[8]

            #per ciò che non è password mi basta che la password inserita sia corretta, per la password invece chiedo anche di confermare il nuovo valore inserito
            if nome_colonna_db != "Password":
                # Utilizzo checkpw per verificare la password inserita a schermo con l'hash presente nel DB
                if not bcrypt.checkpw(password_inserita.encode('utf-8'), hash_db):
                    # La password inserita non corrisponde a quella attuale

                    # Se la label esiste già, la cancello (così non si accumulano messaggi di errore se l'utente sbaglia più volte)
                    if hasattr(popup, "errore_label") and popup.errore_label:
                        popup.errore_label.destroy()

                    popup.errore_label = ctk.CTkLabel(popup.error_container, text="Incorrect current password.", font=FONTS["testo_normale"], text_color="red")
                    popup.errore_label.pack()
                    return
                else:
                    try:
                        # Query di UPDATE dinamica usando f-string SOLO per la colonna (per cui non posso usare i placeholder)
                        # Sfruttiamo try per gestire eventuali errori (es. connessione al DB, colonna inesistente, ecc.)
                        self.cursor.execute(f"UPDATE user SET {nome_colonna_db} = ? WHERE username = ?", (nuovo_valore, self.user[0]))
                        self.conn.commit() # Salva i dati sul file .db
                        
                        if hasattr(popup, "errore_label") and popup.errore_label:
                            popup.errore_label.destroy()

                        popup.errore_label = ctk.CTkLabel(popup.error_container, text="Aggiornamento completato con successo", font=FONTS["testo_normale"], text_color="green")
                        popup.errore_label.pack() 
            
                        print(f"Database aggiornato con successo: {nome_colonna_db}")
                        
                    except sql.Error as e:
                        # Gestisco eventuali errori avvisando l'utente e stampando l'errore specifico per il debug
                        if hasattr(popup, "errore_label") and popup.errore_label:
                            popup.errore_label.destroy()

                        popup.errore_label = ctk.CTkLabel(popup.error_container, text=f"Errore durante l'aggiornamento del DB: {e}", font=FONTS["testo_normale"], text_color="red")
                        popup.errore_label.pack()

            elif nome_colonna_db == "Password":
                valore_conferma = confirm_input.get().strip()
                # Utilizzo checkpw anche qui per verificare la validità della sessione corrente
                if not bcrypt.checkpw(password_inserita.encode('utf-8'), hash_db):

                    # Se la label esiste già, la cancello
                    if hasattr(popup, "errore_label") and popup.errore_label:
                        popup.errore_label.destroy()

                    popup.errore_label =ctk.CTkLabel(popup.error_container, text="Incorrect current password.", font=FONTS["testo_normale"], text_color="red")
                    popup.errore_label.pack()
                    return
                else:
                    if nuovo_valore != valore_conferma:

                        if hasattr(popup, "errore_label") and popup.errore_label:
                            popup.errore_label.destroy()

                        popup.errore_label = ctk.CTkLabel(popup.error_container, text="New passwords do not match.", font=FONTS["testo_normale"], text_color="red")
                        popup.errore_label.pack() 
                        return
                    else:
                        try:
                            # Genero il nuovo hash sicuro a partire dalla nuova password scelta
                            nuovo_hash = bcrypt.hashpw(nuovo_valore.encode('utf-8'), bcrypt.gensalt())
                            
                            # Eseguo l'UPDATE passando l'hash appena calcolato al posto del testo in chiaro
                            self.cursor.execute(f"UPDATE user SET {nome_colonna_db} = ? WHERE username = ?", (nuovo_hash, self.user[0]))
                            self.conn.commit()
                            
                            # Aggiorno la cache locale dell'utente per evitare che i controlli successivi falliscano
                            self.user_data[8] = nuovo_hash
                            
                            if hasattr(popup, "errore_label") and popup.errore_label:
                                popup.errore_label.destroy()
                            popup.errore_label = ctk.CTkLabel(popup.error_container, text="Password updated successfully", font=FONTS["testo_normale"], text_color="green")
                            popup.errore_label.pack()
                            
                        except sql.Error as e:
                            if hasattr(popup, "errore_label") and popup.errore_label:
                                popup.errore_label.destroy()
                        
                            popup.errore_label = ctk.CTkLabel(popup.error_container, text=f"Error updating password: {e}", font=FONTS["testo_normale"], text_color="red")
                            popup.errore_label.pack() 
                            return
                
            # Rinfresca la pagina del profilo così l'utente vede subito il nuovo dato
            self.cambia_pagina_profilo("Personal Info")

        # Creo un container per i messaggi di errore/successo, così si posizionano sempre nello stesso punto e non spostano il layout se appaiono
        popup.error_container = ctk.CTkFrame(popup, height=30, fg_color="transparent")
        popup.error_container.pack(pady=(15, 15), fill="x")
        popup.error_container.pack_propagate(False)
            
        save_btn = ctk.CTkButton(popup, text="Save", font=FONTS["testo_bold"], fg_color=COLORS["blu_acceso"], command=salva_modifica)
        save_btn.pack(pady=(0,10))

    
    
    
    #DATA  
    def mostra_dati(self):

        # Creo i 4 pannelli principali (Anagrafica, Vitals, Therapy, Calendar) che conterranno i vari dati specifici, e poi chiamo le funzioni che mostrano i contenuti specifici di ognuno
        self.anagrafica = ctk.CTkFrame(self.current_page_frame, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.anagrafica.place(relx=0.03, rely=0.03, relheight=0.20, relwidth=0.94)

        self.vitals = ctk.CTkFrame(self.current_page_frame, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.vitals.place(relx=0.03, rely=0.26, relheight=0.71, relwidth=0.70)
        
        self.therapy = ctk.CTkFrame(self.current_page_frame, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.therapy.place(relx=0.75, rely=0.26, relheight=0.51, relwidth=0.22)
        
        self.calendar = ctk.CTkFrame(self.current_page_frame, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.calendar.place(relx=0.75, rely=0.81, relheight=0.16, relwidth=0.22)

        # Ora che ho creato i 4 pannelli principali, chiamo le funzioni che mostrano i contenuti specifici di ognuno
        self.show_next_appointment()
        self.show_current_therapy()
        self.show_patient_vitals(False)
        self.show_patient()

    # Funzione per calcolare l'età del paziente a partire dalla data di nascita, recuperata dal database, così da mostrarla nella sezione anagrafica insieme al nome e cognome
    def get_age(self):
        query = """SELECT (strftime('%Y', 'now') - strftime('%Y', BirthDate)) - (strftime('%m-%d', 'now') < strftime('%m-%d', BirthDate)) AS Age
                FROM User
                WHERE ID = ?""" 

        self.cursor.execute(query, (self.p_id,))
        data = self.cursor.fetchall()[0]

        return data
    
    # Funzione per recuperare i dati del medico curante del paziente
    def get_doctor(self):
        query = """SELECT U.Name, U.Surname, U.ID FROM User U
                JOIN THERAPY T ON U.ID = T.IdDoctor
                GROUP BY T.IdPatient
                HAVING T.IdPatient = ?"""

        self.cursor.execute(query, (self.p_id,))
        data = self.cursor.fetchall()[0]

        return data
    
    # Funzione per recupeare l'appuntamento più vicino, con la possibilità di aggiungere note prima dell'appuntamento stesso che il medico vedrà quando apre il report dell'appuntamento
    def show_next_appointment(self):
        
        self.text = ctk.CTkLabel(self.calendar, text="Next Appointment", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)

        if self.next_app_info:
            app_info = self.next_app_info
            row = ctk.CTkFrame(self.calendar, fg_color="transparent", corner_radius=20)
            row.place(x=20, y=70, relwidth=0.85)

            label_date = ctk.CTkLabel(row, width=160, anchor="w", text=f"{self.next_app_info[1]} - {self.next_app_info[2]}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")

            # do la possibilità all'utente di inviare note al medico prima dell'appuntamento, così se ha bisogno di chiarimenti o vuole anticipare qualche domanda può farlo direttamente da lì, e il medico le vedrà quando apre il report dell'appuntamento
            note = ctk.CTkButton(row, text="Note", width=50, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], border_color=COLORS["bordi"], hover_color=COLORS["bordi"], 
                                    command = lambda app =app_info : self.appointment_note(app))
            note.grid(row=0, column=1, padx=(0,5),pady=10,sticky="e")

            open = ctk.CTkButton(row, text="Note", width=50, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], border_color=COLORS["bordi"], hover_color=COLORS["bordi"], 
                                    command = lambda app =app_info : self.open_appointment(app))
            open.grid(row=0, column=2, padx=(0,5),pady=10,sticky="e")


        else: 
            row = ctk.CTkFrame(self.calendar, fg_color="transparent", corner_radius=20)
            row.place(x=20, y=70, relwidth=0.85)

            label_date = ctk.CTkLabel(row, width=160, anchor="w", text="No Appointments", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")

    # Creo una nota legata all'appuntamento, così l'utente può scrivere al medico prima dell'appuntamento stesso se ha bisogno di chiarimenti o vuole anticipare qualche domanda
    def appointment_note(self, app):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x520")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        date = f"{datetime.today()}"[:10]
        time = f"{datetime.today()}"[11:16]

        title = ctk.CTkLabel(self.edit_window, text="Send Message", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Send to", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f"Dr. {self.doctor_name} {self.doctor_surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_name.place(x=30, y=95)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Date - Time", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=150, anchor="w")
        entry_data = ctk.CTkLabel(self.edit_window, width=340,font=FONTS["testo_normale"], anchor="w", text=f" {date} - {time}",text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_data.place(x=30, y=165)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Message", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_notes.place(x=30, y=220, anchor="w")

        entry_textbox = ctk.CTkTextbox(self.edit_window, width=340, height=180, corner_radius=5, 
                                       font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], wrap="word")
        entry_textbox.place(x=30, y=235)
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=430)
        
        raw_msg = entry_textbox.get("1.0", "end-1c")

        
        # Definisco un testo predefinito legatto all'appuntamento, così l'utente può semplicemente modificare quello se vuole aggiungere qualcosa, invece di scrivere tutto da zero, e il medico capisce subito a cosa si riferisce la nota senza doverla contestualizzare con l'appuntamento
        save = ctk.CTkButton(self.edit_window, text="Send", width=100, corner_radius=20, fg_color=COLORS["blu_acceso"], text_color=COLORS["bianco_puro"], font = FONTS["testo_bold"], hover_color=COLORS["bordi"],
                             command=lambda: self.send_appointment_message(self.p_id, self.id_doctor, date, time, final_msg=f"[Related to the the following appointment {app[1]}  - {app[2]}]: {raw_msg}\n"))
        
        save.place(x=150, y = 470)

    # Salvo la nota sìlegata all'appuntamento nel database, così posso gestire tutto in un secondo momento. AA differenza dei messaggi normali, questa ha una entry predefinita che specifica che si tratta di una nota legata all'appuntamento, così il medico capisce subito a cosa si riferisce senza doverla contestualizzare con l'appuntamento stesso
    def send_message(self, id_sender, id_receiver, date, time, msg):

        # Query di inserimento nel Database
        query = """INSERT INTO NOTIFICATION (IdSender, IdReceiver, Date, Time, Message)
                   VALUES (?, ?, ?, ?, ?)"""
        
        try:
            # Passiamo i valori del dizionario usando le loro chiavi
            self.cursor.execute(query, (
                id_sender,
                id_receiver,
                date,
                time,
                msg
            ))
            
            # Fondamentale per salvare le modifiche nel database
            self.conn.commit() 
            self.output_add.configure(text="Message sent successfully", text_color='green')
            self.mostra_messaggi()
            
        except Exception as e:
            self.output_add.configure(text=f"Error: {e}", text_color='red')
            # In caso di errore facciamo il rollback per sicurezza
            self.conn.rollback()

    # Mostro la terapia attuale del paziente, con la data dell'ultima modifica, così da tenere sempre aggiornato il paziente sulla sua terapia, e fargli capire se è stata modificata di recente o se è un aggiornamento vecchio
    def show_current_therapy(self):
    
        if self.current_therapy[0] and self.current_therapy[1]:
            date = self.current_therapy[0]
            description = self.current_therapy[1]

            # Gestione lunghezza descrizione: se supera i 120 caratteri, mostra un'anteprima
            if len(description) > 120:
                preview_description = description[:117] + "..."
            else:
                preview_description = description
            has_data = True
        else:
            date = None
            description = "No active therapy"
            preview_description = "No active therapy"
            has_data = False
        
        # Titolo della pagina
        self.text = ctk.CTkLabel(self.therapy, text="Current Therapy", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
                     
        # Label e Box della Data di Modifica
        lbl_date = ctk.CTkLabel(self.therapy, text="Modified on:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=80, anchor="w")
        entry_date = ctk.CTkLabel(self.therapy, corner_radius=5, anchor="w", text=f"  {date}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["sfondo_grigino"], width=290, height=30)
        entry_date.place(x=30, y=95)

        # Label e Box della Descrizione della Terapia (Anteprima)
        lbl_description = ctk.CTkLabel(self.therapy, text="Last update:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_description.place(x=30, y=150, anchor="w")
        
        textbox_therapy = ctk.CTkTextbox(self.therapy, corner_radius=5, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["sfondo_grigino"], width=290, height=130)
        textbox_therapy.place(x=30, y=165)

        # Inserimento controllato del testo accorciato
        textbox_therapy.configure(state="normal")
        textbox_therapy.delete("1.0", "end")
        textbox_therapy.insert("1.0", preview_description)
        textbox_therapy.configure(state="disabled")

        # Il bottone compare solo se esiste effettivamente una terapia da mostrare
        if has_data:
            btn_full_details = ctk.CTkButton(self.therapy, text="View Full Details", width=150, height=32, corner_radius=8,
                                             fg_color=COLORS["blu_acceso"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                             command=self.show_therapy)
            btn_full_details.place(x=30, y=315)

        self.output_add = ctk.CTkLabel(self.therapy, width=300, text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=30, y=360)
                     
    
    # Mostro i dati dei parametri vitali del paziente, con la possibilità di aggiungere nuovi dati e di visualizzare il grafico dell'ECG
    def show_patient_vitals(self, error):
        for widget in self.vitals.winfo_children():
            widget.destroy()

        row = ctk.CTkFrame(self.vitals, fg_color="transparent", corner_radius=20)
        row.place(x=20, y=20, relwidth=0.95)

        text = ctk.CTkLabel(row, text="Vitals", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        text.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        
        # Pulscante per visualizzare il grafico dell'ECG
        ecg = ctk.CTkButton(row, text="Plot ECG", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                command = lambda : self.add_ecg())
        ecg.grid(row=0, column=2, padx=(15,5),pady=10,sticky="e")

        # Pulsante per aggiungere nuovi dati dei parametri vitali
        add = ctk.CTkButton(row, text="Add Vitals", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"],  
                                command = lambda : self.add_vitals())
        add.grid(row=0, column=3, padx=(15,5),pady=10,sticky="e")

        row.grid_columnconfigure(1,weight=1)

        # Frame all'interno del pannello, destinato ai grafici
        self.plot_area = ctk.CTkFrame(self.vitals, fg_color="transparent", corner_radius=20,height=430, width=1100)
        self.plot_area.place(x=10,y=100)

        self.output = ctk.CTkLabel(self.vitals, text = f"Select Add Vitals to plot", font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"])
        self.output.place(x=35, y=70)

        self.output_date = ctk.CTkLabel(self.vitals, text = "", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
        self.output_date.place(x=300, y=70)

        #Gestione degli errori nel plotting
        if error:
            # Creiamo la scritta di Errore centrata perfettamente dentro self.plot_area
            label_errore = ctk.CTkLabel(self.plot_area, text="ERROR: Missing values", font=FONTS["titolo"], text_color="red")
            label_errore.place(relx=0.5, rely=0.5, anchor="center")

    # Funzione per mostrare gli esami passati del paziente, con la possibilità di scaricare il report di ogni esame
    def show_patient_exams(self):
        for widget in self.vitals.winfo_children():
            widget.destroy()

        row = ctk.CTkFrame(self.vitals, fg_color="transparent", corner_radius=20)
        row.place(x=20, y=20, relwidth=0.95)

        text = ctk.CTkLabel(row, text="Past Exams", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        text.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        
        self.exams_area = ctk.CTkScrollableFrame(self.vitals, fg_color="transparent", corner_radius=20,height=430, width=1100)
        self.exams_area.place(x=10,y=70)

        # Retrieve degli esami passati
        exams = self.get_past_exams()
        
        # Griglia per mostrare gli esami, con data, descrizione e pulsante per scaricare il report di ogni esame
        for ex in exams:
            id, date, time, text = ex
            row = ctk.CTkFrame(self.exams_area, fg_color="transparent")
            row.pack(fill='x',padx=0, pady=0)

            label_date = ctk.CTkLabel(row, text=f"{date}--{time}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
            label_date.grid(row=0,column=0, padx=15, pady=10, sticky="w")

            label_report = ctk.CTkLabel(row, text=text, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_report.grid(row=0,column=1, padx=15, pady=10, sticky="w")

            # Pulsante per scaricare il report dell'esame, con una funzione dedicata che prende l'id dell'esame così sa quale report scaricare
            download = ctk.CTkButton(row, text="Download Report", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                 command = lambda ex=ex : self.download_report(ex[0], ex[1]))
            download.grid(row=0, column=2, padx=(15,50),pady=10,sticky="e")

            row.grid_columnconfigure(1, weight=1)

    # Funzione per recuperare gli esami passati del paziente dal database, così da mostrarli nella sezione dedicata
    def get_past_exams(self):

        # Recupero i dati degli appuntamenti passati
        query = """SELECT IdAppointment, Date, Time, Notes FROM APPOINTMENT
                WHERE IdPatient = ?
                AND (Date < DATE('now', 'localtime') 
                    OR (Date = DATE('now', 'localtime') AND Time < TIME('now', 'localtime')))
                ORDER BY Date DESC, Time DESC"""
      
        self.cursor.execute(query, (self.p_id,))
        data = self.cursor.fetchall()
        return data

    # Creo un pannello che contiene i dati principali del paziente (nome, cognome, età) e da cui si può accedere alla sezione degli esami passati, inviare messaggi al medico
    def show_patient(self):

        self.text = ctk.CTkLabel(self.current_page_frame, text="Patient Overview", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
            
        row = ctk.CTkFrame(self.current_page_frame, fg_color="transparent", corner_radius=20)
        row.place(x=20, y=70, relwidth=0.98)

        dot_code = ctk.CTkFrame(row, width=24, height=24, corner_radius=12, fg_color=COLORS["blu_acceso"])
        dot_code.grid(row=0,column=0, padx=15, pady=10, sticky="ew")

        testo_frame = ctk.CTkFrame(row, fg_color="transparent")
        testo_frame.grid(row=0, column=1, rowspan=2, padx=15, pady=0, sticky="w")

        nome_cognome_frame = ctk.CTkFrame(testo_frame, fg_color="transparent")
        nome_cognome_frame.pack(anchor="w")

        label_name = ctk.CTkLabel(nome_cognome_frame, text=self.patient_name, font=FONTS["titolo"], text_color=COLORS["testo_scuro"], anchor="w")
        label_name.pack(side="left", padx=(0, 5))

        label_surname = ctk.CTkLabel(nome_cognome_frame, text=self.patient_surname, font=FONTS["titolo"], text_color=COLORS["testo_scuro"], anchor="w")
        label_surname.pack(side="left")

        label_fiscal = ctk.CTkLabel(testo_frame, text=self.patient_fiscal_code, font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"], anchor="w")
        label_fiscal.pack(anchor="w", pady=(0, 0)) 

        label_age = ctk.CTkLabel(row, text=f"Age: {self.patient_age}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
        label_age.grid(row=0,column=2, padx=15, pady=10, sticky="w")

        label_wh = ctk.CTkLabel(row, text=f"W: {self.patient_weight} Kg, H: {self.patient_height} cm", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=150, anchor="w")
        label_wh.grid(row=0,column=3, padx=5, pady=10, sticky="w")

        self.output_add = ctk.CTkLabel(row,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=120)
        self.output_add.grid(row=0, column=6, padx=15, pady=10, sticky="w")

        #Inserisco i vari pulsanti per accedere alle diverse sottosezioni (vitals, esami passati, messaggi)
        message = ctk.CTkButton(row, text="Message", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                command = lambda : self.message(self.p_id, self.doctor_id))
        message.grid(row=0, column=7, padx=(5,15),pady=10,sticky="e")

        record_ecg = ctk.CTkButton(row, text="Record ECG", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                command = lambda : self.record_ecg())
        record_ecg.grid(row=0, column=8, padx=(5,15),pady=10,sticky="e")

        row.grid_columnconfigure(3,weight=1)

    # Messaggi generici (non legati all'appuntamento)
    def message(self, id_sender, id_receiver):
        sender = id_sender
        receiver = id_receiver

        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x520")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        date = f"{datetime.today()}"[:10]
        time = f"{datetime.today()}"[11:16]

        title = ctk.CTkLabel(self.edit_window, text="Send Message", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=COLORS["blu_acceso"])
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Send to", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f"Dr. {self.doctor_name} {self.doctor_surname}" if receiver == self.doctor_id else "Admin", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_name.place(x=30, y=95)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Date - Time", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=150, anchor="w")
        entry_data = ctk.CTkLabel(self.edit_window, width=340,font=FONTS["testo_normale"], anchor="w", text=f" {date} - {time}",text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_data.place(x=30, y=165)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Message", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_notes.place(x=30, y=220, anchor="w")
        
        entry_textbox = ctk.CTkTextbox(self.edit_window, width=340, height=180, corner_radius=5, 
                                       font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], wrap="word")
        entry_textbox.place(x=30, y=235)
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=430)

        save = ctk.CTkButton(self.edit_window, text="Send", width=100, corner_radius=20, fg_color=COLORS["blu_acceso"],font=FONTS["testo_bold"], text_color=COLORS["bianco_puro"],
                             command=lambda: self.send_message(sender, receiver, date, time, entry_textbox.get("1.0", "end-1c")))
        
        save.place(x=150, y = 470)

    # Apro una finrstra pop up per scegliere quale parametro visualizzare e l'intervallo di tempo
    def add_vitals(self):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x300")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Add Vitals", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=COLORS["blu_acceso"])
        dot_code.place(x=346, y=30)
                     
        start_date = ctk.CTkLabel(self.edit_window, text="Start Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        start_date.place(x=30, y=80, anchor="w")
        entry_start = ctk.CTkEntry(self.edit_window, width=150,corner_radius=5, placeholder_text="YYYY-MM-DD", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"])
        entry_start.place(x=30, y=95)

        # Data di inizio e fine delle acquisizioni in formato YYYY-MM-DD
        end_date = ctk.CTkLabel(self.edit_window, text="End Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        end_date.place(x=220, y=80, anchor="w")
        entry_end = ctk.CTkEntry(self.edit_window, width=150,corner_radius=5, placeholder_text="YYYY-MM-DD", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"])
        entry_end.place(x=220, y=95)
        
        # Lista di tutti i parametri da poter selezionare nel menù a tendina
        vitals_list = ["Systolic BP", "Diastolic BP", "Heart Rate", "Step Count", "Sleep Hours", "SPO2", "VO2max"]
        
        vitals = ctk.CTkLabel(self.edit_window, text="Vitals", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        vitals.place(x=30, y=150, anchor="w")
        menu = ctk.CTkOptionMenu(self.edit_window, width=340, values=vitals_list[1:],fg_color=COLORS["bianco_puro"], font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], button_color=COLORS["bianco_puro"],button_hover_color=COLORS["bordi"])
        menu.place(x=30, y=165)
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=250)

        # Bottone di salvataggio: avvia il query dei dati
        save = ctk.CTkButton(self.edit_window, text="Add", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                            command = lambda : self.get_vitals(entry_start.get(), entry_end.get(),menu.get()))
        save.place(x=150, y = 250)

    # Funzione utile ad effettuare la query di tutti i dati di un tipo dal db e ordinarli in un dizionario sulla base di data, se day or night, valore medio, max e min durante quella giornata    
    def get_vitals(self, start, end, vit):
        
        # Converti stringhe in oggetti datetime
        date_start = datetime.strptime(start, "%Y-%m-%d")
        date_end = datetime.strptime(end, "%Y-%m-%d")

        vit_db = {
            "Systolic BP": "SBP",
            "Diastolic BP": "DBP",
            "Heart Rate": "HR",
            "Step Count": "StepCount",
            "Sleep Hours": "SleepHours",
            "SPO2": "SPO2",
            "VO2max": "VO2Max"
        }

        # Sottrazione per trovare il numero dei giorni di acquisizione
        days_range = (date_end - date_start).days + 1
        valori_attesi = 2*days_range

        query = """SELECT num.Date, num.Max, num.Min, num.Mean, num.DayTime
                FROM NUMERICAL_DATA AS num
                JOIN Data ON num.IdNumData = Data.IdData
                WHERE data.IDPatient = ?
                AND data.NameData = ?
                AND num.Date BETWEEN ? AND ?
                AND num.DayTime IN ('Day', 'Night')
                ORDER BY num.Date ASC """
        
        self.cursor.execute(query, (self.p_id, vit_db[vit], start, end))
        records = self.cursor.fetchall()

        if len(records)<valori_attesi:
            self.show_patient_vitals(True)

        else:
            # Creo un dizionario e lo popolo con i dati ottenuti tramite la query
            if vit ==  "Step Count":
                vitals_info = {"dates": [], "max": [], "min": [], "mean": []}
                for row in records:
                    vitals_info["dates"].append(row[0])
                    vitals_info["max"].append(row[1])
                    vitals_info["min"].append(row[2])
                    vitals_info["mean"].append(row[3])

                    self.plot_vitals(vitals_info, vitals_info, vit)

            
            else:
                vitals_info = {
                    "Day":   {"dates": [], "max": [], "min": [], "mean": []},
                    "Night": {"dates": [], "max": [], "min": [], "mean": []}
                }
                
                for row in records:
                    daytime = row[4] # 'Day' oppure 'Night'
                
                    if daytime in vitals_info:
                        vitals_info[daytime]["dates"].append(row[0])
                        vitals_info[daytime]["max"].append(row[1])
                        vitals_info[daytime]["min"].append(row[2])
                        vitals_info[daytime]["mean"].append(row[3])

                self.plot_vitals(vitals_info["Day"], vitals_info["Night"], vit)
            
    # Funzione per la gestione del plot dei dati vitali
    def plot_vitals(self, day, night, vit):
        for widget in self.plot_area.winfo_children():
            widget.destroy()
        
        self.output.destroy()
        self.output_date.destroy()

        # Premendo il bottone della mattina o della sera viene aggionrato il plot di conseguenza (per step count non ho distinzione)
        if vit != "Step Count":
            self.btn_day = ctk.CTkButton(self.vitals, text="Day", width=50, corner_radius=20, hover_color=COLORS["bordi"], 
                                        fg_color=COLORS["bordi"], text_color=COLORS["sfondo_grigino"],command=lambda: self.update_vitals("Day", day, night, vit))
            self.btn_day.place(x=35, y=70)

            self.btn_night = ctk.CTkButton(self.vitals, text="Night", width=50, corner_radius=20, hover_color=COLORS["bordi"], 
                                        fg_color=COLORS["bordi"], text_color=COLORS["sfondo_grigino"], command=lambda: self.update_vitals("Night", night, night, vit))
            self.btn_night.place(x=95, y=70) 

        #Di default vedrò i dati diurni
        self.update_vitals("Day", day, night, vit)
    
    # Passo alla funzione sia i valori diurni che quelli notturni, ma carico solo quelli selezionati
    def update_vitals(self, time, day, night, vit):
        for widget in self.plot_area.winfo_children():
            widget.destroy()

        self.output.destroy()
        self.output_date.destroy()

        # Gestione dei bottoni a seguito della selezione (solo se diverso da step count)
        if vit != "Step Count":
            if time == "Day":
                data = day
                self.btn_day.configure(fg_color=COLORS["bordi"], text_color=COLORS["sfondo_grigino"])
                self.btn_night.configure(fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"])
            elif time == "Night":
                data = night
                self.btn_day.configure(fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"])
                self.btn_night.configure(fg_color=COLORS["bordi"], text_color=COLORS["sfondo_grigino"])
            
        # Generazione di figura con assi, labels, grafici e riempimenti
        fig = Figure(figsize=(8.5, 4),facecolor="none") 
        
        ax = fig.add_subplot(111)       
        ax.set_facecolor("none")

        ax.plot(data["dates"], data["mean"], color=COLORS["blu_acceso"], linewidth=3)
        ax.fill_between(data["dates"], data["min"], data["max"], color=COLORS["blu_acceso"], alpha=0.2, edgecolor='none')
        
        ax.tick_params(axis="x", colors=COLORS["testo_scuro"], labelsize=10, labelbottom=True)
        ax.tick_params(axis="y", colors=COLORS["testo_scuro"], labelsize=10)
        
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_family("sans-serif")
            label.set_visible(True)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.yaxis.grid(True, linestyle="--", alpha=0.3, color=COLORS["testo_scuro"])
        ax.set_axisbelow(True)

        fig.tight_layout()
        fig.subplots_adjust(left=0.075, right=1, top=0.95, bottom=0.25)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_area)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(bg=COLORS["bianco_puro"], highlightthickness=0)
        canvas_widget.pack(fill="both", expand=True)
        
        canvas.draw()

        self.output = ctk.CTkLabel(self.vitals, text = f"Plotting {time} {vit} [{UNITS[vit]}]", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output.place(x=180, y=70)

        self.output_date = ctk.CTkLabel(self.vitals, text = f"Recorded from {day['dates'][0]} to {day['dates'][-1]}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
        self.output_date.place(x=465, y=70)

    # Funzione per il retrieve di tutte le date di ECG disponibili e successiva selezione tramite menu a tendina
    def add_ecg(self):
        
        query = """
            SELECT D.Date, S.Time
            FROM DATA AS D
            JOIN SIGNALS AS S on S.IdSignals = D.IdData 
            WHERE D.IdPatient = ? 
            AND D.NameData = 'ECG'
            ORDER BY D.Date DESC
        """ 

        self.cursor.execute(query, (self.p_id,))
        dates = self.cursor.fetchall()
        date_list = [f"{d[0]} - {d[1]}" for d in dates]

        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x200")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Plot ECG", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=COLORS["blu_acceso"])
        dot_code.place(x=346, y=30)
                     
        start_date = ctk.CTkLabel(self.edit_window, text="Select Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        start_date.place(x=30, y=80, anchor="w")
        menu = ctk.CTkOptionMenu(self.edit_window, width=340, values=date_list,fg_color=COLORS["bianco_puro"], font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], button_color=COLORS["bianco_puro"],button_hover_color=COLORS["bordi"])
        menu.place(x=30, y=95)
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=130)

        save = ctk.CTkButton(self.edit_window, text="Plot", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], border_color=COLORS['bordi'], 
                            command = lambda : self.get_ecg(menu.get()))
        save.place(x=150, y = 150)

        self.index = 0
    
    def get_ecg(self, date):

        query = """SELECT CAST(S.Value AS BLOB), S.Sampling_Freq 
                FROM SIGNALS S
                JOIN DATA as D ON S.IdSignals = D.IdData
                WHERE D.IdPatient = ? 
                AND D.NameData = 'ECG'
                AND D.Date = ?
                AND S.Time = ?"""

        self.cursor.execute(query, (self.p_id, date[:10], date[-5:]))
        record = self.cursor.fetchone()
        
        blob_data = record[0]
        sampling_freq = record[1]

        num_floats = len(blob_data) // 4
        
        self.y = list(struct.unpack(f"{num_floats}f", blob_data))

        self.x = [round(i * (1.0/sampling_freq), 2) for i in range(len(self.y))]

        self.date = date
        print(len(self.x))

        self.plot_ecg()

    def plot_ecg(self):
        # Controlliamo se i bottoni esistono prima di distruggerli
        if hasattr(self, 'btn_day') and self.btn_day is not None:
            self.btn_day.destroy()
            
        if hasattr(self, 'btn_night') and self.btn_night is not None:
            self.btn_night.destroy()

        self.left = ctk.CTkButton(self.vitals, text="<", width=40, corner_radius=20, hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                        fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"],command=lambda: self.update_index("L"))
        self.left.place(x=35, y=70)

        self.right = ctk.CTkButton(self.vitals, text=">", width=40, corner_radius=20, hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                        fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"],command=lambda: self.update_index("R"))
        self.right.place(x=80, y=70)

        x = self.x[500*self.index:500*(self.index+1)]
        y = self.y[500*self.index:500*(self.index+1)]
        
        date = self.date

        for widget in self.plot_area.winfo_children():
            widget.destroy()
     
        self.output.destroy()
        self.output_date.destroy()
        
        fig = Figure(figsize=(8.5,4), facecolor="none") 
        
        ax = fig.add_subplot(111)       
        ax.set_facecolor("none")
        
        ax.plot(x, y, color=COLORS["bordi"], linewidth=3, label="Mean")
        
        ax.tick_params(axis="x", colors=COLORS["testo_scuro"], labelsize=10, labelbottom=True)
        ax.tick_params(axis="y", colors=COLORS["testo_scuro"], labelsize=10)
        
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_family("sans-serif")
            label.set_visible(True)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.yaxis.grid(True, linestyle="--", alpha=0.3, color=COLORS["testo_scuro"])
        ax.set_axisbelow(True)

        fig.subplots_adjust(left=0.075, right=1, top=0.95, bottom=0.25)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_area)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(bg=COLORS["bianco_puro"], highlightthickness=0)
        canvas_widget.pack(fill="both", expand=True)
        
        canvas.draw()

        self.output = ctk.CTkLabel(self.vitals, text = f"Plotting ECG [mV]", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output.place(x=180, y=70)

        self.output_date = ctk.CTkLabel(self.vitals, text = f"Recorded on {date}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
        self.output_date.place(x=385, y=70)

    def update_index(self, direction):
        if direction == "L":
            self.index = self.index - 1
        elif direction == "R":
            self.index = self.index + 1

        if self.index <= 0:
            self.index = 0
        
        if self.index >= 11:
            self.index = 11

        self.plot_ecg()

    # Popup che simula l'abilitazione del wearable per l'acquisizione ECG
    def record_ecg(self):
        self.guidelines = ctk.CTkToplevel()
        self.guidelines.geometry("320x200")
        self.guidelines.configure(fg_color=COLORS["sfondo_grigino"])
        self.guideframe = ctk.CTkLabel(self.guidelines, text="Please, follow the instructions on the wearable to record your ECG.",fg_color=COLORS["sfondo_grigino"], font=FONTS["testo_bold"], text_color=COLORS["testo_scuro"], wraplength=250, anchor="center")
        self.guideframe.place(relx=0.5, rely=0.5, anchor="center")

    


    # APPOINTMENTS
    def mostra_appuntamenti(self):
        
        self.new_appointments_frame = ctk.CTkFrame(self.current_page_frame, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.new_appointments_frame.place(relx=0.03, rely=0.03, relheight=0.40, relwidth=0.94)

        self.past_appointments_frame = ctk.CTkFrame(self.current_page_frame, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.past_appointments_frame.place(relx=0.03, rely=0.5, relheight=0.40, relwidth=0.94)

        self.past_appointments()
        self.new_appointments()

    # Creo 2 sotto-frame scrollable, uno per gli esami passati (con report da scaricare) e uno per quelli futuri (con possibilità di inviare messaggio)
    # Appuntamenti futuri
    def new_appointments(self):
        self.text = ctk.CTkLabel(self.new_appointments_frame, text="Incoming Appointments", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=0)
            
        self.scrollable_new_app = ctk.CTkScrollableFrame(self.new_appointments_frame, fg_color="transparent")
        self.scrollable_new_app.place(x=0, rely=0.1, relheight=0.8, relwidth=1)
            
        new_appointments = self.get_upcoming_appointments()

        if new_appointments:
            for app in new_appointments:
                id, date, time, desc = app
                row = ctk.CTkFrame(self.scrollable_new_app, fg_color="transparent")
                row.pack(fill='x',padx=20, pady=0)

                label_date = ctk.CTkLabel(row, text=f"{date} - {time}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_date.grid(row=0,column=0, padx=15, pady=10, sticky="w")

                dot_code = ctk.CTkFrame(row, width=12, height=12, corner_radius=6, fg_color=COLORS["blu_acceso"])
                dot_code.grid(row=0,column=1, padx=15, pady=10, sticky="ew")

                label_name = ctk.CTkLabel(row, text=f"Dr. {self.doctor_name}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
                label_name.grid(row=0,column=2, padx=15, pady=10, sticky="w")

                label_surname = ctk.CTkLabel(row, text=self.doctor_surname, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
                label_surname.grid(row=0,column=3, padx=15, pady=10, sticky="w")

                label_description = ctk.CTkLabel(row, text=desc, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_description.grid(row=0,column=4, padx=15, pady=10, sticky="w")

                open = ctk.CTkButton(row, text="Details", width=70, corner_radius=20, text_color=COLORS["testo_scuro"],
                                        fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                        command = lambda app=app : self.open_appointment(app))
                open.grid(row=0, column=5, padx=(15,5),pady=10,sticky="e")

                note = ctk.CTkButton(row, text="Write Note", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                        fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                        command = lambda app=app : self.appointment_note(app))
                note.grid(row=0, column=6, padx=(5,15),pady=10,sticky="e")

                row.grid_columnconfigure(4, weight=1)

            else:
                row = ctk.CTkFrame(self.scrollable_new_app, fg_color="transparent", corner_radius=20)
                row.place(x=20, y=70, relwidth=0.85)

                label_date = ctk.CTkLabel(row, width=160, anchor="w", text="No upcoming appointments", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")

    # Funzione per recuperare gli appuntamenti futuri
    def get_upcoming_appointments(self):

        # Recupero i dati degli appuntamenti passati
        query = """SELECT IdAppointment, Date, Time, Notes FROM APPOINTMENT
                WHERE IdPatient = ?
                AND (Date > DATE('now', 'localtime') 
                    OR (Date = DATE('now', 'localtime') AND Time > TIME('now', 'localtime')))
                ORDER BY Date DESC, Time DESC"""
      
        self.cursor.execute(query, (self.p_id,))
        data = self.cursor.fetchall()
        return data
    
    # Funzione utile a visualizzare i dettagli dell'appuntamento selezionato  
    def open_appointment(self, app):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x520")
        self.edit_window.configure(fg_color=COLORS["sfondo_grigino"])
        self.edit_window.title("Appointment Details")

        title = ctk.CTkLabel(self.edit_window, text="Appointment Details", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        lbl_name = ctk.CTkLabel(self.edit_window,text="Doctor",font=FONTS["titolo_menu"], text_color=COLORS["testo_chiaro"])
        lbl_name.place(x=30, y=90, anchor="w")

        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" Dr. {self.doctor_name} {self.doctor_surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], width=340, height=35)
        entry_name.place(x=30, y=105)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Schedule", font=FONTS["titolo_menu"], text_color=COLORS["testo_chiaro"])
        lbl_date.place(x=30, y=170, anchor="w")

        # Mostriamo la data e l'ora prese direttamente dalla variabile 'app' del DB
        entry_date = ctk.CTkLabel(self.edit_window, corner_radius=5, width=340, height=35, font=FONTS["testo_normale"], anchor="w", text=f" {app[1]} - {app[2]}", text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_date.place(x=30, y=185)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Report", font=FONTS["titolo_menu"], text_color=COLORS["testo_chiaro"])
        lbl_notes.place(x=30, y=250, anchor="w")

        # Textbox per mostrare il report dell'appuntamento
        entry_textbox = ctk.CTkTextbox(
            self.edit_window,
            width=340,
            height=180,
            corner_radius=5,
            font=FONTS["testo_normale"],
            text_color=COLORS["testo_scuro"],
            fg_color=COLORS["bianco_puro"],
            wrap="word",
        )
        entry_textbox.place(x=30, y=265)

        # Inserisco la descrizione e blocco la textbox (state="disabled") in modo che l'utente possa solo leggere e non scriverci dentro
        entry_textbox.insert("1.0", app[3])
        entry_textbox.configure(state="disabled")

        # Pulsante di chiusura
        btn_close = ctk.CTkButton(self.edit_window, text="Close", width=100, height=32, corner_radius=10,
                                  fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"], font=FONTS["testo_bold"],
                                  hover_color=COLORS["bordi"],
                                  command=self.edit_window.destroy)
        btn_close.place(x=150, y=470)

    # Appuntamenti passati
    def past_appointments(self):
        self.text = ctk.CTkLabel(self.past_appointments_frame, text="Past Appointments", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=0)
            
        self.scrollable_past_app = ctk.CTkScrollableFrame(self.past_appointments_frame, fg_color="transparent")
        self.scrollable_past_app.place(x=0, rely=0.1, relheight=0.8, relwidth=1)
            
        past_appointments = self.get_past_exams()

        if past_appointments:
            for app in past_appointments:
                id, date, time, desc= app

                query = """
                    SELECT CO.ReportPath from CHECK_OUT AS CO
                    JOIN APPOINTMENT A ON CO.IdAppointment = A.IdAppointment
                    WHERE A.IdAppointment = ?
                    """
            
                self.cursor.execute(query, (id,))
                path = self.cursor.fetchone()


                row = ctk.CTkFrame(self.scrollable_past_app, fg_color="transparent")
                row.pack(fill='x',padx=20, pady=0)

                label_date = ctk.CTkLabel(row, text=f"{date} - {time}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_date.grid(row=0,column=0, padx=15, pady=10, sticky="w")

                dot_code = ctk.CTkFrame(row, width=12, height=12, corner_radius=6, fg_color=COLORS["blu_acceso"])
                dot_code.grid(row=0,column=1, padx=15, pady=10, sticky="ew")

                label_name = ctk.CTkLabel(row, text=f"Dr. {self.doctor_name}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
                label_name.grid(row=0,column=2, padx=15, pady=10, sticky="w")

                label_surname = ctk.CTkLabel(row, text=self.doctor_surname, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
                label_surname.grid(row=0,column=3, padx=15, pady=10, sticky="w")

                label_report = ctk.CTkLabel(row, text=desc, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_report.grid(row=0,column=4, padx=15, pady=10, sticky="w")

                open = ctk.CTkButton(row, text="Details", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                        fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                        command = lambda app=app : self.open_appointment(app))
                open.grid(row=0, column=5, padx=(15,5),pady=10,sticky="e")

                # Pulsante per scaricare il report dell'esame, con una funzione dedicata che prende l'id dell'esame così sa quale report scaricare
                download = ctk.CTkButton(row, text="Download Report", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                 command = lambda path=path, date=date: self.download_report(path, date))
                download.grid(row=0, column=6, padx=(15,5),pady=10,sticky="e")
                row.grid_columnconfigure(4, weight=1)
                row.grid_columnconfigure(4, weight=1)

        else:
            row = ctk.CTkFrame(self.scrollable_past_app, fg_color="transparent", corner_radius=20)
            row.place(x=20, y=70, relwidth=0.85)

            label_date = ctk.CTkLabel(row, width=160, anchor="w", text="No past appointments", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")

    # Seleziono il percorso del report da scaricare e apro una finestra di conferma
    def download_report(self, path, date):
            
            self.path = path[0]

            self.edit_window = ctk.CTkToplevel(self.root)
            self.edit_window.geometry("400x350")
            self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

            title = ctk.CTkLabel(self.edit_window, text="Download Report", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
            title.place(x=30, y=25)

            dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=COLORS["blu_acceso"])
            dot_code.place(x=346, y=30)
                        
            lbl_name = ctk.CTkLabel(self.edit_window, text="Patient", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
            lbl_name.place(x=30, y=80, anchor="w")
            entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {self.patient_name} {self.patient_surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
            entry_name.place(x=30, y=95)

            lbl_date = ctk.CTkLabel(self.edit_window, text="Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
            lbl_date.place(x=30, y=150, anchor="w")
            entry_data = ctk.CTkLabel(self.edit_window, width=340, corner_radius=5, font=FONTS["testo_normale"], anchor="w", text=f"{date}",text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
            entry_data.place(x=30, y=165)

            self.lbl_report = ctk.CTkLabel(self.edit_window, text="Choose File Path", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
            self.lbl_report.place(x=30, y=235, anchor="w")

            add = ctk.CTkButton(self.edit_window, text="Choose", width=150, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"],border_color=COLORS["bordi"], 
                                command=lambda: self.choose_path())
            
            add.place(x=220, y=220)

            self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
            self.output_add.place(x=50, y=260)

            save = ctk.CTkButton(self.edit_window, text="Download", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"],border_color=COLORS["bordi"], 
                                command=lambda: self.download_file())
            save.place(x=150, y = 305)

    # Il file contenuto nel percorso selezionato nel databse viene salvato nel percorso di destinazione
    def download_file(self):
        if self.download:
            self.output_add.configure(text="Report successfully downloaded", text_color='green')
            shutil.copy(self.path, self.download)
        else:
            self.output_add.configure(text="An error occured, try again", text_color='red')

    # La funzione consente la scelta del path di destinazione
    def choose_path(self):
        chosen_path = filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],title="Choose Destination")
    
        if chosen_path:
            self.download = chosen_path
            self.lbl_report.configure(text=f"...{chosen_path[-15:]}")
        else:
            self.download = None





    # SUPPORT
    # Apro pop-up di scrittura della richiesta
    def mostra_support(self):
        
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x480")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        # def on_close_popup():
        #     self.cambia_pagina("Dashboard")

        #     if hasattr(self, 'edit_window') and self.edit_window is not None:
        #         self.edit_window.destroy()
                
        #     self.edit_window = None

        # self.edit_window.protocol("WM_DELETE_WINDOW", on_close_popup)

        date = f"{datetime.today()}"[:10]

        title = ctk.CTkLabel(self.edit_window, text="Support Request", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)
             
        lbl_date = ctk.CTkLabel(self.edit_window, text="Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=80, anchor="w")
        entry_data = ctk.CTkLabel(self.edit_window, corner_radius=5, width=340,font=FONTS["testo_normale"], anchor="w", text=f" {date}",text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_data.place(x=30, y=95)

        options = ["Wearable", "ScheduleIssue", "InconsistentData", "SupportCredentials", "Others"]
        lbl_type = ctk.CTkLabel(self.edit_window, text="Request Type", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_type.place(x=30, y=150, anchor="w")
        menu = ctk.CTkOptionMenu(self.edit_window, width=340, values=options,fg_color=COLORS["bianco_puro"], font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], button_color=COLORS["bianco_puro"],button_hover_color=COLORS["blu_acceso"])
        menu.place(x=30, y=165)
        
        lbl_notes = ctk.CTkLabel(self.edit_window, text="Message", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_notes.place(x=30, y=220, anchor="w")

        entry_textbox = ctk.CTkTextbox(self.edit_window, width=340, height=150, corner_radius=5, 
                                       font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], wrap="word")
        entry_textbox.place(x=30, y=235)

        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=400)

        save = ctk.CTkButton(self.edit_window, text="Send", font = FONTS["testo_bold"], width=100, corner_radius=20, fg_color=COLORS["blu_acceso"], text_color=COLORS["bianco_puro"],
                             command=lambda: self.send_request(entry_data.cget("text"),menu.get(),entry_textbox.get("1.0", "end-1c")))
        save.place(x=150, y = 430)

    # Funzione che gestisce il salvataggio delle richieste
    def send_request(self, date, reqtype, msg):
        
        query = """
        INSERT INTO Support (Date, SupportType, IdRequester, IdAdmin, Message) 
        VALUES (?, ?, ?, ?, ?)
        """        

        self.cursor.execute(query, (date, reqtype, self.p_id, 1, msg))
        self.conn.commit()

        # Controllo se il widget esiste ancora prima di configurarlo
        if hasattr(self, 'output_add') and self.output_add.winfo_exists():
            self.output_add.configure(text="Support Request sent", text_color='green')




    # MESSAGES
    # Apro una finestra con lla conversazione completa con il dottore
    def mostra_messaggi(self):

        self.all_msg = ctk.CTkFrame(self.current_page_frame, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.all_msg.place(relx=0.03, rely=0.03, relheight=0.94, relwidth=0.94)

        self.text = ctk.CTkLabel(self.all_msg, text=f"Messages from Dr. {self.doctor_name} {self.doctor_surname}", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
        
        self.scrollable = ctk.CTkScrollableFrame(self.all_msg, fg_color="transparent")
        self.scrollable.place(x=0, rely=0.1, relheight=0.85, relwidth=1)
        
        msg = self.get_all_messages()
        
        last_date = None

        for m in msg:
            id_msg, id_sender, id_receiver, text, date, time, read, other_user_id = m 

            if date != last_date:
                last_date = date
                
                date_container = ctk.CTkFrame(self.scrollable, fg_color="transparent")
                date_container.pack(fill='x', padx=20, pady=(15, 5))
                
                line = ctk.CTkFrame(date_container, height=1, fg_color=COLORS["bottone_grigio"])
                line.place(relx=0.5, rely=0.5, relwidth=0.9, anchor="center")
                
                date_label = ctk.CTkLabel(date_container, text=f"{'-'*100}  {date}  {'-'*100}", font=FONTS["sottotitolo"], 
                                        text_color=COLORS["testo_chiaro"], fg_color=COLORS["bianco_puro"])
                date_label.pack(anchor="center")

            row = ctk.CTkFrame(self.scrollable, fg_color="transparent")
            row.pack(fill='x', padx=20, pady=2)
            
            if id_sender == self.p_id:
                header_str = f"[{self.patient_name} - {time}]"
                msg_color = COLORS["testo_chiaro"]
                dot_color = COLORS["bordi"]
                dot_size = 12
            else:
                header_str = f"[Dr. {self.doctor_surname} - {time}]"
                msg_color = COLORS["testo_scuro"]
                dot_color = COLORS["blu_acceso"]
                dot_size = 24 if not read else 12

            dot_container = ctk.CTkFrame(row, width=30, height=30, fg_color="transparent")
            dot_container.grid(row=0, column=0, padx=(10, 15), pady=5, sticky="w")
            dot_container.grid_propagate(False)

            dot_code = ctk.CTkFrame(dot_container, width=dot_size, height=dot_size, corner_radius=dot_size // 2, fg_color=dot_color)
            dot_code.place(relx=0.5, rely=0.5, anchor="center")

            label_header = ctk.CTkLabel(row, text=header_str, font=FONTS["testo_normale"], text_color=msg_color, width=160, anchor="w")
            label_header.grid(row=0, column=1, padx=5, pady=5, sticky="w")

            snippet = f"{text[:75]}..." if len(text) > 75 else text
            label_text = ctk.CTkLabel(row, text=snippet, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"], anchor="w")
            label_text.grid(row=0, column=2, padx=15, pady=5, sticky="w")

            edit = ctk.CTkButton(row, text="View", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], 
                                command=lambda i=id_msg, sd=id_sender, tx=text, d=date, t=time: self.view_message(i, sd, tx, d, t))
            edit.grid(row=0, column=3, padx=(15, 10), pady=5, sticky="e")

            row.grid_columnconfigure(2, weight=1)  

    # Retrieve di tutti i messagi tra paziente e dottore nel database
    def get_all_messages(self):
        query = """SELECT msg.IdNotification, msg.IdSender, msg.IdReceiver, 
                        msg.Message, msg.Date, msg.Time, msg.IsRead,
                    CASE 
                        WHEN msg.IdSender = ? THEN msg.IdReceiver 
                        ELSE msg.IdSender 
                        END AS OtherUserID
                    FROM notification AS msg
                    WHERE (msg.IdSender = ? OR msg.IdReceiver = ?)
                    AND (CASE WHEN msg.IdSender = ? THEN msg.IdReceiver ELSE msg.IdSender END) = ?
                    ORDER BY msg.Date DESC, msg.Time DESC
                """
            
        self.cursor.execute(query, (self.p_id, self.p_id, self.p_id, self.p_id, self.doctor_id))
        msg = self.cursor.fetchall()

        return msg     

    # Pop up per visualizzare il messaggio completo ed eventualmente rispondere
    def view_message(self, id, sender, text, date, time):
        
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x520")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Message", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=COLORS["blu_acceso"])
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Sent from: ", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")

        if sender == self.p_id:
            entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f"{self.patient_name} {self.patient_surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
            entry_name.place(x=30, y=95)
        
        else:
            entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f"Dr. {self.doctor_name} {self.doctor_surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
            entry_name.place(x=30, y=95)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Date - Time", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=150, anchor="w")
        entry_data = ctk.CTkLabel(self.edit_window, width=340,font=FONTS["testo_normale"], anchor="w", text=f" {date} - {time}",text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_data.place(x=30, y=165)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Message", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_notes.place(x=30, y=220, anchor="w")
        
        entry_textbox = ctk.CTkTextbox(self.edit_window, width=340, height=180, corner_radius=5, 
                                       font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], wrap="word")
        entry_textbox.place(x=30, y=235)
        entry_textbox.configure(state="normal")
        entry_textbox.delete("1.0", "end")
        entry_textbox.insert("0.0", text)
        entry_textbox.configure(state="disabled")

        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=430)

        if sender != self.p_id:
            reply = ctk.CTkButton(self.edit_window, text="Reply", font = FONTS["testo_bold"], width=100, corner_radius=20, fg_color=COLORS["blu_acceso"], text_color=COLORS["bianco_puro"],
                                command=lambda: self.message(self.p_id, self.doctor_id))
            
            reply.place(x=95, y = 470)

            read = ctk.CTkButton(self.edit_window, text="Read", font = FONTS["testo_bold"], width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=COLORS['bordi'], border_color=COLORS['bordi'],
                                command=lambda: self.read_message(id))
            
            read.place(x=205, y = 470)

    # Gestisco l'effetto del bottone che contrassegna un messaggio come letto
    def read_message(self, id):
        query = "UPDATE Notification SET IsRead = 1 WHERE IDNotification = ?"
        self.cursor.execute(query, (id,))
        self.conn.commit()

        self.output_add.configure(text="Message marked as read", text_color='green')
        
        for widget in self.scrollable.winfo_children():
            widget.destroy()
        
        self.mostra_messaggi()


    def mostra_placeholder(self, nome):
        ctk.CTkLabel(self.current_page_frame, text=f"{nome} page content goes here.", font=FONTS["testo_bold"], text_color=COLORS["testo_scuro"]).place(relx=0.5, rely=0.5, anchor="center")

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
user = ("alombardi",)
PatientApp(user)