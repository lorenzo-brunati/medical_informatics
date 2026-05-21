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
    "titolo_menu": ("Montserrat", 18),
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
        
        # Questa mi serve per distruggere le pagine vecchie quando cambio sezione
        self.current_page_frame = None
        self.profile_page_frame = None

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

    #FUNZIONE PER PESCARE I DATI DAL DB
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
        # 1. Pulisco la pagina attuale e creo un nuovo frame (bianco o grigio a seconda dei gusti) dove mettere i nuovi contenuti
        if self.current_page_frame: 
            self.current_page_frame.destroy()

        self.current_page_frame = ctk.CTkFrame(self.root, fg_color=COLORS["sfondo_grigino"])
        self.current_page_frame.place(relx=0, rely=0.12, relwidth=1, relheight=0.88)
        
        # 2. Riporto tutti i bottoni (testo e icone) allo stato grigio/scuro tranne quelli che sono stati cliccati, quelli diventano blu con testo bianco o icona chiara a seconda del caso
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

        # 3. Funzioni che mostrano i contenuti 
        if nome == "Dashboard":
            self.mostra_dashboard()

        elif nome == "Data":
            self.mostra_placeholder(nome)

        elif nome == "Appointments":
            self.mostra_placeholder(nome)
        
        elif nome == "Support":
            self.mostra_placeholder(nome)

    def mostra_dashboard(self):
        dati = self.recupera_info_db()

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
        #recupero le informazioni personali dal database
        self.cursor.execute("SELECT Name, Surname, BirthDate, Address, PhoneNumber, Email, Username, Password, FiscalCode FROM user WHERE username = ?", (self.user[0],))
        self.user_data = self.cursor.fetchone()

        #Frame principale di contenimento scorrevole (allineato a destra del menu profilo)
        self.content_scroll = ctk.CTkScrollableFrame(self.profile_page_frame, fg_color="transparent", height=600)
        self.content_scroll.pack(fill="both", expand=True, padx=0, pady=(10,0))

        # Sfrutto una griglia all'interno del frame per dividere lo spazio in 2 colonne
        self.content_scroll.grid_columnconfigure(0, weight=1, pad=30)
        self.content_scroll.grid_columnconfigure(1, weight=1, pad=30)

        # Ogni elemento definisce: label, valore dal DB, colonna, e se è modificabile
        campi = [
            {"lbl": "First Name",    "val": self.user_data[0], "col": 1, "modificabile": False},
            {"lbl": "Last Name",     "val": self.user_data[1], "col": 0, "modificabile": False},
            {"lbl": "Birth Date",    "val": self.user_data[2], "col": 1, "modificabile": False},
            {"lbl": "Address",       "val": self.user_data[3], "col": 0, "modificabile": True},
            {"lbl": "Phone Number",  "val": self.user_data[4], "col": 1, "modificabile": True},
            {"lbl": "Email",         "val": self.user_data[5], "col": 0, "modificabile": True},
            {"lbl": "Username",      "val": self.user_data[6], "col": 0, "modificabile": False},
            {"lbl": "Password",      "val": self.user_data[7], "col": 1, "modificabile": True},
            {"lbl": "Fiscal Code",   "val": self.user_data[8], "col": 0, "modificabile": False}
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
        
    def mostra_dati(self):
        # Questa funzione mostra i dati del paziente, per ora è un placeholder che mostra solo un testo, ma in futuro si può espandere per mostrare grafici, tabelle, ecc.     
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