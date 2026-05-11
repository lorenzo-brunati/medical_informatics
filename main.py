import sqlite3 as sql
import customtkinter as ctk
import PIL.Image

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
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()

        self.root = ctk.CTk()
        self.root.title("PatientApp")
        self.root.geometry("1600x900")

        self.setup_gui()

        self.root.mainloop()
    
    def setup_gui(self):
        self.topbar = ctk.CTkFrame(self.root, width=1600, height=80, fg_color="#E8EBF2")
        self.topbar.place(x=0, y=0)

        self.cursor.execute("SELECT name FROM user WHERE username = ?", self.user)
        name = self.cursor.fetchone()[0]

        self.name = ctk.CTkLabel(self.topbar, text=f"Hello, {name} ", font=('Montserrat', 16, "bold", "italic"), text_color="#9DA1A7")
        self.name.place(x=20, y=12)

        self.subtitle = ctk.CTkLabel(self.topbar, text="Welcome back!", font=('Montserrat', 22), text_color="#475569")
        self.subtitle.place(x=20, y=35)

        buttons_names = ["Dashboard", "Data", "Appointments", "Support"]
        self.menu_buttons = []

        self.button_menu = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.button_menu.place(x=300, y=32)

        side_buttons_names = ["Notifications", "Profile"]
        self.side_buttons = []

        self.icon_notif_dark = ctk.CTkImage(light_image=PIL.Image.open("icons/dark_bell.png"), size=(24, 24))
        self.icon_profile_dark = ctk.CTkImage(light_image=PIL.Image.open("icons/dark_user.png"), size=(20, 20))

        self.icon_notif_light = ctk.CTkImage(light_image=PIL.Image.open("icons/light_bell.png"), size=(24, 24))
        self.icon_profile_light = ctk.CTkImage(light_image=PIL.Image.open("icons/light_user.png"), size=(20, 20))


        self.side_topbar = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.side_topbar.place(x=1064, y=22)

        self.profile_menu = ctk.CTkOptionMenu(
            self.root, # Attaccato alla root
            values=["Personal Information", "Settings", "Logout"],
            command=self.handle_dropdown_profile,
            dynamic_resizing=False,
            width=30,
            dropdown_fg_color="#475569",      
            dropdown_hover_color="#BFC6D1",   
            dropdown_text_color="#E8EBF2",    
            dropdown_font=("Montserrat", 8, "bold")
        )

        for name in buttons_names:
            btn = ctk.CTkButton(
                self.button_menu,
                text=name,
                width=160,
                height=30,
                corner_radius=20,
                fg_color="#DCE1E9",
                border_color="#BFC6D1",
                border_width=1,
                hover_color="#BFC6D1",
                text_color="#475569",
                font=("Montserrat", 14))
            

            btn.configure(command=lambda b=btn: self.handle_click_main(b))
            
            btn.pack(side="left", padx=5)
            self.menu_buttons.append(btn)
        
        if self.menu_buttons:
            self.handle_click_main(self.menu_buttons[0])
        

        for name in side_buttons_names:
            side_btn = ctk.CTkButton(
                self.side_topbar,
                text="",
                image=self.icon_profile_dark if name == "Profile" else self.icon_notif_dark,
                width=36,
                height=36,
                corner_radius=18,
                border_color="#BFC6D1",
                fg_color="#DCE1E9",
                border_width=2,
                hover_color="#BFC6D1")

            side_btn.ID = name
            side_btn.configure(command=lambda b=side_btn: self.handle_click_side(b))

            side_btn.pack(side="left", padx=5)
            self.side_buttons.append(side_btn)

    def update_main_button_colors(self, clicked_button):
        for btn in self.menu_buttons:
            btn.configure(fg_color="#DCE1E9", border_color="#BFC6D1", border_width=2, hover_color="#BFC6D1", text_color="#475569", font=("Montserrat", 14))
        for side_btn in self.side_buttons:
            button_id = getattr(side_btn, "ID", "")
            side_btn.configure(image=self.icon_profile_dark if button_id == "Profile" else self.icon_notif_dark, border_width=1, hover_color="#BFC6D1", fg_color="#DCE1E9")
        
        clicked_button.configure(fg_color="#3366cc", border_color="#3366cc", border_width=2, text_color="#E8EBF2", font=("Montserrat", 14, "bold"), hover_color="#3366cc")


    def handle_click_main(self, button):
        self.update_main_button_colors(button)
        
        page = button.cget("text")
        if page == "Dashboard":
            self.show_dashboard();
        elif page == "Data":
            self.show_data();
        elif page == "Appointments":
            self.show_appointments();
        elif page == "Support":
           self.show_support();
    

    def update_side_button_colors(self, clicked_button):
        for side_btn in self.side_buttons:
            button_id = getattr(side_btn, "ID", "")
            side_btn.configure(image=self.icon_profile_dark if button_id == "Profile" else self.icon_notif_dark, border_width=1, hover_color="#BFC6D1", fg_color="#DCE1E9")
        for btn in self.menu_buttons:
            btn.configure(fg_color="#DCE1E9", border_color="#BFC6D1", border_width=2, hover_color="#BFC6D1", text_color="#475569", font=("Montserrat", 14))
        clicked_button.configure(fg_color="#475569", border_width=0, hover_color="#475569", image=self.icon_profile_light if clicked_button.cget("image") == self.icon_profile_dark else self.icon_notif_light)

    def handle_click_side(self, button):
        self.update_side_button_colors(button)

        button_id = getattr(button, "ID", "")
        if button_id == "Notifications":
            self.show_notifications();
        elif button_id == "Profile":
            self.profile_menu.place(x = button.winfo_rootx() - self.root.winfo_rootx() + button.winfo_width() - self.profile_menu.winfo_width(), y = button.winfo_rooty() - self.root.winfo_rooty() + button.winfo_height() - 66)
            self.root.update_idletasks()
            self.profile_menu.update()
            
            self.profile_menu._open_dropdown_menu();

    def handle_dropdown_profile(self, choice):
        print(f"Scelta selezionata: {choice}")
        if choice == "Logout":
            self.root.destroy()
        elif choice == "Personal Information":
            self.show_profile()
        elif choice == "Settings":
            self.show_settings()

    def show_dashboard(self):
        self.mainpage = ctk.CTkFrame(self.root, width=1600, height=820, fg_color="#E8EBF2")
        self.mainpage.place(x=0, y=80)

    def show_data(self):
        self.mainpage = ctk.CTkFrame(self.root, width=1600, height=820, fg_color="#E8EBF2")
        self.mainpage.place(x=0, y=80)

    def show_appointments(self):
        self.mainpage = ctk.CTkFrame(self.root, width=1600, height=820, fg_color="#E8EBF2")
        self.mainpage.place(x=0, y=80)

    def show_support(self):
        self.mainpage = ctk.CTkFrame(self.root, width=1600, height=820, fg_color="#E8EBF2")
        self.mainpage.place(x=0, y=80)

    def show_notifications(self):
        self.mainpage = ctk.CTkFrame(self.root, width=1600, height=820, fg_color="#E8EBF2")
        self.mainpage.place(x=0, y=80)

    def show_profile(self):
        self.mainpage = ctk.CTkFrame(self.root, width=1600, height=820, fg_color="#E8EBF2")
        self.mainpage.place(x=0, y=80)

    def show_settings(self):
        self.mainpage = ctk.CTkFrame(self.root, width=1600, height=820, fg_color="#E8EBF2")
        self.mainpage.place(x=0, y=80)
    

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
user = ("aricci",)
DoctorApp(user)