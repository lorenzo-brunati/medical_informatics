
# Home-Monitoring System for Cardiovascular Diseases

This project is a **Home-Monitoring System for Cardiovascular Diseases** developed as part of the **Medical Informatics** course.

## 1. Setup and Installation

The folder includes a `requirements.txt` file listing all necessary external libraries.
Install them all automatically by running:

```bash
pip install -r requirements.txt

```

### 1.1 Initialize the Database

All system data is securely managed within an SQLite database (`database.db`). To ensure the system is fully operational before launching the application, you must execute the database initialization script:

```bash
python create_db.py

```

During execution, `create_db.py` builds the relational database architecture via the `db_init.sql` schema and populates the tables using the following medical and synthetic datasets included in the repository:

* **Synthetic Clinical Records (`data.xlsx`):** General patient demographics, clinical appointments, messaging logs, technical support requests, and daily cardiovascular vital trends (such as blood pressure and heart rate) were synthetically generated using the **Gemini Large Language Model**.
* **Physiological ECG Waveforms (`ecg.csv`):** Real-world cardiac signal data has been integrated using a data subset from the **St. Petersburg Institute of Cardiological Technics (Incart) 12-lead Arrhythmia Database**, hosted on **PhysioNet**. Specifically, **only the first lead (single-lead derivation)** was extracted from the source database to simulation the ECG signal typically captured by commercial wearable devices.

### 1.2 Additional Folders

The project repository contains two additional folders:

* **`icons/`:** Contains the graphical elements and icons used to build the modern `customtkinter` interface across all dashboards.
* **`report/`:** Houses a sample medical examination report (`report.pdf`). Within this system iteration, this template is **identical for all patients and all past examinations** to simulate standardized clinical documentation outputs.

## 2. How to Run the Application

Once the dependencies are installed and the database is initialized, launch the system by running the main entry point:

```bash
python main.py

```

*(Executing this script will immediately open the user login application interface).*

Use the following predefined credentials to log in and test the application from different users' point of view:

| User Role | Username | Password |
| --- | --- | --- |
| **Admin** | `lbianchi` | `LauraAdm84!` |
| **Doctor** | `ericci` | `ElenaDoc76!` |
| **Patient** | `alombardi` | `AriLom1964!` |

Details about the main user functionalities can be found in the **Project Report**. 

### 2.1 Admin App

In the **Admin App** new users can be created or deleted. Also, support requests can be managed. Lastly, wearable devices can be added, removed or associated to the patients. 

### 2.2 Doctor App

In the **Doctor App** appointments can be added, edited or deleted. Additionally, patients can be managed, visualising data, reports, appointments and messages. For demo purposes, only data for one patient were generated, namely **Arianna Lombardi**, fiscal code **PTGZ4JFEBZ9SDO78**. We recommend opening in more details only this patient. For what regards medical data, only few were generated. Specifically, only records from *2026-05-27* to *2026-06-04* are available. Any time period exceeding this range won't plot any data on the Vitals widget.

### 2.3 Patient App

The **Patient App** offer similar features to the Doctor App, of course limited to the patient side. The same constraints regarding the vitals remain valid also for the Patient App.

## 3. Additional Notes

While the user interface was developed utilizing layout managers such as **Grid** alongside relative positioning of the widgets, launching the application on different computers, monitors, or operating systems may still affect the graphical layout.

If you were to experience issues when launching the application from the `main.py` file, e.g. the specific user application won't open after the Login, try running directly the corresponding .py file (`doctor.py`, `admin.py`, `patient.py`). To do so, you must remove the two comments at the very end of each file, this will allow you to skip the Login procedure.
