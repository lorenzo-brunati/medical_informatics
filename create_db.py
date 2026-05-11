import sqlite3 as sql
import customtkinter as ctk

conn = sql.connect("Project/database.db")
cursor = conn.cursor()

file = open('Project/database.sql', 'r')
cursor.executescript(file.read())

file.close()