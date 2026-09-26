import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


# ---------------------------------------------------------
# Load raw dataset
# ---------------------------------------------------------

df = pd.read_csv(
    DATA_DIR / "HDHI Admission data.csv"
)


# ---------------------------------------------------------
# Check date columns
# ---------------------------------------------------------

print("=" * 70)
print("DATE COLUMN INSPECTION")
print("=" * 70)

for column in ["D.O.A", "D.O.D"]:

    print("\n" + "-" * 70)
    print(column)
    print("-" * 70)

    converted = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    invalid = df.loc[
        converted.isna() & df[column].notna(),
        column
    ]

    print("Original non-null values:", df[column].notna().sum())
    print("Successfully converted:", converted.notna().sum())
    print("Invalid date values:", invalid.shape[0])

    if not invalid.empty:
        print("\nExamples of invalid values:")
        print(invalid.astype(str).value_counts().head(20))


# ---------------------------------------------------------
# Check BNP
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("BNP INSPECTION")
print("=" * 70)

bnp_numeric = pd.to_numeric(
    df["BNP"],
    errors="coerce"
)

invalid_bnp = df.loc[
    bnp_numeric.isna() & df["BNP"].notna(),
    "BNP"
]

print("\nOriginal non-null BNP values:")
print(df["BNP"].notna().sum())

print("\nSuccessfully converted BNP values:")
print(bnp_numeric.notna().sum())

print("\nInvalid BNP values:")
print(invalid_bnp.shape[0])

if not invalid_bnp.empty:
    print("\nExamples of invalid BNP values:")
    print(
        invalid_bnp
        .astype(str)
        .value_counts()
        .head(20)
    )


# ---------------------------------------------------------
# Check Chest Infection
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("CHEST INFECTION INSPECTION")
print("=" * 70)

print(
    df["CHEST INFECTION"]
    .value_counts(dropna=False)
)


# ---------------------------------------------------------
# Check duration columns
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("DURATION COLUMNS")
print("=" * 70)

for column in [
    "DURATION OF STAY",
    "duration of intensive unit stay"
]:

    if column in df.columns:

        print("\n" + column)

        print(
            df[column]
            .value_counts(dropna=False)
            .head(20)
        )


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("QUALITY CHECK COMPLETE")
print("=" * 70)