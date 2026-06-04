import sqlite3 as sql
import customtkinter as ctk
import PIL.Image
from tkinter import messagebox

COLORS = {
    "sfondo_grigino": "#E8EBF2",
    "bianco_puro": "#FFFFFF",
    "blu_acceso": "#3366cc",
    "testo_scuro": "#475569",
    "testo_chiaro": "#9DA1A7",
    "bordi": "#BFC6D1",
    "bottone_grigio": "#DCE1E9"
}

FONTS = {
    "titolo": ("Montserrat", 22, "bold"),
    "sottotitolo": ("Montserrat", 16, "italic"),
    "testo_normale": ("Montserrat", 16),
    "testo_bold": ("Montserrat", 14, "bold"),
    "micro_bold": ("Montserrat", 8, "bold")
}

class AdminApp(ctk.CTk):

    def carica_icone(self):
        self.icon_notif = ctk.CTkImage(light_image=PIL.Image.open("Icons/dark_bell.png"), size=(24, 24))
        self.icon_profile = ctk.CTkImage(light_image=PIL.Image.open("Icons/dark_user.png"), size=(20, 20))

        self.icon_notif_light = ctk.CTkImage(light_image=PIL.Image.open("Icons/light_bell.png"), size=(24, 24))
        self.icon_profile_light = ctk.CTkImage(light_image=PIL.Image.open("Icons/light_user.png"), size=(20, 20))

    def __init__(self, ID):

        super().__init__()
        
        self.buttons_dict = {}

        self.ID = ID
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()

        self.title("AdminApp")
        self.geometry("1250x725")

        self.current_page_frame = None

        self.carica_icone()
        self.setup_gui()
        self.mainloop()
    
    def setup_gui(self):

        self.topbar = ctk.CTkFrame(self, fg_color= COLORS["sfondo_grigino"])
        self.topbar.place(relx=0, rely=0, relheight=0.15, relwidth= 1)
        
        self.welcome()

        self.buttons()

        self.home()

    def home(self):
        self.support()
        self.user()

    def buttons(self):

        self.container = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.container.place(relx=0.35, rely=0, relheight=1, relwidth=0.5)

        """ btn = ctk.CTkButton(self.container, text="Home", text_color=COLORS["testo_scuro"], font=FONTS["titolo"],
                            width=150, height=50, corner_radius=20,
                            fg_color=COLORS["bottone_grigio"], border_color=COLORS["bordi"], hover_color=COLORS["blu_acceso"])
        btn.place(x=30, rely=0.3)

        wear = ctk.CTkButton(self.container, text="Wearables", text_color=COLORS["testo_scuro"], font=FONTS["titolo"],
                            width=150, height=50, corner_radius=20,
                            fg_color=COLORS["bottone_grigio"], border_color=COLORS["bordi"], hover_color=COLORS["blu_acceso"])
        wear.place(x=300, rely=0.3) """


        self.side_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.side_frame.place(x=1100, y=40)

        btn1 = ctk.CTkButton(self.side_frame, text="Profile", image=self.icon_profile, width=38, height=38, corner_radius=19,
                            fg_color=COLORS["bottone_grigio"], border_width=2, border_color=COLORS["bordi"],
                            hover_color=COLORS["bordi"], text_color=COLORS["testo_scuro"], 
                            command=lambda : self.profile(self.ID))
        btn1.pack(side="left", padx=10)

        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.place(relx=0, rely=0.15, relheight=0.85, relwidth=1) 

        self.buttons_dict = {}
        buttons = ["Home", "Wearables"]
        for b in buttons:
            btn = ctk.CTkButton(self.container, text=b, text_color=COLORS["testo_scuro"], font=FONTS["testo_normale"],
                                command = lambda b=b: self.switch_tab(b), width=150, height=40, corner_radius=20,
                                fg_color=COLORS["bottone_grigio"], border_color=COLORS["bordi"], hover_color=COLORS["blu_acceso"])
            btn.pack(side="left", padx=50)
            self.buttons_dict[b] = btn
        
        self.update_buttons("Home")
        self.tab = "Home"

        self.icon_container = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.icon_container.place(relx=0.98, rely=0.05, anchor="ne", relheight=0.8)


    def switch_tab(self, tab):
        self.tab = tab
        self.update_buttons(tab)
        if tab == "Home":
            self.home()
        elif tab == "Wearables":
            self.wearables()

    def setup_tabs(self):
        # Inizializziamo il dizionario (importante per update_buttons)
        self.buttons_dict = {}
        
        # Definiamo solo i due pulsanti necessari
        tabs = ["Edit", "Delete"]
        
        for t in tabs:
            # Creazione del pulsante
            btn = ctk.CTkButton(
                self.header_frame, # Usiamo l'header_frame creato prima
                text=t, 
                text_color=COLORS["testo_scuro"], 
                font=FONTS["testo_bold"],
                # Lambda con t=t per catturare correttamente il valore nel ciclo
                command=lambda t=t: self.switch_tab(t), 
                width=120, 
                height=32, 
                corner_radius=10,
                fg_color=COLORS["bottone_grigio"], 
                hover_color=COLORS["blu_acceso"]
            )
            
            # Li posizioniamo uno accanto all'altro
            btn.pack(side="left", padx=10, pady=5)
            
            # Salviamo il riferimento nel dizionario usando il nome come chiave
            self.buttons_dict[t] = btn

    def update_buttons(self, current_tab):
        for tab, btn in self.buttons_dict.items():
            if tab == current_tab:
                btn.configure(fg_color=COLORS["blu_acceso"], text_color=COLORS["bianco_puro"])
            else:
                btn.configure(fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"])

    def support(self):    
        
        self.container_richieste = ctk.CTkFrame(self.main, fg_color=COLORS["bianco_puro"], corner_radius=20)
        self.container_richieste.place(relx=0.515, rely=0.03, relwidth=0.455, relheight=0.94)

        
        self.titolo = ctk.CTkLabel(self.container_richieste, text="Manage Requests", font=FONTS["titolo"])
        self.titolo.place(relx=0.05, rely=0.05) 

        self.header_frame = ctk.CTkFrame(self.container_richieste, width=550, height=30, fg_color=COLORS["bianco_puro"], corner_radius=10)
        self.header_frame.place(relx=0.5, rely=0.15, relwidth=0.95, anchor= "center")

        ctk.CTkLabel(self.header_frame, text="Name", text_color=COLORS["testo_scuro"], font=FONTS["testo_bold"]).place(x=15, rely=0.5, anchor='w')

        ctk.CTkLabel(self.header_frame, text="Surname", text_color=COLORS["testo_scuro"], font=FONTS["testo_bold"]).place(x=105, rely=0.5, anchor='w')

        ctk.CTkLabel(self.header_frame, text="Type", text_color=COLORS["testo_scuro"], font=FONTS["testo_bold"]).place(x=215, rely=0.5, anchor='w')

        ctk.CTkLabel(self.header_frame, text="ID_Request", text_color=COLORS["testo_scuro"], font=FONTS["testo_bold"]).place(x=330, rely=0.5, anchor='w')

        ctk.CTkLabel(self.header_frame, text="Date", text_color=COLORS["testo_scuro"], font=FONTS["testo_bold"]).place(x=440, rely=0.5, anchor='w')

        self.popola_richieste()

    def user(self):
        #User List 
        self.user_list = ctk.CTkFrame(self.main, fg_color = COLORS["bianco_puro"], corner_radius=20)
        self.user_list.place(relx=0.03, rely=0.03, relwidth=0.455, relheight=0.94)

        self.user_title = ctk.CTkLabel(self.user_list, text="Users List", font=FONTS["titolo"])
        self.user_title.place(x=30, y=25)

        self.popola_utenti()
    
    def welcome(self):
        
        self.cursor.execute("SELECT name FROM user WHERE ID = ?", (self.ID,))
        name = self.cursor.fetchall()[0][0]
        
        self.surname_label = ctk.CTkLabel(self.topbar, text=f"Hello, {name}!", font=FONTS["titolo"], text_color=COLORS["testo_chiaro"])
        self.surname_label.place(x=50, y=30)

        self.welcome_label = ctk.CTkLabel(self.topbar, text="See what's going on", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.welcome_label.place(x=50, y=60)
    
    def popola_utenti(self):
        """Recupera tutti gli utenti dal DB e li inserisce nel frame user_list"""
        # 1. Aggiungiamo 'Id' alla SELECT per poterlo passare ai bottoni
        query = "SELECT Name, Surname, UserType, Username, Id FROM USER WHERE UserType != 'Admin' ORDER BY UserType"
        self.cursor.execute(query)
        utenti = self.cursor.fetchall()

        # Pulizia del frame
        if hasattr(self, 'scroll_frame'):
            self.scroll_frame.destroy()

        self.scroll_frame = ctk.CTkScrollableFrame(self.user_list, fg_color="transparent")
        self.scroll_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.85)

        for utente in utenti:
            nome, cognome, ruolo, username, user_id = utente # user_id recuperato qui
            
            row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            row.pack(fill='x', padx=20)

            # Labels
            ctk.CTkLabel(row, text=nome, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], width=120, anchor="w").grid(row=0, column=0, padx=15, pady=10, sticky='w')
            ctk.CTkLabel(row, text=cognome, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], width=120, anchor="w").grid(row=0, column=1, padx=15, pady=10, sticky='w')
            ctk.CTkLabel(row, text=ruolo, font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"], width=75, anchor="w").grid(row=0, column=2, padx=15, pady=10, sticky='w')
            ctk.CTkLabel(row, text=username, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], width=75, anchor="w").grid(row=0, column=3, padx=15, pady=10, sticky='w')
            ctk.CTkLabel(row, text=user_id, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], width=75, anchor="center").grid(row=0, column=4, padx=15, pady=10, sticky='w')


            """ edit = ctk.CTkButton(row, text="Edit", width=70, corner_radius=20, 
                                 text_color=COLORS["testo_scuro"], fg_color=COLORS["bottone_grigio"], 
                                 hover_color=COLORS["blu_acceso"],
                                 command=lambda u_id=user_id: self.edit_btn(u_id))
            edit.grid(row=0, column=5, padx=(15,5), pady=10, sticky="e") """

            delete = ctk.CTkButton(row, text="Delete", width=70, corner_radius=20, 
                                   text_color=COLORS["testo_scuro"], fg_color=COLORS["bottone_grigio"], 
                                   hover_color=COLORS["blu_acceso"], font=FONTS["testo_normale"], 
                                   command=lambda u_id=user_id: self.delete_btn_user(u_id))
            delete.grid(row=0, column=5, padx=(5,15), pady=10, sticky="e")

            row.grid_columnconfigure((2,3,4), weight=1, uniform="group1")

            row.grid_columnconfigure((0,1), weight=2)

            add = ctk.CTkButton(self.user_list, text="Add", width=70, corner_radius=20, text_color=COLORS["bianco_puro"], 
                                 fg_color=COLORS["blu_acceso"], hover_color=COLORS["bottone_grigio"], 
                                 command=lambda: self.add(self.ID))
            add.place(x=600, y=22)

    def popola_richieste(self):
        """Recupera le richieste di supporto e i nomi dei pazienti """
        # Query con JOIN per ottenere il nome di chi chiede supporto
        query = """
            SELECT USER.Name, USER.Surname, SUPPORT.SupportType, SUPPORT.IdSupport, SUPPORT.Date
            FROM SUPPORT 
            JOIN USER ON SUPPORT.IdRequester = USER.Id 
            ORDER BY SUPPORT.Date DESC
        """

        #WHERE SUPPORT.IdAdmin = ?

        self.cursor.execute(query) #(self.admin_id,)
        richieste = self.cursor.fetchall()

        # Frame scrollabile per le richieste
        self.scroll_req = ctk.CTkScrollableFrame(self.container_richieste, fg_color="transparent")
        self.scroll_req.place(relx=0, rely=0.22, relwidth=1, relheight=0.7)

        for req in richieste:
            nome, cognome, tipo, id_req, date = req
            
            # Creiamo un frame per la riga all'interno dello SCROLLABLE frame
            # Usiamo un'altezza fissa per mantenere l'ordine
            row = ctk.CTkFrame(self.scroll_req, fg_color="transparent", height=40)
            row.pack(fill="x", pady=2) # Spazio tra una riga e l'altra

            row.pack_propagate(False)
            
            ctk.CTkLabel(row, text=nome, font=FONTS["testo_normale"], 
                        text_color=COLORS["testo_scuro"], width=90, anchor="w").place(x=15, rely=0.5, anchor='w')

            ctk.CTkLabel(row, text=cognome, font=FONTS["testo_normale"], 
                        text_color=COLORS["testo_scuro"], width=110, anchor="w").place(x=115, rely=0.5, anchor='w')

            ctk.CTkLabel(row, text=tipo, font=FONTS["testo_normale"], 
                        text_color=COLORS["testo_chiaro"], width=150, anchor="w").place(x=215, rely=0.5, anchor='w')

            ctk.CTkLabel(row, text=id_req, font=FONTS["testo_normale"], 
                        text_color=COLORS["testo_scuro"], width=30, anchor="center").place(x=365, rely=0.5, anchor='w')

            ctk.CTkLabel(row, text=date, font=FONTS["testo_normale"], 
                        text_color=COLORS["testo_scuro"], width=100, anchor="w").place(x=430, rely=0.5, anchor='w')
            
            btn_delete = ctk.CTkButton(row, text="Resolve", width=30, font=FONTS["testo_normale"], corner_radius=20, 
                                 text_color=COLORS["testo_scuro"], fg_color=COLORS["bottone_grigio"], 
                                 hover_color=COLORS["blu_acceso"],
                                command=lambda i=id_req: self.delete_btn_req(i))
            btn_delete.place(x=590, rely=0.5, anchor='w')

            btn_view = ctk.CTkButton(row, text="View", width=20, font=FONTS["testo_normale"], corner_radius=20, 
                                 text_color=COLORS["testo_scuro"], fg_color=COLORS["bottone_grigio"], 
                                 hover_color=COLORS["blu_acceso"],
                                command=lambda i=id_req: self.view(i))
            btn_view.place(x=520, rely=0.5, anchor='w')

            # Lista delle opzioni
            self.filter_options = ["All", "SupportCredentials", "InconsistentData", "Wearable", "ScheduleIssue", "Others"]

            self.filter_menu = ctk.CTkOptionMenu(
                self.container_richieste, 
                values=self.filter_options,
                fg_color=COLORS["bottone_grigio"],
                text_color=COLORS["testo_scuro"],
                command=self.apply_filter 
            )
            self.filter_menu.place(x=215, rely=0.2, anchor='w')

    def wearables(self):

        self.wearables_list = ctk.CTkFrame(self.main, fg_color = COLORS["bianco_puro"], corner_radius=20)
        self.wearables_list.place(relx=0.515, rely=0.03, relwidth=0.455, relheight=0.94)

        self.user_title = ctk.CTkLabel(self.wearables_list, text="Wearables List", font=FONTS["titolo"])
        self.user_title.place(x=30, y=25)
        """Recupera i dati dei wearable e i dettagli dei pazienti associati"""
        
        query = """
            SELECT 
                W.IdWearable, 
                P.IdPatient, 
                U.Name, 
                U.Surname, 
                U.FiscalCode
            FROM WEARABLE_DEVICE AS W
            LEFT JOIN PATIENT_CLINICALDATA as P ON W.IdWearable = p.IdWearable 
            LEFT JOIN USER U ON P.IdPatient = U.Id

            ORDER BY P.IdWearable
        """
        try:
            self.cursor.execute(query)
            dispositivi = self.cursor.fetchall()
        except Exception as e:
            print(f"Errore query wearables: {e}")
            return

        if hasattr(self, 'scroll_frame_wear'):
            self.scroll_frame_wear.destroy()

        self.scroll_frame_wear = ctk.CTkScrollableFrame(self.wearables_list, fg_color="transparent")
        self.scroll_frame_wear.place(relx=0, rely=0.1, relwidth=1, relheight=0.85)


        for dev in dispositivi:
            id_w, id_p, nome, cognome, cf = dev
            
            row_w = ctk.CTkFrame(self.scroll_frame_wear, fg_color="transparent")
            row_w.pack(fill='x', padx=20)

            ctk.CTkLabel(row_w, text=f"W-{id_w}", font=FONTS["testo_normale"], text_color=COLORS["blu_acceso"], width=60).grid(row=0, column=0, padx=10, pady=10)

            ctk.CTkLabel(row_w, text=f"P-{id_p}", font=FONTS["testo_normale"], width=60).grid(row=0, column=1, padx=10, pady=10)

            ctk.CTkLabel(row_w, text=nome, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], width=75, anchor="w").grid(row=0, column=2, padx=10, pady=10, sticky='w')

            ctk.CTkLabel(row_w, text=cognome, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], width=75, anchor="w").grid(row=0, column=3, padx=10, pady=10, sticky='w')

            ctk.CTkLabel(row_w, text=cf, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], width=75, anchor="center").grid(row=0, column=4, padx=(10,35), pady=10, sticky='w')

            if(id_p!=None):
                btn_edit = ctk.CTkButton(row_w, text="Edit", width=70, font=FONTS["testo_normale"], corner_radius=20, 
                                            text_color=COLORS["testo_scuro"], fg_color=COLORS["bottone_grigio"], 
                                            hover_color=COLORS["blu_acceso"],
                                        command=lambda i=id_p, y=id_w: self.edit_w(i,y))
                btn_edit.place(x=565, rely=0.5, anchor='w')
            
            add = ctk.CTkButton(self.wearables_list, text="Add", width=70, corner_radius=20, text_color=COLORS["bianco_puro"], 
                                 fg_color=COLORS["blu_acceso"], hover_color=COLORS["bottone_grigio"], 
                                 command=lambda : self.add_wearable())
            add.place(x=600, y=22)
            
            if(id_p==None):
                btn_associa = ctk.CTkButton(row_w, text="Associate", width=20, font=FONTS["testo_normale"], corner_radius=20, 
                                        text_color=COLORS["testo_scuro"], fg_color=COLORS["bottone_grigio"], 
                                        hover_color=COLORS["blu_acceso"],
                                    command=lambda i=id_w: self.associa(i))
                btn_associa.place(x=445, rely=0.5, anchor='w')

                btn_delete = ctk.CTkButton(row_w, text="Delete", width=20, font=FONTS["testo_normale"], corner_radius=20, 
                                        text_color=COLORS["testo_scuro"], fg_color=COLORS["bottone_grigio"], 
                                        hover_color=COLORS["blu_acceso"],
                                    command=lambda i=id_w: self.delete_w(i))
                btn_delete.place(x=560, rely=0.5, anchor='w')


