import sqlite3 as sql
import customtkinter as ctk

from doctor import DoctorApp
from patient import PatientApp
from admin import AdminApp

import hashlib

def generate_hash(pw):

    pw_bytes = pw.encode('utf-8')
    
    hash_object = hashlib.sha256(pw_bytes)
    
    return hash_object.hexdigest()

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

        hash_pw = generate_hash(pw)

        # Execute SQL Query
        self.cursor.execute("SELECT ID FROM user WHERE username = ?", user)
        ID = self.cursor.fetchone()
        

        if ID is not None: # Existing USERNAME?
            self.cursor.execute("SELECT password FROM user WHERE ID = ?", ID)
            password = self.cursor.fetchone()[0]

            if hash_pw == password:
                self.outcome_label.configure(text=f"Welcome back {user[0]}!")
                self.outcome_label.configure(text_color="green")

                self.cursor.execute("SELECT UserType FROM user WHERE ID = ?", ID)
                user_type = self.cursor.fetchone()[0]

                if user_type == "Patient":
                    self.root.after(500, self.launch_patient, ID)

                elif user_type == "Doctor":
                    self.root.after(500, self.launch_doctor, ID)

                else:
                    self.root.after(500, self.launch_admin, ID)


            else:
                self.outcome_label.configure(text=f"Wrong Password")
                self.outcome_label.configure(text_color="red")

        else:
            self.outcome_label.configure(text="Username doesn't exist.")
            self.outcome_label.configure(text_color="red")

    def launch_patient(self, ID):
        self.root.destroy() 
        PatientApp(ID[0])

    def launch_doctor(self, ID):
        self.root.destroy() 
        DoctorApp(ID)

    def launch_admin(self, ID):
        self.root.destroy() 
        AdminApp(ID[0])

