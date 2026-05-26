import customtkinter as ctk
import sqlite3 as sql

from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
import PIL
import struct

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

        self.doctor = self.get_doctor()
        self.doctor_name = self.doctor[0]
        self.doctor_surname = self.doctor[1]
        self.doctor_id = self.doctor[2]

        # Recupero peso e altezza del paziente
        query = """
                    SELECT Height, Weigth
                    FROM PATIENT_CLINICALDATA
                    WHERE IdPatient = ?
                """
        
        self.cursor.execute(query, self.p_id)
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
        self.icon_notif = ctk.CTkImage(light_image=PIL.Image.open("icons/dark_bell.png"), size=(24, 24))
        self.icon_profile = ctk.CTkImage(light_image=PIL.Image.open("icons/dark_user.png"), size=(20, 20))
        # Versione chiara per quando il tasto diventa blu/scuro
        self.icon_notif_light = ctk.CTkImage(light_image=PIL.Image.open("icons/light_bell.png"), size=(24, 24))
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
        ctk.CTkLabel(self.topbar, text=f"Hello, {nome_utente}", font=FONTS["sottotitolo"], 
                     text_color=COLORS["testo_chiaro"]).place(x=42, y=14)
        ctk.CTkLabel(self.topbar, text="Welcome back!", font=FONTS["titolo"], 
                     text_color=COLORS["testo_scuro"]).place(x=42, y=37)

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

        # Partiamo dalla Dashboard
        self.cambia_pagina("Dashboard")

    def crea_tasto_icona(self, icona, nome):
        btn = ctk.CTkButton(self.side_frame, text="", image=icona, width=38, height=38, corner_radius=19,
                            fg_color=COLORS["bottone_grigio"], border_width=2, border_color=COLORS["bordi"],
                            hover_color=COLORS["bordi"], command=lambda: self.cambia_pagina(nome))
        btn.pack(side="left", padx=5)
        return btn
    
    def cambia_pagina(self, nome):
        # Pulisco la pagina attuale e creo un nuovo frame (bianco o grigio a seconda dei gusti) dove mettere i nuovi contenuti
        if self.current_page_frame: 
            self.current_page_frame.destroy()

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
        if nome == "Notifications":
                    # Inversione: sfondo scuro e icona chiara
                    self.btn_notif.configure(fg_color=COLORS["testo_scuro"], hover_color=COLORS["testo_scuro"], border_color=COLORS["testo_scuro"], image=self.icon_notif_light)
                    self.mostra_placeholder(nome)
        elif nome == "Profile":
                    # Inversione: sfondo scuro e icona chiara
                    self.btn_profile.configure(fg_color=COLORS["testo_scuro"], hover_color=COLORS["testo_scuro"], border_color=COLORS["testo_scuro"], image=self.icon_profile_light)
                    self.mostra_profilo()

        self.btn_notif.configure(fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], image=self.icon_notif) if nome != "Notifications" else None
        self.btn_profile.configure(fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"], image=self.icon_profile) if nome != "Profile" else None

        # Funzioni che mostrano i contenuti 
        if nome == "Dashboard":
            self.mostra_dashboard()

        elif nome == "Data":
            self.mostra_dati()

        elif nome == "Appointments":
            self.mostra_appuntamenti()
        
        elif nome == "Support":
            self.mostra_placeholder(nome)

    #DASHBOARD
    def mostra_dashboard(self):
        dati = self.recupera_latest_data_db()

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
        aggiungi_pannello(0.66, 0.05, 0.30, 0.58, "Therapy", dati["active therapy"])
        aggiungi_pannello(0.66, 0.68, 0.30, 0.26, "Next Appointment", dati["upcoming appointment"])

   #Funzione per recuperare i dati più recenti DAL DB e mostrali nella Dashboard
    def recupera_latest_data_db(self):

        # Funzioncina interna per non ripetere la query chilometrica dei dati numerici
        def get_latest(metrica):
            self.cursor.execute("""
                SELECT N.Mean FROM DATA D 
                JOIN NUMERICAL_DATA N ON D.IdData = N.IdNumData 
                WHERE D.IdPatient = ? AND D.NameData = ? 
                ORDER BY D.Date DESC LIMIT 1
            """, (self.p_id, metrica))
            res = self.cursor.fetchone()
            return f"{res[0]:.1f}" if res else "--"

        # Recupero la terapia
        self.cursor.execute("SELECT Date, Description FROM THERAPY WHERE IdPatient = ? ORDER BY Date DESC LIMIT 1", (self.p_id,))
        self.current_therapy = self.cursor.fetchone()
        self.current_therapy_date = self.current_therapy[0] if self.current_therapy else None
        self.current_therapy_descr = self.current_therapy[1] if self.current_therapy else None
        self.current_therapy = f"{self.current_therapy[0]}: {self.current_therapy[1]}" if self.current_therapy else "No active therapy."

        # Recupero l'appuntamento
        self.cursor.execute("SELECT IDAppointment, Date, Time FROM APPOINTMENT WHERE IdPatient = ? ORDER BY Date ASC LIMIT 1", (self.p_id,))
        self.next_app_info = self.cursor.fetchone()
        self.next_appointment = f"{self.next_app_info[1]} at {self.next_app_info[2]}" if self.next_app_info else "No upcoming appointments."

        # Impacchetto tutto e lo spedisco alla dashboard
        return {
            "vitals": f"SBP: {get_latest('SBP')} mmHg\n\nDBP: {get_latest('DBP')} mmHg\n\nHR: {get_latest('HR')} bpm",
            "fitness": f"VO2 Max: {get_latest('VO2Max')}\n\nSpO2: {get_latest('SPO2')} %",
            "activity": f"Sleep: {get_latest('SleepHours')} h\n\nSteps: {get_latest('StepCount')}",
            "active therapy": f"{self.current_therapy[0]}: {self.current_therapy[1]}" if self.current_therapy else "No active therapy.",
            "upcoming appointment": self.next_appointment
        }

    #PROFILE
    def mostra_profilo(self):
        #creo un frame a sinistra che conterrà le opzioni del profilo (Personal Info, Settings, Logout)
        self.side_frame = ctk.CTkFrame(self.current_page_frame, fg_color=COLORS["blu_acceso"], corner_radius=20)
        self.side_frame.place(x=20, y=12, relheight=0.92, relwidth=0.18)
        
        #opzioni del menu del profilo
        self.profile_buttons = {}
        opzioni = ["Personal Info", "Settings", "Privacy", "Logout"]

        #creo un bottone per ogni opzione del menu del profilo, invsibile per non alterare il layout
        for i, opzione in enumerate(opzioni):
            btn = ctk.CTkButton(self.side_frame, text=f"        {opzione}", font=FONTS["testo_normale"], height=40, width = 256, corner_radius=0, anchor="w", fg_color="transparent", text_color=COLORS["sfondo_grigino"], hover_color=COLORS["testo_scuro"], command=lambda o=opzione: self.cambia_pagina_profilo(o))
            self.profile_buttons[opzione] = btn
            btn.pack(pady=(24,0), anchor="w") if i ==0 else  btn.pack(pady=0, anchor="w")
    
    def cambia_pagina_profilo(self, nome):
        # Questa funzione è chiamata quando clicco su una voce del menu del profilo
        if self.profile_page_frame:
            self.profile_page_frame.destroy()

        self.profile_page_frame = ctk.CTkFrame(self.current_page_frame, fg_color=COLORS["sfondo_grigino"])
        self.profile_page_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
        
        #dinaimica simile a quella dei bottoni principali, ma con colori invertiti 
        for chiave,opt in self.profile_buttons.items():
            if chiave == nome:
                opt.configure(fg_color=COLORS["testo_scuro"])
                 # Qui ci metterei la funzione che mostra la pagina corrispondente, per ora c'è solo un print di prova
            else:
                opt.configure(fg_color="transparent")

        if nome == "Personal Info":
            self.mostra_profile_personal_info()
        elif nome == "Settings":
            self.mostra_placeholder(nome)
        elif nome == "Privacy":
            self.mostra_placeholder(nome)

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
                border_width=1, border_color=COLORS["bordi"], corner_radius=8,
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
                    field_frame, text="Update", width=35, height=30, corner_radius=10,
                    fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"],
                    hover_color=COLORS["bordi"], border_width=1, border_color=COLORS["bordi"], bg_color="white",
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
            current_pw_entry = ctk.CTkEntry(popup, width=250, height=40, border_width=1, corner_radius=8, border_color=COLORS["bordi"], text_color=COLORS["testo_chiaro"], show="*")
            current_pw_entry.pack(pady=(0,15))

            #chiedo di inserire la nuova password
            ctk.CTkLabel(popup, text="New Password:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"]).pack(pady=(0,0), padx=78, anchor="w")
            nuovo_input = ctk.CTkEntry(popup, width=250, height=40, border_width=1, corner_radius=8, border_color=COLORS["bordi"], text_color=COLORS["testo_chiaro"], show="*")
            nuovo_input.pack(pady=(0,15))

            #chiedo conferma della nuova password
            ctk.CTkLabel(popup, text="Confirm New Password:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"]).pack(pady=(0,0), padx=78, anchor="w")
            confirm_input = ctk.CTkEntry(popup, width=250, height=40, border_width=1, corner_radius=8, border_color=COLORS["bordi"], text_color=COLORS["testo_chiaro"], show="*")
            confirm_input.pack(pady=(0,0))

        else:
            ctk.CTkLabel(popup, text="Insert Current Password:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"]).pack(pady=(0,0), padx=78, anchor="w")
            current_pw_entry = ctk.CTkEntry(popup, width=250, height=40, border_width=1, corner_radius=8, border_color=COLORS["bordi"], text_color=COLORS["testo_chiaro"], show="*")
            current_pw_entry.pack(pady=(0,15))

            ctk.CTkLabel(popup, text=f"Insert New {nome_campo}:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"]).pack(pady=(0,0), padx=78, anchor="w")
            nuovo_input = ctk.CTkEntry(popup, width=250, height=40, border_width=1, corner_radius=8, border_color=COLORS["bordi"], text_color=COLORS["testo_chiaro"])
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
            
            #per ciò che non è password mi basta che la password inserita sia corretta, per la password invece chiedo anche di confermare il nuovo valore inserito
            if nome_colonna_db != "Password":
                if password_inserita != self.user_data[7]:
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
                if password_inserita != self.user_data[7]:

                    # Se la label esiste già, la cancello ---
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
                            self.cursor.execute(f"UPDATE user SET {nome_colonna_db} = ? WHERE username = ?", (nuovo_valore, self.user[0]))
                            self.conn.commit()
                            
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
        self.show_patient_vitals()
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
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {self.doctor_name} {self.doctor_surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
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
        save = ctk.CTkButton(self.edit_window, text="Send", width=100, corner_radius=20, fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"],
                             command=lambda: self.send_appointment_message(self.p_id, self.id_doctor, date, time, final_msg=f"[Related to the the following appointment {app[1]}  - {app[2]}]: {raw_msg}\n"))
        
        save.place(x=150, y = 470)

    # Salvo la nota sìlegata all'appuntamento nel database, così posso gestire tutto in un secondo momento. AA differenza dei messaggi normali, questa ha una entry predefinita che specifica che si tratta di una nota legata all'appuntamento, così il medico capisce subito a cosa si riferisce senza doverla contestualizzare con l'appuntamento stesso
    def send_message(self, id_sender, id_receiver, date, time, msg):

        # Query di inserimento nel Database
        query = """INSERT INTO MESSAGES (IdSender, IdReceiver, Date, Time, Content)
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
            
        except Exception as e:
            self.output_add.configure(text=f"Error: {e}", text_color='red')
            # In caso di errore facciamo il rollback per sicurezza
            self.conn.rollback()

    # Mostro la terapia attuale del paziente, con la data dell'ultima modifica, così da tenere sempre aggiornato il paziente sulla sua terapia, e fargli capire se è stata modificata di recente o se è un aggiornamento vecchio
    def show_current_therapy(self):
    
        if self.current_therapy_date and self.current_therapy_descr:
            date = self.current_therapy_date
            description = self.current_therapy_descr
        else:
            date = "No Therapy"
            description = "No Therapy"
            
        self.text = ctk.CTkLabel(self.therapy, text="Current Therapy", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
                     
        lbl_date = ctk.CTkLabel(self.therapy, text="Modified on", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=80, anchor="w")
        entry_date = ctk.CTkLabel(self.therapy, corner_radius=5, anchor="w", text=date, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["sfondo_grigino"], width=290)
        entry_date.place(x=30, y=95)

        lbl_description = ctk.CTkLabel(self.therapy, text="Last Update",font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_description.place(x=30, y=150, anchor="w")
        textbox_therapy = ctk.CTkTextbox(self.therapy,corner_radius=5, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["sfondo_grigino"], width=290, height=150)
        textbox_therapy.place(x=30, y=165)

        textbox_therapy.configure(state="normal")
        textbox_therapy.delete("1.0", "end")
        textbox_therapy.insert("0.0", description)

        self.output_add = ctk.CTkLabel(self.therapy, width=300, text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=320)

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
                                 command = lambda id=id : self.download_report(id))
            download.grid(row=0, column=2, padx=(15,50),pady=10,sticky="e")

            row.grid_columnconfigure(1, weight=1)

    # Funzione per recuperare gli esami passati del paziente dal database, così da mostrarli nella sezione dedicata
    def get_past_exams(self):

        # Recupero i dati degli appuntamenti passati
        query = """SELECT IdAppointment, Date, Time, Description FROM APPOINTMENTS
                WHERE IdPatient = ?
                AND (Date < DATE('now', 'localtime') 
                    OR (Date = DATE('now', 'localtime') AND Time < TIME('now', 'localtime')))
                ORDER BY Date DESC, Time DESC"""
      
        self.cursor.execute(query, (self.p_id,))
        data = self.cursor.fetchall()
        return data

    # Questa funzione serve a scaricare il report cliccando sull'apposito bottone
    def download_report(self, id):
        print("Function still to be written")

    # Creo un pannello che contiene i dati principali del paziente (nome, cognome, età) e da cui si può accedere alla sezione dei parametri vitali, degli esami passati, inviare messaggi al medico
    def show_patient(self):

        self.text = ctk.CTkLabel(self.current, text="Patient Overview", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
            
        row = ctk.CTkFrame(self.current, fg_color="transparent", corner_radius=20)
        row.place(x=20, y=70, relwidth=0.98)

        dot_code = ctk.CTkFrame(row, width=24, height=24, corner_radius=12, fg_color=COLORS["blu_acceso"])
        dot_code.grid(row=0,column=0, padx=15, pady=10, sticky="ew")

        label_name = ctk.CTkLabel(row, text=self.patient_name, font=FONTS["titolo"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
        label_name.grid(row=0,column=1, padx=15, pady=10, sticky="w")

        label_surname = ctk.CTkLabel(row, text=self.patient_surname, font=FONTS["titolo"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
        label_surname.grid(row=0,column=2, padx=15, pady=10, sticky="w")

        label_age = ctk.CTkLabel(row, text=f"Age: {self.patient_age}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
        label_age.grid(row=0,column=3, padx=15, pady=10, sticky="w")

        label_height = ctk.CTkLabel(row, text=f"Height: {self.patient_weight} cm", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
        label_height.grid(row=0,column=4, padx=15, pady=10, sticky="w")

        label_weight = ctk.CTkLabel(row, text=f"Weight: {self.patient_weight} Kg", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
        label_weight.grid(row=0,column=5, padx=15, pady=10, sticky="w")

        self.output_add = ctk.CTkLabel(row,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=120)
        self.output_add.grid(row=0, column=6, padx=15, pady=10, sticky="w")

        #Inserisco i vari pulsanti per accedere alle diverse sottosezioni (vitals, esami passati, messaggi)
        vitals = ctk.CTkButton(row, text="Show Vitals", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"],
                                 command = lambda : self.show_patient_vitals(False))
        vitals.grid(row=0, column=7, padx=(5,5),pady=10,sticky="e")

        message = ctk.CTkButton(row, text="Message", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"],
                                command = lambda : self.message())
        message.grid(row=0, column=8, padx=(5,15),pady=10,sticky="e")

        record_ecg = ctk.CTkButton(row, text="Record ECG", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"],
                                command = lambda : self.record_ecg())
        record_ecg.grid(row=0, column=9, padx=(5,15),pady=10,sticky="e")

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
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {self.doctor_name} {self.doctor_surname}" if receiver == self.doctor_id else "Admin", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
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

        save = ctk.CTkButton(self.edit_window, text="Send", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
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

    # Funzione utile ad effettuare il query di tutti i dati di un tipo dal db e ordinarli in un dizionario sulla base di data, se day or night, valore medio, max e min durante quella giornata    
    def get_vitals(self, start, end, vit):
        
        # Converti stringhe in oggetti datetime
        date_start = datetime.strptime(start, "%Y-%m-%d")
        date_end = datetime.strptime(end, "%Y-%m-%d")

        # Sottrazione per trovare il numero dei giorni di acquisizione
        days_range = (date_end - date_start).days + 1
        valori_attesi = 2*days_range

        query = """SELECT num.Date, num.Max, num.Min, num.Average, num.DayTime
                FROM NumericalData AS num
                JOIN Data ON num.IDNumData = Data.IDData
                WHERE data.IDPatient = ?
                AND data.NameData = ?
                AND num.Date BETWEEN ? AND ?
                AND num.DayTime IN ('Day', 'Night')
                ORDER BY num.Date ASC """
        
        self.cursor.execute(query, (self.IDPat, vit, start, end))
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
            SELECT Date, Time
            FROM DATA 
            WHERE IdPatient = ? 
            AND NameData = 'ECG'
            ORDER BY D.Date DESC
        """

        self.cursor.execute(query, (self.p_id))
        datetime_list = self.cursor.fetchall()

        acquisitions = []

        for riga in datetime_list:
            acquisitions.append(f"{riga[0]} -- {riga[1]}")
        
        acquisitions.insert(0,None)

        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x200")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Plot ECG", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=COLORS["blu_acceso"])
        dot_code.place(x=346, y=30)
                     
        start_date = ctk.CTkLabel(self.edit_window, text="Select Date:", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        start_date.place(x=30, y=80, anchor="w")
        menu = ctk.CTkOptionMenu(self.edit_window, width=340, values=acquisitions[1:],fg_color=COLORS["bianco_puro"], font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], button_color=COLORS["bianco_puro"],button_hover_color=COLORS["bordi"])
        menu.place(x=30, y=95)
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=130)

        # Tramite il bottone 'save' inizio il retrieve vero e proprio del segnale
        save = ctk.CTkButton(self.edit_window, text="Plot", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"],
                                command = lambda : self.get_ecg(menu.get()))
        save.place(x=150, y = 150)
    
    # Conversione del BLOB in float a 32 bit e campionamento
    def get_ecg(self, acquisition):

        # Convertiamo l'intera stringa in un oggetto datetime unico
        dt_converted = datetime.strptime(acquisition, "%Y-%m-%d -- %H:%M")

        # Estraiamo la data e l'ora nel loro formato nativo (oggetti date e time)
        date = dt_converted.date()
        time = dt_converted.time()

        # Query per estrarre il valore del BLOB binario e la frequenza di campionamento
        query = """SELECT S.Value, S.Sampling_Freq 
                FROM SIGNALS S
                JOIN DATA D ON S.IdSignals = D.IdData
                WHERE D.IdPatient = ? 
                AND D.NameData = 'ECG'
                AND D.Date = ?
                AND D.Time = ?"""
        
        self.cursor.execute(query, (self.IDPat, date, time))
        record = self.cursor.fetchall()[0]

        blob_data = record[0]
        sampling_freq = record[1]

        # Calcoliamo quanti numeri float (da 4 byte l'uno) ci sono nel BLOB
        num_floats = len(blob_data) // 4
        
        # 'f' indica il formato float a 32 bit. Moltiplicato per il numero di elementi (es. '500f')
        y = list(struct.unpack(f"{num_floats}f", blob_data))

        # Ricavo l'asse dei tempi (con arrotondamento), partendo dalla freq. di campionamento per tutti i campioni registrati
        x = [round(i * (1.0/sampling_freq), 2) for i in range(len(y))]


        self.plot_ecg(x,y, date, time)

    # Generazione del grafico a partire dai dati raccolti
    def plot_ecg(self, x, y, date, time):
        for widget in self.plot_area.winfo_children():
            widget.destroy()
     
        self.output.destroy()
        self.output_date.destroy()
        
        fig = Figure(figsize=(8.5,4), facecolor="none") 
        
        ax = fig.add_subplot(111)       
        ax.set_facecolor("none")
        
        ax.plot(x, y, color=COLORS["blu_acceso"], linewidth=3, label="Mean")
        
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
        self.output.place(x=35, y=70)

        self.output_date = ctk.CTkLabel(self.vitals, text = f"Recorded on {date} - {time}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
        self.output_date.place(x=240, y=70)

    # Popup che simula l'abilitazione del wearable per l'acquisizione ECG
    def record_ecg(self):
        self.guidelines = ctk.CTkToplevel()
        self.guidelines.geometry("200x320")
        self.guidelines.configure(fg_color=COLORS["sfondo_grigino"])
        self.guideframe = ctk.CTkLabel(self.current_page_frame, text="Please, follow the instructions on the wearable to record your ECG.", font=FONTS["testo_bold"], text_color=COLORS["testo_scuro"], wraplength=100, anchor="center")
        self.guideframe.place(relx=0.5, rely=0.5, anchor="center")

    # APPOINTMENTS
    def mostra_appuntamenti(self):
        self.clear_content_frame()
        
        self.manage = ctk.CTkFrame(self.current_page_frame, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.manage.place(relx=0.03, rely=0.03, relheight=0.20, relwidth=0.94)

        self.appointments_frame = ctk.CTkFrame(self.current_page_frame, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.appointments_frame.place(relx=0.03, rely=0.26, relheight=0.71, relwidth=0.94)

        self.past_appointments()
        self.new_appointments()

    # Creo 2 sotto-frame scrollable, uno per gli esami passati (con report da scaricare) e uno per quelli futuri (con possibilità di inviare messaggio)
    # Appuntamenti futuri
    def new_appointments(self):
        self.text = ctk.CTkLabel(self.appointments_frame, text="Incoming Appointments", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
            
        self.scrollable_new_app = ctk.CTkScrollableFrame(self.appointments_frame, fg_color="transparent")
        self.scrollable_new_app.place(x=0, rely=0.1, relheight=0.4, relwidth=1)
            
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

                open = ctk.CTkButton(row, text="Edit", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                        fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=["bordi"],
                                        command = lambda app=app : self.open_appointment(app))
                open.grid(row=0, column=5, padx=(15,5),pady=10,sticky="e")

                # Pulsante per scaricare il report dell'esame, con una funzione dedicata che prende l'id dell'esame così sa quale report scaricare
                download = ctk.CTkButton(row, text="Download Report", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=COLORS["bordi"],
                                 command = lambda id=id : self.download_report(id))
                download.grid(row=0, column=6, padx=(15,5),pady=10,sticky="e")
                row.grid_columnconfigure(4, weight=1)

            else:
                row = ctk.CTkFrame(self.scrollable_new_app, fg_color="transparent", corner_radius=20)
                row.place(x=20, y=70, relwidth=0.85)

                label_date = ctk.CTkLabel(row, width=160, anchor="w", text="No upcoming appointments", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")

    # Funzione per recuperare gli appuntamenti futuri
    def get_upcoming_appointments(self):

        # Recupero i dati degli appuntamenti passati
        query = """SELECT IdAppointment, Date, Time, Description FROM APPOINTMENTS
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
        lbl_name.place(x=30, y=80, anchor="w")

        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" Dr. {self.doctor_name} {self.doctor_surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], width=340, height=35)
        entry_name.place(x=30, y=95)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Schedule", font=FONTS["titolo_menu"], text_color=COLORS["testo_chiaro"])
        lbl_date.place(x=30, y=150, anchor="w")

        # Mostriamo la data e l'ora prese direttamente dalla variabile 'app' del DB
        entry_date = ctk.CTkLabel(self.edit_window, width=340, height=35, font=FONTS["testo_normale"], anchor="w", text=f" {app[1]} - {app[2]}", text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_date.place(x=30, y=165)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Report", font=FONTS["titolo_menu"], text_color=COLORS["testo_chiaro"])
        lbl_notes.place(x=30, y=220, anchor="w")

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
        entry_textbox.place(x=30, y=235)

        # Inserisco la descrizione e blocco la textbox (state="disabled") in modo che l'utente possa solo leggere e non scriverci dentro
        entry_textbox.insert("1.0", app[3])
        entry_textbox.configure(state="disabled")

        close_btn = ctk.CTkButton(
            self.edit_window,
            text="Close",
            width=100,
            corner_radius=20,
            fg_color=COLORS["bottone_grigio"],
            text_color=COLORS["testo_scuro"],
            hover_color=COLORS["bordi"],
            border_color=COLORS["bordi"],
            command=self.edit_window.destroy,
        )
        close_btn.place(x=150, y=470)

    # Appuntamenti passati
    def past_appointments(self):
        self.text = ctk.CTkLabel(self.appointments_frame, text="Incoming Appointments", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
            
        self.scrollable_past_app = ctk.CTkScrollableFrame(self.appointments_frame, fg_color="transparent")
        self.scrollable_past_app.place(x=0, rely=0.5, relheight=0.4, relwidth=1)
            
        past_appointments = self.get_past_exams()

        if past_appointments:
            for app in past_appointments:
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

                label_report = ctk.CTkLabel(row, text=desc, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_report.grid(row=0,column=4, padx=15, pady=10, sticky="w")

                open = ctk.CTkButton(row, text="Edit", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                        fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=["bordi"],
                                        command = lambda app=app : self.open_new_appointment(app))
                open.grid(row=0, column=5, padx=(15,5),pady=10,sticky="e")

                note = ctk.CTkButton(row, text="Delete", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                        fg_color=COLORS["bottone_grigio"], hover_color=COLORS["bordi"], border_color=["bordi"],
                                        command = lambda app=app : self.appointment_note(app))
                note.grid(row=0, column=6, padx=(5,15),pady=10,sticky="e")

                row.grid_columnconfigure(4, weight=1)

            else:
                row = ctk.CTkFrame(self.scrollable_new_app, fg_color="transparent", corner_radius=20)
                row.place(x=20, y=70, relwidth=0.85)

                label_date = ctk.CTkLabel(row, width=160, anchor="w", text="No past appointments", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")


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
user = ("mrossi",)
PatientApp(user)