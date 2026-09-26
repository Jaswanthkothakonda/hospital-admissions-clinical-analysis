USE hospital_analysis;

-- ============================================================
-- 1. Total Rows
-- ============================================================

SELECT
    COUNT(*) AS total_rows
FROM hospital_admissions;


-- ============================================================
-- 2. Distinct SNO Check
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT sno) AS distinct_sno
FROM hospital_admissions;


-- ============================================================
-- 3. Duplicate SNO Values
-- ============================================================

SELECT
    sno,
    COUNT(*) AS duplicate_count
FROM hospital_admissions
GROUP BY sno
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;


-- ============================================================
-- 4. Missing Core Fields
-- ============================================================

SELECT
    SUM(mrd_no IS NULL) AS missing_mrd_no,
    SUM(age IS NULL) AS missing_age,
    SUM(gender IS NULL) AS missing_gender,
    SUM(outcome IS NULL) AS missing_outcome,
    SUM(type_of_admission_emergency_opd IS NULL) AS missing_admission_type
FROM hospital_admissions;


-- ============================================================
-- 5. Invalid Gender Values
-- ============================================================

SELECT
    gender,
    COUNT(*) AS record_count
FROM hospital_admissions
WHERE gender IS NOT NULL
  AND gender NOT IN ('M', 'F')
GROUP BY gender;


-- ============================================================
-- 6. Invalid Outcome Values
-- ============================================================

SELECT
    outcome,
    COUNT(*) AS record_count
FROM hospital_admissions
WHERE outcome IS NOT NULL
  AND outcome NOT IN ('DISCHARGE', 'EXPIRY', 'DAMA')
GROUP BY outcome;


-- ============================================================
-- 7. Invalid Admission Type Values
-- ============================================================

SELECT
    type_of_admission_emergency_opd AS admission_type,
    COUNT(*) AS record_count
FROM hospital_admissions
WHERE type_of_admission_emergency_opd IS NOT NULL
  AND type_of_admission_emergency_opd NOT IN ('E', 'O')
GROUP BY type_of_admission_emergency_opd;


-- ============================================================
-- 8. Age Range Check
-- ============================================================

SELECT
    COUNT(*) AS invalid_age_records
FROM hospital_admissions
WHERE age IS NOT NULL
  AND (age < 0 OR age > 120);


-- ============================================================
-- 9. Length of Stay Check
-- ============================================================

SELECT
    COUNT(*) AS invalid_duration_records
FROM hospital_admissions
WHERE duration_of_stay IS NOT NULL
  AND duration_of_stay < 0;


-- ============================================================
-- 10. Date Consistency Check
-- ============================================================

SELECT
    COUNT(*) AS invalid_date_order
FROM hospital_admissions
WHERE doa IS NOT NULL
  AND dod IS NOT NULL
  AND dod < doa;


-- ============================================================
-- 11. Missing Clinical Measurements
-- ============================================================

SELECT
    SUM(hb IS NULL) AS missing_hb,
    SUM(tlc IS NULL) AS missing_tlc,
    SUM(platelets IS NULL) AS missing_platelets,
    SUM(glucose IS NULL) AS missing_glucose,
    SUM(urea IS NULL) AS missing_urea,
    SUM(creatinine IS NULL) AS missing_creatinine,
    SUM(bnp IS NULL) AS missing_bnp,
    SUM(ef IS NULL) AS missing_ef
FROM hospital_admissions;


-- ============================================================
-- 12. Invalid Binary Clinical Flags
-- ============================================================

SELECT
    SUM(cad IS NOT NULL AND cad NOT IN (0, 1)) AS invalid_cad,
    SUM(htn IS NOT NULL AND htn NOT IN (0, 1)) AS invalid_htn,
    SUM(dm IS NOT NULL AND dm NOT IN (0, 1)) AS invalid_dm,
    SUM(ckd IS NOT NULL AND ckd NOT IN (0, 1)) AS invalid_ckd,
    SUM(aki IS NOT NULL AND aki NOT IN (0, 1)) AS invalid_aki,
    SUM(heart_failure IS NOT NULL AND heart_failure NOT IN (0, 1)) AS invalid_heart_failure,
    SUM(stemi IS NOT NULL AND stemi NOT IN (0, 1)) AS invalid_stemi,
    SUM(cva_infract IS NOT NULL AND cva_infract NOT IN (0, 1)) AS invalid_cva_infract
FROM hospital_admissions;


-- ============================================================
-- 13. Missing Admission Dates
-- ============================================================

SELECT
    SUM(doa IS NULL) AS missing_doa,
    SUM(dod IS NULL) AS missing_dod,
    SUM(month_year IS NULL) AS missing_month_year
FROM hospital_admissions;


-- ============================================================
-- 14. Data Quality Summary
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT sno) AS distinct_sno,
    SUM(age IS NULL) AS missing_age,
    SUM(gender IS NULL) AS missing_gender,
    SUM(outcome IS NULL) AS missing_outcome,
    SUM(doa IS NULL) AS missing_doa,
    SUM(bnp IS NULL) AS missing_bnp,
    SUM(ef IS NULL) AS missing_ef
FROM hospital_admissions;