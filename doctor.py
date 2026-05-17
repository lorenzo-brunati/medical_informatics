import customtkinter as ctk
import sqlite3 as sql

from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog

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

UNITS = {
    "Systolic BP": "mmHg",       # Millimetri di mercurio
    "Diastolic BP": "mmHg",      # Millimetri di mercurio
    "Heart Rate": "bpm",         # Battiti al minuto
    "Step Count": "steps",       # Conteggio passi
    "Sleep Hours": "hours",        # Ore di sonno
    "SPO2": "%",                 # Percentuale di ossigeno nel sangue
    "VO2max": "mL/kg/min"        # Millilitri di ossigeno per chilogrammo al minuto
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

        self.surname_label = ctk.CTkLabel(self.topbar, text=f"Hello Mr. {surname}", font=FONTS["titolo"], text_color=COLORS["testo_chiaro"])
        self.surname_label.place(x=50, y=30)

        self.welcome_label = ctk.CTkLabel(self.topbar, text="Welcome Back!", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.welcome_label.place(x=50, y=60)

    def nav_buttons(self):

        self.container = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.container.place(relx=0.4, rely=0, relheight=1, relwidth=0.5)

        self.buttons_dict = {}
        buttons = ["Dashboard", "Patients", "Appointments"]
        for b in buttons:
            btn = ctk.CTkButton(self.container, text=b, text_color=COLORS["testo_scuro"], font=FONTS["testo_normale"],
                                command = lambda b=b: self.switch_tab(b), width=150, height=40, corner_radius=20,
                                fg_color=COLORS["bottone_grigio"], border_color=COLORS["bordi"], hover_color=COLORS["blu_acceso"])
            btn.pack(side="left", padx=10)
            self.buttons_dict[b] = btn
        
        self.update_buttons("Dashboard")

    def switch_tab(self, tab):
        self.tab = tab
        self.update_buttons(tab)
        if tab == "Appointments":
            self.appointments()
        elif tab == "Patients":
            self.patients()
        elif tab == "Dashboard":
            self.dashboard()

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
    
    def appointments(self):
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

            if self.tab == "Appointments":
                for widget in self.scrollable.winfo_children():
                    widget.destroy()
                self.appointments()

            elif self.tab == "Patients":
                for widget in self.calendar.winfo_children():
                    widget.destroy()
                self.pat_appointment()

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

            if self.tab == "Appointments":
                for widget in self.scrollable.winfo_children():
                    widget.destroy()
                self.appointments()

            elif self.tab == "Patients":
                for widget in self.calendar.winfo_children():
                    widget.destroy()
                self.pat_appointment()

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

        save = ctk.CTkButton(row, text="Save", width=80, corner_radius=20, fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(1),
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

        if not patient:
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
        
        if self.tab == "Appointments":
            for widget in self.scrollable.winfo_children():
                widget.destroy()
            self.show_incoming()
        
        elif self.tab == "Patients":
            for widget in self.calendar.winfo_children():
                widget.destroy()
            self.pat_appointment()

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
                                 command = lambda id=id, n=name, s=surname, a=age, c=code: self.show_patient(id, n, s, a, c))
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
        
    def show_patient(self, id, name, surname, age, code):
        
        self.IDPat = id
        self.name = name
        self.surname = surname
        self.age = age
        self.code = code

        self.clear_content_frame()

        self.current = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.current.place(relx=0.03, rely=0.03, relheight=0.20, relwidth=0.94)

        self.vitals = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.vitals.place(relx=0.03, rely=0.26, relheight=0.71, relwidth=0.70)
        
        self.therapy = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.therapy.place(relx=0.75, rely=0.26, relheight=0.51, relwidth=0.22)
        
        self.calendar = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.calendar.place(relx=0.75, rely=0.81, relheight=0.16, relwidth=0.22)

        self.pat_appointment()
        self.pat_therapy()
        self.pat_vitals()
        self.pat_current()

    def pat_appointment(self):
        
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
        
        self.cursor.execute(query, (self.IDPat,))
        app = self.cursor.fetchall()

        if app:
            app = app[0]
            row = ctk.CTkFrame(self.calendar, fg_color="transparent", corner_radius=20)
            row.place(x=20, y=70, relwidth=0.85)

            label_date = ctk.CTkLabel(row, width=160, anchor="w", text=f"{app[1]} - {app[2]}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
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
            row.place(x=20, y=70, relwidth=0.85)

            label_date = ctk.CTkLabel(row, width=160, anchor="w", text="No Appointments", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")

            add = ctk.CTkButton(row, text="Add", width=50, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(1),
                                    command = lambda : self.add_appointment_popup(self.name, self.surname, self.code))
            add.grid(row=0, column=1, padx=(0,15),pady=10,sticky="e")

    def pat_therapy(self):
    
        query = """SELECT Date, Description FROM Therapy
                WHERE IDPatient = ?
                ORDER BY Date DESC LIMIT 1"""

        self.cursor.execute(query, (self.IDPat,))
        current  = self.cursor.fetchall()[0]

        if current:
            date = current[0]
            description = current[1]
        else:
            date = "No Therapy"
            description = "No Therapy"
            
        self.text = ctk.CTkLabel(self.therapy, text="Current Therapy", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.therapy, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
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
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                    command = lambda : self.edit_therapy())
        edit.place(x=270, y=340)
        
    def edit_therapy(self):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x500")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Edit Therapy", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
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
                             command=lambda: self.save_therapy(entry_data.cget("text"),entry_textbox.get("1.0", "end-1c")))
        save.place(x=150, y = 450)
    
    def save_therapy(self, date, description):
        description = description.strip()
    
        if not description:
            self.output_add.configure(text="Therapy description cannot be empty", text_color=self.risk_code(4))
            return

        query = """
        INSERT INTO Therapy (Date, Description, IDDoctor, IDPatient) 
        VALUES (?, ?, ?, ?)"""
        self.cursor.execute(query, (date, description, self.ID[0], self.IDPat))

        try:
            # Prova a cambiare self.ID[0] in self.ID se ti dà errore
            self.cursor.execute(query, (date, description, self.ID[0], self.IDPat))
            self.conn.commit()
            print("Salvataggio completato con successo!")
        except Exception as e:
            print(f"Errore fatale di SQLite: {e}")      

        self.output_add.configure(text="New Therapy added!", text_color=self.risk_code(1))
        
        for widget in self.therapy.winfo_children():
            widget.destroy()

        self.pat_therapy()

    def pat_vitals(self):
        for widget in self.vitals.winfo_children():
            widget.destroy()

        row = ctk.CTkFrame(self.vitals, fg_color="transparent", corner_radius=20)
        row.place(x=20, y=20, relwidth=0.95)

        text = ctk.CTkLabel(row, text="Vitals", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        text.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        
        ecg = ctk.CTkButton(row, text="Plot ECG", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                command = lambda : self.add_ecg())
        ecg.grid(row=0, column=2, padx=(15,5),pady=10,sticky="e")

        add = ctk.CTkButton(row, text="Add Vitals", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                command = lambda : self.add_vitals())
        add.grid(row=0, column=3, padx=(15,5),pady=10,sticky="e")

        row.grid_columnconfigure(1,weight=1)

        self.plot_area = ctk.CTkFrame(self.vitals, fg_color="transparent", corner_radius=20,height=430, width=1100)
        self.plot_area.place(x=10,y=100)

        self.output = ctk.CTkLabel(self.vitals, text = f"Select Add Vitals to plot", font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"])
        self.output.place(x=35, y=70)

        self.output_date = ctk.CTkLabel(self.vitals, text = "", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
        self.output_date.place(x=300, y=70)
        
    def pat_exams(self):
        for widget in self.vitals.winfo_children():
            widget.destroy()

        row = ctk.CTkFrame(self.vitals, fg_color="transparent", corner_radius=20)
        row.place(x=20, y=20, relwidth=0.95)

        text = ctk.CTkLabel(row, text="Past Exams", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        text.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        
        self.exams_area = ctk.CTkScrollableFrame(self.vitals, fg_color="transparent", corner_radius=20,height=430, width=1100)
        self.exams_area.place(x=10,y=70)

        exams = [(1, "2026-05-05", "Suffering from Arythmia")] # get past exams
        for ex in exams:
            id, date, text = ex
            row = ctk.CTkFrame(self.exams_area, fg_color="transparent")
            row.pack(fill='x',padx=0, pady=0)

            label_date = ctk.CTkLabel(row, text=date, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
            label_date.grid(row=0,column=0, padx=15, pady=10, sticky="w")

            label_report = ctk.CTkLabel(row, text=text, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_report.grid(row=0,column=1, padx=15, pady=10, sticky="w")

            download = ctk.CTkButton(row, text="Download Report", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                 command = lambda id=id : self.download_report(id))
            download.grid(row=0, column=2, padx=(15,50),pady=10,sticky="e")

            row.grid_columnconfigure(1, weight=1)

    def get_exams(self):
        print("Get Exams!")

    def pat_current(self):
        self.text = ctk.CTkLabel(self.current, text="Current Patient", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
            
        row = ctk.CTkFrame(self.current, fg_color="transparent", corner_radius=20)
        row.place(x=20, y=70, relwidth=0.98)

        dot_code = ctk.CTkFrame(row, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
        dot_code.grid(row=0,column=0, padx=15, pady=10, sticky="ew")

        label_name = ctk.CTkLabel(row, text=self.name, font=FONTS["titolo"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
        label_name.grid(row=0,column=1, padx=15, pady=10, sticky="w")

        label_surname = ctk.CTkLabel(row, text=self.surname, font=FONTS["titolo"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
        label_surname.grid(row=0,column=2, padx=15, pady=10, sticky="w")

        label_age = ctk.CTkLabel(row, text=f"Age: {self.age}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
        label_age.grid(row=0,column=3, padx=15, pady=10, sticky="w")

        self.output_add = ctk.CTkLabel(row,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=120)
        self.output_add.grid(row=0, column=4, padx=15, pady=10, sticky="w")

        vitals = ctk.CTkButton(row, text="Show Vitals", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                 command = lambda : self.pat_vitals())
        vitals.grid(row=0, column=5, padx=(5,5),pady=10,sticky="e")

        exams = ctk.CTkButton(row, text="Past Exams", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                command = lambda : self.pat_exams())
        exams.grid(row=0, column=6, padx=(5,5),pady=10,sticky="e")

        check_out = ctk.CTkButton(row, text="Check-out", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                 command = lambda : self.check_out())
        check_out.grid(row=0, column=7, padx=(5,5),pady=10,sticky="e")

        message = ctk.CTkButton(row, text="Message", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                command = lambda : self.message())
        message.grid(row=0, column=8, padx=(5,15),pady=10,sticky="e")

        row.grid_columnconfigure(3,weight=1)

    def add_vitals(self):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x300")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Add Vitals", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
        dot_code.place(x=346, y=30)
                     
        start_date = ctk.CTkLabel(self.edit_window, text="Start Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        start_date.place(x=30, y=80, anchor="w")
        entry_start = ctk.CTkEntry(self.edit_window, width=150,corner_radius=5, placeholder_text="YYYY-MM-DD", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"])
        entry_start.place(x=30, y=95)

        end_date = ctk.CTkLabel(self.edit_window, text="End Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        end_date.place(x=220, y=80, anchor="w")
        entry_end = ctk.CTkEntry(self.edit_window, width=150,corner_radius=5, placeholder_text="YYYY-MM-DD", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"])
        entry_end.place(x=220, y=95)
        
        vitals_list = ["Systolic BP", "Diastolic BP", "Heart Rate", "Step Count", "Sleep Hours", "SPO2", "VO2max"]
        
        vitals = ctk.CTkLabel(self.edit_window, text="Vitals", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        vitals.place(x=30, y=150, anchor="w")
        menu = ctk.CTkOptionMenu(self.edit_window, width=340, values=vitals_list[1:],fg_color=COLORS["bianco_puro"], font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], button_color=COLORS["bianco_puro"],button_hover_color=self.risk_code(self.code))
        menu.place(x=30, y=165)
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=250)

        save = ctk.CTkButton(self.edit_window, text="Add", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
                            command = lambda : self.get_vitals(entry_start.get(), entry_end.get(),menu.get()))
        save.place(x=150, y = 250)

    def get_vitals(self, start, end, vit):
        
        """query = SELECT num.Date, num.Max, num.Min, num.Average, num.StandardDeviation
                    FROM NumericalData AS num
                    JOIN Data on num.IDNumData = IData
                    WHERE data.IDPatient = ?
                    AND data.NameData = ?
                    AND num.Date BETWEEN ? AND ?
                    ORDER BY num.Date ASC
            
        self.cursor.execute(query, (self.IDPat, vit, start, end))
        records = self.cursor.fetchall()

        dates =  [row[0] for row in records]
        max = [row[1] for row in records]
        min = [row[2] for row in records]
        mean = [row[3] for row in records]
        std = [row[4] for row in records]"""

        dates = ["05-01", "05-02", "05-03", "05-04", "05-05", "05-06", "05-07", "05-08", "05-09", "05-10"]               
        max = [36.5, 36.6, 36.8, 37.5, 38.4, 38.1, 37.4, 36.9, 36.6, 36.5]

        min = [35.8, 35.9, 36.0, 36.2, 36.5, 36.4, 36.1, 35.9, 35.8, 35.7]
        mean = [36.1, 36.2, 36.4, 36.8, 37.3, 37.1, 36.6, 36.3, 36.1, 36.0]
        
        self.plot_vitals(dates, mean, min, max, vit)

    def plot_vitals(self, dates, mean, min, max, vit):
        for widget in self.plot_area.winfo_children():
            widget.destroy()
        
        self.output.destroy()
        self.output_date.destroy()
     
        fig = Figure(figsize=(8.5,4), facecolor="none") 
        
        ax = fig.add_subplot(111)       
        ax.set_facecolor("none")
        
        ax.plot(dates, mean, color=self.risk_code(self.code), linewidth=3, label="Mean")
        ax.fill_between(dates, min, max, color=self.risk_code(self.code), alpha=0.2, edgecolor='none')
        
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

        self.output = ctk.CTkLabel(self.vitals, text = f"Plotting {vit} [{UNITS[vit]}]", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output.place(x=35, y=70)

        self.output_date = ctk.CTkLabel(self.vitals, text = f"Recorded from {dates[0]} to {dates[-1]}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
        self.output_date.place(x=300, y=70)

    def add_ecg(self):
        date_list = ["none","2026-05-05"]
        
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x200")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Plot ECG", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
        dot_code.place(x=346, y=30)
                     
        start_date = ctk.CTkLabel(self.edit_window, text="Select Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        start_date.place(x=30, y=80, anchor="w")
        menu = ctk.CTkOptionMenu(self.edit_window, width=340, values=date_list[1:],fg_color=COLORS["bianco_puro"], font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], button_color=COLORS["bianco_puro"],button_hover_color=self.risk_code(self.code))
        menu.place(x=30, y=95)
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=130)

        save = ctk.CTkButton(self.edit_window, text="Plot", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
                            command = lambda : self.get_ecg(menu.get()))
        save.place(x=150, y = 150)
    
    def get_ecg(self, date):

        query = """"""

        x = [round(i * 0.01, 2) for i in range(500)]

        _single_beat = [
            0.0, 0.0, 0.0, 0.0, 0.01, 0.02, 0.04, 0.08, 0.12, 0.14,  # Onda P
            0.15, 0.14, 0.11, 0.07, 0.03, 0.01, 0.0, 0.0, -0.05, -0.15, # Discesa Q
            -0.25, -0.1, 0.2, 0.6, 1.0, 1.4, 1.3, 0.8, 0.3, -0.1,    # Picco R e discesa S
            -0.35, -0.2, -0.05, 0.0, 0.01, 0.02, 0.03, 0.04, 0.06, 0.09,
            0.13, 0.18, 0.24, 0.3, 0.34, 0.35, 0.34, 0.31, 0.26, 0.21,  # Onda T
            0.15, 0.1, 0.06, 0.04, 0.02, 0.01, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        ]
        y = _single_beat * 5

        self.plot_ecg(x,y, date)

    def plot_ecg(self, x, y, date):
        for widget in self.plot_area.winfo_children():
            widget.destroy()
     
        self.output.destroy()
        self.output_date.destroy()
        
        fig = Figure(figsize=(8.5,4), facecolor="none") 
        
        ax = fig.add_subplot(111)       
        ax.set_facecolor("none")
        
        ax.plot(x, y, color=self.risk_code(self.code), linewidth=3, label="Mean")
        
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

        self.output_date = ctk.CTkLabel(self.vitals, text = f"Recorded on {date}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
        self.output_date.place(x=300, y=70)

    # ===========================
    # -------- DASHBOARD --------
    # ===========================

    def message(self):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x520")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        date = f"{datetime.today()}"[:10]
        time = f"{datetime.today()}"[11:16]

        title = ctk.CTkLabel(self.edit_window, text="Send Message", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Send to", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {self.name} {self.surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
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
                             command=lambda: self.send_message(date, time, entry_textbox.get("1.0", "end-1c")))
        
        save.place(x=150, y = 470)

    def send_message(self, date, time, msg):
        self.output_add.configure(text="Function still to be written", text_color=self.risk_code(4))

    def check_out(self):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x420")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        date = f"{datetime.today()}"[:10]

        title = ctk.CTkLabel(self.edit_window, text="Medical Examination", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Patient", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {self.name} {self.surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_name.place(x=30, y=95)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=150, anchor="w")
        entry_data = ctk.CTkLabel(self.edit_window, width=340,font=FONTS["testo_normale"], anchor="w", text=f" {date}",text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_data.place(x=30, y=165)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Notes", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_notes.place(x=30, y=220, anchor="w")

        entry_notes = ctk.CTkEntry(self.edit_window, width=340,font=FONTS["testo_normale"], placeholder_text=f" Enter addtional notes",text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_notes.place(x=30, y=235)

        self.lbl_report = ctk.CTkLabel(self.edit_window, text="Add Report", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.lbl_report.place(x=30, y=305, anchor="w")

        add = ctk.CTkButton(self.edit_window, text="Upload File", width=150, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
                             command=lambda: self.upload_file())
        
        add.place(x=220, y=290)

        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=330)

        save = ctk.CTkButton(self.edit_window, text="Save", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
                             command=lambda: self.save_report(date, entry_notes.get()))
        save.place(x=150, y = 370)

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Upload PDF", filetypes=[("File PDF", "*.pdf")]
        )

        if file_path:
            self.file_path = file_path
            name = file_path.split("/")[-1]
            self.lbl_report.configure(text=f"{name}")
        
    def save_report(self, date, notes):
        self.output_add.configure(text="Function still to be written", text_color=self.risk_code(4))

    def download_report(self, id):
        print("Function still to be written")

ID = (11,)
DoctorApp(ID)