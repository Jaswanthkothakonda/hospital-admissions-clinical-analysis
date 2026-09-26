import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "outputs"
CHART_DIR = BASE_DIR / "charts"

CHART_DIR.mkdir(exist_ok=True)


# =========================================================
# LOAD CLEANED DATA
# =========================================================

input_file = OUTPUT_DIR / "hospital_admission_cleaned.csv"

df = pd.read_csv(input_file)


# =========================================================
# DATE CONVERSION
# =========================================================

df["doa"] = pd.to_datetime(
    df["doa"],
    errors="coerce"
)


# =========================================================
# AGE GROUPS
# =========================================================

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


# =========================================================
# 1. OUTCOME DISTRIBUTION
# =========================================================

outcome_counts = (
    df["outcome"]
    .value_counts()
)

plt.figure(figsize=(9, 6))

plt.bar(
    outcome_counts.index,
    outcome_counts.values
)

plt.title(
    "Hospital Admission Outcomes"
)

plt.xlabel(
    "Outcome"
)

plt.ylabel(
    "Number of Patients"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "01_outcome_distribution.png",
    dpi=300
)

plt.close()


# =========================================================
# 2. EMERGENCY VS OPD ADMISSIONS
# =========================================================

admission_counts = (
    df["type_of_admission_emergency_opd"]
    .value_counts()
)

admission_labels = {
    "E": "Emergency",
    "O": "OPD"
}

admission_counts.index = [
    admission_labels.get(
        value,
        value
    )
    for value in admission_counts.index
]

plt.figure(figsize=(9, 6))

plt.bar(
    admission_counts.index,
    admission_counts.values
)

plt.title(
    "Emergency vs OPD Admissions"
)

plt.xlabel(
    "Admission Type"
)

plt.ylabel(
    "Number of Patients"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "02_admission_type.png",
    dpi=300
)

plt.close()


# =========================================================
# 3. AGE GROUP DISTRIBUTION
# =========================================================

age_counts = (
    df["age_group"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(10, 6))

plt.bar(
    age_counts.index.astype(str),
    age_counts.values
)

plt.title(
    "Patient Distribution by Age Group"
)

plt.xlabel(
    "Age Group"
)

plt.ylabel(
    "Number of Patients"
)

plt.xticks(
    rotation=0
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "03_age_group_distribution.png",
    dpi=300
)

plt.close()


# =========================================================
# 4. MONTHLY ADMISSION TREND
# =========================================================

monthly_admissions = (
    df.groupby(
        df["doa"].dt.to_period("M")
    )
    .size()
)

monthly_dates = (
    monthly_admissions
    .index
    .to_timestamp()
)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_dates,
    monthly_admissions.values,
    marker="o"
)

plt.title(
    "Monthly Hospital Admissions"
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Number of Admissions"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "04_monthly_admissions.png",
    dpi=300
)

plt.close()


# =========================================================
# 5. MEDICAL CONDITION PREVALENCE
# =========================================================

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
            (
                condition,
                percentage
            )
        )


condition_df = pd.DataFrame(
    condition_results,
    columns=[
        "condition",
        "percentage"
    ]
)

condition_df = condition_df.sort_values(
    "percentage",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    condition_df["condition"],
    condition_df["percentage"]
)

plt.title(
    "Medical Condition Prevalence"
)

plt.xlabel(
    "Prevalence (%)"
)

plt.ylabel(
    "Medical Condition"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "05_condition_prevalence.png",
    dpi=300
)

plt.close()


# =========================================================
# 6. LENGTH OF STAY BY OUTCOME
# =========================================================

stay_by_outcome = (
    df.groupby("outcome")[
        "duration_of_stay"
    ]
    .mean()
    .sort_values()
)

plt.figure(figsize=(9, 6))

plt.bar(
    stay_by_outcome.index,
    stay_by_outcome.values
)

plt.title(
    "Average Length of Stay by Outcome"
)

plt.xlabel(
    "Outcome"
)

plt.ylabel(
    "Average Length of Stay (Days)"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "06_length_of_stay_by_outcome.png",
    dpi=300
)

plt.close()


# =========================================================
# 7. OUTCOME PERCENTAGE BY ADMISSION TYPE
# =========================================================

admission_outcome = (
    pd.crosstab(
        df["type_of_admission_emergency_opd"],
        df["outcome"],
        normalize="index"
    )
    * 100
)

admission_outcome = admission_outcome.rename(
    index={
        "E": "Emergency",
        "O": "OPD"
    }
)

outcome_order = [
    "DISCHARGE",
    "EXPIRY",
    "DAMA"
]

available_outcomes = [
    outcome
    for outcome in outcome_order
    if outcome in admission_outcome.columns
]

admission_outcome = (
    admission_outcome[
        available_outcomes
    ]
)

plt.figure(figsize=(10, 6))

x = range(
    len(admission_outcome.index)
)

width = 0.25

for index, outcome in enumerate(
    available_outcomes
):

    values = admission_outcome[
        outcome
    ]

    positions = [
        value + (
            index - (
                len(available_outcomes) - 1
            ) / 2
        ) * width
        for value in x
    ]

    plt.bar(
        positions,
        values,
        width=width,
        label=outcome
    )


plt.xticks(
    list(x),
    admission_outcome.index
)

plt.title(
    "Outcome Percentage by Admission Type"
)

plt.xlabel(
    "Admission Type"
)

plt.ylabel(
    "Percentage (%)"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    CHART_DIR / "07_outcome_by_admission_type.png",
    dpi=300
)

plt.close()


# =========================================================
# 8. CLINICAL MEASUREMENTS BY OUTCOME
# =========================================================

clinical_data = (
    df.groupby("outcome")[
        ["glucose", "ef"]
    ]
    .mean()
)

available_outcomes = [
    outcome
    for outcome in [
        "DAMA",
        "DISCHARGE",
        "EXPIRY"
    ]
    if outcome in clinical_data.index
]

clinical_data = clinical_data.loc[
    available_outcomes
]


# -------------------------
# Glucose
# -------------------------

plt.figure(figsize=(9, 6))

plt.bar(
    clinical_data.index,
    clinical_data["glucose"]
)

plt.title(
    "Average Glucose by Outcome"
)

plt.xlabel(
    "Outcome"
)

plt.ylabel(
    "Average Glucose"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "08_average_glucose_by_outcome.png",
    dpi=300
)

plt.close()


# -------------------------
# Ejection Fraction
# -------------------------

plt.figure(figsize=(9, 6))

plt.bar(
    clinical_data.index,
    clinical_data["ef"]
)

plt.title(
    "Average Ejection Fraction by Outcome"
)

plt.xlabel(
    "Outcome"
)

plt.ylabel(
    "Average Ejection Fraction"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "09_average_ef_by_outcome.png",
    dpi=300
)

plt.close()


# =========================================================
# COMPLETION
# =========================================================

print("=" * 80)
print("VISUALIZATION COMPLETE")
print("=" * 80)

print("\nCharts saved to:")
print(CHART_DIR)

print("\nGenerated charts:")

for chart in sorted(CHART_DIR.glob("*.png")):
    print(
        "-",
        chart.name
    )

print("\n")
print("=" * 80)