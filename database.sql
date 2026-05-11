

CREATE TABLE IF NOT EXISTS USER (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(20),
    Surname VARCHAR(20),
    BirthDate DATE,
    Address VARCHAR(30),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(30),
    Username VARCHAR(30) NOT NULL UNIQUE,
    Password VARCHAR(30) NOT NULL,
    FiscalCode CHAR(16) UNIQUE,
    UserType VARCHAR( 10) CHECK ( UserType IN ('Doctor','Patient','Admin')) 
);

CREATE TABLE IF NOT EXISTS PATIENT_CLINICALDATA (
    IdPatient INTEGER PRIMARY KEY,
    Height REAL,
    Gender CHAR(1) CHECK ( Gender IN ('M','F')),
    RiskCode INTEGER,
    FOREIGN KEY (IdPatient) REFERENCES USER(Id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS DOCTOR (
   IdDoctor INTEGER PRIMARY KEY, 
   FOREIGN KEY (IdDoctor) REFERENCES USER(Id) 
      ON DELETE CASCADE
      ON UPDATE CASCADE
 );

 CREATE TABLE IF NOT EXISTS ADMIN( 
   IdAdmin INTEGER PRIMARY KEY,
   FOREIGN KEY (IdAdmin) REFERENCES USER (Id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
 );

CREATE TABLE IF NOT EXISTS SUPPORT (
    IdSupport INTEGER PRIMARY KEY AUTOINCREMENT,
    Date DATE,
    SupportType VARCHAR(20) CHECK (SupportType IN ('SupportCredentials','InconsistentData','Wearable','ScheduleIssue','Others' )),
    IdRequester INTEGER NOT NULL,
    IdAdmin INTEGER NOT NULL,
    FOREIGN KEY (IdRequester) REFERENCES USER(Id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (IdAdmin) REFERENCES ADMIN(IdAdmin)
        ON DELETE CASCADE
        ON UPDATE CASCADE   
);

CREATE TABLE IF NOT EXISTS THERAPY (
    IdTherapy INTEGER PRIMARY KEY AUTOINCREMENT,
    Date DATE,
    Description VARCHAR(300),
    IdDoctor INTEGER NOT NULL,
    IdPatient INTEGER NOT NULL,
    FOREIGN KEY (IdDoctor) REFERENCES DOCTOR(IdDoctor) 
        ON DELETE CASCADE
         ON UPDATE CASCADE,
    FOREIGN KEY (IdPatient) REFERENCES PATIENT_CLINICALDATA(IdPatient)
        ON DELETE CASCADE
        ON UPDATE CASCADE     
);

CREATE TABLE IF NOT EXISTS THR_PERSONALIZED (
    IdPatient INTEGER PRIMARY KEY,
    ThresholdValue REAL,
    ThresholdSBP REAL,
    ThresholdDBP REAL,
    ThresholdSpO2 REAL,
    ThresholdUpperHeartRate REAL,
    ThresholdLowerHeartRate REAL,
    IdTherapy INTEGER NOT NULL,
    FOREIGN KEY (IdPatient) REFERENCES PATIENT_CLINICALDATA(IdPatient)
     ON DELETE CASCADE
     ON UPDATE CASCADE,
    FOREIGN KEY (IdTherapy) REFERENCES THERAPY(IdTherapy)
     ON DELETE CASCADE
     ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS APPOINTMENT (
    IdAppointment INTEGER PRIMARY KEY AUTOINCREMENT,
    Date DATE,
    Time CHAR(5) CHECK (Time LIKE '__:__'),
    Report VARCHAR(255),
    IdPatient INTEGER NOT NULL,
    IdDoctor INTEGER NOT NULL,
    FOREIGN KEY (IdPatient) REFERENCES PATIENT_CLINICALDATA(IdPatient)
        ON DELETE CASCADE
        ON UPDATE CASCADE,  
    FOREIGN KEY (IdDoctor) REFERENCES DOCTOR(IdDoctor)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS WEARABLE_DEVICE (
    IdWearable INTEGER PRIMARY KEY AUTOINCREMENT,
    IdPatient INTEGER NOT NULL,
    FOREIGN KEY (IdPatient) REFERENCES PATIENT_CLINICALDATA(IdPatient)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS DATA (
    IdData INTEGER PRIMARY KEY AUTOINCREMENT, 
    NameData VARCHAR(20) CHECK ( NameData IN ('SBP','DBP','StepCount','SleepHours','SleepQualityIndex','Weight','ECG','HR','VO2Max','SPO2')),
    Date DATE,
    IdPatient INTEGER NOT NULL,
    IdWearable INTEGER NOT NULL,
    FOREIGN KEY (IdPatient) REFERENCES PATIENT_CLINICALDATA(IdPatient)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (IdWearable) REFERENCES WEARABLE_DEVICE(IdWearable)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS NUMERICAL_DATA (
    IdNumData INTEGER PRIMARY KEY,
    Date DATE,
    Max REAL,
    Min REAL,
    Mean REAL,
    StandardDeviation REAL,
    DayTime VARCHAR(5) CHECK (DayTime IN ('Day','Night')),
    FOREIGN KEY (IdNumData) REFERENCES DATA(IdData)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS SIGNALS (
    IdSignals INTEGER PRIMARY KEY,
    Value BLOB,
    Sampling_Freq INTEGER,
    FOREIGN KEY (IdSignals) REFERENCES DATA(IdData)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);



BEGIN TRANSACTION;

INSERT INTO USER (Id, Name, Surname, BirthDate, Address, PhoneNumber, Email, Username, Password, FiscalCode, UserType) VALUES
(1, 'Mario', 'Rossi', '1985-03-12', 'Via Roma 12', '+390212345001', 'm.rossi@mail.it', 'mrossi', 'pass001', 'RSSMRA85C12F205A', 'Patient'),
(2, 'Giulia', 'Bianchi', '1990-07-22', 'Via Verdi 8', '+390212345002', 'g.bianchi@mail.it', 'gbianchi', 'pass002', 'BNCGLI90L62F205B', 'Patient'),
(3, 'Luca', 'Verdi', '1978-11-04', 'Via Po 17', '+390112345003', 'l.verdi@mail.it', 'lverdi', 'pass003', 'VRDLCA78S04L219C', 'Patient'),
(4, 'Laura', 'Russo', '1995-01-18', 'Via Dante 5', '+390612345004', 'l.russo@mail.it', 'lrusso', 'pass004', 'RSSLRA95A58H501D', 'Patient'),
(5, 'Giuseppe', 'Ferrari', '1969-09-30', 'Via Garibaldi 21', '+390812345005', 'g.ferrari@mail.it', 'gferrari', 'pass005', 'FRRGPP69P30F839E', 'Patient'),
(6, 'Sara', 'Conti', '1988-05-09', 'Via Torino 14', '+390512345006', 's.conti@mail.it', 'sconti', 'pass006', 'CNTSRA88E49A944F', 'Patient'),
(7, 'Anna', 'Marini', '2001-02-27', 'Via Milano 3', '+390412345007', 'a.marini@mail.it', 'amarini', 'pass007', 'MRNNNA01B67L736G', 'Patient'),
(8, 'Marco', 'Galli', '1982-12-11', 'Via Napoli 19', '+390912345008', 'm.galli@mail.it', 'mgalli', 'pass008', 'GLLMRC82T11G273H', 'Patient'),
(9, 'Lucia', 'Romano', '1975-04-03', 'Via Firenze 6', '+390552345009', 'l.romano@mail.it', 'lromano', 'pass009', 'RMNLCU75D43D612I', 'Patient'),
(10, 'Francesca', 'Colombo', '1993-10-15', 'Via Genova 10', '+390102345010', 'f.colombo@mail.it', 'fcolombo', 'pass010', 'CLLFNC93R55C351L', 'Patient'),
(11, 'Andrea', 'Ricci', '1976-06-21', 'Via Cavour 2', '+390212345011', 'a.ricci@mail.it', 'aricci', 'doc001', 'RCCNDR76H21F205M', 'Doctor'),
(12, 'Elena', 'Moretti', '1981-08-14', 'Via Lazio 4', '+390612345012', 'e.moretti@mail.it', 'emoretti', 'doc002', 'MRTLNE81M54H501N', 'Doctor'),
(13, 'Paolo', 'Greco', '1972-03-09', 'Via Veneto 13', '+390812345013', 'p.greco@mail.it', 'pgreco', 'doc003', 'GRCPLA72C09F839P', 'Doctor'),
(14, 'Chiara', 'Lombardi', '1987-01-25', 'Via Umbria 9', '+390512345014', 'c.lombardi@mail.it', 'clombardi', 'doc004', 'LMBCHR87A65A944Q', 'Doctor'),
(15, 'Matteo', 'Fontana', '1979-07-02', 'Via Liguria 7', '+390102345015', 'm.fontana@mail.it', 'mfontana', 'doc005', 'FNTMTT79L02C351R', 'Doctor'),
(16, 'Valentina', 'Riva', '1984-11-19', 'Via Sicilia 20', '+390912345016', 'v.riva@mail.it', 'vriva', 'doc006', 'RVAVNT84S59G273S', 'Doctor'),
(17, 'Stefano', 'Costa', '1968-05-28', 'Via Puglia 11', '+390802345017', 's.costa@mail.it', 'scosta', 'doc007', 'CSTSFN68E28A662T', 'Doctor'),
(18, 'Martina', 'Barbieri', '1991-09-06', 'Via Emilia 18', '+390522345018', 'm.barbieri@mail.it', 'mbarbieri', 'doc008', 'BRBMTN91P46H223U', 'Doctor'),
(19, 'Davide', 'Serra', '1980-12-03', 'Via Sardegna 15', '+390702345019', 'd.serra@mail.it', 'dserra', 'doc009', 'SRRDVD80T03B354V', 'Doctor'),
(20, 'Federica', 'Villa', '1974-04-16', 'Via Trento 1', '+390462345020', 'f.villa@mail.it', 'fvilla', 'doc010', 'VLLFRC74D56L378Z', 'Doctor'),
(21, 'Roberto', 'Mancini', '1983-02-10', 'Via Aosta 5', '+390112345021', 'r.mancini@mail.it', 'rmancini', 'adm001', 'MNCRRT83B10L219A', 'Admin'),
(22, 'Simona', 'Rinaldi', '1986-06-23', 'Via Como 16', '+390312345022', 's.rinaldi@mail.it', 'srinaldi', 'adm002', 'RNLSMN86H63C933B', 'Admin'),
(23, 'Giorgio', 'Leone', '1977-10-12', 'Via Parma 8', '+390522345023', 'g.leone@mail.it', 'gleone', 'adm003', 'LNEGGR77R12G337C', 'Admin'),
(24, 'Ilaria', 'Santoro', '1992-03-05', 'Via Pisa 22', '+390502345024', 'i.santoro@mail.it', 'isantoro', 'adm004', 'SNTLRI92C45G702D', 'Admin'),
(25, 'Nicola', 'Caruso', '1989-08-29', 'Via Bari 6', '+390802345025', 'n.caruso@mail.it', 'ncaruso', 'adm005', 'CRSNCL89M29A662E', 'Admin'),
(26, 'Alessia', 'Ferri', '1996-12-17', 'Via Siena 3', '+390572345026', 'a.ferri@mail.it', 'aferri', 'adm006', 'FRRLSS96T57I726F', 'Admin'),
(27, 'Enrico', 'De Luca', '1971-01-31', 'Via Lecce 4', '+390832345027', 'e.deluca@mail.it', 'edeluca', 'adm007', 'DLCNRC71A31E506G', 'Admin'),
(28, 'Marta', 'Gatti', '1980-09-08', 'Via Rimini 12', '+390541345028', 'm.gatti@mail.it', 'mgatti', 'adm008', 'GTTMRT80P48H294H', 'Admin'),
(29, 'Fabio', 'Marchetti', '1985-05-20', 'Via Modena 2', '+390592345029', 'f.marchetti@mail.it', 'fmarchetti', 'adm009', 'MRCFBA85E20F257I', 'Admin'),
(30, 'Silvia', 'Bianco', '1990-11-02', 'Via Padova 9', '+390492345030', 's.bianco@mail.it', 'sbianco', 'adm010', 'BNCSLV90S42G224L', 'Admin');

INSERT INTO PATIENTCLINICALDATA (IdPatient, Height, Gender, RiskCode) VALUES
(1, 175.0, 'M', 2), (2, 168.0, 'F', 1), (3, 181.0, 'M', 3), (4, 164.0, 'F', 1), (5, 172.0, 'M', 4),
(6, 170.0, 'F', 2), (7, 160.0, 'F', 1), (8, 178.0, 'M', 2), (9, 166.0, 'F', 3), (10, 169.0, 'F', 1);

INSERT INTO DOCTOR (IdDoctor) VALUES
(11), (12), (13), (14), (15), (16), (17), (18), (19), (20);

INSERT INTO ADMIN (IdAdmin) VALUES
(21), (22), (23), (24), (25), (26), (27), (28), (29), (30);

INSERT INTO WEARABLE_DEVICE (IdWearable, IdPatient) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10);

INSERT INTO SUPPORT (IdSupport, Date, SupportType, IdRequester, IdAdmin) VALUES
(1, '2026-04-01', 'SupportCredentials', 1, 21),
(2, '2026-04-02', 'Wearable', 2, 22),
(3, '2026-04-03', 'InconsistentData', 3, 23),
(4, '2026-04-04', 'ScheduleIssue', 4, 24),
(5, '2026-04-05', 'Others', 5, 25),
(6, '2026-04-06', 'Wearable', 6, 26),
(7, '2026-04-07', 'SupportCredentials', 7, 27),
(8, '2026-04-08', 'InconsistentData', 8, 28),
(9, '2026-04-09', 'ScheduleIssue', 9, 29),
(10, '2026-04-10', 'Others', 10, 30);

INSERT INTO THERAPY (IdTherapy, Date, Description, IdDoctor, IdPatient) VALUES
(1, '2026-03-15', 'Monitoraggio pressione arteriosa per 30 giorni', 11, 1),
(2, '2026-03-16', 'Programma attivita fisica leggera e controllo sonno', 12, 2),
(3, '2026-03-17', 'Controllo frequenza cardiaca e saturazione', 13, 3),
(4, '2026-03-18', 'Follow-up nutrizionale con monitoraggio peso', 14, 4),
(5, '2026-03-19', 'Valutazione rischio cardiovascolare', 15, 5),
(6, '2026-03-20', 'Monitoraggio notturno della qualita del sonno', 16, 6),
(7, '2026-03-21', 'Controllo attivita giornaliera e passi', 17, 7),
(8, '2026-03-22', 'Valutazione performance cardiorespiratoria', 18, 8),
(9, '2026-03-23', 'Monitoraggio pressione e SpO2', 19, 9),
(10, '2026-03-24', 'Piano di controllo parametri generali', 20, 10);

INSERT INTO THR_PERSONALIZED (IdPatient, ThresholdValue, ThresholdSBP, ThresholdDBP, ThresholdSpO2, ThresholdUpperHeartRate, ThresholdLowerHeartRate, IdTherapy) VALUES
(1, 0.80, 140, 90, 94, 120, 50, 1),
(2, 0.70, 135, 85, 95, 115, 52, 2),
(3, 0.85, 145, 92, 94, 125, 48, 3),
(4, 0.65, 132, 84, 96, 110, 55, 4),
(5, 0.90, 150, 95, 93, 130, 48, 5),
(6, 0.75, 138, 88, 95, 118, 50, 6),
(7, 0.60, 130, 82, 96, 108, 55, 7),
(8, 0.72, 136, 86, 95, 116, 52, 8),
(9, 0.88, 148, 94, 93, 128, 48, 9),
(10, 0.68, 134, 84, 96, 112, 54, 10);

INSERT INTO APPOINTMENT (IdAppointment, Date, Time, Report, IdPatient, IdDoctor) VALUES
(1, '2026-05-06', '09:00', 'Pressione nella norma, proseguire monitoraggio', 1, 11),
(2, '2026-05-06', '09:30', 'Buona aderenza al piano di attivita', 2, 12),
(3, '2026-05-07', '10:00', 'Controllare picchi di frequenza cardiaca', 3, 13),
(4, '2026-05-07', '10:30', 'Peso stabile, nessuna variazione significativa', 4, 14),
(5, '2026-05-08', '11:00', 'Rischio elevato, programmato nuovo controllo', 5, 15),
(6, '2026-05-08', '11:30', 'Sonno irregolare, suggerita igiene del sonno', 6, 16),
(7, '2026-05-09', '12:00', 'Aumentare progressivamente i passi giornalieri', 7, 17),
(8, '2026-05-09', '12:30', 'VO2Max coerente con eta e anamnesi', 8, 18),
(9, '2026-05-10', '14:00', 'SpO2 da ricontrollare in fascia notturna', 9, 19),
(10, '2026-05-10', '14:30', 'Parametri generali stabili', 10, 20);

INSERT INTO DATA (IdData, NameData, Date, IdPatient, IdWearable) VALUES
(1, 'SBP', '2026-05-01', 1, 1),
(2, 'DBP', '2026-05-01', 2, 2),
(3, 'StepCount', '2026-05-01', 3, 3),
(4, 'SleepHours', '2026-05-01', 4, 4),
(5, 'SleepQualityIndex', '2026-05-01', 5, 5),
(6, 'Weight', '2026-05-01', 6, 6),
(7, 'HR', '2026-05-01', 7, 7),
(8, 'VO2Max', '2026-05-01', 8, 8),
(9, 'SPO2', '2026-05-01', 9, 9),
(10, 'SBP', '2026-05-02', 10, 10),
(11, 'ECG', '2026-05-01', 1, 1),
(12, 'ECG', '2026-05-01', 2, 2),
(13, 'ECG', '2026-05-01', 3, 3),
(14, 'ECG', '2026-05-01', 4, 4),
(15, 'ECG', '2026-05-01', 5, 5),
(16, 'ECG', '2026-05-02', 6, 6),
(17, 'ECG', '2026-05-02', 7, 7),
(18, 'ECG', '2026-05-02', 8, 8),
(19, 'ECG', '2026-05-02', 9, 9),
(20, 'ECG', '2026-05-02', 10, 10);

INSERT INTO NUMERICAL_DATA (IdNumData, Date, Max, Min, Mean, StandardDeviation, DayTime) VALUES
(1, '2026-05-01', 132, 118, 124.5, 4.6, 'Day'),
(2, '2026-05-01', 84, 72, 78.2, 3.1, 'Day'),
(3, '2026-05-01', 9200, 3100, 6450, 1550, 'Day'),
(4, '2026-05-01', 8.1, 5.9, 6.8, 0.7, 'Night'),
(5, '2026-05-01', 91, 64, 77.5, 8.4, 'Night'),
(6, '2026-05-01', 72.8, 72.1, 72.4, 0.2, 'Day'),
(7, '2026-05-01', 104, 58, 73.6, 10.8, 'Day'),
(8, '2026-05-01', 42.1, 38.9, 40.3, 1.1, 'Day'),
(9, '2026-05-01', 99, 95, 97.2, 1.0, 'Day'),
(10, '2026-05-02', 146, 128, 136.4, 6.2, 'Day');

INSERT INTO SIGNALS (IdSignals, Value, Sampling_Freq) VALUES
(11, X'0102030405060708', 250),
(12, X'1112131415161718', 250),
(13, X'2122232425262728', 250),
(14, X'3132333435363738', 250),
(15, X'4142434445464748', 250),
(16, X'5152535455565758', 250),
(17, X'6162636465666768', 250),
(18, X'7172737475767778', 250),
(19, X'8182838485868788', 250),
(20, X'9192939495969798', 250);

COMMIT;

SELECT 
    U.Id AS IdPatient,
    U.Name || ' ' || U.Surname AS PatientName,
    P.Gender,
    P.Height,
    P.RiskCode,
    T.Description AS Therapy,
    D.NameData,
    N.Mean,
    N.Max,
    N.Min,
    N.DayTime
FROM USER U
JOIN PATIENTCLINICALDATA P 
    ON U.Id = P.IdPatient
JOIN THERAPY T 
    ON P.IdPatient = T.IdPatient
JOIN DATA D 
    ON P.IdPatient = D.IdPatient
JOIN NUMERICAL_DATA N 
    ON D.IdData = N.IdNumData
ORDER BY U.Id;