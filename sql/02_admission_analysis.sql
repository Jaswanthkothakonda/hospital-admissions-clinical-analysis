USE hospital_analysis;

-- ============================================================
-- 1. Total Admissions
-- ============================================================

SELECT
    COUNT(*) AS total_admissions
FROM hospital_admissions;


-- ============================================================
-- 2. Admissions by Outcome
-- ============================================================

SELECT
    outcome,
    COUNT(*) AS admissions,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM hospital_admissions),
        2
    ) AS percentage
FROM hospital_admissions
GROUP BY outcome
ORDER BY admissions DESC;


-- ============================================================
-- 3. Admissions by Admission Type
-- E = Emergency
-- O = OPD
-- ============================================================

SELECT
    type_of_admission_emergency_opd AS admission_type,
    COUNT(*) AS admissions,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM hospital_admissions),
        2
    ) AS percentage
FROM hospital_admissions
GROUP BY type_of_admission_emergency_opd
ORDER BY admissions DESC;


-- ============================================================
-- 4. Admissions by Gender
-- ============================================================

SELECT
    gender,
    COUNT(*) AS admissions,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM hospital_admissions),
        2
    ) AS percentage
FROM hospital_admissions
GROUP BY gender
ORDER BY admissions DESC;


-- ============================================================
-- 5. Average Age
-- ============================================================

SELECT
    ROUND(AVG(age), 2) AS average_age
FROM hospital_admissions
WHERE age IS NOT NULL;


-- ============================================================
-- 6. Average Length of Stay
-- ============================================================

SELECT
    ROUND(AVG(duration_of_stay), 2) AS average_length_of_stay
FROM hospital_admissions
WHERE duration_of_stay IS NOT NULL;


-- ============================================================
-- 7. Average Length of Stay by Outcome
-- ============================================================

SELECT
    outcome,
    COUNT(*) AS admissions,
    ROUND(AVG(duration_of_stay), 2) AS average_length_of_stay
FROM hospital_admissions
WHERE duration_of_stay IS NOT NULL
GROUP BY outcome
ORDER BY average_length_of_stay DESC;


-- ============================================================
-- 8. Outcome by Admission Type
-- ============================================================

SELECT
    type_of_admission_emergency_opd AS admission_type,
    outcome,
    COUNT(*) AS admissions
FROM hospital_admissions
GROUP BY
    type_of_admission_emergency_opd,
    outcome
ORDER BY
    admission_type,
    admissions DESC;


-- ============================================================
-- 9. Outcome by Gender
-- ============================================================

SELECT
    gender,
    outcome,
    COUNT(*) AS admissions
FROM hospital_admissions
GROUP BY
    gender,
    outcome
ORDER BY
    gender,
    admissions DESC;


-- ============================================================
-- 10. Average Glucose by Outcome
-- ============================================================

SELECT
    outcome,
    ROUND(AVG(glucose), 2) AS average_glucose
FROM hospital_admissions
WHERE glucose IS NOT NULL
GROUP BY outcome
ORDER BY average_glucose DESC;


-- ============================================================
-- 11. Average Ejection Fraction by Outcome
-- ============================================================

SELECT
    outcome,
    ROUND(AVG(ef), 2) AS average_ejection_fraction
FROM hospital_admissions
WHERE ef IS NOT NULL
GROUP BY outcome
ORDER BY average_ejection_fraction DESC;


-- ============================================================
-- 12. Medical Condition Prevalence
-- ============================================================

SELECT
    'CAD' AS medical_condition,
    SUM(CASE WHEN cad = 1 THEN 1 ELSE 0 END) AS admissions
FROM hospital_admissions

UNION ALL

SELECT
    'HTN',
    SUM(CASE WHEN htn = 1 THEN 1 ELSE 0 END)
FROM hospital_admissions

UNION ALL

SELECT
    'ACS',
    SUM(CASE WHEN acs = 1 THEN 1 ELSE 0 END)
FROM hospital_admissions

UNION ALL

SELECT
    'Diabetes',
    SUM(CASE WHEN dm = 1 THEN 1 ELSE 0 END)
FROM hospital_admissions

UNION ALL

SELECT
    'Heart Failure',
    SUM(CASE WHEN heart_failure = 1 THEN 1 ELSE 0 END)
FROM hospital_admissions

UNION ALL

SELECT
    'AKI',
    SUM(CASE WHEN aki = 1 THEN 1 ELSE 0 END)
FROM hospital_admissions

UNION ALL

SELECT
    'Anaemia',
    SUM(CASE WHEN anaemia = 1 THEN 1 ELSE 0 END)
FROM hospital_admissions

UNION ALL

SELECT
    'CKD',
    SUM(CASE WHEN ckd = 1 THEN 1 ELSE 0 END)
FROM hospital_admissions

UNION ALL

SELECT
    'STEMI',
    SUM(CASE WHEN stemi = 1 THEN 1 ELSE 0 END)
FROM hospital_admissions

UNION ALL

SELECT
    'Stable Angina',
    SUM(CASE WHEN stable_angina = 1 THEN 1 ELSE 0 END)
FROM hospital_admissions

ORDER BY admissions DESC;

-- ============================================================
-- 13. Missing Values in Key Clinical Fields
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    SUM(bnp IS NULL) AS missing_bnp,
    SUM(ef IS NULL) AS missing_ef,
    SUM(glucose IS NULL) AS missing_glucose,
    SUM(hb IS NULL) AS missing_hb,
    SUM(tlc IS NULL) AS missing_tlc,
    SUM(platelets IS NULL) AS missing_platelets,
    SUM(creatinine IS NULL) AS missing_creatinine,
    SUM(urea IS NULL) AS missing_urea
FROM hospital_admissions;


-- ============================================================
-- 14. Emergency Admission Outcomes
-- ============================================================

SELECT
    outcome,
    COUNT(*) AS emergency_admissions
FROM hospital_admissions
WHERE type_of_admission_emergency_opd = 'E'
GROUP BY outcome
ORDER BY emergency_admissions DESC;


-- ============================================================
-- 15. OPD Admission Outcomes
-- ============================================================

SELECT
    outcome,
    COUNT(*) AS opd_admissions
FROM hospital_admissions
WHERE type_of_admission_emergency_opd = 'O'
GROUP BY outcome
ORDER BY opd_admissions DESC;