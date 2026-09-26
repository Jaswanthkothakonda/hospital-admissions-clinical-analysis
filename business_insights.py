import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"

input_file = OUTPUT_DIR / "hospital_admission_cleaned.csv"


# ---------------------------------------------------------
# Load cleaned data
# ---------------------------------------------------------

df = pd.read_csv(input_file)


# ---------------------------------------------------------
# Convert dates
# ---------------------------------------------------------

df["doa"] = pd.to_datetime(
    df["doa"],
    errors="coerce"
)


# ---------------------------------------------------------
# Create age groups
# ---------------------------------------------------------

age_bins = [
    0,
    18,
    30,
    45,
    60,
    75,
    200
]

age_labels = [
    "0-17",
    "18-29",
    "30-44",
    "45-59",
    "60-74",
    "75+"
]

df["age_group"] = pd.cut(
    df["age"],
    bins=age_bins,
    labels=age_labels,
    right=False
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

print("=" * 80)
print("HOSPITAL DATA ANALYSIS - BUSINESS INSIGHTS")
print("=" * 80)


# ---------------------------------------------------------
# 1. Overall outcome insights
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("1. OVERALL OUTCOME INSIGHTS")
print("=" * 80)

outcome_counts = df["outcome"].value_counts()

outcome_percentages = (
    df["outcome"]
    .value_counts(normalize=True)
    * 100
)

print("\nOutcome counts:")
print(outcome_counts)

print("\nOutcome percentages:")
print(
    outcome_percentages.round(2)
)


# ---------------------------------------------------------
# 2. Admission type insights
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("2. ADMISSION TYPE INSIGHTS")
print("=" * 80)

admission_counts = (
    df["type_of_admission_emergency_opd"]
    .value_counts()
)

admission_percentages = (
    df["type_of_admission_emergency_opd"]
    .value_counts(normalize=True)
    * 100
)

print("\nAdmission counts:")
print(admission_counts)

print("\nAdmission percentages:")
print(
    admission_percentages.round(2)
)


# ---------------------------------------------------------
# 3. Emergency vs OPD outcomes
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("3. EMERGENCY VS OPD OUTCOMES")
print("=" * 80)

admission_outcome = pd.crosstab(
    df["type_of_admission_emergency_opd"],
    df["outcome"],
    normalize="index"
) * 100

print(
    admission_outcome.round(2)
)


# ---------------------------------------------------------
# 4. Age group insights
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("4. AGE GROUP INSIGHTS")
print("=" * 80)

age_distribution = (
    df["age_group"]
    .value_counts()
    .sort_index()
)

age_percentage = (
    df["age_group"]
    .value_counts(normalize=True)
    .sort_index()
    * 100
)

print("\nAge group counts:")
print(age_distribution)

print("\nAge group percentages:")
print(
    age_percentage.round(2)
)


# ---------------------------------------------------------
# 5. Length of stay insights
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("5. LENGTH OF STAY INSIGHTS")
print("=" * 80)

average_stay = df["duration_of_stay"].mean()
median_stay = df["duration_of_stay"].median()

print("\nAverage length of stay:")
print(round(average_stay, 2))

print("\nMedian length of stay:")
print(round(median_stay, 2))


stay_by_admission = (
    df.groupby(
        "type_of_admission_emergency_opd"
    )["duration_of_stay"]
    .mean()
)

print("\nAverage stay by admission type:")
print(
    stay_by_admission.round(2)
)


# ---------------------------------------------------------
# 6. Medical condition insights
# ---------------------------------------------------------

conditions = [
    "cad",
    "htn",
    "acs",
    "dm",
    "heart_failure",
    "aki",
    "anaemia",
    "ckd",
    "stemi"
]

condition_results = []

for condition in conditions:

    if condition not in df.columns:
        continue

    valid_values = df[condition].notna().sum()

    positive_values = (
        df[condition] == 1
    ).sum()

    if valid_values > 0:

        percentage = (
            positive_values /
            valid_values
        ) * 100

        condition_results.append(
            {
                "condition": condition,
                "count": positive_values,
                "percentage": percentage
            }
        )


condition_df = pd.DataFrame(
    condition_results
)

condition_df = condition_df.sort_values(
    "percentage",
    ascending=False
)

print("\nMedical condition prevalence:")
print(
    condition_df.round(2)
    .to_string(index=False)
)


# ---------------------------------------------------------
# 7. Clinical measurements
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("7. CLINICAL MEASUREMENT INSIGHTS")
print("=" * 80)

clinical_columns = [
    "hb",
    "tlc",
    "platelets",
    "glucose",
    "urea",
    "creatinine",
    "bnp",
    "ef"
]

clinical_columns = [
    column
    for column in clinical_columns
    if column in df.columns
]

clinical_summary = (
    df[clinical_columns]
    .describe()
    .T
)

print(
    clinical_summary.round(2)
)


# ---------------------------------------------------------
# 8. Outcome by age
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("8. OUTCOME BY AGE GROUP")
print("=" * 80)

age_outcome = pd.crosstab(
    df["age_group"],
    df["outcome"],
    normalize="index"
) * 100

print(
    age_outcome.round(2)
)


# ---------------------------------------------------------
# 9. Outcome by gender
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("9. OUTCOME BY GENDER")
print("=" * 80)

gender_outcome = pd.crosstab(
    df["gender"],
    df["outcome"],
    normalize="index"
) * 100

print(
    gender_outcome.round(2)
)


# ---------------------------------------------------------
# 10. Monthly admission volume
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("10. MONTHLY ADMISSION VOLUME")
print("=" * 80)

monthly_admissions = (
    df.groupby(
        df["doa"].dt.to_period("M")
    )
    .size()
)

print(
    monthly_admissions
)


# ---------------------------------------------------------
# Save business analysis tables
# ---------------------------------------------------------

outcome_counts.to_csv(
    OUTPUT_DIR / "business_outcome_counts.csv"
)

outcome_percentages.round(2).to_csv(
    OUTPUT_DIR / "business_outcome_percentages.csv"
)

admission_counts.to_csv(
    OUTPUT_DIR / "business_admission_counts.csv"
)

admission_percentages.round(2).to_csv(
    OUTPUT_DIR / "business_admission_percentages.csv"
)

age_distribution.to_csv(
    OUTPUT_DIR / "business_age_distribution.csv"
)

age_percentage.round(2).to_csv(
    OUTPUT_DIR / "business_age_percentage.csv"
)

condition_df.round(2).to_csv(
    OUTPUT_DIR / "business_condition_prevalence.csv",
    index=False
)

clinical_summary.round(2).to_csv(
    OUTPUT_DIR / "business_clinical_summary.csv"
)

monthly_admissions.to_csv(
    OUTPUT_DIR / "business_monthly_admissions.csv"
)


# ---------------------------------------------------------
# Completion
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("BUSINESS INSIGHTS ANALYSIS COMPLETE")
print("=" * 80)

print("\nBusiness analysis tables saved to:")
print(OUTPUT_DIR)