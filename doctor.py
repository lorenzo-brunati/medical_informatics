import customtkinter as ctk
import sqlite3 as sql

from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from tkinter import filedialog
import shutil

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
        
from PIL import Image
import struct

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

UNITS = {
    "Systolic BP": "mmHg",       # Millimetri di mercurio
    "Diastolic BP": "mmHg",      # Millimetri di mercurio
    "Heart Rate": "bpm",         # Battiti al minuto
    "Step Count": "steps",       # Conteggio passi
    "Sleep Hours": "hours",        # Ore di sonno
    "SPO2": "%",                 # Percentuale di ossigeno nel sangue
    "VO2max": "mL/kg/min"        # Millilitri di ossigeno per chilogrammo al minuto
}

VITALS = {
    "Heart Rate": "HR",
    "Systolic BP": "SBP",
    "Diastolic BP": "DBP",
    "Step Count": "StepCount",
    "Sleep Hours": "SleepHours",
    "SPO2": "SPO2",
    "VO2max": "VO2Max"
}

class DoctorApp():
    def __init__(self, ID):
        
        self.ID = ID
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()
        
        self.root = ctk.CTk()
        self.root.title("DoctorApp")

        self.root.geometry("1600x900")
        
        self.upload_icons()
    
        self.setup_gui()
        self.root.mainloop()

    def upload_icons(self):
        self.img_profile = ctk.CTkImage(
            light_image=Image.open("icons/dark_user.png"),
            dark_image=Image.open("icons/light_user.png"),
            size=(24,24)
        )
        
        self.img_notifications = ctk.CTkImage(
            light_image=Image.open("icons/dark_bell.png"),
            dark_image=Image.open("icons/light_bell.png"),
            size=(24,24)
        )
        
        self.img_support = ctk.CTkImage(
            light_image=Image.open("icons/dark_bell.png"),
            dark_image=Image.open("icons/light_bell.png"),
            size=(24,24)
        )        

    def setup_gui(self):

        self.topbar = ctk.CTkFrame(self.root, fg_color=COLORS["sfondo_grigino"])
        self.topbar.place(relx=0, rely=0, relheight=0.15, relwidth=1)

        self.main = ctk.CTkFrame(self.root, fg_color=COLORS["sfondo_grigino"])
        self.main.place(relx=0, rely=0.15, relheight=0.85, relwidth=1)

        self.welcome()
        self.nav_buttons()

        self.dashboard()

    def clear_content_frame(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def welcome(self):

        self.cursor.execute("SELECT name, surname FROM user WHERE ID = ?", self.ID)
        ns = self.cursor.fetchall()[0] 
        self.DocName = ns[0]
        self.DocSurname = ns[1]

        self.surname_label = ctk.CTkLabel(self.topbar, text=f"Hello Dr. {self.DocSurname}", font=FONTS["titolo"], text_color=COLORS["testo_chiaro"])
        self.surname_label.place(x=50, y=30)

        self.welcome_label = ctk.CTkLabel(self.topbar, text="Welcome Back!", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.welcome_label.place(x=50, y=60)

    def nav_buttons(self):

        self.container = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.container.place(relx=0.35, rely=0, relheight=1, relwidth=0.5)

        self.buttons_dict = {}
        buttons = ["Dashboard", "Patients", "Appointments"]
        for b in buttons:
            btn = ctk.CTkButton(self.container, text=b, text_color=COLORS["testo_scuro"], font=FONTS["testo_normale"],
                                command = lambda b=b: self.switch_tab(b), width=150, height=40, corner_radius=20,
                                fg_color=COLORS["bottone_grigio"], border_color=COLORS["bordi"], hover_color=COLORS["blu_acceso"])
            btn.pack(side="left", padx=10)
            self.buttons_dict[b] = btn
        
        self.update_buttons("Dashboard")
        self.tab = "Dashboard"

        self.icon_container = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.icon_container.place(relx=0.98, rely=0.05, anchor="ne", relheight=0.8)

        self.side_buttons()

    def side_buttons(self):
        self.btn_profile = ctk.CTkButton(self.icon_container, text="", image=self.img_profile, width=40, height=40, corner_radius=20, fg_color=COLORS["bottone_grigio"],
                                         hover_color=COLORS["blu_acceso"], border_color=COLORS["bordi"], border_width=1, command=self.mostra_profilo)
        self.btn_profile.pack(side="right", padx=6, pady=5)

        self.btn_support = ctk.CTkButton(self.icon_container, text="", image=self.img_support, width=40, height=40, corner_radius=20, fg_color=COLORS["bottone_grigio"],
                                         hover_color=COLORS["blu_acceso"], border_color=COLORS["bordi"], border_width=1, command=self.support_popup)
        self.btn_support.pack(side="right", padx=6, pady=5)

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
                SELECT app.IDAppointment, app.Date, app.Time, user.Name, user.Surname, pat.RiskCode, app.Notes, user.FiscalCode
                FROM Appointment AS app
                JOIN Patient_ClinicalData AS pat ON app.IDPatient = pat.IDPatient
                JOIN User ON app.IDPatient = user.ID
                LEFT JOIN Check_Out AS co ON app.IDAppointment = co.IDAppointment
                WHERE app.IDDoctor = ? 
                AND app.Date >= DATE('now')
                AND co.IDAppointment IS NULL
                ORDER BY Date, Time ASC"""
                        
        self.cursor.execute(query, self.ID)
        return self.cursor.fetchall()

    def show_incoming(self):

        self.text = ctk.CTkLabel(self.incoming, text="Incoming Appointments", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
        
        self.scrollable = ctk.CTkScrollableFrame(self.incoming, fg_color="transparent")
        self.scrollable.place(x=0, rely=0.1, relheight=0.85, relwidth=1)
        
        appointments = self.get_appointments()
        for app in appointments:
            id, date, time, name, surname, code, report, fiscal = app

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

            label_fiscal = ctk.CTkLabel(row, text=fiscal, font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"],width=200, anchor="w")
            label_fiscal.grid(row=0,column=4, padx=15, pady=10, sticky="w")

            label_report = ctk.CTkLabel(row, text=report, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_report.grid(row=0,column=5, padx=15, pady=10, sticky="w")

            edit = ctk.CTkButton(row, text="Edit", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(1),
                                 command = lambda app=app : self.edit_appointment(app))
            edit.grid(row=0, column=6, padx=(15,5),pady=10,sticky="e")

            delete = ctk.CTkButton(row, text="Delete", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(4),
                                command = lambda app=app : self.delete_appointment(app))
            delete.grid(row=0, column=7, padx=(5,15),pady=10,sticky="e")

            row.grid_columnconfigure(5, weight=1)

    def edit_appointment(self, app):
        id, date, time, name, surname, code, report, fiscal = app

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

            self.output_edit.configure(text=f"Appointment #{id} deleted", text_color=self.risk_code(4))

            if self.tab == "Appointments":
                for widget in self.scrollable.winfo_children():
                    widget.destroy()
                self.appointments()

            elif self.tab == "Patients":
                for widget in self.calendar.winfo_children():
                    widget.destroy()
                self.pat_appointment()

        id, date, time, name, surname, code, report, fiscal = app

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
                    SET date = ?, time = ?, notes = ? 
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
        
        entry_name = ctk.CTkEntry(row, corner_radius=5, placeholder_text="Fiscal Code", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width = 200)
        entry_name.grid(row=0, column=2, padx=15, pady=10, sticky="w")
        
        entry_report = ctk.CTkEntry(row, corner_radius=5, placeholder_text="Notes", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=350)
        entry_report.grid(row=0, column=3, padx=15, pady=10, sticky="w")

        self.output_add = ctk.CTkLabel(row,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], width=200)
        self.output_add.grid(row=0, column=4, padx=15, pady=10, sticky="w")

        save = ctk.CTkButton(row, text="Save", width=80, corner_radius=20, fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(1),
                             command=lambda : self.add_appointment(entry_date.get(), entry_time.get(), entry_name.get(),entry_report.get()))
        save.grid(row=0, column=5, padx=15, pady=10, sticky="e")

        row.grid_columnconfigure(3, weight=1)

    def add_appointment(self, date, time, fiscal, report):
        if not date or not time or not fiscal:
            self.output_add.configure(text="Missing Fields", text_color=self.risk_code(4))
            return

        check_query = """SELECT ID FROM User 
                    WHERE UserType = ? AND fiscalcode = ?"""
        self.cursor.execute(check_query, ("Patient", fiscal))
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

        query = """INSERT INTO Appointment (date, time, notes, IDPatient, IDDoctor) 
                VALUES (?, ?, ?, ?, ?)"""
    
        self.cursor.execute(query, (date, time, report, id_pat, self.ID[0]))
        self.conn.commit()
        
        self.output_add.configure(text="New Appointment added", text_color=self.risk_code(1))
        
        if self.tab == "Appointments":
            for widget in self.scrollable.winfo_children():
                widget.destroy()
            self.show_incoming()
        
        elif self.tab == "Patients":
            for widget in self.calendar.winfo_children():
                widget.destroy()
            self.pat_appointment()

    def add_appointment_popup(self, name, surname, fiscal, code):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x500")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Add Appointment", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(code))
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Name and Surname", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {name} {surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_name.place(x=30, y=95)

        lbl_surname = ctk.CTkLabel(self.edit_window, text="Fiscal Code",font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_surname.place(x=30, y=150, anchor="w")
        entry_surname = ctk.CTkLabel(self.edit_window,  corner_radius=5,text=f" {fiscal}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
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
                             command=lambda: self.add_appointment(entry_data.get(), entry_time.get(), fiscal, entry_notes.get()))
        
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
            id, name, surname, code, appdate, age, fiscal_code, weight, height = pat
            
            row = ctk.CTkFrame(self.scrollable, fg_color="transparent")
            row.pack(fill='x',padx=20, pady=0)

            label_name = ctk.CTkLabel(row, text=name, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_name.grid(row=0,column=1, padx=15, pady=10, sticky="w")

            label_surname = ctk.CTkLabel(row, text=surname, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_surname.grid(row=0,column=2, padx=15, pady=10, sticky="w")

            label_fiscal = ctk.CTkLabel(row, text=fiscal_code, font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"],width=200, anchor="w")
            label_fiscal.grid(row=0,column=3, padx=15, pady=10, sticky="w")

            label_age = ctk.CTkLabel(row, text=f"Age: {age}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_age.grid(row=0,column=4, padx=15, pady=10, sticky="w")

            dot_code = ctk.CTkFrame(row, width=12, height=12, corner_radius=6, fg_color=self.risk_code(code))
            dot_code.grid(row=0,column=0, padx=15, pady=10, sticky="ew")

            app = f"Next Appointment: {appdate}" if appdate else "No Appointments planned"
            label_date = ctk.CTkLabel(row, text=app, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=5, padx=15, pady=10, sticky="w")

            edit = ctk.CTkButton(row, text="Open", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(code),
                                 command = lambda id=id, n=name, s=surname, a=age, c=code, f=fiscal_code, w=weight, h=height: self.show_patient(id, n, s, a, c, f, w, h))
            edit.grid(row=0, column=6, padx=(15,5),pady=10,sticky="e")

            row.grid_columnconfigure(5, weight=1)

    def get_patients(self):
        
        query = """SELECT user.ID, user.Name, user.Surname, pat.RiskCode, MIN(app.Date) AS NextAppointment,
                (strftime('%Y', 'now') - strftime('%Y', user.birthdate)) - (strftime('%m-%d', 'now') < strftime('%m-%d', user.birthdate)) AS Age, user.FiscalCode,
                pat.Weight, pat.Height
                FROM user 
                JOIN Patient_ClinicalData AS pat ON user.ID = pat.IDPatient
                LEFT JOIN Appointment AS app ON app.IDPatient = user.ID 
                    AND app.IDDoctor = ? 
                    AND app.Date >= DATE('now')
                    AND NOT EXISTS (
                        SELECT 1 
                        FROM Check_Out 
                        WHERE Check_Out.IDAppointment = app.IDAppointment
                    )
                GROUP BY user.ID
                ORDER BY 
                    CASE WHEN MIN(app.Date) IS NULL THEN 1 ELSE 0 END ASC,
                    NextAppointment ASC;"""

        self.cursor.execute(query, self.ID)
        patients = self.cursor.fetchall()

        return patients 
        
    def show_patient(self, id, name, surname, age, code, fiscal_code, weight, height):
        
        self.update_buttons("Patients")

        self.IDPat = id
        self.name = name
        self.surname = surname
        self.age = age
        self.code = code
        self.fiscal_code = fiscal_code
        self.weight = weight
        self.height = height 

        self.clear_content_frame()

        self.current = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.current.place(relx=0.03, rely=0.03, relheight=0.20, relwidth=0.70)

        self.last_message = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.last_message.place(relx=0.75, rely=0.03, relheight=0.20, relwidth=0.22)

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
        self.pat_message()

    def pat_appointment(self):
        
        self.text = ctk.CTkLabel(self.calendar, text="Next Appointment", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)

        query = """
                SELECT app.IDAppointment, MIN(app.Date), app.Time, user.Name, user.Surname, pat.RiskCode, app.Notes, user.FiscalCode
                FROM Appointment AS app
                JOIN Patient_ClinicalData AS pat ON app.IDPatient = pat.IDPatient
                JOIN User ON app.IDPatient = user.ID
                LEFT JOIN Check_Out AS co ON app.IDAppointment = co.IDAppointment
                WHERE app.IDPatient = ?
                AND app.IDDoctor = ?
                AND app.Date >= DATE('now')
                AND co.IDAppointment IS NULL
                LIMIT 1"""
                 
        self.cursor.execute(query, (self.IDPat, self.ID[0]))
        app = self.cursor.fetchall()[0]

        if app[0]:
            row = ctk.CTkFrame(self.calendar, fg_color="transparent", corner_radius=20)
            row.place(x=20, y=70, relwidth=0.85)

            label_date = ctk.CTkLabel(row, width=160, anchor="w", text=f"{app[1]} - {app[2]}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")
            
            if app[1] == f"{datetime.today()}"[:10]:
                check_out = ctk.CTkButton(row, text="Check-out", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                 command = lambda id = self.IDPat: self.create_report(id, self.name, self.surname, self.code, self.fiscal_code, app[1]))
                check_out.grid(row=0, column=1, padx=(5,5),pady=10,sticky="e")
                
            else:
                edit = ctk.CTkButton(row, text="Edit", width=50, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(1),
                                    command = lambda app=app : self.edit_appointment(app))
                edit.grid(row=0, column=1, padx=(0,5),pady=10,sticky="e")

                delete = ctk.CTkButton(row, text="Delete", width=50, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(4),
                                    command = lambda app=app : self.delete_appointment(app))
                delete.grid(row=0, column=2, padx=(0,15),pady=10,sticky="e")
            
            row.grid_columnconfigure(0, weight=1)
        else: 
            row = ctk.CTkFrame(self.calendar, fg_color="transparent", corner_radius=20)
            row.place(x=20, y=70, relwidth=0.85)

            label_date = ctk.CTkLabel(row, width=160, anchor="w", text="No Appointments", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=0, padx=(15,0), pady=10, sticky="w")

            add = ctk.CTkButton(row, text="Add", width=50, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(1),
                                    command = lambda : self.add_appointment_popup(self.name, self.surname, self.fiscal_code, self.code))
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
        self.text.place(relx=0.08, y=25)

        dot_code = ctk.CTkFrame(self.therapy, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
        dot_code.place(relx=0.85, y=30)
                     
        lbl_date = ctk.CTkLabel(self.therapy, text="Modified on", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=80, anchor="w")
        entry_date = ctk.CTkLabel(self.therapy, corner_radius=5, anchor="w", text=date, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["sfondo_grigino"], width=290)
        entry_date.place(relx=0.08, y=95, relwidth=0.84)

        lbl_description = ctk.CTkLabel(self.therapy, text="Last Update",font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_description.place(relx=0.08, y=150, anchor="w")
        textbox_therapy = ctk.CTkTextbox(self.therapy,corner_radius=5, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["sfondo_grigino"], width=290, height=150)
        textbox_therapy.place(relx=0.08, y=165, relwidth=0.84)

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
        
        if self.tab == "Patients":
            for widget in self.therapy.winfo_children():
                widget.destroy()

            self.pat_therapy()

    def edit_risk_code(self):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("350x250")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])
        
        title = ctk.CTkLabel(self.edit_window, text="Edit Risk Code", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        row = ctk.CTkFrame(self.edit_window, fg_color="transparent")
        row.pack(fill='x', padx=30, pady=(100, 10))

        row.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        for i in range(1,5):
            
            dot_code = ctk.CTkButton(row, width=24, height=24, corner_radius=12, fg_color=self.risk_code(i), text="",
                                hover_color=self.risk_code(i), command = lambda c = i : self.save_risk_code(c))
            dot_code.grid(row=0,column=i, padx=5, pady=10)

        self.output = ctk.CTkLabel(self.edit_window, width=200, text="Choose the new Risk Code", anchor="center", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output.place(x=75, y=200)
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=200, text="", anchor="center", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=75, y=180)

    def save_risk_code(self, code):
        dict = {1: "Null", 2: "Low", 3: "Intermediate", 4: "High"}
        self.output_add.configure(text="Updated Risk Code")
        
        self.output.destroy()
        self.output = ctk.CTkLabel(self.edit_window, width=200, text=f"from {dict[self.code]} to {dict[code]}", anchor="center", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output.place(x=75, y=200)
        
        self.code = code
        self.clear_content_frame()
        self.show_patient(self.IDPat, self.name, self.surname, self.age, self.code, self.fiscal_code, self.weight, self.height)

    def get_threshold(self):
        query = """SELECT thr.ThresholdSBP, thr.ThresholdDBP, thr.ThresholdSPO2, thr.ThresholdUpperHeartRate, thr.ThresholdLowerHeartRate, pat.RiskCode
                FROM Thr_personalized AS thr
                JOIN Patient_ClinicalData AS pat ON pat.IDPatient = thr.IDPatient
                WHERE thr.IDPatient = ?"""

        self.cursor.execute(query, (self.IDPat,))
        thr = self.cursor.fetchall()[0]
        return thr

    def edit_threshold(self):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x500")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        thr = self.get_threshold()
        self.sbp, self.dbp, self.spo2, self.uhr, self.lhr, code = thr

        title = ctk.CTkLabel(self.edit_window, text="Edit Thresholds", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(code))
        dot_code.place(x=346, y=30)
                     
        lbl_sbp = ctk.CTkLabel(self.edit_window, text="Threshold SBP [mmHg]", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_sbp.place(x=30, y=80, anchor="w")
        entry_sbp = ctk.CTkEntry(self.edit_window, corner_radius=5, placeholder_text=f"{self.sbp}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_sbp.place(x=30, y=95)

        lbl_dbp = ctk.CTkLabel(self.edit_window, text="Threshold DBP [mmHg]", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_dbp.place(x=30, y=150, anchor="w")
        entry_dbp = ctk.CTkEntry(self.edit_window, corner_radius=5, placeholder_text=f"{self.dbp}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_dbp.place(x=30, y=165)

        lbl_spo2 = ctk.CTkLabel(self.edit_window, text="Threshold SPO2", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_spo2.place(x=30, y=220, anchor="w")
        entry_spo2 = ctk.CTkEntry(self.edit_window, corner_radius=5, placeholder_text=f"{self.spo2}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_spo2.place(x=30, y=235)

        lbl_lhr = ctk.CTkLabel(self.edit_window, text="Threshold Lower HR [bpm]", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_lhr.place(x=30, y=290, anchor="w")
        entry_lhr = ctk.CTkEntry(self.edit_window, corner_radius=5, placeholder_text=f"{self.lhr}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_lhr.place(x=30, y=305)

        lbl_uhr = ctk.CTkLabel(self.edit_window, text="Threshold Upper HR [bpm]", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_uhr.place(x=30, y=360, anchor="w")
        entry_uhr = ctk.CTkEntry(self.edit_window, corner_radius=5, placeholder_text=f"{self.uhr}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_uhr.place(x=30, y=375)

        self.output_edit = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_edit.place(x=50, y=415)

        save = ctk.CTkButton(self.edit_window, text="Save", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(1),
                             command=lambda: self.save_threshold((entry_sbp.get(), entry_dbp.get(), entry_spo2.get(), entry_lhr.get(), entry_uhr.get())))
        save.place(x=150, y = 450)

    def save_threshold(self, thr):
        if thr[0]:
            self.sbp = thr[0]
        if thr[1]:
            self.dbp = thr[1]
        if thr[2]:
            self.spo2 = thr[2]
        if thr[4]:
            self.uhr = thr[4]
        if thr[3]:
            self.lhr = thr[3]

        thr = (self.sbp, self.dbp, self.spo2, self.uhr, self.lhr, self.IDPat)
        
        query = """UPDATE Thr_personalized SET ThresholdSBP=?, ThresholdDBP=?, ThresholdSPO2=?, ThresholdUpperHeartRate=?, ThresholdLowerHeartRate=?
                WHERE IdPatient = ?"""

        self.cursor.execute(query, thr)
        self.conn.commit()

        self.output_edit.configure(text="Threshold updated", text_color=self.risk_code(1))
        
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

        self.plot_area = ctk.CTkFrame(self.vitals, fg_color="transparent", corner_radius=20, width=1100, height=430)
        self.plot_area.place(x=10,y=100)

        self.output = ctk.CTkLabel(self.vitals, text = f"Select Add Vitals to plot", font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"])
        self.output.place(x=35, y=70)

        self.output_date = ctk.CTkLabel(self.vitals, text = "", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
        self.output_date.place(x=300, y=70)

        self.btn_day = ctk.CTkButton(self.vitals, text="", width=50, corner_radius=20, hover_color=COLORS["bianco_puro"],
                                        fg_color=COLORS["bianco_puro"], text_color=COLORS["bianco_puro"])
        self.btn_day.place(x=300, y=70)

        self.btn_night = ctk.CTkButton(self.vitals, text="", width=50, corner_radius=20, hover_color=COLORS["bianco_puro"],
                                    fg_color=COLORS["bianco_puro"], text_color=COLORS["bianco_puro"])
        self.btn_night.place(x=300, y=70) 

        self.left = ctk.CTkButton(self.vitals, text="", width=50, corner_radius=20, hover_color=COLORS["bianco_puro"],
                                        fg_color=COLORS["bianco_puro"], text_color=COLORS["bianco_puro"])
        self.left.place(x=300, y=70)

        self.right = ctk.CTkButton(self.vitals, text="", width=50, corner_radius=20, hover_color=COLORS["bianco_puro"],
                                    fg_color=COLORS["bianco_puro"], text_color=COLORS["bianco_puro"])
        self.right.place(x=300, y=70) 

        self.error = ctk.CTkLabel(self.plot_area, text="", font=FONTS["titolo"], text_color=self.risk_code(4))
        self.error.place(relx=0.5, rely=0.5, anchor="center")
        
    def pat_exams(self):
        for widget in self.vitals.winfo_children():
            widget.destroy()

        row = ctk.CTkFrame(self.vitals, fg_color="transparent", corner_radius=20)
        row.place(x=20, y=20, relwidth=0.95)

        text = ctk.CTkLabel(row, text="Past Exams", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        text.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        
        self.exams_area = ctk.CTkScrollableFrame(self.vitals, fg_color="transparent", corner_radius=20)
        self.exams_area.place(x=10,y=70, relheight=0.85, relwidth=0.98)

        exams = self.get_exams()
        for ex in exams:
            id, date, notes, path = ex
            row = ctk.CTkFrame(self.exams_area, fg_color="transparent")
            row.pack(fill='x',padx=0, pady=0)

            label_date = ctk.CTkLabel(row, text=date, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
            label_date.grid(row=0,column=0, padx=15, pady=10, sticky="w")

            label_report = ctk.CTkLabel(row, text=notes, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_report.grid(row=0,column=1, padx=15, pady=10, sticky="w")

            if path:
                download = ctk.CTkButton(row, text="Download Report", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                 command = lambda path=path, date=date: self.download_report(path, date))
                download.grid(row=0, column=2, padx=(15,50),pady=10,sticky="e")
            else:
                check_out = ctk.CTkButton(row, text="Check-out", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                 command = lambda id = self.IDPat, d=date: self.create_report(id, self.name, self.surname, self.code, self.fiscal_code, d))
                check_out.grid(row=0, column=2, padx=(15,50),pady=10,sticky="e")

            row.grid_columnconfigure(1, weight=1)

    def get_exams(self):
        query = """SELECT app.IDAppointment, app.Date, app.Notes, out.ReportPath
                FROM Appointment AS app
                LEFT JOIN check_out AS out ON out.IDAppointment = app.IDAppointment
                WHERE app.IDPatient = ?
                AND app.Date <= Date('now')
                ORDER BY DATE DESC"""
            
        self.cursor.execute(query,(self.IDPat,))
        return self.cursor.fetchall()

    def pat_current(self):
        self.all = False
        self.text = ctk.CTkLabel(self.current, text="Current Patient", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
            
        row = ctk.CTkFrame(self.current, fg_color="transparent", corner_radius=20)
        row.place(x=20, y=70, relwidth=0.98)

        dot_code = ctk.CTkButton(row, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code), text="",
                                hover_color=self.risk_code(self.code), command = lambda : self.edit_risk_code())
        dot_code.grid(row=0,column=0, padx=15, pady=10, sticky="ew")

        testo_frame = ctk.CTkFrame(row, fg_color="transparent")
        testo_frame.grid(row=0, column=1, rowspan=2, padx=15, pady=0, sticky="w")

        nome_cognome_frame = ctk.CTkFrame(testo_frame, fg_color="transparent")
        nome_cognome_frame.pack(anchor="w")

        label_name = ctk.CTkLabel(nome_cognome_frame, text=self.name, font=FONTS["titolo"], text_color=COLORS["testo_scuro"], anchor="w")
        label_name.pack(side="left", padx=(0, 5))

        label_surname = ctk.CTkLabel(nome_cognome_frame, text=self.surname, font=FONTS["titolo"], text_color=COLORS["testo_scuro"], anchor="w")
        label_surname.pack(side="left")

        label_fiscal = ctk.CTkLabel(testo_frame, text=self.fiscal_code, font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"], anchor="w")
        label_fiscal.pack(anchor="w", pady=(0, 0)) # Gestisci qui la vicinanza millimetrica

        label_age = ctk.CTkLabel(row, text=f"Age: {self.age}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
        label_age.grid(row=0,column=2, padx=15, pady=10, sticky="w")

        label_wh = ctk.CTkLabel(row, text=f"W: {self.weight} Kg, H: {self.height} cm", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=150, anchor="w")
        label_wh.grid(row=0,column=3, padx=5, pady=10, sticky="w")

        label_wh.bind("<Button-1>", lambda e: self.update_wh())

        threshold = ctk.CTkButton(row, text="Threshold", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                 command = lambda : self.edit_threshold())
        threshold.grid(row=0, column=4, padx=(5,5),pady=10,sticky="e")


        vitals = ctk.CTkButton(row, text="Show Vitals", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                 command = lambda : self.pat_vitals())
        vitals.grid(row=0, column=5, padx=(5,5),pady=10,sticky="e")

        exams = ctk.CTkButton(row, text="Past Exams", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                command = lambda : self.pat_exams())
        exams.grid(row=0, column=6, padx=(5,5),pady=10,sticky="e")

        message = ctk.CTkButton(row, text="Message", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                command = lambda : self.message(self.IDPat))
        message.grid(row=0, column=7, padx=(5,30),pady=10,sticky="e")

        row.grid_columnconfigure(3,weight=1)

    def update_wh(self):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x300")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Edit Weight and Height", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
        dot_code.place(x=346, y=30)
                     
        lbl_height = ctk.CTkLabel(self.edit_window, text="Height [cm]", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_height.place(x=30, y=150, anchor="w")
        entry_height = ctk.CTkEntry(self.edit_window, corner_radius=5, placeholder_text=f"{self.height}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_height.place(x=30, y=165)

        lbl_weight = ctk.CTkLabel(self.edit_window, text="Weight [kg]", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_weight.place(x=30, y=80, anchor="w")
        entry_weight = ctk.CTkEntry(self.edit_window, corner_radius=5, placeholder_text=f"{self.weight}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_weight.place(x=30, y=95)

        self.output_edit = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_edit.place(x=50, y=210)

        save = ctk.CTkButton(self.edit_window, text="Save", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
                             command=lambda: self.save_wh(entry_weight.get(), entry_height.get()))
        save.place(x=150, y = 250)

    def save_wh(self, w,h):
        if w:
            self.weight = w
        if h:
            self.height = h
            
        self.pat_current()

        query = """UPDATE Patient_ClinicalData 
           SET Weight = ?, Height = ? 
           WHERE IdPatient = ?"""

        self.cursor.execute(query, (self.weight, self.height, self.IDPat))
        self.conn.commit()

        self.output_edit.configure(text="Weight and Height updated", text_color=self.risk_code(1))
        
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
        menu = ctk.CTkOptionMenu(self.edit_window, width=340, values=vitals_list,fg_color=COLORS["bianco_puro"], font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], button_color=COLORS["bianco_puro"],button_hover_color=self.risk_code(self.code))
        menu.place(x=30, y=165)
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=250)

        save = ctk.CTkButton(self.edit_window, text="Add", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
                            command = lambda : self.get_vitals(entry_start.get(), entry_end.get(),VITALS[menu.get()]))
        save.place(x=150, y = 250)

    def get_vitals(self, start, end, vit):
        
        try:
            date_start = datetime.strptime(start, "%Y-%m-%d")
            date_end = datetime.strptime(end, "%Y-%m-%d")
        except:
            for widget in self.plot_area.winfo_children():
                widget.destroy()
                
            self.error = ctk.CTkLabel(self.plot_area, text="", font=FONTS["titolo"], text_color=self.risk_code(4))
            self.error.place(relx=0.5, rely=0.5, anchor="center")
            self.error.configure(text="Wrong Date Format, try again")
            return

        days_range = (date_end - date_start).days + 1
        valori_attesi = 2*days_range

        query = """SELECT strftime('%m-%d', num.Date), num.Max, num.Min, num.Mean, num.DayTime
                FROM Numerical_Data AS num
                JOIN Data ON num.IDNumData = Data.IDData
                WHERE data.IDPatient = ?
                AND data.NameData = ?
                AND num.Date BETWEEN ? AND ?
                AND num.DayTime IN ('Day', 'Night')
                ORDER BY num.Date ASC"""
                
        vitals = {
            "Day":   {"dates": [], "max": [], "min": [], "mean": []},
            "Night": {"dates": [], "max": [], "min": [], "mean": []}
        }
        
        self.cursor.execute(query, (self.IDPat, vit, start, end))
        records = self.cursor.fetchall()

        if len(records)<valori_attesi or valori_attesi <= 0:
            for widget in self.plot_area.winfo_children():
                widget.destroy()
                
            self.error = ctk.CTkLabel(self.plot_area, text="", font=FONTS["titolo"], text_color=self.risk_code(4))
            self.error.place(relx=0.5, rely=0.5, anchor="center")
            self.error.configure(text="No data available for the selected time period")

        else:

            for row in records:
                daytime = row[4] # 'Day' oppure 'Night'
            
                if daytime in vitals:
                    vitals[daytime]["dates"].append(row[0])
                    vitals[daytime]["max"].append(row[1])
                    vitals[daytime]["min"].append(row[2])
                    vitals[daytime]["mean"].append(row[3])

            self.plot_vitals(vitals["Day"], vitals["Night"], vit)
        
    def plot_vitals(self, day, night, vit):
        for widget in self.plot_area.winfo_children():
            widget.destroy()
        
        self.left.destroy()
        self.right.destroy()

        self.output.destroy()
        self.output_date.destroy()
     
        if vit not in ("StepCount", "SleepHours"):

            self.btn_day = ctk.CTkButton(self.vitals, text="Day", width=50, corner_radius=20, hover_color=self.risk_code(self.code),
                                        fg_color=self.risk_code(self.code), text_color=COLORS["bianco_puro"],command=lambda: self.update_vitals("Day", day, night, vit))
            self.btn_day.place(x=35, y=70)

            self.btn_night = ctk.CTkButton(self.vitals, text="Night", width=50, corner_radius=20, hover_color=self.risk_code(self.code),
                                        fg_color=COLORS["bottone_grigio"], text_color=COLORS["bianco_puro"], command=lambda: self.update_vitals("Night", night, night, vit))
            self.btn_night.place(x=95, y=70) 

        self.update_vitals("Day", day, night, vit)
    
    def update_vitals(self, time, day, night, vit):
        for widget in self.plot_area.winfo_children():
            widget.destroy()

        self.output.destroy()
        self.output_date.destroy()

        print(vit)
        if vit not in ("SleepHours", "StepCount"):
            shift = 0
            if time == "Day":
                data = day
                self.btn_day.configure(fg_color=self.risk_code(self.code), text_color=COLORS["bianco_puro"])
                self.btn_night.configure(fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"])
            elif time == "Night":
                data = night
                self.btn_day.configure(fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"])
                self.btn_night.configure(fg_color=self.risk_code(self.code), text_color=COLORS["bianco_puro"])
        
        else:
            time = ""
            shift = 145
            data = day
            if self.btn_day:
                self.btn_day.destroy()
            if self.btn_night:
                self.btn_night.destroy()


        fig = Figure(figsize=(8.5, 4),facecolor="none") 
        
        ax = fig.add_subplot(111)       
        ax.set_facecolor("none")

        ax.plot(data["dates"], data["mean"], color=self.risk_code(self.code), linewidth=3)
        ax.fill_between(data["dates"], data["min"], data["max"], color=self.risk_code(self.code), alpha=0.2, edgecolor='none')
        
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

        vit = next((k for k, v in VITALS.items() if v == vit), None)

        self.output = ctk.CTkLabel(self.vitals, text = f"Plotting {time} {vit} [{UNITS[vit]}]", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output.place(x=180-shift, y=70)

        self.output_date = ctk.CTkLabel(self.vitals, text = f"Recorded from {day['dates'][0]} to {day['dates'][-1]}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
        self.output_date.place(x=465-shift, y=70)

    def add_ecg(self):
        
        query = """
            SELECT D.Date, S.Time
            FROM DATA AS D
            JOIN signals AS S on S.IdSignals = D.IDData 
            WHERE D.IdPatient = ? 
            AND D.NameData = 'ECG'
            ORDER BY D.Date DESC
        """ 

        self.cursor.execute(query, (self.IDPat,))
        dates = self.cursor.fetchall()
        
        date_list = [f"{d[0]} - {d[1]}" for d in dates]

        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x200")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Plot ECG", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
        dot_code.place(x=346, y=30)
                     
        start_date = ctk.CTkLabel(self.edit_window, text="Select Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        start_date.place(x=30, y=80, anchor="w")
        menu = ctk.CTkOptionMenu(self.edit_window, width=340, values=date_list,fg_color=COLORS["bianco_puro"], font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], button_color=COLORS["bianco_puro"],button_hover_color=self.risk_code(self.code))
        menu.place(x=30, y=95)
        
        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=130)

        save = ctk.CTkButton(self.edit_window, text="Plot", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
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

        self.cursor.execute(query, (self.IDPat, date[:10], date[-5:]))
        record = self.cursor.fetchall()[0]
        
        blob_data = record[0]
        sampling_freq = record[1]

        num_floats = len(blob_data) // 4
        
        self.y = list(struct.unpack(f"{num_floats}f", blob_data))

        self.x = [round(i * (1.0/sampling_freq), 2) for i in range(len(self.y))]

        self.date = date
        print(len(self.x))

        self.plot_ecg()

    def plot_ecg(self):
        self.btn_day.destroy()
        self.btn_night.destroy()

        self.left = ctk.CTkButton(self.vitals, text="<", width=40, corner_radius=20, hover_color=self.risk_code(self.code),
                                        fg_color=COLORS["bottone_grigio"], text_color=COLORS["testo_scuro"],command=lambda: self.update_index("L"))
        self.left.place(x=35, y=70)

        self.right = ctk.CTkButton(self.vitals, text=">", width=40, corner_radius=20, hover_color=self.risk_code(self.code),
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

    def pat_message(self):
        self.text = ctk.CTkLabel(self.last_message, text="Last Message", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
        
        self.msg_frame = ctk.CTkFrame(self.last_message, fg_color="transparent")
        self.msg_frame.place(x=5, rely=0.5, relheight=0.45, relwidth=0.98)
        
        messages = self.get_all_messages(self.IDPat)
        counter=0 #Number of messages 1
        for msg in messages:
            if counter < 1:
                id_msg, id_sender, id_receiver, counterpart_name, counterpart_surname, risk_code, text, date, time, read = msg
                counter += 1
                
                row = ctk.CTkFrame(self.msg_frame, fg_color="transparent")
                row.pack(fill='x',padx=20, pady=0)

                dot_code = ctk.CTkFrame(row, width=12, height=12, corner_radius=6, fg_color=self.risk_code(self.code))
                dot_code.grid(row=0,column=0, padx=15, pady=10, sticky="ew")

                label_text = ctk.CTkLabel(row, text=f"{text[:10]}...", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_text.grid(row=0,column=1, padx=10, pady=10, sticky="w")

                edit = ctk.CTkButton(row, text="View", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(self.code),
                                    command = lambda i=self.IDPat, n=self.name, s=self.surname, c=self.code: self.view_all(i, n, s, c))
                edit.grid(row=0, column=2, padx=(15,5),pady=10,sticky="e")

                row.grid_columnconfigure(1, weight=1)

    # ===========================
    # ---------- EXTRA ----------
    # ===========================

    def message(self, idpat):
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
                             command=lambda: self.send_message(idpat, date, time, entry_textbox.get("1.0", "end-1c")))
        
        save.place(x=150, y = 470)

    def send_message(self, idpat, date, time, msg):
        query = """
                INSERT INTO notification (IDSender, IDReceiver, Message, Date, Time, IsRead)
                VALUES (?, ?, ?, ?, ?, 0);
                """
        self.cursor.execute(query, (self.ID[0], idpat, msg, date, time))
        self.conn.commit()

        self.output_add.configure(text="Message sent!", text_color=self.risk_code(1))

        if self.all:
            for widget in self.main.winfo_children():
                widget.destroy()
            self.view_all(idpat, self.name, self.surname, self.code)
        else:
            for widget in self.last_message.winfo_children():
                widget.destroy()
            self.pat_message()
    
    def check_out(self, id, name, surname, code, fiscal):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x420")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        date = f"{datetime.today()}"[:10]
        
        self.get_app_id(id)
        
        title = ctk.CTkLabel(self.edit_window, text="Medical Examination", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(code))
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Patient", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {name} {surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
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

        add = ctk.CTkButton(self.edit_window, text="Upload File", width=150, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(code),
                             command=lambda: self.upload_file())
        
        add.place(x=220, y=290)

        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=330)

        save = ctk.CTkButton(self.edit_window, text="Save", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(code),
                             command=lambda: self.save_report())
        save.place(x=150, y = 370)

    def create_report(self, id , name, surname, code, fiscal, appdate):
        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("600x770")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        self.get_app_id(id, appdate)
        
        title = ctk.CTkLabel(self.edit_window, text="Medical Examination", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(code))
        dot_code.place(x=546, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Patient", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {name} {surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=540)
        entry_name.place(x=30, y=95)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Exam Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=150, anchor="w")
        entry_data = ctk.CTkLabel(self.edit_window, width=540,font=FONTS["testo_normale"], anchor="w", text=f" {appdate}",text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_data.place(x=30, y=165)

        lbl_text = ctk.CTkLabel(self.edit_window, text="Report", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_text.place(x=30, y=220, anchor="w")
        entry_textbox = ctk.CTkTextbox(self.edit_window, width=540, height=180, corner_radius=5, 
                                       font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], wrap="word")
        entry_textbox.place(x=30, y=235)

        lbl_therapy = ctk.CTkLabel(self.edit_window, text="Therapy", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_therapy.place(x=30, y=435, anchor="w")
        entry_therapy = ctk.CTkTextbox(self.edit_window, width=540, height=90, corner_radius=5, 
                                       font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"], wrap="word")
        entry_therapy.place(x=30, y=450)

        lbl_notes = ctk.CTkLabel(self.edit_window, text="Additional Notes", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_notes.place(x=30, y=560, anchor="w")
        entry_notes = ctk.CTkEntry(self.edit_window, width=540,font=FONTS["testo_normale"], placeholder_text=f"Enter additional notes",text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_notes.place(x=30, y=575)

        self.lbl_report = ctk.CTkLabel(self.edit_window, text="Choose Path", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.lbl_report.place(x=30, y=630, anchor="w")

        add = ctk.CTkButton(self.edit_window, text="Choose Path", width=150, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(code),
                             command=lambda: self.choose_path())
        
        add.place(x=420, y=620)

        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=150, y=670)

        save = ctk.CTkButton(self.edit_window, text="Create and Download", width=200, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(code),
                             command=lambda: self.create_automatic(name, surname, fiscal, appdate, entry_textbox.get("1.0", "end-1c"), entry_therapy.get("1.0", "end-1c"), entry_notes.get()))
        save.place(x=200, y = 710)

    def create_automatic(self, name, surname, fiscal, appdate, report, therapy, notes):
        query = """SELECT ID FROM User WHERE fiscalCode = ?"""
        self.cursor.execute(query,(fiscal,))
        self.IDPat = self.cursor.fetchall()[0][0]

        date = f"{datetime.today()}"[:10]
        self.save_therapy(date, therapy)

        path = self.download
        
        doc = SimpleDocTemplate(path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottom=40)
        story = []
        
        styles = getSampleStyleSheet()
        
        header = ParagraphStyle('Header', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, textColor=COLORS["blu_acceso"])
        title = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, spaceAfter=20, alignment=1, textColor=COLORS["blu_acceso"])
        section = ParagraphStyle('Section', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=12, spaceBefore=15, spaceAfter=5, textColor=COLORS["blu_acceso"])
        main = ParagraphStyle('Main', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=COLORS["testo_scuro"])
        label = ParagraphStyle('Label', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=COLORS["testo_scuro"])

        story.append(Paragraph(f"Dr. {self.DocName.upper()} {self.DocSurname.upper()}", header))
        story.append(Paragraph("Cardiovascular Disease Monitoring", main))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Medical Examination Report", title))
        story.append(Spacer(1, 10))
        
        patient = [
            [Paragraph("Patient:", label), Paragraph(f"{name} {surname}", main), 
            Paragraph("Exam Date:", label), Paragraph(appdate, main)],
            [Paragraph("Fiscal Code:", label), Paragraph(fiscal, main), 
            Paragraph("Report Date:", label), Paragraph(date, main)]
        ]
        
        table = Table(patient, colWidths=[80, 180, 80, 180])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Report of the Examination", section))
        story.append(Paragraph(report, main))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("Therapy", section))
        story.append(Paragraph(therapy, main))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("Additional Notes", section))
        story.append(Paragraph(notes, main))
        story.append(Spacer(1, 40))
        
        signature = Table([["", Paragraph(f"Signature <br/>Dr. {self.DocName} {self.DocSurname}", label)]], colWidths=[340, 180])
        signature.setStyle(TableStyle([
            ('ALIGN', (1,0), (1,0), 'CENTER'),
            ('LINEABOVE', (1,0), (1,0), 1, colors.HexColor("#718096")),
            ('PADDING', (1,0), (1,0), 5)
        ]))
        story.append(signature)

        doc.build(story)
        
        query = "INSERT INTO check_out (IDAppointment, ReportPath) VALUES (?,?)"
        self.cursor.execute(query,((self.IDApp[0], path)))
        self.conn.commit()

        if self.tab == "Dashboard":
            for widget in self.todays.winfo_children():
                widget.destroy()
            self.show_today()
        elif self.tab == "Patients":
            for widget in self.calendar.winfo_children():
                widget.destroy()
            self.pat_appointment()

            for widget in self.vitals.winfo_children():
                widget.destroy()
            self.pat_exams()

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Upload PDF", filetypes=[("File PDF", "*.pdf")]
        )

        if file_path:
            self.file_path = file_path
            print(file_path)
            self.lbl_report.configure(text=f"...{file_path[-15:]}")
        
    def get_app_id(self, id, appdate):
        query = "SELECT IDAppointment FROM Appointment AS app WHERE IDPatient = ? AND Date = ?"
        self.cursor.execute(query, (id,appdate))
        self.IDApp = self.cursor.fetchall()[0]

    def save_report(self):
        query = "INSERT INTO Check_Out (IDAppointment, ReportPath) VALUES (?, ?)"
        self.cursor.execute(query, (self.IDApp[0], f"report/report_{self.IDApp}.pdf"))
        self.conn.commit()

        shutil.copy(self.file_path, f"report/report_{self.IDApp[0]}.pdf")
        self.output_add.configure(text="Report uploaded successfully", text_color=self.risk_code(1))

    def download_report(self, path, date):
        self.path = path

        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x350")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Download Report", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(self.code))
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Patient", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {self.name} {self.surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
        entry_name.place(x=30, y=95)

        lbl_date = ctk.CTkLabel(self.edit_window, text="Date", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_date.place(x=30, y=150, anchor="w")
        entry_data = ctk.CTkLabel(self.edit_window, width=340,font=FONTS["testo_normale"], anchor="w", text=f"{date}",text_color=COLORS["testo_scuro"], fg_color=COLORS["bianco_puro"])
        entry_data.place(x=30, y=165)

        self.lbl_report = ctk.CTkLabel(self.edit_window, text="Choose File Path", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.lbl_report.place(x=30, y=235, anchor="w")

        add = ctk.CTkButton(self.edit_window, text="Choose", width=150, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
                             command=lambda: self.choose_path())
        
        add.place(x=220, y=220)

        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=260)

        save = ctk.CTkButton(self.edit_window, text="Download", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
                             command=lambda: self.download_file())
        save.place(x=150, y = 305)

    def download_file(self):
        if self.download:
            self.output_add.configure(text="Report successfully downloaded", text_color=self.risk_code(1))
            shutil.copy(self.path, self.download)
        else:
            self.output_add.configure(text="An error occured, try again", text_color=self.risk_code(4))

    def choose_path(self):
        chosen_path = filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],title="Choose Destination")
    
        if chosen_path:
            self.download = chosen_path
            self.lbl_report.configure(text=f"...{chosen_path[-15:]}")
        else:
            self.download = None

    def support_popup(self):
        self.btn_support.configure(fg_color=COLORS["blu_acceso"], image=ctk.CTkImage(Image.open("icons/light_bell.png"), size=(24,24)))

        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x480")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])
        self.edit_window.protocol("WM_DELETE_WINDOW", self.edit_window.destroy())

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

        save = ctk.CTkButton(self.edit_window, text="Send", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=COLORS["blu_acceso"],
                             command=lambda: self.send_request(entry_data.cget("text"),menu.get(),entry_textbox.get("1.0", "end-1c")))
        save.place(x=150, y = 430)

    def send_request(self, date, reqtype, msg):
        
        query = """
        INSERT INTO Support (Date, SupportType, IdRequester, IDAdmin, Message) 
        VALUES (?, ?, ?, ?, ?)
        """        

        self.cursor.execute(query, (date, reqtype, self.ID[0], 1, msg))
        self.conn.commit()

        self.output_add.configure(text="Support Request sent", text_color="green")


    # ===========================
    # -------- DASHBOARD --------
    # ===========================

    def dashboard(self):
        self.clear_content_frame()

        self.todays = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.todays.place(relx=0.03, rely=0.03, relheight=0.4, relwidth=0.6)

        self.critical = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.critical.place(relx=0.03, rely=0.5, relheight=0.47, relwidth=0.6)
        
        self.messages = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.messages.place(relx=0.66, rely=0.03, relheight=0.94, relwidth=0.31)

        self.show_today()
        self.show_critical()
        self.show_messages()
    
    def show_today(self):
        self.text = ctk.CTkLabel(self.todays, text="Today's Appointments", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
        
        self.scrollable = ctk.CTkScrollableFrame(self.todays, fg_color="transparent")
        self.scrollable.place(x=0, rely=0.2, relheight=0.75, relwidth=0.98)
        
        appointments = self.get_todays_appointments()
        if appointments:
            for app in appointments:
                id, IDPat, date, time, name, surname, code, report, age, fiscal, w, h = app
                row = ctk.CTkFrame(self.scrollable, fg_color="transparent")
                row.pack(fill='x',padx=20, pady=0)

                label_date = ctk.CTkLabel(row, text=f"{time}", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_date.grid(row=0,column=0, padx=15, pady=10, sticky="w")

                dot_code = ctk.CTkFrame(row, width=12, height=12, corner_radius=6, fg_color=self.risk_code(code))
                dot_code.grid(row=0,column=1, padx=15, pady=10, sticky="ew")

                label_name = ctk.CTkLabel(row, text=name, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
                label_name.grid(row=0,column=2, padx=15, pady=10, sticky="w")

                label_surname = ctk.CTkLabel(row, text=surname, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
                label_surname.grid(row=0,column=3, padx=15, pady=10, sticky="w")

                label_fiscal = ctk.CTkLabel(row, text=fiscal, font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"],width=75, anchor="w")
                label_fiscal.grid(row=0,column=4, padx=15, pady=10, sticky="w")

                label_report = ctk.CTkLabel(row, text=report, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_report.grid(row=0,column=5, padx=15, pady=10, sticky="w")

                check_out = ctk.CTkButton(row, text="Check-out", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(code),
                                    command = lambda id = IDPat, n = name, s = surname, c = code, f=fiscal, d=date: self.create_report(id, n, s, c, f, d))
                check_out.grid(row=0, column=6, padx=(15,5),pady=10,sticky="e")

                edit = ctk.CTkButton(row, text="Open", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(code),
                                    command = lambda id=IDPat, n=name, s=surname, a=age, c=code, f=fiscal, w=w, h=h: self.show_patient(id, n, s, a, c, f, w, h))
                edit.grid(row=0, column=7, padx=(15,5),pady=10,sticky="e")

                row.grid_columnconfigure(5, weight=1)
        else:
            row = ctk.CTkFrame(self.scrollable, fg_color="transparent")
            row.pack(fill='x',padx=20, pady=0)

            label = ctk.CTkLabel(row, text="No appointments planned for today", font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"])
            label.grid(row=0,column=0, padx=5, pady=10, sticky="w")

    def get_todays_appointments(self):
        
        query = """
                SELECT app.IDAppointment, pat.IDPatient, app.Date, app.Time, user.Name, user.Surname, pat.RiskCode, app.Notes,
                (strftime('%Y', 'now') - strftime('%Y', user.birthdate)) - (strftime('%m-%d', 'now') < strftime('%m-%d', user.birthdate)) AS Age, user.FiscalCode,
                pat.Weight, pat.Height
                FROM Appointment AS app
                JOIN Patient_ClinicalData AS pat ON app.IDPatient = pat.IDPatient
                JOIN User ON app.IDPatient = user.ID
                LEFT JOIN Check_Out AS co ON app.IDAppointment = co.IDAppointment
                WHERE app.Date = DATE('now')
                AND app.IDDoctor = ?
                AND co.IDAppointment IS NULL
                ORDER BY Date, Time ASC"""

        self.cursor.execute(query, self.ID)
        return self.cursor.fetchall()

    def show_critical(self):
        self.text = ctk.CTkLabel(self.critical, text="Critical Patients", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
        
        self.scrollable = ctk.CTkScrollableFrame(self.critical, fg_color="transparent")
        self.scrollable.place(x=0, rely=0.2, relheight=0.75, relwidth=0.98)
        
        patients = self.get_critical()
        for pat in patients:
            id, name, surname, code, appdate, age, fiscal, w, h = pat
            
            row = ctk.CTkFrame(self.scrollable, fg_color="transparent")
            row.pack(fill='x',padx=20, pady=0)

            label_name = ctk.CTkLabel(row, text=name, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_name.grid(row=0,column=1, padx=15, pady=10, sticky="w")

            label_surname = ctk.CTkLabel(row, text=surname, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_surname.grid(row=0,column=2, padx=(15,5), pady=10, sticky="w")

            label_age = ctk.CTkLabel(row, text=f"Age: {age}", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
            label_age.grid(row=0,column=3, padx=15, pady=10, sticky="w")

            dot_code = ctk.CTkFrame(row, width=12, height=12, corner_radius=6, fg_color=self.risk_code(code))
            dot_code.grid(row=0,column=0, padx=15, pady=10, sticky="ew")

            app = f"Next Appointment: {appdate}" if appdate else "No Appointments planned"
            label_date = ctk.CTkLabel(row, text=app, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
            label_date.grid(row=0,column=4, padx=15, pady=10, sticky="w")

            edit = ctk.CTkButton(row, text="Open", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                 fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(code),
                                 command = lambda id=id, n=name, s=surname, a=age, c=code, f=fiscal, w=w, h=h: self.show_patient(id, n, s, a, c, f, w, h))
            edit.grid(row=0, column=5, padx=(15,5),pady=10,sticky="e")

            row.grid_columnconfigure(4, weight=1)

    def get_critical(self):
        
        query = """SELECT user.ID, user.Name, user.Surname, pat.RiskCode, MIN(app.Date) AS NextAppointment,
                (strftime('%Y', 'now') - strftime('%Y', user.birthdate)) - (strftime('%m-%d', 'now') < strftime('%m-%d', user.birthdate)) AS Age, user.FiscalCode,
                pat.Weight, pat.Height
                FROM user 
                JOIN Patient_ClinicalData AS pat ON user.ID = pat.IDPatient
                LEFT JOIN Appointment AS app ON app.IDPatient = user.ID 
                    AND app.IDDoctor = ? 
                    AND app.Date >= DATE('now')
                    AND NOT EXISTS (
                        SELECT 1 
                        FROM Check_Out 
                        WHERE Check_Out.IDAppointment = app.IDAppointment
                    )
                WHERE pat.RiskCode = 4
                GROUP BY user.ID
                ORDER BY 
                    CASE WHEN MIN(app.Date) IS NULL THEN 1 ELSE 0 END ASC,
                    NextAppointment ASC;"""

        self.cursor.execute(query, self.ID)
        patients = self.cursor.fetchall()

        return patients  

    def show_messages(self):
        self.text = ctk.CTkLabel(self.messages, text="Recent Messages", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
        
        self.scrollable = ctk.CTkScrollableFrame(self.messages, fg_color="transparent")
        self.scrollable.place(x=0, rely=0.1, relheight=0.85, relwidth=0.98)
        
        messages = self.get_messages()
        if messages:
            for msg in messages:
                id, idpat, name, surname, code, text, date, time, read = msg
                
                row = ctk.CTkFrame(self.scrollable, fg_color="transparent")
                row.pack(fill='x',padx=20, pady=0)

                label_name = ctk.CTkLabel(row, text=name, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
                label_name.grid(row=0,column=1, padx=5, pady=10, sticky="w")

                label_surname = ctk.CTkLabel(row, text=surname, font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],width=75, anchor="w")
                label_surname.grid(row=0,column=2, padx=5, pady=10, sticky="w")

                dot_code = ctk.CTkFrame(row, width=12, height=12, corner_radius=6, fg_color=self.risk_code(code))
                dot_code.grid(row=0,column=0, padx=15, pady=10, sticky="ew")

                label_text = ctk.CTkLabel(row, text=f"{text[:10]}...", font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"])
                label_text.grid(row=0,column=3, padx=10, pady=10, sticky="w")

                edit = ctk.CTkButton(row, text="View", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                    fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(code),
                                    command = lambda i=idpat, n=name, s=surname, c=code: self.view_all(i, n, s, c))
                edit.grid(row=0, column=4, padx=(15,5),pady=10,sticky="e")

                row.grid_columnconfigure(3, weight=1)
        else:
            row = ctk.CTkFrame(self.scrollable, fg_color="transparent")
            row.pack(fill='x',padx=20, pady=0)

            label = ctk.CTkLabel(row, text="No messages to read", font=FONTS["testo_normale"], text_color=COLORS["testo_chiaro"],width=75, anchor="w")
            label.grid(row=0,column=1, padx=5, pady=10, sticky="w")

    def get_messages(self):

        query = """SELECT msg.IDNotification, msg.IDSender, user.Name, user.Surname, pat.RiskCode, msg.Message, msg.Date, msg.Time, msg.ISRead 
                FROM notification AS msg
                LEFT JOIN user ON msg.IDSender = user.ID
                LEFT JOIN Patient_ClinicalData AS pat ON user.ID = pat.IDPatient
                WHERE msg.IDReceiver = ? 
                AND msg.IsRead = 0
                GROUP BY msg.IDSender
                ORDER BY msg.Date DESC, msg.Time DESC"""

        self.cursor.execute(query, self.ID)
        messages = self.cursor.fetchall()
        
        return messages
    
    def view_message(self, id, pat, name, surname, code, text, date, time):
        
        self.name = name
        self.surname = surname
        self.code = code

        self.edit_window = ctk.CTkToplevel(self.root)
        self.edit_window.geometry("400x520")
        self.edit_window.configure(fg_color=COLORS["bottone_grigio"])

        title = ctk.CTkLabel(self.edit_window, text="Message", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        title.place(x=30, y=25)

        dot_code = ctk.CTkFrame(self.edit_window, width=24, height=24, corner_radius=12, fg_color=self.risk_code(code))
        dot_code.place(x=346, y=30)
                     
        lbl_name = ctk.CTkLabel(self.edit_window, text="Message from", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        lbl_name.place(x=30, y=80, anchor="w")
        entry_name = ctk.CTkLabel(self.edit_window, corner_radius=5, text=f" {name} {surname}", anchor="w", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"],fg_color=COLORS["bianco_puro"], width=340)
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

        self.output_add = ctk.CTkLabel(self.edit_window, width=300,text="", font=FONTS["testo_normale"], text_color=COLORS["testo_scuro"])
        self.output_add.place(x=50, y=430)

        reply = ctk.CTkButton(self.edit_window, text="Reply", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
                             command=lambda: self.message(pat))
        
        reply.place(x=95, y = 470)

        read = ctk.CTkButton(self.edit_window, text="Read", width=100, corner_radius=20, fg_color=COLORS["bianco_puro"], text_color=COLORS["testo_scuro"], hover_color=self.risk_code(self.code),
                             command=lambda: self.read_message(id, pat, name, surname, code))
        
        read.place(x=205, y = 470)

    def read_message(self, id, pat, name, surname, code):
        query = "UPDATE Notification SET isread = 1 WHERE IDNotification = ?"
        self.cursor.execute(query, (id,))
        self.conn.commit()

        self.output_add.configure(text="Message marked as read", text_color=self.risk_code(1))
        
        for widget in self.scrollable.winfo_children():
            widget.destroy()
        
        self.view_all(pat, name, surname, code)

    def get_all_messages(self, pat):
        query = """SELECT msg.IDNotification, msg.IDSender, msg.IDReceiver, 
                user.Name, user.Surname, pat.RiskCode, 
                msg.Message, msg.Date, msg.Time, msg.ISRead 
                FROM notification AS msg
                JOIN user ON user.ID = CASE 
                WHEN msg.IDSender = ? THEN msg.IDReceiver 
                ELSE msg.IDSender 
                END
                LEFT JOIN Patient_ClinicalData AS pat ON user.ID = pat.IDPatient
                WHERE (msg.IDSender = ? OR msg.IDReceiver = ?)
                    AND (msg.IDSender = ? OR msg.IDReceiver = ?)
                ORDER BY msg.Date DESC, msg.Time DESC"""
            
        self.cursor.execute(query, (pat, pat, pat, self.ID[0], self.ID[0]))
        msg = self.cursor.fetchall()

        return msg

    def view_all(self, pat, name, surname, code):
        self.clear_content_frame()
        self.all = True

        self.all_msg = ctk.CTkFrame(self.main, corner_radius=20, fg_color=COLORS["bianco_puro"])
        self.all_msg.place(relx=0.03, rely=0.03, relheight=0.94, relwidth=0.94)

        self.text = ctk.CTkLabel(self.all_msg, text=f"Messages from {name} {surname}", font=FONTS["titolo"], text_color=COLORS["testo_scuro"])
        self.text.place(x=30, y=25)
        
        self.scrollable = ctk.CTkScrollableFrame(self.all_msg, fg_color="transparent")
        self.scrollable.place(x=0, rely=0.1, relheight=0.85, relwidth=1)
        
        msg = self.get_all_messages(pat)
        
        self.name = name
        self.surname = surname
        self.code = code
        
        last_date = None

        for m in msg:
            id_msg, id_sender, id_receiver, counterpart_name, counterpart_surname, risk_code, text, date, time, read = m 

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
            
            if id_sender == pat:
                header_str = f"[{name} - {time}]"
                msg_color = COLORS["testo_scuro"]
                dot_color = self.risk_code(code)
                dot_size = 24 if not read else 12
            else:
                header_str = f"[Dr. {self.DocSurname} - {time}]"
                msg_color = COLORS["testo_chiaro"]
                dot_color = COLORS["blu_acceso"]
                dot_size = 12

            dot_container = ctk.CTkFrame(row, width=30, height=30, fg_color="transparent")
            dot_container.grid(row=0, column=0, padx=(10, 15), pady=5, sticky="w")
            dot_container.grid_propagate(False)

            dot_code = ctk.CTkFrame(dot_container, width=dot_size, height=dot_size, corner_radius=dot_size // 2, fg_color=dot_color)
            dot_code.place(relx=0.5, rely=0.5, anchor="center")

            label_header = ctk.CTkLabel(row, text=header_str, font=FONTS["testo_normale"], text_color=msg_color, width=160, anchor="w")
            label_header.grid(row=0, column=1, padx=5, pady=5, sticky="w")

            snippet = f"{text[:25]}..." if len(text) > 25 else text
            label_text = ctk.CTkLabel(row, text=snippet, font=FONTS["sottotitolo"], text_color=COLORS["testo_chiaro"], anchor="w")
            label_text.grid(row=0, column=2, padx=15, pady=5, sticky="w")

            edit = ctk.CTkButton(row, text="View", width=70, corner_radius=20, text_color=COLORS["testo_scuro"], 
                                fg_color=COLORS["bottone_grigio"], hover_color=self.risk_code(code),
                                command=lambda i=id_msg, p=pat, n=name, s=surname, c=code, tx=text, d=date, t=time: self.view_message(i, p, n, s, c, tx, d, t))
            edit.grid(row=0, column=3, padx=(15, 10), pady=5, sticky="e")

            row.grid_columnconfigure(2, weight=1)       

    def mostra_profilo(self):
        print("Profilo")

ID = (3,)
DoctorApp(ID)