import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# Load raw admission data
# ---------------------------------------------------------

input_file = DATA_DIR / "HDHI Admission data.csv"

df = pd.read_csv(input_file)

print("=" * 70)
print("RAW DATA")
print("=" * 70)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ---------------------------------------------------------
# Clean column names
# ---------------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace("/", "_", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace("-", "_", regex=False)
    .str.replace(" ", "_", regex=False)
)

print("\nCleaned column names:")
print(df.columns.tolist())


# ---------------------------------------------------------
# Remove completely empty rows
# ---------------------------------------------------------

before_empty = len(df)

df = df.dropna(how="all")

after_empty = len(df)

print("\nCompletely empty rows removed:", before_empty - after_empty)


# ---------------------------------------------------------
# Remove exact duplicate rows
# ---------------------------------------------------------

before_duplicates = len(df)

df = df.drop_duplicates()

after_duplicates = len(df)

print("Duplicate rows removed:", before_duplicates - after_duplicates)


# ---------------------------------------------------------
# Clean string columns
# ---------------------------------------------------------

string_columns = df.select_dtypes(include="object").columns

for column in string_columns:

    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )


# ---------------------------------------------------------
# Convert known missing-value placeholders
# ---------------------------------------------------------

missing_values = [
    "",
    "EMPTY",
    "empty",
    "NA",
    "N/A",
    "NULL",
    "null",
    "None",
    "\\"
]

df = df.replace(
    missing_values,
    pd.NA
)


# ---------------------------------------------------------
# Convert admission date
# ---------------------------------------------------------

def parse_mixed_date(series):
    """
    Parse dates where the dataset contains both
    month-first and day-first formats.
    """

    result = pd.to_datetime(
        series,
        format="%m/%d/%Y",
        errors="coerce"
    )

    failed = result.isna() & series.notna()

    result.loc[failed] = pd.to_datetime(
        series.loc[failed],
        format="%d/%m/%Y",
        errors="coerce"
    )

    return result


df["doa"] = parse_mixed_date(df["doa"])


# ---------------------------------------------------------
# Convert discharge date
# ---------------------------------------------------------

df["dod"] = parse_mixed_date(df["dod"])


# ---------------------------------------------------------
# Convert numeric columns
# ---------------------------------------------------------

numeric_columns = [
    "sno",
    "age",
    "duration_of_stay",
    "duration_of_intensive_unit_stay",
    "hb",
    "tlc",
    "platelets",
    "glucose",
    "urea",
    "creatinine",
    "bnp",
    "ef"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ---------------------------------------------------------
# Convert binary medical columns to numeric
# ---------------------------------------------------------

binary_columns = [
    "smoking",
    "alcohol",
    "dm",
    "htn",
    "cad",
    "prior_cmp",
    "ckd",
    "raised_cardiac_enzymes",
    "severe_anaemia",
    "anaemia",
    "stable_angina",
    "acs",
    "stemi",
    "atypical_chest_pain",
    "heart_failure",
    "hfref",
    "hfnef",
    "valvular",
    "chb",
    "sss",
    "aki",
    "cva_infract",
    "cva_bleed",
    "af",
    "vt",
    "psvt",
    "congenital",
    "uti",
    "neuro_cardiogenic_syncope",
    "orthostatic",
    "infective_endocarditis",
    "dvt",
    "cardiogenic_shock",
    "shock",
    "pulmonary_embolism",
    "chest_infection"
]

for column in binary_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ---------------------------------------------------------
# Standardize categorical columns
# ---------------------------------------------------------

categorical_columns = [
    "gender",
    "rural",
    "type_of_admission_emergency_opd",
    "outcome"
]

for column in categorical_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .str.upper()
        )


# ---------------------------------------------------------
# Create month/year from admission date
# ---------------------------------------------------------

if "doa" in df.columns:

    df["admission_year"] = df["doa"].dt.year

    df["admission_month"] = df["doa"].dt.month

    df["admission_month_name"] = (
        df["doa"].dt.month_name()
    )

    df["month_year"] = (
        df["doa"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )


# ---------------------------------------------------------
# Calculate length of stay from dates
# ---------------------------------------------------------

if "doa" in df.columns and "dod" in df.columns:

    df["calculated_duration_of_stay"] = (
        df["dod"] - df["doa"]
    ).dt.days


# ---------------------------------------------------------
# Check calculated stay values
# ---------------------------------------------------------

if "calculated_duration_of_stay" in df.columns:

    negative_stay = (
        df["calculated_duration_of_stay"] < 0
    ).sum()

    print(
        "\nNegative calculated stay values:",
        negative_stay
    )


# ---------------------------------------------------------
# Display cleaned data information
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("CLEANED DATA")
print("=" * 70)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ---------------------------------------------------------
# Data types
# ---------------------------------------------------------

print("\nData types:")

print(df.dtypes)


# ---------------------------------------------------------
# Missing values
# ---------------------------------------------------------

print("\nMissing values:")

missing = (
    df.isnull()
    .sum()
    .sort_values(ascending=False)
)

missing = missing[missing > 0]

if missing.empty:

    print("No missing values.")

else:

    print(missing)


# ---------------------------------------------------------
# Duplicate check
# ---------------------------------------------------------

print("\nDuplicate rows after cleaning:")

print(
    df.duplicated().sum()
)


# ---------------------------------------------------------
# Save cleaned dataset
# ---------------------------------------------------------

output_file = (
    OUTPUT_DIR /
    "hospital_admission_cleaned.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# Completion message
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("CLEANING COMPLETE")
print("=" * 70)

print("Cleaned file saved to:")

print(output_file)