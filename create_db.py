import sqlite3
import csv
import pandas as pd

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

file = open('db_init.sql', 'r')
cursor.executescript(file.read())
file.close()

def load_ecg():
    csv_file_path = "ecg.csv"

    ids_signals = [19, 38, 57, 76, 95, 114, 133, 152, 171]
    sampling_freq = 257
    time_val = "21:00"

    print("Elaboration of Table: SIGNALS...")

    with open(csv_file_path, mode="r") as file:
        reader = csv.reader(file)

        for index, row in enumerate(reader):


            current_id = ids_signals[index]
            ecg_numbers = row[1:]

            csv_string_value = ",".join(ecg_numbers)

            sql_query = """
                INSERT INTO SIGNALS (IdSignals, Value, Sampling_Freq, Time)
                VALUES (?, ?, ?, ?)
            """

            cursor.execute(
                sql_query, (current_id, csv_string_value, sampling_freq, time_val)
            )

    conn.commit()
    print(
        f"✅ {len(ids_signals)} rows successfully inserted in 'SIGNALS'."
    )
    
def populate_database(excel_path, db_path):
    
    print(f"Reading Excel file: {excel_path}...")

    insertion_order = [
        "USER",
        "PATIENT_CLINICALDATA",
        "DOCTOR",
        "ADMIN",
        "SUPPORT",
        "THERAPY",
        "THR_PERSONALIZED",
        "APPOINTMENT",
        "WEARABLE_DEVICE",
        "DATA",
        "NUMERICAL_DATA",
        "NOTIFICATION",
        "CHECK_OUT",
        "PATHOLOGY",
        "USER_PATHOLOGIES",
    ]

    for table_name in insertion_order:
       
        print(f"Elaboration of Table: {table_name}...")

        df = pd.read_excel(excel_path, sheet_name=table_name)

        if df.empty:
            print(f"Sheet '{table_name}' is empty.")
            continue

        for col in df.columns:
            
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col], errors="coerce")
                df[col] = df[col].dt.strftime("%Y-%m-%d")

            elif "time" in col.lower() and col.lower() != "daytime":

                df[col] = pd.to_datetime(
                    df[col], format="%H:%M", errors="coerce"
                ).dt.time
                df[col] = df[col].apply(
                    lambda x: x.strftime("%H:%M") if pd.notnull(x) else None
                )

            elif (
                df[col].dtype == "object"
                and col.lower() != "value"
                and col.lower() != "report"
            ):
                if any(
                    x in col.lower()
                    for x in [
                        "id",
                        "height",
                        "threshold",
                        "max",
                        "min",
                        "mean",
                        "freq",
                    ]
                ):
                    df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.astype(object).where(pd.notnull(df), None)

        columns = ", ".join(df.columns)
        placeholders = ", ".join(["?"] * len(df.columns))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        rows_to_insert = [tuple(x) for x in df.to_numpy()]

        try:
            cursor.executemany(query, rows_to_insert)
            conn.commit()
            print(
                f"✅ {len(rows_to_insert)} rows successfully inserted in '{table_name}'."
            )
        except sqlite3.Error as e:
            conn.rollback()
            print(
                f"❌ Error in table '{table_name}': {e}"
            )

    load_ecg()

    conn.close()
    print("\nDB successfully populated!")


EXCEL_PATH = "data.xlsx"
DB_PATH = "database.db"

populate_database(EXCEL_PATH, DB_PATH)