##################################################################

##################################################################

#  Sezione pop-up windows

    def edit_btn(self, user_id):
        # 1. Recuperiamo i dati attuali dal DB
        self.cursor.execute("SELECT Name, Surname, Username, Password FROM USER WHERE Id = ?", (user_id,))
        user_data = self.cursor.fetchone()
        
        if not user_data:
            print("Utente non trovato")
            return

        current_name, current_surname, current_username, current_psw = user_data

        self.edit_window = ctk.CTkToplevel(self)
        self.edit_window.geometry("450x400")
        self.edit_window.configure(fg_color=COLORS["sfondo_grigino"])
        self.edit_window.title(f"Edit User: ID {user_id}")
        self.edit_window.grab_set() # Blocca la finestra principale

        title = ctk.CTkLabel(self.edit_window, text="Edit User Details", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.pack(pady=(20, 20))

        # --- CAMPI DI INPUT ---
        # Nome
        ctk.CTkLabel(self.edit_window, text=f"Name: {current_name}", font=FONTS["testo_bold"]).pack(padx=30, anchor="w")

        # Cognome
        ctk.CTkLabel(self.edit_window, text=f"Surname: {current_surname}", font=FONTS["testo_bold"]).pack(padx=30, anchor="w")

        # Username
        ctk.CTkLabel(self.edit_window, text="Username:", font=FONTS["testo_bold"]).pack(padx=30, anchor="w")
        entry_username = ctk.CTkEntry(self.edit_window, width=300)
        entry_username.insert(0, current_username) # Inserisce lo username attuale
        entry_username.pack(pady=(0, 20))

        # Password
        ctk.CTkLabel(self.edit_window, text="Password:", font=FONTS["testo_bold"]).pack(padx=30, anchor="w")
        entry_psw = ctk.CTkEntry(self.edit_window, width=300)
        entry_psw.insert(0, current_psw) # Inserisce psw attuale
        entry_psw.pack(pady=(0, 15))

        def save_changes():
            new_user = entry_username.get()
            new_psw = entry_psw.get()

            try:
                self.cursor.execute("""
                    UPDATE USER 
                    SET Username = ?, Password = ? 
                    WHERE Id = ?
                """, (new_user, new_psw, user_id))
                
                self.conn.commit()
                print("Dati aggiornati con successo!")
                
                self.edit_window.destroy() # Chiude la popup
                self.popola_utenti()       # Ricarica la tabella principale con i nuovi dati
                
            except Exception as e:
                print(f"Errore nel salvataggio: {e}")

        # --- BOTTONI ---
        btn_frame = ctk.CTkFrame(self.edit_window, fg_color="transparent")
        btn_frame.pack(pady=20)

        save_btn = ctk.CTkButton(btn_frame, text="Save Changes", fg_color="green", hover_color="#1E5631",
                                text_color=COLORS["bianco_puro"], command=save_changes)
        save_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", fg_color=COLORS["bianco_puro"], 
                                text_color=COLORS["testo_scuro"], command=self.edit_window.destroy)
        cancel_btn.pack(side="left", padx=10)

    def delete_btn_req(self, id_req):
        self.delete_window = ctk.CTkToplevel(self)
        self.delete_window.geometry("400x200")
        self.delete_window.configure(fg_color=COLORS["bottone_grigio"])
        self.delete_window.title("Confirm")
        
        self.delete_window.grab_set()

        title = ctk.CTkLabel(self.delete_window, text="Resolve Request", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        start_date = ctk.CTkLabel(self.delete_window, text=f"Are you sure to resolve this request? (ID={id_req})", 
                                font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        start_date.place(x=30, y=80, anchor="w")

        def confirm_yes():
            try:
                query = "DELETE FROM SUPPORT WHERE IdSupport = ?"
                self.cursor.execute(query, (id_req,))
                self.conn.commit()
                
                self.delete_window.destroy()

                self.popola_richieste()
                
                print(f"Richiesta {id_req} eliminata con successo.")
            except Exception as e:
                print(f"Errore durante la cancellazione: {e}")

        yes = ctk.CTkButton(self.delete_window, width=100, text='Yes',
                            fg_color="red", hover_color="#8B0000", text_color="white",
                            command=confirm_yes)
        yes.place(x=30, y=120)

        no = ctk.CTkButton(self.delete_window, width=100, text='No',
                        fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], 
                        command=self.delete_window.destroy)
        no.place(x=200, y=120)
    
    def view(self, id_req):
        # 1. Recupero del messaggio dal database
        try:
            self.cursor.execute("SELECT Message FROM SUPPORT WHERE IdRequester = ?", (id_req,))
            result = self.cursor.fetchone()
            messaggio_utente = result[0] if result and result[0] else "Nessun testo presente nel report."
        except Exception as e:
            print(f"Errore recupero messaggio: {e}")
            return

        # 2. Setup Finestra
        self.view_window = ctk.CTkToplevel(self)
        self.view_window.geometry("400x320") # Più alta per ospitare due aree di testo
        self.view_window.configure(fg_color=COLORS["sfondo_grigino"])
        self.view_window.title("View Request")
        self.view_window.grab_set()

        # Titolo
        title = ctk.CTkLabel(self.view_window, text="User Request", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.pack(pady=(20, 10), padx=30, anchor="w")

        lbl_notes = ctk.CTkLabel(self.view_window, text="Message:", font=FONTS["testo_bold"], text_color=COLORS["testo_scuro"])
        lbl_notes.place(x=30, y=80, anchor="w")

        display_text = ctk.CTkTextbox(self.view_window, width=340, height=180, corner_radius=5, 
                                    font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], wrap="word")
        display_text.insert("0.0", messaggio_utente)
        display_text.configure(state="disabled") # Disabilitato per evitare modifiche al messaggio originale
        display_text.place(x=30, y=100)
                     
    def apply_filter(self, choice):
            """Filtra le richieste in base al tipo selezionato nel menu"""
            
            # 1. Costruiamo la query base
            query = """
            SELECT USER.Name, USER.Surname, SUPPORT.SupportType, SUPPORT.IdSupport, SUPPORT.Date
            FROM SUPPORT 
            JOIN USER ON SUPPORT.IdRequester = USER.Id 
            """
            params = ()

            if choice != "All":
                query += " WHERE SupportType = ?"
                params = (choice,)
                
            query += " ORDER BY SUPPORT.Date DESC"

            try:
                self.cursor.execute(query, params)
                filtered_results = self.cursor.fetchall()
                
                # 4. Ricarichiamo la visualizzazione
                self.display_filtered_requests(filtered_results)
                
            except Exception as e:
                print(f"Errore durante il filtraggio: {e}")

    def display_filtered_requests(self, richieste):
        """Svuota il frame e mostra solo i dati filtrati"""
        # Pulizia del frame 
        for widget in self.scroll_req.winfo_children():
            widget.destroy()

        for req in richieste:
            nome, cognome, tipo, id_req, date = req
            
            # Creiamo un frame per la riga all'interno dello SCROLLABLE frame
            # Usiamo un'altezza fissa per mantenere l'ordine
            row = ctk.CTkFrame(self.scroll_req, fg_color="transparent", height=40)
            row.pack(fill="x", pady=2) # Spazio tra una riga e l'altra

            row.pack_propagate(False)
            
            ctk.CTkLabel(row, text=nome, font=FONTS["testo_normale"], 
                        text_color=COLORS["testo_scuro"], width=90, anchor="w").place(x=15, rely=0.5, anchor='w')

            ctk.CTkLabel(row, text=cognome, font=FONTS["testo_normale"], 
                        text_color=COLORS["testo_scuro"], width=110, anchor="w").place(x=115, rely=0.5, anchor='w')

            ctk.CTkLabel(row, text=tipo, font=FONTS["testo_normale"], 
                        text_color=COLORS["testo_chiaro"], width=110, anchor="w").place(x=215, rely=0.5, anchor='w')

            ctk.CTkLabel(row, text=id_req, font=FONTS["testo_normale"], 
                        text_color=COLORS["testo_scuro"], width=50, anchor="center").place(x=355, rely=0.5, anchor='w')

            ctk.CTkLabel(row, text=date, font=FONTS["testo_normale"], 
                        text_color=COLORS["testo_scuro"], width=100, anchor="w").place(x=430, rely=0.5, anchor='w')
            
            btn_delete = ctk.CTkButton(row, text="Resolve", width=30, font=FONTS["testo_normale"], corner_radius=20, 
                                 text_color=COLORS["testo_scuro"], fg_color=COLORS["bottone_grigio"], 
                                 hover_color=COLORS["blu_acceso"],
                                command=lambda i=id_req: self.delete_btn_req(i))
            btn_delete.place(x=590, rely=0.5, anchor='w')

            btn_view = ctk.CTkButton(row, text="View", width=20, font=FONTS["testo_normale"], corner_radius=20, 
                                 text_color=COLORS["testo_scuro"], fg_color=COLORS["bottone_grigio"], 
                                 hover_color=COLORS["blu_acceso"],
                                command=lambda i=id_req: self.view(i))
            btn_view.place(x=520, rely=0.5, anchor='w')
 
    def delete_btn_user(self, user_id):

        self.delete_window = ctk.CTkToplevel(self)
        self.delete_window.geometry("400x200")
        self.delete_window.configure(fg_color=COLORS["bottone_grigio"])
        self.delete_window.title("Confirm Deletion")
        
        self.delete_window.grab_set()

        title = ctk.CTkLabel(self.delete_window, text="Delete User", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        start_date = ctk.CTkLabel(self.delete_window, text=f"Are you sure to delete user {user_id}?", 
                                font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        start_date.place(x=30, y=80, anchor="w")
        
        def confirm_yes():
            try:
                self.cursor.execute("DELETE FROM USER WHERE Id = ?", (user_id,))
                self.conn.commit()
                self.delete_window.destroy()
                self.popola_utenti() # Ricarica la lista utenti aggiornata
            except Exception as e:
                print(f"Errore SQL: {e}")
                
        yes = ctk.CTkButton(self.delete_window, width=100, text='Yes',
                            fg_color="red", hover_color="#8B0000", text_color="white",
                            command=confirm_yes)
        yes.place(x=30, y=120)

        no = ctk.CTkButton(self.delete_window, width=100, text='No',
                        fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"],
                        command=self.delete_window.destroy)
        no.place(x=200, y=120)

    def add(self, ID):
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.geometry("500x650") # Spazio extra per i campi dinamici
        self.add_window.configure(fg_color=COLORS["sfondo_grigino"])
        self.add_window.title("Add New User")
        self.add_window.grab_set()

        title = ctk.CTkLabel(self.add_window, text="Create New User", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.pack(pady=(20, 10))

        # --- CAMPI BASE ---
        entry_name = self.create_input_field("Name:", "Enter name...")
        entry_surname = self.create_input_field("Surname:", "Enter surname...")
        entry_username = self.create_input_field("Username:", "Enter username...")
        entry_password = self.create_input_field("Password:", "Enter password...", is_password=True)

        # --- SELEZIONE RUOLO ---
        ctk.CTkLabel(self.add_window, text="Role:", font=FONTS["testo_bold"]).pack(padx=40, anchor="w")
        role_option = ctk.CTkOptionMenu(
            self.add_window, 
            values=["Doctor", "Patient"], 
            fg_color=COLORS["bottone_grigio"],
            text_color=COLORS["testo_scuro"],
            width=320,
            command=lambda choice: self.toggle_patient_fields(choice) # Chiama la funzione al cambio
        )
        role_option.set("Patient")
        role_option.pack(pady=(0, 15))

        # --- FRAME DINAMICO PER PAZIENTI ---
        self.patient_extra_frame = ctk.CTkFrame(self.add_window, fg_color="transparent")
        # Lo mostriamo subito perché il default è "Patient"
        self.patient_extra_frame.pack(fill="x", padx=40)

        ctk.CTkLabel(self.patient_extra_frame, text="First Appointment Date (YYYY-MM-DD):", font=FONTS["testo_bold"]).pack(anchor="w")
        entry_date = ctk.CTkEntry(self.patient_extra_frame, width=320, placeholder_text="2024-12-31")
        entry_date.pack(pady=(0, 10))

        ctk.CTkLabel(self.patient_extra_frame, text="Assign Doctor:", font=FONTS["testo_bold"]).pack(anchor="w")

        # 1. Recupero ID, Nome e Cognome
        self.cursor.execute("SELECT Id, Name, Surname FROM USER WHERE UserType = 'Doctor'")
        results = self.cursor.fetchall()

        # 2. Creo un dizionario: {"Nome Cognome": Id}
        # Esempio: {"Mario Rossi": 1, "Luigi Bianchi": 2}
        self.doctors_map = {f"{d[1]} {d[2]}": d[0] for d in results}
        
        # Prendo solo i nomi per popolare il menu a tendina
        doctor_names = list(self.doctors_map.keys())

        doctor_option = ctk.CTkOptionMenu(
            self.patient_extra_frame, 
            fg_color=COLORS["bottone_grigio"],
            values=doctor_names if doctor_names else ["No doctors available"],
            text_color=COLORS["testo_scuro"],
            width=320
        )
        doctor_option.pack(pady=(0, 10))

        # --- LOGICA DI SALVATAGGIO ---
        def save_new_user():
            role = role_option.get()
            
            try:
                # 1. Inserimento Utente
                self.cursor.execute("""
                    INSERT INTO USER (Name, Surname, Username, Password, UserType) 
                    VALUES (?, ?, ?, ?, ?)
                """, (entry_name.get(), entry_surname.get(), entry_username.get(), entry_password.get(), role))
                
                user_id = self.cursor.lastrowid # Recuperiamo l'ID appena creato

                
               
                # PRENdO L'ID DAL DIZIONARIO
                selected_name = doctor_option.get()
                # Recupero l'ID corrispondente al nome selezionato
                selected_doctor_id = self.doctors_map.get(selected_name)

                # 2. Se è un paziente, creo l'appuntamento
                if role == "Patient":
                    doc_name = doctor_option.get()
                    self.cursor.execute("""
                        INSERT INTO APPOINTMENT (IdPatient, IdDoctor, Date) 
                        VALUES (?, ?, ?)
                    """, (user_id, selected_doctor_id, entry_date.get()))
                    self.cursor.execute("""
                        INSERT INTO PATIENT_CLINICALDATA (IdPatient, IdAdmin) 
                        VALUES (?,?)
                    """,(user_id, ID))

                self.conn.commit()
                self.add_window.destroy()
                self.popola_utenti()
            except Exception as e:
                print(f"Error: {e}")

        save_btn = ctk.CTkButton(self.add_window, text="Add User", command=save_new_user, width=200, height=40)
        save_btn.pack(pady=20)

    def create_input_field(self, label, placeholder, is_password=False):
        ctk.CTkLabel(self.add_window, text=label, font=FONTS["testo_bold"]).pack(padx=40, anchor="w")
        entry = ctk.CTkEntry(self.add_window, width=320, placeholder_text=placeholder, show="*" if is_password else "")
        entry.pack(pady=(0, 10))
        return entry

    def toggle_patient_fields(self, choice):
        """Mostra o nasconde i campi appuntamento in base al ruolo scelto"""
        if choice == "Patient":
            self.patient_extra_frame.pack(fill="x", padx=40, before=self.add_window.children[list(self.add_window.children)[-1]])
        else:
            self.patient_extra_frame.pack_forget()

    def profile(self, ID):
        try:
            self.cursor.execute("""
                SELECT Name, Surname, Username, Address, PhoneNumber, Email
                FROM USER 
                WHERE ID = ?
            """, (ID,))
            admin_data = self.cursor.fetchone()
        except Exception as e:
            print(f"Errore recupero profilo: {e}")
            return

        if not admin_data:
            print("Profilo Admin non trovato")
            return

        # Unpacking dei dati
        name, surname, user, addr, phone, mail = admin_data

        # 2. Setup Finestra
        self.profile_window = ctk.CTkToplevel(self)
        self.profile_window.geometry("500x700")
        self.profile_window.configure(fg_color=COLORS["sfondo_grigino"])
        self.profile_window.title("Admin Profile")
        self.profile_window.grab_set()

        title = ctk.CTkLabel(self.profile_window, text="Your Profile", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.pack(pady=(20, 20))

        # Dizionario per contenere le Entry e recuperarle dopo
        self.profile_entries = {}

        # Lista dei campi da creare
        fields = [
            ("Name", name),
            ("Surname", surname),
            ("Username", user),
            ("Address", addr),
            ("PhoneNumber", phone),
            ("Email", mail),
        ]

        # Creazione dinamica dei campi
        for label_text, value in fields:
            label = ctk.CTkLabel(self.profile_window, text=f"{label_text}:", font=FONTS["testo_bold"])
            label.pack(padx=50, anchor="w")
            
            entry = ctk.CTkEntry(self.profile_window, width=350)
            entry.insert(0, str(value) if value else "")
            entry.pack(pady=(0, 10))
            
            self.profile_entries[label_text] = entry

        # 3. Logica di aggiornamento
        def update_profile():
            try:
                # Recuperiamo i nuovi valori dalle Entry
                updated_data = {k: v.get() for k, v in self.profile_entries.items()}
                
                self.cursor.execute("""
                    UPDATE USER SET 
                        Name = ?, Surname = ?, Username = ?, 
                        Address = ?, PhoneNumber = ?, Email = ?
                    WHERE ID = ?
                """, (
                    updated_data["Name"], updated_data["Surname"], updated_data["Username"],
                    updated_data["Address"], updated_data["PhoneNumber"],
                    updated_data["Email"], ID
                ))
                
                self.conn.commit()
                print("Profilo aggiornato con successo!")
                self.profile_window.destroy()
                
            except Exception as e:
                print(f"Errore durante l'aggiornamento: {e}")

        # Tasto per salvare le modifiche
        update_btn = ctk.CTkButton(
            self.profile_window, 
            text="Update Profile", 
            fg_color=COLORS["blu_acceso"],
            width=200, 
            height=40,
            command=update_profile
        )
        update_btn.pack(pady=30)
    
    def add_wearable(self):
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.geometry("500x250") 
        self.add_window.configure(fg_color=COLORS["sfondo_grigino"])
        self.add_window.title("New Wearable")
        self.add_window.grab_set()

        title = ctk.CTkLabel(self.add_window, text="Add New Wearable", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.pack(pady=(20, 10))

        # --- CAMPI BASE ---
        entry_id = self.create_input_field("Wearable Id:", "Enter Id...")

        # 1. Recupero ID, Nome e Cognome
        self.cursor.execute("SELECT IdWearable FROM WEARABLE_DEVICE ")
        results = self.cursor.fetchall()

        # --- LOGICA DI SALVATAGGIO ---
        def save_new_wearable():
            
            # 1. Inserimento Utente
            self.cursor.execute("""
                INSERT INTO WEARABLE_DEVICE (IdWearable) 
                VALUES (?)
            """, (entry_id.get(),))

            self.conn.commit()
            self.add_window.destroy()
            self.wearables()      
        
        save_btn = ctk.CTkButton(self.add_window, text="Add Wearable", command=save_new_wearable, width=200, height=40)
        save_btn.pack(pady=20)
    
    def associa(self, w_id):
        self.assoc_window = ctk.CTkToplevel(self)
        self.assoc_window.geometry("500x300") 
        self.assoc_window.configure(fg_color=COLORS["sfondo_grigino"])
        self.assoc_window.title("Associa Wearable")
        self.assoc_window.grab_set()

        title = ctk.CTkLabel(self.assoc_window, text="Associate New Wearable to Patient", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.pack(pady=(20, 10))

        # --- CAMPI DI INPUT ---
        ctk.CTkLabel(self.assoc_window, text=f"Wearable ID = {w_id}", font=FONTS["testo_bold"]).pack(padx=40, pady=40, anchor="w")

        # 1. Creiamo un frame contenitore per la riga del Patient ID
        row_patient = ctk.CTkFrame(self.assoc_window, fg_color="transparent")
        row_patient.pack(fill="x", padx=40, pady=(0, 30))

        # 2. Mettiamo la Label a sinistra dentro il frame
        lbl_patient = ctk.CTkLabel(row_patient, text="Patient ID:", font=FONTS["testo_bold"])
        lbl_patient.pack(side="left")

        # 3. Mettiamo l'Entry a sinistra (quindi accanto alla label) con un po' di spazio
        entry_patient = ctk.CTkEntry(row_patient, width=60, placeholder_text="e.g. 12")
        entry_patient.pack(side="left", padx=10)

        # 2. LOGICA DI ASSOCIAZIONE
        def confirm_association():
            p_id = entry_patient.get().strip()

            if not w_id or not p_id:
                print("Error: Both IDs are required")
                return

            try:
                # Verifica preliminare: il paziente esiste ed è un Patient?
                self.cursor.execute("SELECT Name FROM USER WHERE Id = ? AND UserType = 'Patient'", (p_id,))
                patient_exists = self.cursor.fetchone()

                if not patient_exists:
                    print(f"Error: Patient ID {p_id} not found or not a patient")
                    return
                
                self.cursor.execute("""
                    UPDATE PATIENT_CLINICALDATA SET IdWearable = ? WHERE IdPatient = ?""", (w_id, p_id))
                
                #"""self.cursor.execute("""
                    #INSERT INTO PATIENT_CLINICALDATA (IdWearable, IdAdmin) 
                    #VALUES (?,?)
                    #""", (entry_id.get(), ID)) """

                self.conn.commit()
                print(f"Successfully associated Wearable {w_id} to Patient {p_id}")
                
                self.assoc_window.destroy()
                # Refresh wearables
                if hasattr(self, 'wearables'):
                    self.wearables()
                
            except Exception as e:
                # Gestione errore se l'ID wearable è già esistente (Primary Key violation)
                print(f"Database Error: {e}")

        # --- TASTO ASSOCIA  ---
        assoc_btn = ctk.CTkButton(
            self.assoc_window, 
            text="Confirm Association", 
            fg_color="green", 
            hover_color="#006400", # Il verde scuro che abbiamo scelto prima
            width=200, 
            height=40,
            command=confirm_association
        )
        assoc_btn.pack(pady=10)

    def edit_w(self, user_id, w_id):
                # 1. Recuperiamo i dati attuali dal DB
        self.cursor.execute("SELECT Name, Surname FROM USER WHERE Id = ?", (user_id,))
        user_data = self.cursor.fetchone()
        

        if not user_data:
            print("Utente non trovato")
            return

        current_name, current_surname = user_data

        self.edit_window = ctk.CTkToplevel(self)
        self.edit_window.geometry("450x400")
        self.edit_window.configure(fg_color=COLORS["sfondo_grigino"])
        self.edit_window.title(f"Edit User: ID {user_id}")
        self.edit_window.grab_set() # Blocca la finestra principale

        title = ctk.CTkLabel(self.edit_window, text="Edit Details", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.pack(pady=(20, 20))

        # -- CAMPI DI INPUT --
        # Nome
        ctk.CTkLabel(self.edit_window, text="Name:", font=FONTS["testo_bold"]).pack(padx=30, anchor="w")
        entry_name = ctk.CTkEntry(self.edit_window, width=300)
        entry_name.insert(0, current_name) # Inserisce il nome attuale
        entry_name.pack(pady=(0, 15))

        # Cognome
        ctk.CTkLabel(self.edit_window, text="Surname:", font=FONTS["testo_bold"]).pack(padx=30, anchor="w")
        entry_surname = ctk.CTkEntry(self.edit_window, width=300)
        entry_surname.insert(0, current_surname) # Inserisce il cognome attuale
        entry_surname.pack(pady=(0, 15))

        # Username
        ctk.CTkLabel(self.edit_window, text=f"ID Patient: {user_id}", font=FONTS["testo_bold"]).pack(padx=30, anchor="w")

        ctk.CTkLabel(self.edit_window,  text="ID Wearable:", font=FONTS["testo_bold"]).pack(padx=30, anchor="w")
        entry_w_id = ctk.CTkEntry(self.edit_window, width=300)
        entry_w_id.insert(0, w_id) 
        entry_w_id.pack(pady=(0, 20))

        def save_changes():
            new_w_id = entry_w_id.get().strip()
            
            try:
                # 1. CONTROLLO PREVENTIVO: Chi ha questo wearable?
                self.cursor.execute("""
                    SELECT U.Name, U.Surname 
                    FROM USER U
                    JOIN PATIENT_CLINICALDATA P ON U.Id = P.IdPatient
                    WHERE P.IdWearable = ? AND P.IdPatient != ?
                """, (new_w_id, user_id))
                
                already_assigned = self.cursor.fetchone()

                if already_assigned:
                    # Se troviamo qualcuno, mostriamo un messaggio specifico
                    nome_p, cognome_p = already_assigned
                    messagebox.showwarning("Warning", 
                        f"Wearable {new_w_id} is already assigned to:\n{nome_p} {cognome_p}.\n\n"
                        "Please choose another device.")
                    return # Interrompiamo qui, non salviamo nulla
                

                self.cursor.execute("UPDATE PATIENT_CLINICALDATA SET IdWearable = ? WHERE IdPatient = ?", (new_w_id, user_id))
                
                self.conn.commit()
                self.edit_window.destroy()

                messagebox.showinfo("Success", "Updated successfully!")
                self.popola_utenti()
                self.wearables()

            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Error", f"An error occurred: {e}")

        # --- BOTTONI ---
        btn_frame = ctk.CTkFrame(self.edit_window, fg_color="transparent")
        btn_frame.pack(pady=20)

        save_btn = ctk.CTkButton(btn_frame, text="Save Changes", fg_color="green", hover_color="#1E5631",
                                text_color=COLORS["bianco_puro"], command=save_changes)
        save_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", fg_color=COLORS["bianco_puro"], 
                                text_color=COLORS["testo_scuro"], command=self.edit_window.destroy)
        cancel_btn.pack(side="left", padx=10)

    def delete_w(self, w_id):
        self.delete_window = ctk.CTkToplevel(self)
        self.delete_window.geometry("400x200")
        self.delete_window.configure(fg_color=COLORS["bottone_grigio"])
        self.delete_window.title("Confirm")
        
        self.delete_window.grab_set()

        title = ctk.CTkLabel(self.delete_window, text="Delete Wearable", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        start_date = ctk.CTkLabel(self.delete_window, text=f"Are you sure to delete this wearable? (ID={w_id})", 
                                font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        start_date.place(x=30, y=80, anchor="w")

        def confirm_yes():
            try:
                query = "DELETE FROM WEARABLE_DEVICE WHERE IdWearable = ?"
                self.cursor.execute(query, (w_id,))
                self.conn.commit()
                
                self.delete_window.destroy()

                self.wearables()
                
                print(f"Wearable {w_id} eliminato con successo.")
            except Exception as e:
                print(f"Errore durante la cancellazione: {e}")

        yes = ctk.CTkButton(self.delete_window, width=100, text='Yes',
                            fg_color="red", hover_color="#8B0000", text_color="white",
                            command=confirm_yes)
        yes.place(x=30, y=120)

        no = ctk.CTkButton(self.delete_window, width=100, text='No',
                        fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], 
                        command=self.delete_window.destroy)
        no.place(x=200, y=120)

if __name__ == "__main__":
    # Simula quello che succederebbe dopo il login
    user_test = 2 
    app = AdminApp(user_test) # Passo la stringa
    app.mainloop()


















""" def view(self, id_req):
        # 1. Recupero del messaggio dal database
        try:
            self.cursor.execute("SELECT Message FROM APPOINTMENTS WHERE Id = ?", (id_req,))
            result = self.cursor.fetchone()
            messaggio_utente = result[0] if result and result[0] else "Nessun testo presente nel report."
        except Exception as e:
            print(f"Errore recupero messaggio: {e}")
            return

        # 2. Setup Finestra
        self.view_window = ctk.CTkToplevel(self)
        self.view_window.geometry("500x650") # Più alta per ospitare due aree di testo
        self.view_window.configure(fg_color=COLORS["bianco_puro"])
        self.view_window.title("View & Reply to Request")
        self.view_window.grab_set()

        # Titolo
        title = ctk.CTkLabel(self.view_window, text="User Request", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.pack(pady=(20, 10), padx=30, anchor="w")

        # --- AREA VISUALIZZAZIONE MESSAGGIO (Sola lettura) ---
        label_req = ctk.CTkLabel(self.view_window, text="Received Message:", font=FONTS["testo_bold"])
        label_req.pack(padx=30, anchor="w")
        
        display_text = ctk.CTkTextbox(self.view_window, width=440, height=150, font=FONTS["testo_normale"])
        display_text.insert("0.0", messaggio_utente)
        display_text.configure(state="disabled") # Disabilitato per evitare modifiche al messaggio originale
        display_text.pack(pady=(5, 20), padx=30)

        # --- AREA RISPOSTA (Scrivibile) ---
        label_reply = ctk.CTkLabel(self.view_window, text="Your Reply:", font=FONTS["testo_bold"])
        label_reply.pack(padx=30, anchor="w")
        
        reply_text = ctk.CTkTextbox(self.view_window, width=440, height=150, font=FONTS["testo_normale"])
        reply_text.pack(pady=(5, 20), padx=30)

        # 3. Logica di Invio Risposta
        def send_reply():
            risposta = reply_text.get("0.0", "end").strip() # Prende tutto il testo inserito
            
            if not risposta:
                print("La risposta è vuota!")
                return

            try:
                # Assumo che esista una colonna 'AdminReply' o simile nella tabella APPOINTMENTS
                # Se non esiste, dovrai crearla nel DB o usare una tabella di messaggistica dedicata
                self.cursor.execute(
                
                #UPDATE APPOINTMENTS
                #SET AdminReply = ? 
                #WHERE Id = ?
                , (risposta, id_req))
                self.conn.commit()
                print("Risposta inviata con successo!")
                self.view_window.destroy()
                    
            except Exception as e:
                    print(f"Errore durante l'invio della risposta: {e}")
            # Tasto Invio
            send_btn = ctk.CTkButton(
                self.view_window, 
                text="Send Reply", 
                fg_color=COLORS["blu_acceso"],
                width=200, 
                height=40,
                command=send_reply
            )
            send_btn.pack(pady=20) """