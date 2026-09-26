CREATE DATABASE IF NOT EXISTS hospital_analysis;

USE hospital_analysis;

DROP TABLE IF EXISTS hospital_admissions;

CREATE TABLE hospital_admissions (
    sno INT,
    mrd_no VARCHAR(50),
    doa DATE,
    dod DATE,
    age INT,
    gender VARCHAR(10),
    rural VARCHAR(10),
    type_of_admission_emergency_opd VARCHAR(10),
    month_year DATE,
    duration_of_stay INT,
    duration_of_intensive_unit_stay INT,
    outcome VARCHAR(20),

    smoking TINYINT,
    alcohol TINYINT,
    dm TINYINT,
    htn TINYINT,
    cad TINYINT,
    prior_cmp TINYINT,
    ckd TINYINT,

    hb DECIMAL(10,2),
    tlc DECIMAL(10,2),
    platelets DECIMAL(10,2),
    glucose DECIMAL(10,2),
    urea DECIMAL(10,2),
    creatinine DECIMAL(10,2),
    bnp DECIMAL(12,2),
    raised_cardiac_enzymes TINYINT,
    ef DECIMAL(10,2),

    severe_anaemia TINYINT,
    anaemia TINYINT,
    stable_angina TINYINT,
    acs TINYINT,
    stemi TINYINT,
    atypical_chest_pain TINYINT,
    heart_failure TINYINT,
    hfref TINYINT,
    hfnef TINYINT,
    valvular TINYINT,
    chb TINYINT,
    sss TINYINT,
    aki TINYINT,
    cva_infarct TINYINT,
    cva_bleed TINYINT,
    af TINYINT,
    vt TINYINT,
    psvt TINYINT,
    congenital TINYINT,
    uti TINYINT,
    neuro_cardiogenic_syncope TINYINT,
    orthostatic TINYINT,
    infective_endocarditis TINYINT,
    dvt TINYINT,
    cardiogenic_shock TINYINT,
    shock TINYINT,
    pulmonary_embolism TINYINT,
    chest_infection TINYINT,

    admission_year INT,
    admission_month INT,
    admission_month_name VARCHAR(20),
    calculated_duration_of_stay INT
);
show tables;

describe hospital_admissions;

SELECT COUNT(*) AS total_rows
FROM hospital_admissions;

