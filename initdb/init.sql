CREATE TABLE medecins (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    specialite VARCHAR(50) DEFAULT 'Cardiologie',
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    date_naissance DATE,
    sexe CHAR(1)
    -- Pas encore de clé étrangère ici
);

CREATE TABLE dossiers_patients (
    id SERIAL PRIMARY KEY,
    patient_id INT,
    date_creation DATE DEFAULT CURRENT_DATE,
    historique TEXT
);

CREATE TABLE secretaire (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE cabinets_medicals (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    adresse VARCHAR(255)
);

CREATE TABLE dispositifs_medicaux (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    type VARCHAR(50),
    patient_id INT
);

CREATE TABLE comptes_rendus (
    id SERIAL PRIMARY KEY,
    dossier_patient_id INT,
    date_compte_rendu DATE DEFAULT CURRENT_DATE,
    contenu TEXT
);

CREATE TABLE alertes_medicales (
    id SERIAL PRIMARY KEY,
    patient_id INT,
    date_alerte DATE DEFAULT CURRENT_DATE,
    type_alert VARCHAR(50),
    message TEXT
);

ALTER TABLE dossiers_patients ADD CONSTRAINT fk_patient FOREIGN KEY (patient_id) REFERENCES patients(id);
ALTER TABLE dispositifs_medicaux ADD CONSTRAINT fk_patient_dm FOREIGN KEY (patient_id) REFERENCES patients(id);
ALTER TABLE comptes_rendus ADD CONSTRAINT fk_dossier FOREIGN KEY (dossier_patient_id) REFERENCES dossiers_patients(id);