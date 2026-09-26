import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"

input_file = OUTPUT_DIR / "hospital_admission_cleaned.csv"

df = pd.read_csv(input_file)

# Convert dates again after loading CSV
df["doa"] = pd.to_datetime(df["doa"], errors="coerce")
df["dod"] = pd.to_datetime(df["dod"], errors="coerce")


# ---------------------------------------------------------
# Basic dataset overview
# ---------------------------------------------------------

print("=" * 70)
print("HOSPITAL DATA ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)

print("\nTotal admissions:")
print(len(df))

print("\nDate range:")

print("First admission:", df["doa"].min())
print("Last admission :", df["doa"].max())


# ---------------------------------------------------------
# 1. Gender distribution
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("GENDER DISTRIBUTION")
print("=" * 70)

gender_counts = df["gender"].value_counts()

print(gender_counts)

print("\nGender percentage:")

print(
    (gender_counts / len(df) * 100)
    .round(2)
)


# ---------------------------------------------------------
# 2. Outcome distribution
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("OUTCOME DISTRIBUTION")
print("=" * 70)

outcome_counts = df["outcome"].value_counts()

print(outcome_counts)

print("\nOutcome percentage:")

print(
    (outcome_counts / len(df) * 100)
    .round(2)
)


# ---------------------------------------------------------
# 3. Admission type
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("ADMISSION TYPE")
print("=" * 70)

admission_type_counts = (
    df["type_of_admission_emergency_opd"]
    .value_counts()
)

print(admission_type_counts)

print("\nAdmission type percentage:")

print(
    (admission_type_counts / len(df) * 100)
    .round(2)
)


# ---------------------------------------------------------
# 4. Rural / Urban distribution
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("RURAL / URBAN DISTRIBUTION")
print("=" * 70)

location_counts = df["rural"].value_counts()

print(location_counts)

print("\nPercentage:")

print(
    (location_counts / len(df) * 100)
    .round(2)
)


# ---------------------------------------------------------
# 5. Age statistics
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("AGE ANALYSIS")
print("=" * 70)

print(df["age"].describe())

print("\nAverage age:")
print(round(df["age"].mean(), 2))

print("\nMedian age:")
print(df["age"].median())


# ---------------------------------------------------------
# 6. Age groups
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

age_group_counts = (
    df["age_group"]
    .value_counts()
    .sort_index()
)

print("\n")
print("Age group distribution:")

print(age_group_counts)


# ---------------------------------------------------------
# 7. Length of stay
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("LENGTH OF STAY")
print("=" * 70)

print(
    df["duration_of_stay"]
    .describe()
)

print("\nAverage length of stay:")
print(
    round(
        df["duration_of_stay"].mean(),
        2
    )
)

print("\nMedian length of stay:")
print(
    df["duration_of_stay"].median()
)


# ---------------------------------------------------------
# 8. Medical condition prevalence
# ---------------------------------------------------------

medical_conditions = [
    "dm",
    "htn",
    "cad",
    "prior_cmp",
    "ckd",
    "anaemia",
    "stable_angina",
    "acs",
    "stemi",
    "atypical_chest_pain",
    "heart_failure",
    "hfref",
    "hfnef",
    "valvular",
    "aki",
    "af",
    "vt",
    "uti",
    "dvt",
    "shock",
    "pulmonary_embolism",
    "chest_infection"
]

condition_results = []

for condition in medical_conditions:

    if condition in df.columns:

        total = df[condition].notna().sum()

        positive = (
            df[condition] == 1
        ).sum()

        if total > 0:

            percentage = (
                positive / total
            ) * 100

            condition_results.append(
                {
                    "condition": condition,
                    "count": positive,
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

print("\n")
print("=" * 70)
print("MEDICAL CONDITION PREVALENCE")
print("=" * 70)

print(
    condition_df.to_string(
        index=False
    )
)


# ---------------------------------------------------------
# 9. Monthly admissions
# ---------------------------------------------------------

monthly_admissions = (
    df.dropna(subset=["doa"])
    .groupby(
        df["doa"].dt.to_period("M")
    )
    .size()
)

print("\n")
print("=" * 70)
print("MONTHLY ADMISSIONS")
print("=" * 70)

print(monthly_admissions)


# ---------------------------------------------------------
# 10. Outcome by gender
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("OUTCOME BY GENDER")
print("=" * 70)

outcome_gender = pd.crosstab(
    df["gender"],
    df["outcome"]
)

print(outcome_gender)


# ---------------------------------------------------------
# 11. Outcome by admission type
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("OUTCOME BY ADMISSION TYPE")
print("=" * 70)

outcome_admission_type = pd.crosstab(
    df["type_of_admission_emergency_opd"],
    df["outcome"]
)

print(outcome_admission_type)


# ---------------------------------------------------------
# 12. Clinical measurements summary
# ---------------------------------------------------------

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

print("\n")
print("=" * 70)
print("CLINICAL MEASUREMENTS")
print("=" * 70)

print(
    df[clinical_columns]
    .describe()
    .transpose()
)


# ---------------------------------------------------------
# VISUALIZATIONS
# ---------------------------------------------------------

sns.set_theme(style="whitegrid")


# ---------------------------------------------------------
# Chart 1 - Gender
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

gender_counts.plot(
    kind="bar"
)

plt.title("Admissions by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Admissions")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "01_admissions_by_gender.png",
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# Chart 2 - Outcome
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

outcome_counts.plot(
    kind="bar"
)

plt.title("Admission Outcomes")
plt.xlabel("Outcome")
plt.ylabel("Number of Admissions")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "02_admission_outcomes.png",
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# Chart 3 - Age distribution
# ---------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.hist(
    df["age"].dropna(),
    bins=20
)

plt.title("Age Distribution of Admissions")
plt.xlabel("Age")
plt.ylabel("Number of Admissions")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "03_age_distribution.png",
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# Chart 4 - Age groups
# ---------------------------------------------------------

plt.figure(figsize=(9, 5))

age_group_counts.plot(
    kind="bar"
)

plt.title("Admissions by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Admissions")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "04_admissions_by_age_group.png",
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# Chart 5 - Admission type
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

admission_type_counts.plot(
    kind="bar"
)

plt.title("Admissions by Admission Type")
plt.xlabel("Admission Type")
plt.ylabel("Number of Admissions")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "05_admission_type.png",
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# Chart 6 - Rural / Urban
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

location_counts.plot(
    kind="bar"
)

plt.title("Admissions by Location Type")
plt.xlabel("Location Type")
plt.ylabel("Number of Admissions")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "06_rural_urban.png",
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# Chart 7 - Monthly admissions
# ---------------------------------------------------------

plt.figure(figsize=(12, 5))

monthly_admissions.plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Hospital Admissions")
plt.xlabel("Month")
plt.ylabel("Number of Admissions")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "07_monthly_admissions.png",
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# Chart 8 - Medical conditions
# ---------------------------------------------------------

top_conditions = condition_df.head(10)

plt.figure(figsize=(10, 6))

plt.barh(
    top_conditions["condition"],
    top_conditions["percentage"]
)

plt.title("Top Medical Conditions by Admission Percentage")
plt.xlabel("Percentage of Records")
plt.ylabel("Condition")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "08_medical_conditions.png",
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# Chart 9 - Length of stay
# ---------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.hist(
    df["duration_of_stay"].dropna(),
    bins=20
)

plt.title("Length of Hospital Stay")
plt.xlabel("Duration of Stay (Days)")
plt.ylabel("Number of Admissions")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "09_length_of_stay.png",
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# Completion
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("EXPLORATORY ANALYSIS COMPLETE")
print("=" * 70)

print("\nCharts saved to:")

print(OUTPUT_DIR)