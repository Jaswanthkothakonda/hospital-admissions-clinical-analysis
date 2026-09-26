import pandas as pd
from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


# Load datasets
admission_df = pd.read_csv(
    DATA_DIR / "HDHI Admission data.csv"
)

mortality_df = pd.read_csv(
    DATA_DIR / "HDHI Mortality Data.csv"
)

pollution_df = pd.read_csv(
    DATA_DIR / "HDHI Pollution Data.csv"
)


def inspect_missing_values(name, df):
    print("\n")
    print("=" * 70)
    print(f"{name} - MISSING VALUES")
    print("=" * 70)

    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("No missing values found.")
    else:
        print(missing)


def inspect_duplicates(name, df):
    print("\n")
    print("=" * 70)
    print(f"{name} - DUPLICATES")
    print("=" * 70)

    duplicate_count = df.duplicated().sum()

    print("Duplicate rows:", duplicate_count)


def inspect_unique_values(name, df, columns):
    print("\n")
    print("=" * 70)
    print(f"{name} - UNIQUE VALUES")
    print("=" * 70)

    for column in columns:
        if column in df.columns:
            print(f"\n{column}:")
            print(df[column].value_counts(dropna=False).head(20))


def inspect_numeric_columns(name, df):
    print("\n")
    print("=" * 70)
    print(f"{name} - NUMERIC SUMMARY")
    print("=" * 70)

    print(df.describe(include="all").transpose())


# ---------------------------------------------------------
# Admission Data
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("ADMISSION DATA QUALITY INSPECTION")
print("=" * 70)

print("\nShape:")
print(admission_df.shape)

print("\nData Types:")
print(admission_df.dtypes)

inspect_missing_values(
    "ADMISSION DATA",
    admission_df
)

inspect_duplicates(
    "ADMISSION DATA",
    admission_df
)

inspect_unique_values(
    "ADMISSION DATA",
    admission_df,
    [
        "GENDER",
        "RURAL",
        "TYPE OF ADMISSION-EMERGENCY/OPD",
        "OUTCOME",
        "SMOKING",
        "ALCOHOL",
        "DM",
        "HTN",
        "CAD",
        "PRIOR CMP",
        "CKD",
        "SEVERE ANAEMIA",
        "ANAEMIA",
        "STABLE ANGINA",
        "ACS",
        "STEMI",
        "ATYPICAL CHEST PAIN",
        "HEART FAILURE",
        "HFREF",
        "HFNEF",
        "VALVULAR",
        "CHB",
        "SSS",
        "AKI",
        "CVA INFARCT",
        "CVA BLEED",
        "AF",
        "VT",
        "PSVT",
        "CONGENITAL",
        "UTI",
        "NEURO CARDIOGENIC SYNCOPE",
        "ORTHOSTATIC",
        "INFECTIVE ENDOCARDITIS",
        "DVT",
        "CARDIOGENIC SHOCK",
        "SHOCK",
        "PULMONARY EMBOLISM",
        "CHEST INFECTION"
    ]
)

# ---------------------------------------------------------
# Mortality Data
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("MORTALITY DATA QUALITY INSPECTION")
print("=" * 70)

print("\nShape:")
print(mortality_df.shape)

print("\nData Types:")
print(mortality_df.dtypes)

inspect_missing_values(
    "MORTALITY DATA",
    mortality_df
)

inspect_duplicates(
    "MORTALITY DATA",
    mortality_df
)

inspect_unique_values(
    "MORTALITY DATA",
    mortality_df,
    [
        "GENDER",
        "RURAL/URBAN"
    ]
)

# ---------------------------------------------------------
# Pollution Data
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("POLLUTION DATA QUALITY INSPECTION")
print("=" * 70)

print("\nShape:")
print(pollution_df.shape)

print("\nData Types:")
print(pollution_df.dtypes)

inspect_missing_values(
    "POLLUTION DATA",
    pollution_df
)

inspect_duplicates(
    "POLLUTION DATA",
    pollution_df
)

inspect_unique_values(
    "POLLUTION DATA",
    pollution_df,
    [
        "PROMINENT POLLUTANT"
    ]
)

print("\nPollution numeric summary:")
print(
    pollution_df.describe(include="all").transpose()
)