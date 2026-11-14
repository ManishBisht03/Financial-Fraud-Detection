
import sqlite3
from pathlib import Path
import pandas as pd

print("Creating Financial Fraud Detection SQL database...")

# Folder containing the summary CSV files
summary_folder = Path("summaries")

# Database file to create
database_file = Path("fraud_analysis.db")

# Summary CSV files and their SQL table names
files_to_load = {
    "overall_fraud_summary.csv": "overall_fraud_summary",
    "fraud_by_type.csv": "fraud_by_type",
    "fraud_by_step.csv": "fraud_by_step",
    "fraud_by_type_and_status.csv": "fraud_by_type_and_status",
    "fraud_flag_summary.csv": "fraud_flag_summary"
}

if not summary_folder.exists():
    raise FileNotFoundError("The summaries folder was not found.")

# Connect to SQLite (creates the database if needed)
with sqlite3.connect(database_file) as connection:

    for csv_file, table_name in files_to_load.items():
        file_path = summary_folder / csv_file

        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")

        data = pd.read_csv(file_path)

        data.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )

        print(
            f"Loaded {csv_file}: "
            f"{len(data)} rows -> table '{table_name}'"
        )

    # Verify that all SQL tables were created
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' ORDER BY name"
    )
    tables = cursor.fetchall()

    print("\nTables available in the database:")
    for table in tables:
        print("-", table[0])

print("\nSQL database created successfully.")
print("Database location:", database_file.resolve())
