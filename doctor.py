import customtkinter as ctk
import sqlite3 as sql

from datetime import datetime

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
    "testo_normale": ("Montserrat", 16),
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
        self.topbar.place(relx=0, rely=0, relheight=0.15, relwidth=1)

        self.main = ctk.CTkFrame(self.root, fg_color=COLORS["sfondo_grigino"])
        self.main.place(relx=0, rely=0.15, relheight=0.85, relwidth=1)

        self.welcome()
        self.nav_buttons()

    def clear_content_frame(self):
        for widget in self.main.winfo_children():
            widget.destroy()

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
        if tab == "Appointments":
            self.apppointments()
        elif tab == "Patients":
            self.patients()

    def update_buttons(self, current_tab):
        for tab, btn in self.buttons_dict.items():
            if tab == current_tab:
                btn.configure(fg_color=COLORS["blu_acceso"], text_color=COLORS["bianco_puro"])
            else:
                btn.configure(fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"])

    def risk_code(self, code):
        
        risk_colors = {
                1: "#2ecc71",
                2: "#f1c40f",
                3: "#e67e22",
                4: "#e74c3c" 
        }

        return risk_colors[code]

    # ==========================
    # ------ APPOINTMENTS ------
    # ==========================
    
    def apppointments(self):
        self.clear_content_frame()
        
        self.manage = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.manage.place(relx=0.03, rely=0.03, relheight=0.20, relwidth=0.94)

        self.incoming = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.incoming.place(relx=0.03, rely=0.26, relheight=0.71, relwidth=0.94)

        self.show_incoming()
        self.new_appointment()

    def get_appointments(self):
        
        query = """
                SELECT app.IDAppointment, app.Date, app.Time, user.Name, user.Surname, pat.RiskCode, app.Report
                FROM Appointment AS app
                JOIN Patient_ClinicalData AS pat ON app.IDPatient = pat.IDPatient
                JOIN User ON app.IDPatient = user.ID
                ORDER BY Date, Time ASC"""
               # WHERE app.IDDoctor = ?"""         

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def show_incoming(self):

        self.text = ctk.CTkLabel(self.incoming, text="Incoming Appointments", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
        
        self.scrollable = ctk.CTkScrollableFrame(self.incoming, fg_color="transparent")
        self.scrollable.place(x=0, rely=0.1, relheight=0.85, relwidth=1)
        
        appointments = self.get_appointments()
        for app in appointments:
            id, date, time, name, surname, code, report = app
            row = ctk.CTkFrame(self.scrollable, fg_color="transparent")
            row.pack(fill='x',padx=20, pady=0)

            label_date = ctk.CTkLabel(row, text=f"{date} - {time}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=0, padx=15, pady=10, sticky="w")

            dot_code = ctk.CTkFrame(row, width=12, height=12, corner_radius=6, fg_color=self.risk_code(code))
            dot_code.grid(row=0,column=1, padx=15, pady=10, sticky="ew")

            label_name = ctk.CTkLabel(row, text=name, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_name.grid(row=0,column=2, padx=15, pady=10, sticky="w")

            label_surname = ctk.CTkLabel(row, text=surname, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_surname.grid(row=0,column=3, padx=15, pady=10, sticky="w")

            label_report = ctk.CTkLabel(row, text=report, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_report.grid(row=0,column=4, padx=15, pady=10, sticky="w")

            edit = ctk.CTkButton(row, text="Edit", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(1),
                                 command = lambda app=app : self.edit_appointment(app))
            edit.grid(row=0, column=5, padx=(15,5),pady=10,sticky="e")

            delete = ctk.CTkButton(row, text="Delete", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(4),
                                command = lambda app=app : self.delete_appointment(app))
            delete.grid(row=0, column=6, padx=(5,15),pady=10,sticky="e")

            row.grid_columnconfigure(4, weight=1)

    def edit_appointment(self, app):
        id, date, time, name, surname, code, report = app

        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x500")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Edit Appointment", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(code))
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Name", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {name}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_name.place(x=30, y=95)

        lbl_surname = ctk.CTkLabel(self.edit_window, text="Surname",font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_surname.place(x=30, y=150, anchor="w")
        entry_surname = ctk.CTkLabel(self.edit_window,  corner_radius=5,text=f" {surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_surname.place(x=30, y=165)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=220, anchor="w")
        entry_data = ctk.CTkEntry(self.edit_window, width=340,font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        entry_data.insert(0, date)
        entry_data.place(x=30, y=235)

        lbl_time = ctk.CTkLabel(self.edit_window, text="Time", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_time.place(x=30, y=290, anchor="w")
        entry_time = ctk.CTkEntry(self.edit_window, width=340,font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        entry_time.insert(0, time)
        entry_time.place(x=30, y=305)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Notes", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_notes.place(x=30, y=360, anchor="w")
        entry_notes = ctk.CTkEntry(self.edit_window, width=340,font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        entry_notes.insert(0, report)
        entry_notes.place(x=30, y=375)

        self.output_edit = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_edit.place(x=50, y=415)

        save = ctk.CTkButton(self.edit_window, text="Edit", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(1),
                             command=lambda: self.save_appointment_changes(id, entry_data.get(), entry_time.get(), entry_notes.get()))
        save.place(x=150, y = 450)
    
    def delete_appointment(self, app):
        def delete(id):
            query = """DELETE FROM Appointment WHERE IDAppointment = ?"""
            self.cursor.execute(query, (id,))
            self.conn.commit()
            # -- SEND NOTIFICATIONS ---

            self.output_edit.configure(text=f"Appointment #{id} deleted", text_color=self.risk_code(4))

            for widget in self.scrollable.winfo_children():
                widget.destroy()

            self.show_incoming()

        id, date, time, name, surname, code, report = app

        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x500")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Delete Appointment", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(code))
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Name", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {name}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_name.place(x=30, y=95)

        lbl_surname = ctk.CTkLabel(self.edit_window, text="Surname",font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_surname.place(x=30, y=150, anchor="w")
        entry_surname = ctk.CTkLabel(self.edit_window,  corner_radius=5,text=f" {surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_surname.place(x=30, y=165)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=220, anchor="w")
        entry_data = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {date}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_data.place(x=30, y=235)

        lbl_time = ctk.CTkLabel(self.edit_window, text="Time", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_time.place(x=30, y=290, anchor="w")
        entry_time = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {time}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_time.place(x=30, y=305)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Notes", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_notes.place(x=30, y=360, anchor="w")
        entry_notes = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {report}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_notes.place(x=30, y=375)

        self.output_edit = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_edit.place(x=50, y=415)

        save = ctk.CTkButton(self.edit_window, text="Delete", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(4),
                             command=lambda id=id : delete(id))
        save.place(x=150, y = 450)

    def save_appointment_changes(self, id, date, time, report):
        check_query = """SELECT IDAppointment FROM Appointment 
                    WHERE date = ? AND time = ? AND IDAppointment != ?"""
        
        self.cursor.execute(check_query, (date, time, id))
        conflict = self.cursor.fetchall()

        if conflict:
            self.output_edit.configure(text="Time slot already booked", text_color=self.risk_code(4))
        else:
            query = """UPDATE Appointment 
                    SET date = ?, time = ?, report = ? 
                    WHERE IDAppointment = ?"""

            self.cursor.execute(query, (date, time, report,id))
            self.conn.commit()
            # -- SEND NOTIFICATIONS ---


            self.output_edit.configure(text=f"Appointment #{id} updated", text_color=self.risk_code(1))

            for widget in self.scrollable.winfo_children():
                widget.destroy()

            self.show_incoming()

    def new_appointment(self):
        self.text = ctk.CTkLabel(self.manage, text="Add Appointment", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
            
        row = ctk.CTkFrame(self.manage, fg_color="transparent", corner_radius=20)
        row.place(x=20, y=70, relwidth=1)

        entry_date = ctk.CTkEntry(row, corner_radius=5, placeholder_text="YYYY-MM-DD", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"])
        entry_date.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        entry_time = ctk.CTkEntry(row, corner_radius=5, placeholder_text="HH:MM", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"])
        entry_time.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        
        entry_name = ctk.CTkEntry(row, corner_radius=5, placeholder_text="Name", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"])
        entry_name.grid(row=0, column=2, padx=15, pady=10, sticky="w")
        
        entry_surname = ctk.CTkEntry(row, corner_radius=5, placeholder_text="Surname", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"])
        entry_surname.grid(row=0, column=3, padx=15, pady=10, sticky="w")
        
        entry_report = ctk.CTkEntry(row, corner_radius=5, placeholder_text="Notes", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"],width=400)
        entry_report.grid(row=0, column=4, padx=15, pady=10, sticky="w")

        self.output_add = ctk.CTkLabel(row,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=200)
        self.output_add.grid(row=0, column=5, padx=15, pady=10, sticky="w")

        save = ctk.CTkButton(row, text="Save", width=80, corner_radius=20, fg_color=COLORS["bottone_grigino"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(1),
                             command=lambda : self.add_appointment(entry_date.get(), entry_time.get(), entry_name.get(),entry_surname.get(),entry_report.get()))
        save.grid(row=0, column=6, padx=15, pady=10, sticky="e")

        row.grid_columnconfigure(4, weigth=1)

    def add_appointment(self, date, time, name, surname, report):
        if not date or not time or not name or not surname:
            self.output_add.configure(text="Missing Fields", text_color=self.risk_code(4))
            return

        check_query = """SELECT ID FROM User 
                    WHERE UserType = ? AND name = ? AND surname = ?"""
        self.cursor.execute(check_query, ("Patient",name, surname))
        patient = self.cursor.fetchall()

        if not patient:  # Se fetchone() restituisce None, il paziente non esiste
            self.output_add.configure(text="No Patient found", text_color=self.risk_code(4))
            return

        id_pat = patient[0][0]

        check_query = """SELECT IDAppointment FROM Appointment 
                        WHERE date = ? AND time = ?"""
        self.cursor.execute(check_query, (date, time))
        slot = self.cursor.fetchall()

        if slot:
            self.output_add.configure(text="Time slot already booked", text_color=self.risk_code(4))
            return

        query = """INSERT INTO Appointment (date, time, report, IDPatient, IDDoctor) 
                VALUES (?, ?, ?, ?, ?)"""
    
        self.cursor.execute(query, (date, time, report, id_pat, self.ID[0]))
        self.conn.commit()
        # -- SEND NOTIFICATIONS ---
        
        self.output_add.configure(text="New Appointment added", text_color=self.risk_code(1))
        
        for widget in self.scrollable.winfo_children():
            widget.destroy()
            
        self.show_incoming()

    def add_appointment_popup(self, name, surname, code):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x500")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Add Appointment", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(code))
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Name", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {name}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_name.place(x=30, y=95)

        lbl_surname = ctk.CTkLabel(self.edit_window, text="Surname",font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_surname.place(x=30, y=150, anchor="w")
        entry_surname = ctk.CTkLabel(self.edit_window,  corner_radius=5,text=f" {surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_surname.place(x=30, y=165)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=220, anchor="w")
        entry_data = ctk.CTkEntry(self.edit_window, width=340,font=FONTS["testo_normale"], placeholder_text="YYYY-MM-DD",text_color=COLORS["testo_scuro"])
        entry_data.place(x=30, y=235)

        lbl_time = ctk.CTkLabel(self.edit_window, text="Time", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_time.place(x=30, y=290, anchor="w")
        entry_time = ctk.CTkEntry(self.edit_window, width=340,font=FONTS["testo_normale"], placeholder_text="HH-MM", text_color=COLORS["testo_scuro"])
        entry_time.place(x=30, y=305)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Notes", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_notes.place(x=30, y=360, anchor="w")
        entry_notes = ctk.CTkEntry(self.edit_window, width=340,placeholder_text="Additional notes",font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        entry_notes.place(x=30, y=375)

        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=415)

        save = ctk.CTkButton(self.edit_window, text="Add", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(1),
                             command=lambda: self.add_appointment(entry_data.get(), entry_time.get(), name, surname, entry_notes.get()))
        
        save.place(x=150, y = 450)
    
    # ===========================
    # --------- PATIENT ---------
    # ===========================

    def patients(self):
        self.clear_content_frame()

        self.patient_list = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.patient_list.place(relx=0.03, rely=0.03, relheight=0.94, relwidth=0.94)

        self.text = ctk.CTkLabel(self.patient_list, text="Your Patients", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
        
        self.scrollable = ctk.CTkScrollableFrame(self.patient_list, fg_color="transparent")
        self.scrollable.place(x=0, rely=0.1, relheight=0.85, relwidth=1)
        
        patients = self.get_patients()
        for pat in patients:
            id, name, surname, code, appdate, age = pat
            
            row = ctk.CTkFrame(self.scrollable, fg_color="transparent")
            row.pack(fill='x',padx=20, pady=0)

            label_name = ctk.CTkLabel(row, text=name, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_name.grid(row=0,column=1, padx=15, pady=10, sticky="w")

            label_surname = ctk.CTkLabel(row, text=surname, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_surname.grid(row=0,column=2, padx=15, pady=10, sticky="w")

            label_age = ctk.CTkLabel(row, text=f"Age: {age}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_age.grid(row=0,column=3, padx=15, pady=10, sticky="w")

            dot_code = ctk.CTkFrame(row, width=12, height=12, corner_radius=6, fg_color=self.risk_code(code))
            dot_code.grid(row=0,column=0, padx=15, pady=10, sticky="ew")

            label_date = ctk.CTkLabel(row, text=f"Next Appointment: {appdate}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=4, padx=15, pady=10, sticky="w")

            edit = ctk.CTkButton(row, text="Open", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(1),
                                 command = lambda id=id, n=name, s=surname, c=code: self.show_patient(id, n, s, c))
            edit.grid(row=0, column=5, padx=(15,5),pady=10,sticky="e")

            row.grid_columnconfigure(4, weight=1)

    def get_patients(self):
        query = """SELECT user.ID, user.Name, user.Surname, pat.RiskCode, app.Date,
                (strftime('%Y', 'now') - strftime('%Y', user.birthdate)) - 
                (strftime('%m-%d', 'now') < strftime('%m-%d', user.birthdate)) AS Age
                FROM user JOIN Patient_ClinicalData AS pat ON user.ID = pat.IDPatient
                LEFT JOIN Appointment AS app ON app.IDPatient = user.ID
                ORDER BY app.Date ASC"""
                # JOIN Doctor AS doc ON doc.IDPatient = pat.IDPatient
                # WHERE doc.IDDoctor = ?

        self.cursor.execute(query)
        patients = self.cursor.fetchall()

        return patients 
        
    def show_patient(self, id, name, surname, code):
        self.clear_content_frame()

        self.current = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.current.place(relx=0.03, rely=0.03, relheight=0.20, relwidth=0.94)

        self.vitals = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.vitals.place(relx=0.03, rely=0.26, relheight=0.71, relwidth=0.70)
        
        self.therapy = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.therapy.place(relx=0.75, rely=0.26, relheight=0.51, relwidth=0.22)
        
        self.calendar = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.calendar.place(relx=0.75, rely=0.81, relheight=0.16, relwidth=0.22)

        self.pat_appointment(id, name, surname, code)
        self.pat_therapy(id, code)
        self.pat_vitals(id)

    def pat_appointment(self, id, name, surname, code):
        
        self.text = ctk.CTkLabel(self.calendar, text="Next Appointment", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)

        query = """
                SELECT app.IDAppointment, app.Date, app.Time, user.Name, user.Surname, pat.RiskCode, app.Report
                FROM Appointment AS app
                JOIN Patient_ClinicalData AS pat ON app.IDPatient = pat.IDPatient
                JOIN User ON app.IDPatient = user.ID
                WHERE app.IDPatient = ? LIMIT 1"""
                # AND app.IDDoctor = ?
                # #AND date > DATE('now')
        
        self.cursor.execute(query, (id,))
        app = self.cursor.fetchall()

        if app:
            app = app[0]
            row = ctk.CTkFrame(self.calendar, fg_color="transparent", corner_radius=20)
            row.place(x=20, y=70, relwidth=0.95)

            label_date = ctk.CTkLabel(row, width=180, anchor="w", text=f"{app[1]} - {app[2]}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")

            edit = ctk.CTkButton(row, text="Edit", width=50, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(1),
                                    command = lambda app=app : self.edit_appointment(app))
            edit.grid(row=0, column=1, padx=(0,5),pady=10,sticky="e")

            delete = ctk.CTkButton(row, text="Delete", width=50, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(4),
                                    command = lambda app=app : self.delete_appointment(app))
            delete.grid(row=0, column=2, padx=(0,15),pady=10,sticky="e")
        else: 
            row = ctk.CTkFrame(self.calendar, fg_color="transparent", corner_radius=20)
            row.place(x=20, y=70, relwidth=0.95)

            label_date = ctk.CTkLabel(row, width=250, anchor="w", text="No Appointments", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")

            add = ctk.CTkButton(row, text="Add", width=50, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(1),
                                    command = lambda : self.add_appointment_popup(name, surname, code))
            add.grid(row=0, column=1, padx=(0,15),pady=10,sticky="e")

    def pat_therapy(self, id, code):
        query = """SELECT Date, Description FROM Therapy
                WHERE IDPatient = ?
                ORDER BY Date DESC LIMIT 1"""

        self.cursor.execute(query, (id,))
        current  = self.cursor.fetchall()[0]

        if current:
            date = current[0]
            description = current[1]
        else:
            date = "No Therapy"
            description = "No Therapy"
            
        self.text = ctk.CTkLabel(self.therapy, text="Current Therapy", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.therapy, width=24, height=24, corner_radius=12, fg_color=self.risk_code(code))
        dot_code.place(x=300, y=30)
                     
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

        edit = ctk.CTkButton(self.therapy, text="Edit", width=50, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(1),
                                    command = lambda id=id: self.edit_therapy(id, code))
        edit.place(x=280, y=340)
        
    def edit_therapy(self, id, code):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x500")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Edit Therapy", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(code))
        dot_code.place(x=346, y=30)

        today = datetime.today().strftime("%Y-%m-%d")       
        lbl_date = ctk.CTkLabel(self.edit_window, text="Date", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=80)
        entry_data = ctk.CTkLabel(self.edit_window, anchor="w",width=340,font=FONTS["testo_normale"], text=today,text_color=COLORS["testo_scuro"])
        entry_data.place(x=30, y=110)

        entry_textbox = ctk.CTkTextbox(self.edit_window, width=340, height=220, corner_radius=5, 
                                       font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], wrap="word")
        entry_textbox.place(x=30, y=155)
        
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=415)

        save = ctk.CTkButton(self.edit_window, text="Add", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(1),
                             command=lambda: self.save_therapy(id, entry_data.cget("text"),entry_textbox.get("1.0", "end-1c")))
        save.place(x=150, y = 450)
    
    def save_therapy(self, id, date, description):
        description = description.strip()
    
        if not description:
            self.output_add.configure(text="Therapy description cannot be empty", text_color=self.risk_code(4))
            return

        query = """
        INSERT INTO Therapy (Date, Description, IDDoctor, IDPatient) 
        VALUES (?, ?, ?, ?)"""
    
        self.cursor.execute(query, (date, description, self.ID[0], id))
        self.conn.commit()
        
        self.output_add.configure(text="New Therapy added!", text_color=self.risk_code(1))







ID = (11,)
DoctorApp(ID)