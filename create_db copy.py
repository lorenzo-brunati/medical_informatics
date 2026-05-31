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
    
    # 2. Caricamento del file Excel
    print(f"Reading Excel file: {excel_path}...")

    # 3. Definizione dell'ordine tassativo di inserimento (rispetta i vincoli FK)
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

    # 4. Iterazione sui fogli nell'ordine corretto
    for table_name in insertion_order:
       
        print(f"Elaboration of Table: {table_name}...")

        # Legge il foglio specifico
        df = pd.read_excel(excel_path, sheet_name=table_name)

        if df.empty:
            print(f"ℹ️ Il foglio '{table_name}' è vuoto. Salto.")
            continue

        # 5. Pulizia e conversione dei dati (Numeri e Date)
        for col in df.columns:
            # Se la colonna contiene 'date' nel nome, la convertiamo in stringa YYYY-MM-DD per SQLite
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col], errors="coerce")
                # SQLite non ha un tipo DATE nativo, memorizza le date come stringhe 'YYYY-MM-DD'
                df[col] = df[col].dt.strftime("%Y-%m-%d")

            # Se la colonna contiene 'time' nel nome, formattiamo in HH:MM:SS
            elif "time" in col.lower() and col.lower() != "daytime":
                # Gestisce sia oggetti datetime.time che stringhe
                df[col] = pd.to_datetime(
                    df[col], format="%H:%M", errors="coerce"
                ).dt.time
                df[col] = df[col].apply(
                    lambda x: x.strftime("%H:%M") if pd.notnull(x) else None
                )

            # Forza i numeri (Float/Int) dove appropriato, convertendo i valori non validi in NaN/None
            elif (
                df[col].dtype == "object"
                and col.lower() != "value"
                and col.lower() != "report"
            ):
                # Se la colonna dovrebbe essere numerica (es. Height, Threshold, Id...)
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

        # Gestione dei valori nulli di Pandas (NaN) convertiti in None per il database (NULL)
        df = df.astype(object).where(pd.notnull(df), None)

        # 6. Generazione della query SQL Dinamica ed esecuzione
        columns = ", ".join(df.columns)
        placeholders = ", ".join(["?"] * len(df.columns))
        # Utilizziamo INSERT OR IGNORE o INSERT OR REPLACE a seconda delle preferenze.
        # Qui usiamo INSERT INTO standard. Se ci sono duplicati, fallirà notificandolo.
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Trasformiamo il dataframe in una lista di tuple per l'inserimento bulk
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
                f"❌ Errore durante l'inserimento nella tabella '{table_name}': {e}"
            )

    load_ecg()

    # 7. Chiusura connessione
    conn.close()
    print("\nDB successfully populated!")


# Sostituisci con i tuoi percorsi reali
EXCEL_PATH = "data.xlsx"
DB_PATH = "database.db"  # Il tuo file di database SQLite

populate_database(EXCEL_PATH, DB_PATH)