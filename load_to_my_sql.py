import getpass
import sys

import pandas as pd
import mysql.connector
from mysql.connector import Error

CSV_PATH = "outputs/hospital_admission_cleaned.csv"

DB_HOST = "127.0.0.1"
DB_NAME = "hospital_analysis"


TEXT_COLUMNS = [
    "mrd_no",
    "gender",
    "rural",
    "type_of_admission_emergency_opd",
    "outcome",
    "admission_month_name",
]

DATE_COLUMNS = [
    "doa",
    "dod",
    "month_year",
]

INTEGER_COLUMNS = [
    "sno",
    "age",
    "duration_of_stay",
    "duration_of_intensive_unit_stay",
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
    "chest_infection",
    "admission_year",
    "admission_month",
    "calculated_duration_of_stay",
]

DECIMAL_COLUMNS = [
    "hb",
    "tlc",
    "platelets",
    "glucose",
    "urea",
    "creatinine",
    "bnp",
    "ef",
]


def prepare_dataframe():
    print("Reading cleaned CSV...")
    df = pd.read_csv(
        CSV_PATH,
        dtype={"mrd_no": "string"}
    )

    print(f"Rows found: {len(df)}")
    print(f"Columns found: {len(df.columns)}")

    # Convert date columns
    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        ).dt.date

    # Convert integer columns
    for column in INTEGER_COLUMNS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Convert decimal columns
    for column in DECIMAL_COLUMNS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Convert pandas missing values to Python None
    df = df.astype(object).where(pd.notna(df), None)

    return df


def main():
    print("Hospital Admissions → MySQL Import")
    print("-" * 50)

    username = input("MySQL username [root]: ").strip()

    if not username:
        username = "root"

    password = getpass.getpass("MySQL password: ")

    try:
        df = prepare_dataframe()

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=username,
            password=password,
            database=DB_NAME
        )

        if not connection.is_connected():
            print("Could not connect to MySQL.")
            sys.exit(1)

        print("Connected to MySQL successfully.")

        cursor = connection.cursor()

        print("Clearing existing table data...")
        cursor.execute("TRUNCATE TABLE hospital_admissions")

        columns = list(df.columns)

        column_sql = ", ".join(
            f"`{column}`" for column in columns
        )

        placeholders = ", ".join(
            ["%s"] * len(columns)
        )

        insert_sql = f"""
            INSERT INTO hospital_admissions ({column_sql})
            VALUES ({placeholders})
        """

        rows = list(df.itertuples(index=False, name=None))

        batch_size = 1000

        print(f"Importing {len(rows)} rows...")

        for start in range(0, len(rows), batch_size):
            batch = rows[start:start + batch_size]

            cursor.executemany(
                insert_sql,
                batch
            )

            connection.commit()

            processed = min(
                start + batch_size,
                len(rows)
            )

            print(
                f"Imported {processed}/{len(rows)} rows..."
            )

        cursor.execute(
            "SELECT COUNT(*) FROM hospital_admissions"
        )

        total_rows = cursor.fetchone()[0]

        print("-" * 50)
        print(f"Import completed successfully.")
        print(f"Rows in MySQL: {total_rows}")

        cursor.execute("""
            SELECT outcome, COUNT(*)
            FROM hospital_admissions
            GROUP BY outcome
            ORDER BY COUNT(*) DESC
        """)

        print("\nOutcome counts:")
        for outcome, count in cursor.fetchall():
            print(f"{outcome}: {count}")

        cursor.close()
        connection.close()

    except Error as error:
        print("-" * 50)
        print("MySQL error:")
        print(error)
        print("-" * 50)
        sys.exit(1)

    except FileNotFoundError:
        print(f"CSV file not found: {CSV_PATH}")
        sys.exit(1)

    except Exception as error:
        print("-" * 50)
        print("Unexpected error:")
        print(error)
        print("-" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()