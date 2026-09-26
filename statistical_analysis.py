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

df["dod"] = pd.to_datetime(
    df["dod"],
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
print("HOSPITAL DATA - STATISTICAL ANALYSIS")
print("=" * 80)


# ---------------------------------------------------------
# 1. Outcome percentage by admission type
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("1. OUTCOME PERCENTAGE BY ADMISSION TYPE")
print("=" * 80)

outcome_by_admission = pd.crosstab(
    df["type_of_admission_emergency_opd"],
    df["outcome"],
    normalize="index"
) * 100

print(
    outcome_by_admission.round(2)
)


# ---------------------------------------------------------
# 2. Outcome percentage by gender
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("2. OUTCOME PERCENTAGE BY GENDER")
print("=" * 80)

outcome_by_gender = pd.crosstab(
    df["gender"],
    df["outcome"],
    normalize="index"
) * 100

print(
    outcome_by_gender.round(2)
)


# ---------------------------------------------------------
# 3. Outcome percentage by age group
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("3. OUTCOME PERCENTAGE BY AGE GROUP")
print("=" * 80)

outcome_by_age = pd.crosstab(
    df["age_group"],
    df["outcome"],
    normalize="index"
) * 100

print(
    outcome_by_age.round(2)
)


# ---------------------------------------------------------
# 4. Length of stay by outcome
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("4. LENGTH OF STAY BY OUTCOME")
print("=" * 80)

stay_by_outcome = (
    df.groupby("outcome")["duration_of_stay"]
    .agg(
        [
            "count",
            "mean",
            "median",
            "min",
            "max"
        ]
    )
)

print(
    stay_by_outcome.round(2)
)


# ---------------------------------------------------------
# 5. Length of stay by admission type
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("5. LENGTH OF STAY BY ADMISSION TYPE")
print("=" * 80)

stay_by_admission = (
    df.groupby(
        "type_of_admission_emergency_opd"
    )["duration_of_stay"]
    .agg(
        [
            "count",
            "mean",
            "median",
            "min",
            "max"
        ]
    )
)

print(
    stay_by_admission.round(2)
)


# ---------------------------------------------------------
# 6. Major conditions by outcome
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

print("\n")
print("=" * 80)
print("6. CONDITION PREVALENCE BY OUTCOME")
print("=" * 80)

condition_outcome_results = []

for condition in conditions:

    if condition not in df.columns:
        continue

    for outcome in sorted(
        df["outcome"].dropna().unique()
    ):

        subset = df[
            df["outcome"] == outcome
        ]

        valid = subset[condition].notna().sum()

        positive = (
            subset[condition] == 1
        ).sum()

        if valid > 0:

            percentage = (
                positive / valid
            ) * 100

            condition_outcome_results.append(
                {
                    "condition": condition,
                    "outcome": outcome,
                    "count": positive,
                    "percentage": percentage
                }
            )


condition_outcome_df = pd.DataFrame(
    condition_outcome_results
)

print(
    condition_outcome_df.round(2)
    .to_string(index=False)
)


# ---------------------------------------------------------
# 7. Average age by outcome
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("7. AVERAGE AGE BY OUTCOME")
print("=" * 80)

age_by_outcome = (
    df.groupby("outcome")["age"]
    .agg(
        [
            "count",
            "mean",
            "median",
            "min",
            "max"
        ]
    )
)

print(
    age_by_outcome.round(2)
)


# ---------------------------------------------------------
# 8. Emergency vs OPD outcome counts
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("8. EMERGENCY VS OPD OUTCOME COUNTS")
print("=" * 80)

emergency_opd_outcomes = pd.crosstab(
    df["type_of_admission_emergency_opd"],
    df["outcome"]
)

print(
    emergency_opd_outcomes
)


# ---------------------------------------------------------
# 9. EF by outcome
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("9. EJECTION FRACTION BY OUTCOME")
print("=" * 80)

ef_by_outcome = (
    df.groupby("outcome")["ef"]
    .agg(
        [
            "count",
            "mean",
            "median",
            "min",
            "max"
        ]
    )
)

print(
    ef_by_outcome.round(2)
)


# ---------------------------------------------------------
# 10. Glucose by outcome
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("10. GLUCOSE BY OUTCOME")
print("=" * 80)

glucose_by_outcome = (
    df.groupby("outcome")["glucose"]
    .agg(
        [
            "count",
            "mean",
            "median",
            "min",
            "max"
        ]
    )
)

print(
    glucose_by_outcome.round(2)
)


# ---------------------------------------------------------
# Save analysis tables
# ---------------------------------------------------------

outcome_by_admission.round(2).to_csv(
    OUTPUT_DIR / "outcome_by_admission_type.csv"
)

outcome_by_gender.round(2).to_csv(
    OUTPUT_DIR / "outcome_by_gender.csv"
)

outcome_by_age.round(2).to_csv(
    OUTPUT_DIR / "outcome_by_age_group.csv"
)

stay_by_outcome.round(2).to_csv(
    OUTPUT_DIR / "length_of_stay_by_outcome.csv"
)

stay_by_admission.round(2).to_csv(
    OUTPUT_DIR / "length_of_stay_by_admission.csv"
)

condition_outcome_df.round(2).to_csv(
    OUTPUT_DIR / "condition_by_outcome.csv",
    index=False
)

age_by_outcome.round(2).to_csv(
    OUTPUT_DIR / "age_by_outcome.csv"
)

ef_by_outcome.round(2).to_csv(
    OUTPUT_DIR / "ef_by_outcome.csv"
)

glucose_by_outcome.round(2).to_csv(
    OUTPUT_DIR / "glucose_by_outcome.csv"
)


# ---------------------------------------------------------
# Completion
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("STATISTICAL ANALYSIS COMPLETE")
print("=" * 80)

print("\nAnalysis tables saved to:")
print(OUTPUT_DIR)